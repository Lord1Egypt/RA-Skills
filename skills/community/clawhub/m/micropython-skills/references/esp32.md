# ESP32 Platform Reference

## GPIO Pin Map — ESP32 (Classic)

| GPIO | ADC | Touch | Notes |
|------|-----|-------|-------|
| 0 | - | T1 | **Strapping pin** — boot mode select. Has internal pull-up. Avoid for general use. |
| 1 | - | - | TX0 (UART0 default). Used for serial output. |
| 2 | ADC2_2 | T2 | **Strapping pin** — must be LOW for flash boot. Often connected to onboard LED. |
| 3 | - | - | RX0 (UART0 default). Used for serial input. |
| 4 | ADC2_0 | T0 | General purpose, safe to use |
| 5 | - | - | **Strapping pin** — VSPI CS0. Internal pull-up. |
| 12 | ADC2_5 | T5 | **Strapping pin** — must be LOW at boot for correct flash voltage. |
| 13 | ADC2_4 | T4 | General purpose |
| 14 | ADC2_6 | T6 | General purpose |
| 15 | ADC2_3 | T3 | **Strapping pin** — internal pull-up. Silent boot control. |
| 16 | - | - | General purpose (UART2 RX default) |
| 17 | - | - | General purpose (UART2 TX default) |
| 18 | - | - | VSPI SCK. General purpose. |
| 19 | - | - | VSPI MISO. General purpose. |
| 21 | - | - | I2C SDA default. General purpose. |
| 22 | - | - | I2C SCL default. General purpose. |
| 23 | - | - | VSPI MOSI. General purpose. |
| 25 | ADC2_8 | - | DAC1. General purpose. |
| 26 | ADC2_9 | - | DAC2. General purpose. |
| 27 | ADC2_7 | T7 | General purpose |
| 32 | ADC1_4 | T9 | General purpose, safe ADC |
| 33 | ADC1_5 | T8 | General purpose, safe ADC |
| 34 | ADC1_6 | - | **Input only** — no internal pull-up/down |
| 35 | ADC1_7 | - | **Input only** — no internal pull-up/down |
| 36 (VP) | ADC1_0 | - | **Input only** — no internal pull-up/down |
| 39 (VN) | ADC1_3 | - | **Input only** — no internal pull-up/down |

### Key Rules

- **ADC1** (GPIO 32-39): Always available, use these for analog reads
- **ADC2** (GPIO 0,2,4,12-15,25-27): **Cannot be used while WiFi is active**
- **Input-only** (GPIO 34,35,36,39): No output capability, no pull-up/down
- **Strapping pins** (GPIO 0,2,5,12,15): Affect boot behavior — avoid unless necessary
- GPIO 6-11: Connected to flash memory — **do not use**

## ESP32-S3 Differences

| Feature | ESP32 | ESP32-S3 |
|---------|-------|----------|
| CPU | Xtensa dual-core 240MHz | Xtensa dual-core 240MHz |
| USB | External CP2102/CH340 | Native USB-OTG |
| GPIO count | 34 | 45 |
| ADC | 2x 12-bit | 2x 12-bit |
| Touch | 10 channels | 14 channels |
| AI acceleration | No | Vector instructions |
| BLE | 4.2 | 5.0 |
| PSRAM | Up to 4MB (SPIRAM) | Up to 8MB (Octal SPI) |

ESP32-S3 uses different default pin assignments — always check the specific board's schematic.

## ESP32-C3 Differences

- RISC-V single-core 160MHz (not Xtensa)
- Only 22 GPIO pins
- WiFi + BLE 5.0 (no classic Bluetooth)
- USB Serial/JTAG built-in
- Lower power consumption

## WiFi API

```python
import network

# Station mode (connect to router)
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("SSID", "password")
sta.isconnected()       # True/False
sta.ifconfig()          # (ip, mask, gateway, dns)
sta.status("rssi")      # Signal strength in dBm
sta.disconnect()
sta.active(False)

# AP mode (create hotspot)
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="ESP32-AP", password="12345678",
          authmode=network.AUTH_WPA2_PSK, channel=6, max_clients=4)
ap.ifconfig()
```

## BLE API

```python
import bluetooth

ble = bluetooth.BLE()
ble.active(True)
ble.config('mac')          # Get BLE MAC address
ble.gap_advertise(interval_us, adv_data)  # Start advertising
ble.gap_scan(duration_ms)  # Scan for devices
ble.irq(handler)           # Set event handler

# Common IRQ events:
# _IRQ_CENTRAL_CONNECT = 1
# _IRQ_CENTRAL_DISCONNECT = 2
# _IRQ_SCAN_RESULT = 5
# _IRQ_SCAN_DONE = 6
```

## Deep Sleep

```python
import machine

# Wake after time
machine.deepsleep(10000)  # 10 seconds, in milliseconds

# Wake on external pin (ext0 — single pin)
from machine import Pin
machine.deepsleep()       # Will wake on configured source

# Wake on touch pad
import esp32
esp32.wake_on_touch(True)
machine.deepsleep()

# Check wake reason after boot
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print("Woke from deep sleep")
```

Power consumption in deep sleep: ~10uA (ESP32), ~7uA (ESP32-S3).

## Touch Pad

ESP32 has capacitive touch on GPIO 0,2,4,12-15,27,32,33:

```python
from machine import TouchPad, Pin

tp = TouchPad(Pin(4))
value = tp.read()  # Returns capacitance value — lower = touched
# Typical: untouched ~600, touched ~100 (varies by wiring)
```

## Internal Temperature Sensor

```python
import esp32
temp_f = esp32.raw_temperature()  # Fahrenheit (integer)
temp_c = (temp_f - 32) * 5 / 9
```

Note: This reads the chip die temperature, not ambient. Useful for thermal monitoring.

## NVS (Non-Volatile Storage)

Persistent key-value store that survives reboots and deep sleep:

```python
import esp32

nvs = esp32.NVS("my_namespace")
nvs.set_i32("boot_count", 42)
nvs.commit()

value = nvs.get_i32("boot_count")  # Returns 42

# For strings, use blob:
nvs.set_blob("device_id", b"esp32-001")
nvs.commit()
buf = bytearray(20)
length = nvs.get_blob("device_id", buf)
device_id = buf[:length].decode()
```

## Common Board Pin Quick Reference

### ESP32-DevKitC / ESP32-WROOM-32

- Built-in LED: GPIO 2
- I2C default: SDA=21, SCL=22
- SPI (VSPI): SCK=18, MOSI=23, MISO=19, CS=5
- UART2: TX=17, RX=16
- Safe ADC pins: 32, 33, 34, 35, 36, 39

### ESP32-S3-DevKitC

- Built-in RGB LED (WS2812): GPIO 48
- I2C default: SDA=8, SCL=9 (varies by board)
- USB: GPIO 19 (D-) / GPIO 20 (D+) — do not use for GPIO
