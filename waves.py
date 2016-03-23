import simplegui, math

DENSITY = 1
WIDTH = 600
HEIGHT = 600
INITX = 50
INITY = 300
WAVELENGTH = 200
SPEED = 100
AMP = 100

class Wave:
    def __init__(self, direction, amp, wavelength, start, freq, colour):
        self._dir = direction
        self._amp = amp
        self._wavelength = wavelength
        self._start = start
        self._freq = freq
        self._time_per = 1/freq
        self._time = 0
        self._colour = colour
        self._continuous = False
    
    def draw(self, canvas):
        x = self._start[0]
        y = self._start[1]
        distance = int(self._freq * self._wavelength * self._time)
        
        for x_inc in range(0, min(distance * DENSITY,  (WIDTH - 100) * DENSITY)):
            canvas.draw_point([x + (self._dir * float(x_inc)) / DENSITY,
                               y + self._amp * 
                               math.sin((self._time * 2 * math.pi * self._freq) -
                                        (x_inc * 2 * math.pi / (self._wavelength * DENSITY))
                                       )
                              ],
                              self._colour)
        if self._continuous:
            self._time += time_inc
    
    def continuous(self):
        self._continuous = not self._continuous
    
    def get_pos(self, x):
        distance = self._freq * self._wavelength * self._time
        if x > distance:
            return 0
        else:
            return self._amp * math.sin((self._time * 2 * math.pi * self._freq) -
                                        (x * 2 * math.pi / (self._wavelength))
                                       )
    
    def inc_half_wavelength(self):
        self._time += 1.0 / (2 * self._freq)
    
    def dec_half_wavelength(self):
        self._time -= 1.0 / (2 * self._freq)
    
    def reset(self):
        self._time = 0
        self._continuous = False
    
def draw_res(canvas):
    x = INITX
    y = INITY
    
    for x_inc in range(0, (WIDTH - 2 * INITX) * DENSITY, DENSITY):
        canvas.draw_point([x + float(x_inc) / DENSITY,
                           y + wave1.get_pos(float(x_inc) / DENSITY) + wave2.get_pos(WIDTH - 2 * INITX - float(x_inc) / DENSITY)
                          ],
                          'Yellow'
                         )

time_inc = 1/120.0
wave1 = Wave(1, AMP, WAVELENGTH, [INITX, INITY], SPEED / float(WAVELENGTH), 'Blue')
wave2 = Wave(-1, AMP, WAVELENGTH, [WIDTH - INITX, INITY], SPEED / float(WAVELENGTH), 'Red')

def stop_start():
    wave1.continuous()
    wave2.continuous()

def reset():
    wave1.reset()
    wave2.reset()

def double_speed():
    global time_inc
    time_inc *= 2

def halve_speed():
    global time_inc
    time_inc /= 2

def reset_speed():
    global time_inc
    time_inc = 1/120.0

def reverse_time():
    global time_inc
    time_inc *= -1

# Handler to draw on canvas
def draw(canvas):
    wave1.draw(canvas)
    wave2.draw(canvas)
    draw_res(canvas)

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", WIDTH, HEIGHT)
frame.add_button('Stop/Start Wave 1', wave1.continuous)
frame.add_button('Stop/Start Wave 2', wave2.continuous)
frame.add_button('Stop/Start Both', stop_start)
frame.add_label('')
frame.add_button('Reverse Time', reverse_time)
frame.add_label('')
frame.add_button('Wave 1 + 0.5 wavelength', wave1.inc_half_wavelength)
frame.add_button('Wave 1 - 0.5 wavelength', wave1.dec_half_wavelength)
frame.add_label('')
frame.add_button('Wave 2 + 0.5 wavelength', wave2.inc_half_wavelength)
frame.add_button('Wave 2 - 0.5 wavelength', wave2.dec_half_wavelength)
frame.add_label('')
frame.add_button('x2', double_speed, 40)
frame.add_button('x0.5', halve_speed, 40)
frame.add_button('Reset Speed', reset_speed)
frame.add_label('')
frame.add_button('Reset', reset)
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()
