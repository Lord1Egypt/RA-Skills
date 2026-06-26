---
name: micropython-skills/actuator
description: MicroPython actuator control — GPIO output, PWM (LED/servo/motor), stepper motor, WS2812 NeoPixel, buzzer.
---

# Actuator Control

Code templates for controlling outputs and actuators on MicroPython devices.
All actuator operations are **Cautious tier** — inform the user what you're about to do before executing.

Before running any actuator code, confirm with the user:
- Which GPIO pin(s) are connected
- What the load is (LED, motor, relay, etc.)
- Whether wiring has been verified (especially for high-current devices)

## GPIO Output (Digital High/Low)

```python
from machine import Pin
import json
try:
    led = Pin(2, Pin.OUT)  # Built-in LED on many ESP32 boards
    led.value(1)  # Turn ON
    print("RESULT:" + json.dumps({"pin": 2, "state": "HIGH"}))
except Exception as e:
    print("ERROR:" + str(e))
```

For relay control, same pattern but be aware relays may be active-low:
```python
relay = Pin(5, Pin.OUT)
relay.value(0)  # Active-low relay: 0 = ON, 1 = OFF
```

## LED Blink

```python
from machine import Pin
import time, json
try:
    led = Pin(2, Pin.OUT)
    count = 5
    for i in range(count):
        led.value(1)
        time.sleep(0.5)
        led.value(0)
        time.sleep(0.5)
    print("RESULT:" + json.dumps({"blinked": count}))
except Exception as e:
    print("ERROR:" + str(e))
```

## PWM — LED Dimming

```python
from machine import Pin, PWM
import json
try:
    pwm = PWM(Pin(2), freq=1000)
    # duty: 0 (off) to 1023 (full brightness) on ESP32
    # On RP2040, duty range is 0-65535
    duty_value = 512  # ~50% brightness
    pwm.duty(duty_value)
    print("RESULT:" + json.dumps({"pin": 2, "freq": 1000, "duty": duty_value}))
except Exception as e:
    print("ERROR:" + str(e))
finally:
    # Always offer cleanup:
    # pwm.deinit()
    pass
```

## PWM — Servo Motor

Standard servos: 50Hz PWM, pulse width 0.5ms (0deg) to 2.5ms (180deg).

```python
from machine import Pin, PWM
import json
try:
    servo = PWM(Pin(13), freq=50)

    def set_angle(angle):
        # Map 0-180 degrees to duty cycle
        # ESP32: duty 0-1023 at 50Hz (20ms period)
        # 0.5ms = 2.5% duty = 26, 2.5ms = 12.5% duty = 128
        duty = int(26 + (angle / 180) * (128 - 26))
        servo.duty(duty)
        return duty

    target = 90  # degrees
    d = set_angle(target)
    print("RESULT:" + json.dumps({"angle": target, "duty": d}))
except Exception as e:
    print("ERROR:" + str(e))
```

## PWM — DC Motor Speed

Control motor speed via PWM through a driver (L298N, L293D, TB6612, etc.):

```python
from machine import Pin, PWM
import json
try:
    # Motor driver pins
    enable = PWM(Pin(14), freq=1000)  # Speed (PWM)
    in1 = Pin(26, Pin.OUT)  # Direction
    in2 = Pin(27, Pin.OUT)

    # Forward at 75% speed
    in1.value(1)
    in2.value(0)
    speed_pct = 75
    enable.duty(int(speed_pct / 100 * 1023))

    print("RESULT:" + json.dumps({
        "direction": "forward",
        "speed_pct": speed_pct,
    }))
except Exception as e:
    print("ERROR:" + str(e))
```

## Stepper Motor (ULN2003 Driver)

28BYJ-48 stepper with ULN2003 driver board:

```python
from machine import Pin
import time, json
try:
    # ULN2003 input pins
    pins = [Pin(p, Pin.OUT) for p in [25, 26, 27, 14]]

    # Half-step sequence for smoother rotation
    sequence = [
        [1,0,0,0], [1,1,0,0], [0,1,0,0], [0,1,1,0],
        [0,0,1,0], [0,0,1,1], [0,0,0,1], [1,0,0,1],
    ]

    steps = 512  # ~90 degrees for 28BYJ-48
    delay_ms = 2

    for i in range(steps):
        phase = sequence[i % len(sequence)]
        for j, pin in enumerate(pins):
            pin.value(phase[j])
        time.sleep_ms(delay_ms)

    # Turn off all coils
    for pin in pins:
        pin.value(0)

    print("RESULT:" + json.dumps({"steps": steps, "delay_ms": delay_ms}))
except Exception as e:
    # Clean up pins on error
    for pin in pins:
        pin.value(0)
    print("ERROR:" + str(e))
```

## WS2812 / NeoPixel LED Strip

```python
from machine import Pin
from neopixel import NeoPixel
import json
try:
    num_leds = 8
    np = NeoPixel(Pin(5), num_leds)

    # Set all LEDs to a color (R, G, B) — values 0-255
    color = (0, 50, 0)  # Dim green
    for i in range(num_leds):
        np[i] = color
    np.write()

    print("RESULT:" + json.dumps({
        "num_leds": num_leds,
        "color_rgb": list(color),
    }))
except Exception as e:
    print("ERROR:" + str(e))
```

Rainbow effect:
```python
from machine import Pin
from neopixel import NeoPixel
import time, json
try:
    np = NeoPixel(Pin(5), 8)

    def wheel(pos):
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)

    for cycle in range(3):  # 3 rainbow cycles
        for j in range(256):
            for i in range(8):
                np[i] = wheel((i * 32 + j) & 255)
            np.write()
            time.sleep_ms(20)

    # Turn off
    for i in range(8):
        np[i] = (0, 0, 0)
    np.write()
    print("RESULT:" + json.dumps({"effect": "rainbow", "cycles": 3}))
except Exception as e:
    print("ERROR:" + str(e))
```

## Buzzer / Piezo

Tone generation via PWM:

```python
from machine import Pin, PWM
import time, json
try:
    buzzer = PWM(Pin(15))

    # Play a melody (frequency in Hz, duration in ms)
    melody = [(262, 200), (330, 200), (392, 200), (523, 400)]  # C E G C5

    for freq, duration in melody:
        buzzer.freq(freq)
        buzzer.duty(512)  # 50% duty for audible tone
        time.sleep_ms(duration)
        buzzer.duty(0)    # Silence between notes
        time.sleep_ms(50)

    buzzer.deinit()
    print("RESULT:" + json.dumps({"melody_notes": len(melody)}))
except Exception as e:
    try:
        buzzer.deinit()
    except:
        pass
    print("ERROR:" + str(e))
```
