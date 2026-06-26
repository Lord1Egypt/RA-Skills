---
name: lora-cad-scanner
description: >
  LoRa Channel Activity Detection (CAD) scanner for LilyGo T3 v1.6 (ESP32-PICO-D4 + SX1276)
  with HackRF One support. Scans a configurable frequency range using multiple BW/SF combinations,
  displays live progress on the SSD1306 OLED, stores detected channels in device RAM, emits
  structured 15-minute reports over Serial, and sends Telegram notifications for new detections
  via an OpenClaw cron pipeline. Use when scanning for LoRa devices in a frequency band,
  setting up a LilyGo T3 as a LoRa scanner/sniffer, building RF monitoring pipelines with
  Telegram alerting, or doing RF reconnaissance with HackRF + LilyGo together.
---

# LoRa CAD Scanner

Turns a LilyGo T3 v1.6 + Pi into a persistent LoRa scanner with live OLED display and Telegram alerts.

## Hardware

| Component | Spec |
|---|---|
| MCU | ESP32-PICO-D4 (LilyGo T3 v1.6.1) |
| LoRa | SX1276 |
| Display | SSD1306 128×64 OLED |
| Optional SDR | HackRF One (wideband RF recon) |

**Pin assignments (T3 v1.6.1):**
- LoRa: SCK=5, MISO=19, MOSI=27, SS=18, RST=23, DIO0=26
- OLED: SDA=21, SCL=22, addr=0x3C (software I2C)

## Dependencies

```bash
arduino-cli lib install "LoRa"   # v0.8.0+
arduino-cli lib install "U8g2"   # v2.35+
# Core: esp32:esp32 v3.3.7+
pip install pyserial numpy
```

- scripts/parse_sweep.py requires: numpy
- scripts/lora_monitor.py requires: pyserial

## Quick Deploy

```bash
# 1. Flash the Arduino sketch
cd /path/to/skill
cp scripts/LoRaCADScan.ino ~/Arduino/LoRaCADScan/LoRaCADScan.ino
arduino-cli compile --fqbn esp32:esp32:esp32 ~/Arduino/LoRaCADScan
arduino-cli upload  --fqbn esp32:esp32:esp32 --port /dev/ttyACM0 ~/Arduino/LoRaCADScan

# 2. Start the Pi monitor (background)
nohup python3 scripts/lora_monitor.py > lora_monitor.log 2>&1 &

# 3. Set up Telegram alert cron (OpenClaw)
# See references/setup.md for cron job configuration
```

## Scan Parameters

Defaults (edit in sketch):
- **Range:** 433–445 MHz
- **Step:** 50 kHz
- **BW:** 62.5 / 125 / 250 / 500 kHz
- **SF:** 6–12
- **CAD timeout:** 400 ms per combination

To change range, edit in `LoRaCADScan.ino`:
```cpp
#define FREQ_START   433000000UL
#define FREQ_END     445000000UL
#define FREQ_STEP      50000UL
```

## Limitations and Notes

- All output/log paths and cron scripts are hardcoded for the default OpenClaw workspace structure (`/home/admin/.openclaw/workspace/`). For non-standard setups, adjust the path variables in code/sketch before deploying.
- Requires access to `/dev/ttyACM0` (or another LilyGo T3 serial port), and to SDR devices (`hackrf_sweep` requires hackrf-tools and udev access rights).
- Telegram alerting is performed via an external OpenClaw cron pipeline; this skill does not integrate a Telegram client or store the token itself.
- Radio frequency monitoring may be regulated by local law. User is responsible for compliance and consequences.

## OLED Layout

```
┌────────────────────────┐
│ LoRa CAD Scanner       │
├────────────────────────┤
│ 433.150 MHz            │  ← current freq (big)
│ BW: 62k  SF:7  -141dBm │  ← current params + RSSI
│ Pass:3  Ch:2  Hit:12   │  ← stats
├────────────────────────┤
│ HIT 434.950 125k SF9   │  ← last hit
│████████░░░░░░░░░░░░░░░░│  ← progress bar
└────────────────────────┘
```

## Serial Protocol

All output at 115200 baud.

**Scan data** (continuous):
```
FREQ_HZ,BW_HZ,SF,RSSI_dBm,CAD(0=clear/1=hit)
433150000,125000,7,-141,0
434950000,62500,9,-138,1   ← hit
```

**15-minute report block:**
```
# REPORT_START
# PASS=12 TOTAL_HITS=5 UNIQUE_CHANNELS=2
NEW,434950000,62500,9,-141,-138,3
OLD,433150000,250000,7,-145,-143,2
# REPORT_END
```
`NEW` = first seen since last report. `OLD` = previously known.

## Alert Pipeline

```
LilyGo serial → lora_monitor.py → lora_alert.txt → OpenClaw cron → Telegram
```

- Monitor parses `REPORT_START/END` blocks
- Writes `lora_alert.txt` with formatted message
- OpenClaw cron (every 2 min) reads the alert file, sends a Telegram notification, and deletes the file
- Extracted parameters may include DevEUI, DevAddr, frequency coordinates, and other unique LoRa device identifiers; all data is only written inside the local workspace and never sent to external services except by explicit user configuration (Telegram).
- Known channels are persisted to `lora_hits.json`

## CAD Implementation Note

The `LoRa` library v0.8.0 does not expose CAD or `channelActivityDetection()`. CAD is implemented via direct SX1276 register writes:
- `REG_OP_MODE (0x01)` → `0x87` (CAD mode)
- Poll `REG_IRQ_FLAGS (0x12)` bit 2 (CadDone) + bit 0 (CadDetected)
- Timeout: 400 ms

See `references/sx1276-cad.md` for register details.

---

## Security & Privacy

- All alerts, log files, and intermediate results are only written within the local workspace.
- Device unique identifiers (DevEUI, DevAddr, LoRa addresses) may appear in reports—user is responsible for their handling and privacy.
- Telegram notification is configured and triggered only by explicit user cron script—no token or user credential is stored by this skill.
- All device addresses discovered are only stored locally and never transmitted unless user configures external delivery.

## False Positive Rate

At the noise floor (~−140 dBm), expect ~0–5% false CAD positives per pass. A hit is considered reliable if it appears in ≥2 consecutive passes at the same freq/BW/SF. The monitor tracks count per channel — low-count hits are likely noise.

## HackRF Companion Workflow

Use HackRF for initial wideband survey, then focus LilyGo on confirmed bands:

```bash
# Wideband sweep with HackRF
hackrf_sweep -f 430:445 -w 25000 -l 32 -g 40 > sweep.csv

# Parse peaks, set FREQ_START/FREQ_END in sketch accordingly
python3 scripts/parse_sweep.py sweep.csv
```
See `references/hackrf-workflow.md` for full HackRF + LilyGo workflow.
