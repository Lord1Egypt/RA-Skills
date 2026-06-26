# Setup Guide

## Prerequisites

- LilyGo T3 v1.6.1 connected via USB
- `arduino-cli` installed with `esp32:esp32` core v3.3+
- Python 3 + `pyserial` (`pip install pyserial`)
- OpenClaw running on the Pi

## 1. Flash the Sketch

```bash
# Install libraries (once)
arduino-cli lib install "LoRa"
arduino-cli lib install "U8g2"

# Create sketch directory
mkdir -p ~/Arduino/LoRaCADScan
cp scripts/LoRaCADScan.ino ~/Arduino/LoRaCADScan/

# Compile + flash
arduino-cli compile --fqbn esp32:esp32:esp32 ~/Arduino/LoRaCADScan
arduino-cli upload  --fqbn esp32:esp32:esp32 --port /dev/ttyACM0 ~/Arduino/LoRaCADScan
```

Expected Serial output after boot:
```
# LoRa CAD Scanner v3
# SX127x: 0x12
# HW OK — scanning
# PASS 1
433000000,62500,6,-141,0
...
```

## 2. Verify OLED

If the OLED is black after flashing, run an I2C scan first:

```bash
# Flash I2C scanner to find address and pins
# Expected for T3 v1.6.1: SDA=21, SCL=22, addr=0x3C
```

The sketch uses software I2C (`U8G2_SSD1306_128X64_NONAME_F_SW_I2C`) with explicit pin numbers — this is intentional to avoid hardware I2C pin-mux issues on ESP32-PICO-D4.

## 3. Start the Pi Monitor

```bash
# Copy monitor script to workspace
cp scripts/lora_monitor.py /path/to/workspace/

# Run in background
nohup python3 lora_monitor.py > lora_monitor.log 2>&1 &

# Check it's running
tail -f lora_monitor.log
```

Monitor output:
```
[2026-03-25 07:04:26] Connected to /dev/ttyACM0
[2026-03-25 07:04:27] 433900000,250000,11,-141,0
[2026-03-25 07:19:26] # REPORT_START
[2026-03-25 07:19:26] Report: 2 channels, 1 new
[2026-03-25 07:19:26] Alert written: 📡 LoRa CAD Report...
```

## 4. Configure Telegram Alerts (OpenClaw)

Add this cron job via OpenClaw to deliver alerts:

```
Schedule: every 2 minutes
Payload: agentTurn
Message: "Check if /path/to/workspace/lora_alert.txt exists and has content. 
          If yes: read it, send to user via Telegram, delete the file. 
          If no: do nothing."
sessionTarget: isolated
```

## 5. Adjust Scan Range

Edit `LoRaCADScan.ino` defines and re-flash:

```cpp
#define FREQ_START   433000000UL   // Hz
#define FREQ_END     445000000UL   // Hz  
#define FREQ_STEP      50000UL     // Hz (50 kHz)
#define REPORT_INTERVAL_MS  (15UL * 60UL * 1000UL)  // 15 min
#define MAX_HITS  64               // max unique channels in RAM
```

## 6. File Locations (defaults)

| File | Purpose |
|---|---|
| `lora_scan.log` | Full scan log |
| `lora_hits.json` | Persistent known channels |
| `lora_alert.txt` | Pending Telegram alert (deleted after send) |
| `lora_monitor_stdout.log` | Monitor process stdout |
