---
name: micropython-skills/sensor
description: MicroPython sensor reading — DHT11/22, BME280, MPU6050, ADC, ultrasonic HC-SR04, photoresistor, generic I2C sensors.
---

# Sensor Reading

Code templates for reading common sensors on MicroPython devices.
All sensor reads are **Safe tier** — execute directly without user confirmation.

Always adapt pin numbers to the target board. When unsure, ask the user which GPIO pins are connected.

## DHT11 / DHT22 (Temperature & Humidity)

```python
import dht, json
from machine import Pin
try:
    # DHT22 is more accurate; use dht.DHT11 for DHT11
    sensor = dht.DHT22(Pin(4))  # Adapt GPIO pin
    sensor.measure()
    print("RESULT:" + json.dumps({
        "temperature_c": sensor.temperature(),
        "humidity_pct": sensor.humidity(),
    }))
except Exception as e:
    print("ERROR:" + str(e))
```

Notes:
- DHT22 range: -40~80C, 0-100% RH, accuracy +-0.5C
- DHT11 range: 0~50C, 20-80% RH, accuracy +-2C
- Minimum 2s between reads for DHT22, 1s for DHT11
- Needs a 4.7k-10k pull-up resistor on data pin (many modules have this built-in)

## BME280 (Temperature, Pressure, Humidity)

I2C sensor, common addresses: 0x76 or 0x77.

```python
from machine import Pin, I2C
import json
try:
    i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=100000)
    addrs = i2c.scan()
    bme_addr = 0x76 if 0x76 in addrs else (0x77 if 0x77 in addrs else None)
    if not bme_addr:
        print("ERROR:BME280 not found. I2C scan: " + str(["0x{:02x}".format(a) for a in addrs]))
        raise SystemExit

    # Read calibration and raw data — simplified using BME280 register map
    # For production use, recommend uploading a bme280 library via mpremote fs cp
    # Quick raw read of chip ID to verify:
    chip_id = i2c.readfrom_mem(bme_addr, 0xD0, 1)[0]
    if chip_id == 0x60:
        sensor_type = "BME280"
    elif chip_id == 0x58:
        sensor_type = "BMP280 (no humidity)"
    else:
        sensor_type = "Unknown (chip_id=0x{:02x})".format(chip_id)

    print("RESULT:" + json.dumps({
        "sensor": sensor_type,
        "address": "0x{:02x}".format(bme_addr),
        "note": "Upload bme280.py library for full T/P/H reading: mpremote fs cp bme280.py :",
    }))
except Exception as e:
    print("ERROR:" + str(e))
```

With library uploaded (`mpremote mip install bme280` or manual upload):
```python
import bme280, json
from machine import Pin, I2C
try:
    i2c = I2C(0, sda=Pin(21), scl=Pin(22))
    sensor = bme280.BME280(i2c=i2c)
    t, p, h = sensor.values  # Returns strings like "23.45C", "1013.25hPa", "48.7%"
    print("RESULT:" + json.dumps({"temperature": t, "pressure": p, "humidity": h}))
except Exception as e:
    print("ERROR:" + str(e))
```

## MPU6050 (Accelerometer + Gyroscope)

I2C address: 0x68 (or 0x69 with AD0 high).

```python
from machine import Pin, I2C
import json, struct
try:
    i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)
    addr = 0x68

    # Wake up MPU6050 (power management register)
    i2c.writeto_mem(addr, 0x6B, b'\x00')

    # Read 14 bytes starting at 0x3B (accel + temp + gyro)
    data = i2c.readfrom_mem(addr, 0x3B, 14)
    ax, ay, az, temp_raw, gx, gy, gz = struct.unpack(">hhhhhhh", data)

    # Convert: accel in g (default +-2g range), gyro in deg/s (default +-250)
    print("RESULT:" + json.dumps({
        "accel_g": {"x": ax/16384, "y": ay/16384, "z": az/16384},
        "gyro_dps": {"x": gx/131, "y": gy/131, "z": gz/131},
        "temp_c": temp_raw/340 + 36.53,
    }))
except Exception as e:
    print("ERROR:" + str(e))
```

## ADC (Analog-to-Digital Converter)

```python
from machine import ADC, Pin
import json
try:
    adc = ADC(Pin(34))  # ESP32 ADC1 pins: 32-39
    # ESP32 attenuation settings:
    # ADC.ATTN_0DB: 0-1.1V (most accurate)
    # ADC.ATTN_6DB: 0-1.5V
    # ADC.ATTN_11DB: 0-3.3V (full range)
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_12BIT)  # 0-4095

    raw = adc.read()
    voltage = raw / 4095 * 3.3  # Approximate voltage

    print("RESULT:" + json.dumps({
        "raw": raw,
        "voltage_v": round(voltage, 3),
        "attenuation": "11dB (0-3.3V)",
    }))
except Exception as e:
    print("ERROR:" + str(e))
```

Notes:
- ESP32 ADC is non-linear; for precision, use calibration lookup or external ADC
- ADC2 pins (GPIO 0,2,4,12-15,25-27) cannot be used while WiFi is active
- RP2040: use `ADC(26)`, `ADC(27)`, `ADC(28)` — 12-bit, 0-3.3V range

## HC-SR04 Ultrasonic Distance

```python
from machine import Pin, time_pulse_us
import time, json
try:
    trigger = Pin(5, Pin.OUT)
    echo = Pin(18, Pin.IN)

    trigger.value(0)
    time.sleep_us(2)
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)

    duration = time_pulse_us(echo, 1, 30000)  # timeout 30ms (~5m max)
    if duration < 0:
        print("ERROR:No echo received (object too far or not connected)")
    else:
        distance_cm = duration * 0.0343 / 2
        print("RESULT:" + json.dumps({
            "distance_cm": round(distance_cm, 1),
            "duration_us": duration,
        }))
except Exception as e:
    print("ERROR:" + str(e))
```

## Photoresistor (LDR)

Light level via ADC — brighter light = lower resistance = higher ADC value (with pull-down) or lower (with pull-up voltage divider):

```python
from machine import ADC, Pin
import json
try:
    adc = ADC(Pin(34))
    adc.atten(ADC.ATTN_11DB)
    raw = adc.read()
    # Map to rough percentage (depends on voltage divider circuit)
    light_pct = round(raw / 4095 * 100, 1)
    print("RESULT:" + json.dumps({"raw": raw, "light_pct": light_pct}))
except Exception as e:
    print("ERROR:" + str(e))
```

## Generic I2C Sensor Read

Template for reading arbitrary I2C registers:

```python
from machine import Pin, I2C
import json
try:
    i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=100000)
    addr = 0x48  # Target device address
    reg = 0x00   # Register to read
    nbytes = 2   # Number of bytes to read

    data = i2c.readfrom_mem(addr, reg, nbytes)
    print("RESULT:" + json.dumps({
        "address": "0x{:02x}".format(addr),
        "register": "0x{:02x}".format(reg),
        "data_hex": " ".join("0x{:02x}".format(b) for b in data),
        "data_bytes": list(data),
    }))
except Exception as e:
    print("ERROR:" + str(e))
```
