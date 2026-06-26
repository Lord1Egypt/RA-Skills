---
name: micropython-skills
version: "1.0.0"
description: >
  Program and interact with embedded development boards (ESP32, ESP32-S3, ESP32-C3, ESP8266,
  NodeMCU, Raspberry Pi Pico, RP2040, STM32) through real-time REPL. This skill turns
  microcontroller hardware into an AI-programmable co-processor — read sensors, control
  actuators, flash firmware, diagnose devices, and deploy algorithms.
  Trigger when the user mentions any dev board or hardware interaction: ESP32, ESP8266,
  NodeMCU, Pico, 开发板, 板子, 单片机, 嵌入式, microcontroller, development board,
  sensor reading, GPIO, LED, motor, relay, I2C, SPI, UART, ADC, PWM, servo, DHT, BME280,
  temperature sensor, 传感器, 读传感器, 控制电机, 继电器, flash firmware, 烧录, 刷固件,
  刷机, mpremote, MicroPython, IoT, MQTT, WiFi on board, 设备没反应, device not responding,
  or any task involving programming or controlling a physical microcontroller board.
metadata:
  clawdbot:
    emoji: "🔌"
    homepage: "https://github.com/0x1abin/agents-workspace"
    os:
      - linux
      - darwin
      - win32
    requires:
      bins:
        - python3
        - mpremote
        - esptool
    files:
      - "SKILL.md"
      - ".claude/settings.local.json"
      - "evals/evals.json"
      - "scripts/device_probe.py"
      - "scripts/firmware_flash.py"
      - "scripts/wifi_setup.py"
      - "scripts/webrepl_exec.py"
      - "skills/sensor/SKILL.md"
      - "skills/actuator/SKILL.md"
      - "skills/network/SKILL.md"
      - "skills/diagnostic/SKILL.md"
      - "skills/algorithm/SKILL.md"
      - "references/connections.md"
      - "references/esp32.md"
      - "references/safety.md"
---

# micropython-skills

AI Agent programmable co-processor skill collection. You (the Agent) generate MicroPython code,
push it to devices via REPL, parse structured output, and iterate — turning hardware into your
extended capability.

## Quick Start

> **Python command**: Use `python3` on macOS/Linux, `python` on Windows.
> On Windows, `python3` is often a Microsoft Store stub that silently fails (exit code 49).
> On macOS/Linux, `python` may not exist or may point to Python 2.

Every interaction follows this flow:

1. **Probe** — Run `python3 {SKILL_DIR}/scripts/device_probe.py` to discover connected devices
   - `status: "ok"` → Device has MicroPython, proceed to step 2
   - `status: "no_firmware"` → ESP chip detected but no MicroPython. Ask user to confirm, then flash: `python3 {SKILL_DIR}/scripts/firmware_flash.py --port PORT --yes`
   - `status: "no_device"` → No device connected. Guide user to connect hardware.
   - `status: "permission_denied"` → Serial port not accessible. On Linux: `sudo chmod 666 /dev/ttyACM0`. On Windows: check Device Manager for driver issues.
2. **Connect** — Default: USB via mpremote. Optional: WiFi via WebREPL (user must request)
3. **Execute** — Generate MicroPython code and push to device
4. **Parse** — Scan stdout for tagged lines (RESULT:/ERROR:/STATUS:/LOG:)
5. **Iterate** — Adjust code based on results, repeat steps 3-5

Where `{SKILL_DIR}` is the directory containing this SKILL.md file.

## Connection Management

### Default: USB (mpremote)

Always start by probing for devices:
```bash
python3 {SKILL_DIR}/scripts/device_probe.py
```

Execute code on device:
```bash
mpremote exec "import machine; print('RESULT:' + str(machine.freq()))"
```

Run a script file:
```bash
mpremote run script.py
```

For multi-line code, write a temporary `.py` file locally, then `mpremote run /path/to/task.py`.

Serial port names vary by platform:

| Platform | Port Format | Example |
|----------|------------|---------|
| Linux | /dev/ttyUSB0, /dev/ttyACM0 | `mpremote connect /dev/ttyACM0` |
| macOS | /dev/cu.usbserial-*, /dev/cu.usbmodem* | `mpremote connect /dev/cu.usbmodem14101` |
| Windows | COM3, COM4, ... | `mpremote connect COM3` |

The scripts auto-detect the port — you rarely need to specify it manually.

### Optional: WiFi (WebREPL)

Only switch to WiFi when the user explicitly requests it. The switch flow:

1. Ask user for WiFi SSID and password
2. Push WiFi + WebREPL config to device via USB:
   ```bash
   python3 {SKILL_DIR}/scripts/wifi_setup.py --ssid "SSID" --password "PASS" --webrepl-password "repl123"
   ```
3. Note the IP address from the output
4. From now on, execute code over WiFi:
   ```bash
   python3 {SKILL_DIR}/scripts/webrepl_exec.py --host 192.168.1.100 --password repl123 --code "print('hello')"
   ```
5. USB cable can be disconnected

For detailed command reference, read `./references/connections.md`.

## Sub-skill Router

Based on user intent, read the corresponding sub-skill for domain-specific templates:

| User Intent Keywords | Sub-skill Path | Safety Tier |
|---------------------|----------------|-------------|
| temperature, humidity, DHT, BME280, pressure, IMU, accelerometer, ADC, analog, ultrasonic, light sensor, photoresistor, read sensor | `./skills/sensor/SKILL.md` | Safe |
| GPIO, LED, blink, PWM, servo, motor, stepper, relay, NeoPixel, WS2812, buzzer, output, control, drive | `./skills/actuator/SKILL.md` | Cautious |
| WiFi, MQTT, HTTP, BLE, Bluetooth, NTP, WebSocket, AP mode, network, connect internet, publish, subscribe | `./skills/network/SKILL.md` | Cautious |
| PID, filter, Kalman, state machine, scheduler, data logging, moving average, control loop, algorithm | `./skills/algorithm/SKILL.md` | Safe |
| scan I2C, scan SPI, device info, memory, filesystem, diagnose, health check, benchmark, pin state, what's connected | `./skills/diagnostic/SKILL.md` | Safe |
| save to device, 保存到设备, 开机自启, auto start, 下次还能用, persist, 断电保存 | See "Program Persistence" section below | Cautious/Dangerous |
| flash firmware, burn firmware, install MicroPython, no firmware, 烧录, 刷固件, 刷机 | `scripts/firmware_flash.py` | Dangerous |
| recovery, not responding, stuck, boot.py, main.py, reflash, brick | `./references/safety.md` | Dangerous |

When a task spans multiple domains (e.g., "read sensor and publish via MQTT"), read all relevant sub-skills.

## Structured Output Protocol

All MicroPython code you generate for the device MUST use tagged output lines:

| Tag | Purpose | Example |
|-----|---------|---------|
| `RESULT:` | Success data (JSON) | `RESULT:{"temp":23.5,"hum":61}` |
| `ERROR:` | Error info | `ERROR:OSError: [Errno 19] ENODEV` |
| `STATUS:` | Status indicator | `STATUS:ok` |
| `LOG:` | Debug info | `LOG:sampling at 100Hz` |

Code template — every snippet you generate should follow this pattern:
```python
import json
from machine import Pin
try:
    # ... your operation here ...
    print("RESULT:" + json.dumps({"key": value}))
except Exception as e:
    print("ERROR:" + str(e))
```

Parse rules:
- Scan device stdout line by line
- Extract lines starting with `RESULT:`, `ERROR:`, `STATUS:`, `LOG:`
- Ignore all other output (MicroPython boot messages, REPL prompts, etc.)
- If `ERROR:` is found, diagnose and retry with adjusted code

## Safety Rules

| Tier | Operations | Agent Behavior |
|------|-----------|----------------|
| Safe | Sensor read, I2C/SPI scan, memory check, pin read, diagnostics | Execute directly |
| Cautious | GPIO output, PWM, WiFi connect, file write on device | Inform user what you're about to do, then execute |
| Dangerous | Overwrite boot.py/main.py, format filesystem, OTA update, flash firmware | **Must get explicit user confirmation**. Always backup first: `mpremote fs cp :boot.py /tmp/boot.py.bak` |

Hard constraints:
- Never hardcode WiFi passwords in scripts saved to device — use variables or prompt user
- All loops must have iteration limits or timeouts — never generate infinite loops without exit conditions
- Before overwriting boot.py or main.py, always backup the existing file first
- Before controlling high-current devices (motors, relays), ask user to confirm wiring

For complete recovery procedures, read `./references/safety.md`.

## Workflow

As the Agent operating this co-processor, follow this mental model:

1. **Understand intent** — What does the user want to achieve with the hardware?
2. **Check connection** — Run device_probe.py if you haven't yet. Know your device's platform and capabilities.
3. **Route to sub-skill** — Read the relevant sub-skill SKILL.md for code templates and domain knowledge
4. **Generate code** — Write MicroPython code following the output protocol. Adapt pin numbers and parameters to the target platform.
5. **Push and capture** — Execute via mpremote or WebREPL, capture full stdout
6. **Parse results** — Extract RESULT:/ERROR: lines, parse JSON data
7. **Decide next step** — If ERROR, diagnose and adjust. If RESULT, present to user or use for next operation.
8. **Maintain state** — Remember which pins are in use, which peripherals are initialized, what the device's platform is
9. **Offer persistence** — After a program runs successfully, ask the user if they want to save it to the device or set it to auto-start on boot

## Program Persistence

After a program runs successfully, offer the user two options:

### Option 1: Save to Device (for later manual use)

Save the script to the device's filesystem so it can be run anytime without re-uploading:

```bash
# Save script to device
mpremote fs cp local_script.py :my_program.py

# List saved scripts on device
mpremote fs ls

# Run a saved script
mpremote exec "exec(open('my_program.py').read())"
```

This is a **Cautious** operation — inform the user before writing files to the device.

### Option 2: Auto-start on Boot (write to main.py)

If the user wants the program to run automatically every time the device powers on:

1. **Always ask first** — "要设置为开机自动运行吗？注意：如果程序有问题可能导致设备无法正常连接。"
2. **Backup existing main.py** (if any):
   ```bash
   mpremote fs cp :main.py ./main.py.bak
   ```
3. **Upload as main.py**:
   ```bash
   mpremote fs cp local_script.py :main.py
   ```
4. **Important**: For auto-start scripts, wrap the main logic in a try/except and add a short startup delay so the user can interrupt if needed:
   ```python
   import time
   time.sleep(2)  # 2s window for Ctrl-C interrupt
   # ... main logic ...
   ```

This is a **Dangerous** operation — require explicit user confirmation.

### Disable Auto-start

If the device becomes hard to access due to a problematic main.py:
```bash
# Rename to disable (if mpremote can still connect)
mpremote exec "import os; os.rename('main.py', 'main.py.disabled')"
mpremote reset

# Or delete it
mpremote exec "import os; os.remove('main.py')"
mpremote reset
```

If the device is completely unresponsive, follow the recovery steps in `./references/safety.md`.

## Platform Adaptation

After probing, adapt code to the detected platform:

| Platform | Key Capabilities |
|----------|-----------------|
| esp32 / esp32s3 | WiFi, BLE, Touch Pad, Deep Sleep, ULP, Hall Sensor |
| rp2040 | PIO state machines, dual core, no WiFi (unless Pico W) |
| stm32 | More timers, CAN bus, DAC |
| Generic | Standard `machine` module API only |

For ESP32-specific pin maps and APIs, read `./references/esp32.md`.

## Reference Files

Read these on demand — not every interaction needs them:

| File | When to Read |
|------|-------------|
| `./references/connections.md` | Troubleshooting connection issues, mpremote advanced usage, WebREPL protocol details |
| `./references/esp32.md` | ESP32-specific pin maps, strapping pin warnings, deep sleep, NVS, BLE/WiFi API details |
| `./references/safety.md` | Device recovery, boot.py restore, filesystem repair, electrical safety |

## Dependencies

Agent-side requirements:
- `mpremote` — `pip install mpremote` (required for USB connection)
- `esptool` — `pip install esptool` (required for chip detection and firmware flashing)
- `pyserial` — `pip install pyserial` (required on **Windows** for COM port auto-detection; recommended on all platforms)
- `websocket-client` — `pip install websocket-client` (only needed for WiFi/WebREPL mode)
- Python 3.8+

> **Windows notes**:
> - Use `python` instead of `python3` to run scripts. On many Windows systems, `python3` is a Microsoft Store stub that returns exit code 49. On macOS/Linux, use `python3`.
> - Without `pyserial`, the scripts fall back to parsing the `mode` command output for COM port detection, which provides less detail (no VID/PID info). Install `pyserial` for best results.

Device-side requirements:
- MicroPython firmware v1.19+ (v1.22+ recommended) — auto-installed by `firmware_flash.py` if missing
- USB connection or WiFi reachability

## External Endpoints

This skill accesses external services during specific operations:

| Endpoint | When Accessed | Purpose | Required? |
|----------|--------------|---------|-----------|
| `https://micropython.org/download/{board}/` | Firmware flashing only (`firmware_flash.py`) | Download latest stable MicroPython firmware binary for the detected chip | Only when flashing firmware |
| `https://micropython.org/resources/firmware/...` | Firmware flashing only | Direct firmware `.bin` download URL | Only when flashing firmware |

No telemetry, analytics, or data is sent to any external service. The skill operates entirely locally except for firmware downloads.

## Security & Privacy

- **No data collection**: This skill does not collect, transmit, or store any user data
- **No telemetry**: No usage analytics, crash reports, or tracking of any kind
- **Local-only operation**: All device communication happens over local USB serial or local WiFi (WebREPL). No cloud relay or proxy is used
- **WiFi credentials**: When provided by the user, WiFi credentials are passed directly to the device via `mpremote` and written to the device's `boot.py`. They are never logged, stored on the host machine, or transmitted to external services
- **Firmware source**: Firmware binaries are downloaded exclusively from `micropython.org`, the official MicroPython project site
- **File system access**: Helper scripts only access serial ports and the system temp directory (for firmware caching). No other host files are read or modified

## Trust & Verification

- **Open source**: Full source code is available at the homepage repository
- **No obfuscation**: All Python scripts and Markdown files are human-readable
- **Auditable**: The `scripts/` directory contains 4 self-contained Python scripts with no external dependencies beyond `mpremote`, `esptool`, `pyserial`, and `websocket-client`
- **Evals included**: The `evals/evals.json` file contains 5 test scenarios covering device probe, sensor read, actuator control, diagnostics, and recovery
