import pyglet
import math

ACCELERATION = 50
ROTATION_SPEED = 20
MAX_SPEED = 300
window = pyglet.window.Window()

def nacti_obrazek(nazev): # funkce
    obrazek = pyglet.image.load('./' + nazev)
    obrazek.anchor_x = obrazek.width//2
    obrazek.anchor_y = obrazek.height//2
    return obrazek

obrazky_lodi = [
    nacti_obrazek('playerShip1_green.png'),
    nacti_obrazek('playerShip1_orange.png')]

obrazky_meteoru = [
    nacti_obrazek('meteorGrey_small1.png'),
    nacti_obrazek('meteorGrey_small2.png'),
    nacti_obrazek('meteorGrey_tiny1.png'),
    nacti_obrazek('meteorGrey_tiny2.png')]



#obrazek_lod = pyglet.image.load('./ship.png')
#obrazek_meteor = pyglet.image.load('./meteor.png')
#obrazek_lod.anchor_x = obrazek_lod.width//2
#obrazek_lod.anchor_y = obrazek_lod.height//2
#obrazek_meteor.anchor_x = obrazek_meteor.width//2
#obrazek_meteor.anchor_y = obrazek_meteor.height//2

batch = pyglet.graphics.Batch()  # dávka

class SpaceObject:
    def __init__(self, x, y, rotation, obrazek):
        self.x = x
        self.y = y
        self.rotation = 90 - rotation
        self.speed_x = 0
        self.speed_y = 0
        self.rotation_speed = 0
        self.sprite = pyglet.sprite.Sprite(obrazek, batch=batch)
        self.radius = 20

    def tick(self,dt):
        if self.x > window.width:  # kdyz objekt zmizi, tak se objevi na nove strane
            self.x -= window.width
        if self.x < 0:
            self.x += window.width
        if self.y > window.height:
            self.y -= window.height
        if self.y < 0:
            self.y += window.height

        # aktualizace polohy
        self.x = self.x + dt * self.speed_x
        self.y = self.y + dt * self.speed_y
        self.rotation = self.rotation + dt * self.rotation_speed

        # nastaveni parametru obrazku
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.rotation = 90 - self.rotation

from random import randint #chci nahodne cislo nejake velikosti

class Asteroid(SpaceObject):
    def __init__(self, x, y, rotation):
        super().__init__(x, y, rotation, choice(obrazky_meteoru))
        self.speed_x = randint(-100, 100)
        self.speed_y = randint(-100, 100)
        self.rotation_speed = randint(-100, 100)

from random import choice

class Spaceship(SpaceObject):
    def __init__(self, x, y, rotation):
        super().__init__(x, y, rotation, choice(obrazky_lodi)) #funkce super zavola funkci Space Object, super mi predstavuje self nadtridy

    def tick(self,dt):
        if pyglet.window.key.LEFT in pressed_keys:
            self.rotation_speed += ROTATION_SPEED
        if pyglet.window.key.RIGHT in pressed_keys:
            self.rotation_speed -= ROTATION_SPEED

        rotation_radians = math.radians(self.rotation)

        if pyglet.window.key.UP in pressed_keys:
            self.speed_x += dt * ACCELERATION * math.cos(rotation_radians)
            self.speed_y += dt * ACCELERATION * math.sin(rotation_radians)

        if pyglet.window.key.DOWN in pressed_keys:
            self.speed_x -= dt * ACCELERATION * math.cos(rotation_radians)
            self.speed_y -= dt * ACCELERATION * math.sin(rotation_radians)
        # max speed
        self.speed_x = min(self.speed_x, MAX_SPEED)
        self.speed_x = max(self.speed_x, -MAX_SPEED)
        self.speed_y = min(self.speed_y, MAX_SPEED)
        self.speed_y = max(self.speed_y, -MAX_SPEED)

        super().tick(dt)


objects = []
#for i  in range (13):  # pocet raketek
    #objects.append(Spaceship(window.width//2, window.height//2, i * 30))
objects.append(Spaceship(window.width//2, window.height//2,0))

for i in range(5):
    objects.append(Asteroid(window.width//2, window.height//2,0))

def tick(dt):
    for item in objects:
        item.tick(dt)

from pyglet import gl
def draw():
      window.clear()
      for x_offset in (-window.width, 0, window.width):
          for y_offset in (-window.height, 0, window.height):
              gl.glPushMatrix()
              gl.glTranslatef(x_offset, y_offset, 0)
              batch.draw()
              for item in objects:
                  draw_circle(item.x, item.y, item.radius)
              #   item.sprite.draw()
              gl.glPopMatrix()
def draw2():
    window.clear()
    batch.draw()
    #for item in objects:
        #item.sprite.draw()

pressed_keys = set()
from pyglet.window import key
def on_key_press(symbol, modifiers):   # symbol je to, co jsem zmackla
    pressed_keys.add(symbol) # podle toho vim, ktere jsem  stiskla klavesy, toto je mnozina, nepotrebuji na na klic
    print(pressed_keys)

def on_key_release(symbol, modifiers):
    pressed_keys.discard(symbol)
    print(pressed_keys)

window.push_handlers(  #nastaveni pro knihovnu,
        on_key_press=on_key_press,
        on_key_release=on_key_release,
        on_draw=draw #knihovna vi, ze ma zavolat funkci, zaregirstuji, ze knihovna ma zavolat tu funkci
        )
pyglet.clock.schedule_interval(tick, 0.02)

def draw_circle(x, y, radius):
    iterations = 20
    s = math.sin(2*math.pi / iterations)
    c = math.cos(2*math.pi / iterations)

    dx, dy = radius, 0

    gl.glBegin(gl.GL_LINE_STRIP)
    for i in range(iterations+1):
        gl.glVertex2f(x+dx, y+dy)
        dx, dy = (dx*c - dy*s), (dy*c + dx*s)
    gl.glEnd()



pyglet.app.run()
