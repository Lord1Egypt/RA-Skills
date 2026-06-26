---
name: micropython-skills/diagnostic
description: MicroPython device diagnostics — system info, I2C/SPI bus scan, pin state, filesystem, memory, performance benchmarks.
---

# Device Diagnostics

Templates for probing device health and discovering connected peripherals.
All operations in this sub-skill are **Safe tier** — execute directly without user confirmation.

## System Info

Comprehensive device information snapshot:

```python
import sys, gc, json, machine
try:
    import os
    gc.collect()
    u = os.uname()
    s = os.statvfs("/")
    info = {
        "platform": sys.platform,
        "machine": u.machine,
        "release": u.release,
        "freq_mhz": machine.freq() // 1000000,
        "mem_free_kb": gc.mem_free() // 1024,
        "mem_alloc_kb": gc.mem_alloc() // 1024,
        "storage_free_kb": (s[0] * s[3]) // 1024,
        "storage_total_kb": (s[0] * s[2]) // 1024,
    }
    print("RESULT:" + json.dumps(info))
except Exception as e:
    print("ERROR:" + str(e))
```

## I2C Bus Scan

Discovers I2C devices. Adapt SDA/SCL pins to the target board:

```python
from machine import Pin, I2C
import json
try:
    # Common ESP32 defaults: SDA=21, SCL=22
    # Common RP2040 defaults: SDA=0, SCL=1
    i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=100000)
    addrs = i2c.scan()
    devices = [{"addr": a, "hex": "0x{:02x}".format(a)} for a in addrs]
    print("RESULT:" + json.dumps({"i2c_devices": devices, "count": len(addrs)}))
except Exception as e:
    print("ERROR:" + str(e))
```

Common I2C addresses for identification:

| Address | Common Device |
|---------|--------------|
| 0x23 | BH1750 light sensor |
| 0x3C/0x3D | SSD1306 OLED display |
| 0x48 | ADS1115 ADC |
| 0x50 | AT24C EEPROM |
| 0x68 | MPU6050 IMU / DS3231 RTC |
| 0x76/0x77 | BME280/BMP280 sensor |

## SPI Bus Check

Verify SPI peripheral initialization:

```python
from machine import Pin, SPI
import json
try:
    spi = SPI(1, baudrate=1000000, polarity=0, phase=0,
              sck=Pin(18), mosi=Pin(23), miso=Pin(19))
    print("RESULT:" + json.dumps({"spi": "initialized", "baudrate": 1000000}))
except Exception as e:
    print("ERROR:" + str(e))
```

## Pin State Read

Read all common GPIO pins to see current state:

```python
from machine import Pin
import json
try:
    states = {}
    # Adjust pin range for your board (ESP32: 0-39, RP2040: 0-29)
    for p in [0,2,4,5,12,13,14,15,16,17,18,19,21,22,23,25,26,27,32,33,34,35,36,39]:
        try:
            pin = Pin(p, Pin.IN)
            states[str(p)] = pin.value()
        except:
            states[str(p)] = "N/A"
    print("RESULT:" + json.dumps({"pin_states": states}))
except Exception as e:
    print("ERROR:" + str(e))
```

## Filesystem Browse

List files and check storage:

```python
import os, json
try:
    def ls(path="/"):
        result = []
        for name in os.listdir(path):
            full = path.rstrip("/") + "/" + name
            try:
                s = os.stat(full)
                is_dir = s[0] & 0x4000
                result.append({"name": name, "size": s[6], "dir": bool(is_dir)})
            except:
                result.append({"name": name, "size": -1, "dir": False})
        return result

    s = os.statvfs("/")
    files = ls("/")
    print("RESULT:" + json.dumps({
        "files": files,
        "storage_free_kb": (s[0] * s[3]) // 1024,
        "storage_total_kb": (s[0] * s[2]) // 1024,
    }))
except Exception as e:
    print("ERROR:" + str(e))
```

## Network Status

Check WiFi connection (ESP32/Pico W only):

```python
import json
try:
    import network
    sta = network.WLAN(network.STA_IF)
    ap = network.WLAN(network.AP_IF)
    info = {
        "sta_active": sta.active(),
        "sta_connected": sta.isconnected(),
        "sta_config": list(sta.ifconfig()) if sta.isconnected() else None,
        "ap_active": ap.active(),
        "ap_config": list(ap.ifconfig()) if ap.active() else None,
    }
    if sta.isconnected():
        info["rssi"] = sta.status("rssi") if hasattr(sta, "status") else None
    print("RESULT:" + json.dumps(info))
except ImportError:
    print("RESULT:" + json.dumps({"wifi_available": False}))
except Exception as e:
    print("ERROR:" + str(e))
```

## Performance Benchmark

Simple timing test to gauge CPU performance:

```python
import time, gc, json
try:
    gc.collect()
    mem_before = gc.mem_free()

    # Integer math benchmark
    start = time.ticks_us()
    s = 0
    for i in range(10000):
        s += i * i
    int_us = time.ticks_diff(time.ticks_us(), start)

    # Float math benchmark
    start = time.ticks_us()
    x = 1.0
    for i in range(10000):
        x = x * 1.0001
    float_us = time.ticks_diff(time.ticks_us(), start)

    gc.collect()
    mem_after = gc.mem_free()

    print("RESULT:" + json.dumps({
        "int_10k_us": int_us,
        "float_10k_us": float_us,
        "mem_overhead_bytes": mem_before - mem_after,
    }))
except Exception as e:
    print("ERROR:" + str(e))
```
