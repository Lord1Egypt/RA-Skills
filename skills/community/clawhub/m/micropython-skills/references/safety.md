# Safety Constraints & Recovery

## Operation Safety Tiers

| Tier | Operations | Agent Behavior | Rationale |
|------|-----------|----------------|-----------|
| **Safe** | Sensor read, I2C/SPI scan, memory check, pin read, diagnostics, algorithm execution | Execute directly | Read-only, no side effects |
| **Cautious** | GPIO output, PWM, WiFi connect, file write to device, mip install | Inform user before executing | May affect hardware or device state |
| **Dangerous** | Overwrite boot.py/main.py, format filesystem, OTA update, deep sleep, factory reset, **flash firmware** | **Require explicit user confirmation** + auto-backup | May brick device or cause data loss |

## Firmware Flashing Safety

`firmware_flash.py` automates firmware download and flashing. Because `erase_flash` **permanently deletes all data** on the device, strict safety rules apply:

1. **Always confirm with user** before flashing — show chip type, firmware version, and port
2. **Explain the consequences**: erase_flash destroys all files (boot.py, main.py, user scripts)
3. **Use `--yes` flag only** when the Agent has already received explicit user consent
4. **After flashing fails**: the device may be in an incomplete state. Retry the flash or guide the user to bootloader mode (hold BOOT, press RESET)
5. **Firmware source**: only download from micropython.org — never use untrusted URLs

## boot.py / main.py Protection

These files run automatically on boot. A bad boot.py can make the device inaccessible.

### Before Modifying

Always backup first:
```bash
mpremote fs cp :boot.py ./boot.py.bak
mpremote fs cp :main.py ./main.py.bak
```

### If boot.py Causes Boot Loop

1. **Interrupt**: During boot, rapidly send Ctrl-C via mpremote:
   ```bash
   mpremote exec --no-follow ""
   # Then quickly:
   mpremote exec "import os; os.remove('boot.py')"
   ```

2. **Safe mode boot** (ESP32): Hold BOOT button during reset — some firmware builds skip boot.py

3. **Last resort**: Re-flash MicroPython firmware entirely (see Firmware Recovery below)

### Restoring Backup

```bash
mpremote fs cp ./boot.py.bak :boot.py
mpremote reset
```

## Device Recovery Steps

Follow this escalation sequence when a device is unresponsive:

### Level 1: Software Interrupt

```bash
# Send Ctrl-C to interrupt running code
mpremote exec --no-follow ""
# Or simply:
mpremote reset
```

This works if the device is running a loop but REPL is still responsive.

### Level 2: Soft Reset

```bash
mpremote reset
```

Restarts MicroPython interpreter. boot.py and main.py will run again.

### Level 3: Remove Problematic Scripts

If boot.py/main.py are causing issues, try to remove them between resets:

```bash
# After reset, quickly execute before boot.py runs:
mpremote exec "import os; os.rename('main.py', 'main.py.disabled')"
```

### Level 4: Safe Mode / Bootloader

**ESP32:**
1. Hold BOOT button
2. Press and release RESET button
3. Release BOOT button
4. Device enters bootloader mode — firmware can be flashed

**RP2040 (Pico):**
1. Hold BOOTSEL button
2. Connect USB cable
3. Release BOOTSEL — appears as USB drive
4. Copy new firmware .uf2 file to the drive

### Level 5: Firmware Reflash

Complete firmware reinstall. This erases all user files.

**ESP32:**
```bash
# Install esptool
pip install esptool

# Erase flash completely (use COM3 on Windows, /dev/ttyUSB0 on Linux)
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash

# Flash new firmware (use COM3 on Windows, /dev/ttyUSB0 on Linux)
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-firmware.bin
```

Download firmware from: https://micropython.org/download/

## Electrical Safety

### Current Limits

| Parameter | ESP32 | RP2040 |
|-----------|-------|--------|
| Max per GPIO pin | 40mA (recommended 20mA) | 12mA (recommended 4mA) |
| Max total GPIO current | 1.2A | ~50mA total |
| Logic level | 3.3V | 3.3V |

### Rules

- **Never connect 5V directly** to any GPIO pin — use a voltage divider or level shifter
- **Use driver circuits** for motors, relays, solenoids — GPIO cannot drive them directly
- **Common drivers**: MOSFET (logic-level), L298N, ULN2003, TB6612
- **LED resistor**: Always use a current-limiting resistor (220-1k ohm) for direct LED connections
- **Relay modules**: Most relay modules have optoisolation and built-in driver — safe to connect directly to GPIO
- **Servo power**: Power servos from a separate 5V supply, not from the board's 3.3V rail

### Before Controlling High-Current Devices

Ask the user to confirm:
1. What device is connected to the pin?
2. Is there a driver circuit between GPIO and the load?
3. Is the power supply adequate for the load?

## WiFi Credential Safety

- Never save WiFi passwords in files that persist on the device in plaintext
- The `wifi_setup.py` script writes credentials to boot.py — warn user that credentials are stored on device
- For production deployments, use NVS encrypted storage or provisioning protocols
- Never echo or print WiFi passwords in RESULT: output

## Loop Safety

All loops in generated MicroPython code must have exit conditions:

```python
# Bad — infinite loop with no escape
while True:
    read_sensor()

# Good — bounded iteration
for i in range(100):
    read_sensor()
    time.sleep(1)

# Good — timeout-based
deadline = time.time() + 60  # 60 second max
while time.time() < deadline:
    read_sensor()
    time.sleep(1)
```

If the user requests continuous monitoring, implement it with a bounded duration and offer to extend:
```python
# Run for 30 seconds, then stop and report
duration_s = 30
```

## Emergency Stop

If something goes wrong during actuator control:

1. **Ctrl-C via mpremote** — interrupts running code immediately
2. **mpremote reset** — soft resets the device, all GPIO returns to default state
3. **Unplug USB / disconnect power** — ultimate hardware stop
4. **After recovery**: Check if the actuator needs explicit deactivation (e.g., relay might latch)
