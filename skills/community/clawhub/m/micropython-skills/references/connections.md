# Connection Reference

## mpremote Command Reference

`mpremote` is the official MicroPython remote control tool. It communicates with devices over USB serial.

### Device Discovery

```bash
# List connected devices
mpremote devs

# Connect to a specific port
mpremote connect /dev/ttyUSB0
```

### Code Execution

```bash
# Execute a one-liner
mpremote exec "import machine; print(machine.freq())"

# Run a local .py file on the device (does not upload; streams code)
mpremote run script.py

# Execute on a specific port
mpremote connect /dev/ttyUSB0 exec "print('hello')"
```

### File System Operations

```bash
# List files on device
mpremote fs ls

# Copy local file to device
mpremote fs cp local_file.py :remote_file.py

# Copy file from device to local
mpremote fs cp :boot.py ./boot.py.bak

# Remove file on device
mpremote fs rm :old_file.py

# Create directory on device
mpremote fs mkdir :lib

# Show file contents
mpremote fs cat :boot.py
```

### Package Installation

```bash
# Install from micropython-lib
mpremote mip install umqtt.simple
mpremote mip install bme280

# Install from URL
mpremote mip install github:user/repo/package.py
```

### Device Control

```bash
# Soft reset
mpremote reset

# Hard reset (same as pressing reset button)
mpremote exec "import machine; machine.reset()"

# Enter raw REPL (for automated tools)
mpremote raw-repl
```

### Command Chaining

mpremote supports chaining commands with `+`:

```bash
# Connect, copy file, then run it
mpremote connect /dev/ttyUSB0 + fs cp main.py :main.py + reset

# Backup boot.py, then write new one
mpremote fs cp :boot.py ./boot.py.bak + fs cp new_boot.py :boot.py
```

### Mount Local Directory

Share a local directory with the device (files accessed on demand):

```bash
# Mount current dir as device's filesystem
mpremote mount .
# Now the device can import from your local files
```

## WebREPL Protocol

WebREPL allows wireless REPL access over WiFi via WebSocket.

### Setup Flow

1. Connect device via USB first
2. Run WiFi + WebREPL setup:
   ```bash
   python3 scripts/wifi_setup.py --ssid "MyWiFi" --password "secret"
   ```
3. Note the IP address from output
4. Use `scripts/webrepl_exec.py` to execute code wirelessly

### Protocol Details

- Transport: WebSocket (`ws://device_ip:8266`)
- Authentication: Password sent as first message after connection
- REPL modes:
  - Normal REPL: Human-readable, includes prompts (`>>>`)
  - Raw REPL: Machine-readable, entered with Ctrl-A (`\x01`)
    - Send code followed by Ctrl-D (`\x04`) to execute
    - Output ends with Ctrl-D + `>` marker
    - Exit raw REPL with Ctrl-B (`\x02`)

### WebREPL Configuration on Device

The device needs two files:

**webrepl_cfg.py:**
```python
PASS = "your_password"
```

**boot.py (auto-connect):**
```python
import network, time
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("SSID", "PASSWORD")
for _ in range(30):
    if sta.isconnected():
        break
    time.sleep(0.5)
import webrepl
webrepl.start()
```

## USB to WiFi Switch Flow

Complete procedure to transition from USB to WiFi operation:

1. **Verify USB works**: `mpremote devs` — ensure device is visible
2. **Get WiFi credentials**: Ask user for SSID and password
3. **Push config**: `python3 scripts/wifi_setup.py --ssid X --password Y`
4. **Verify**: Output should show `RESULT:{"ip":"...","webrepl_port":8266}`
5. **Test WiFi**: `python3 scripts/webrepl_exec.py --host IP --password P --code "print('ok')"`
6. **Switch**: From now on, use `webrepl_exec.py` instead of `mpremote exec`
7. **USB optional**: Cable can be disconnected after WiFi is confirmed working

### Fallback

If WiFi setup fails or device becomes unreachable:
1. Reconnect USB cable
2. `mpremote reset` — soft reset
3. `mpremote exec "import os; os.remove('boot.py')"` — remove auto-connect boot.py
4. Re-try setup with correct credentials

## WSL2 USB Passthrough

WSL2 does not natively see USB devices. To use mpremote from WSL2:

### Setup (one-time, on Windows host)

1. Install usbipd-win: `winget install usbipd`
2. In PowerShell (admin): `usbipd list` — find the ESP32 bus ID
3. Bind: `usbipd bind --busid <BUSID>`
4. Attach to WSL: `usbipd attach --wsl --busid <BUSID>`

### Usage

After attaching, the device appears in WSL2 as `/dev/ttyACM0` or `/dev/ttyUSB0`.

```bash
# Verify in WSL2
ls /dev/ttyACM* /dev/ttyUSB* 2>/dev/null
mpremote devs
```

### Re-attach After Reconnect

USB passthrough is lost when the device is unplugged or WSL2 restarts.
Re-run `usbipd attach --wsl --busid <BUSID>` each time.

## Connection Status Detection

To verify if a device is reachable before executing:

**USB:**
```bash
mpremote devs 2>&1 | grep -q "tty" && echo "connected" || echo "no device"
```

**WiFi:**
```bash
python3 scripts/webrepl_exec.py --host IP --password P --code "print('STATUS:ok')" --timeout 5
```
