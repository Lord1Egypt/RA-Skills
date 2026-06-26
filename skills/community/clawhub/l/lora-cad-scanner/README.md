# lora-cad-scanner

A LoRa Channel Activity Detection (CAD) scanner skill for OpenClaw. Turns a **LilyGo T3 v1.6** + **Raspberry Pi** into a persistent LoRa band monitor with live OLED display, protocol decoding, and Telegram alerts.

Optionally pairs with a **HackRF One** for wideband RF reconnaissance before focusing the LoRa scanner.

---

## What it does

1. **Sweeps** 433–445 MHz (configurable) across 6 bandwidths × 7 spreading factors using SX1276 CAD mode — detecting the LoRa preamble chirp, not just energy
2. **Opens a 10-second RX window** on any frequency where CAD fires above the RSSI threshold — waiting for a real packet
3. **Decodes captured packets** — identifies LoRaWAN, Cayenne LPP, TTN Mapper, Meshtastic, plain text, and more
4. **Displays live scan state** on the OLED — current frequency, BW, SF, RSSI, and last hit
5. **Sends Telegram alerts** immediately on packet capture (with decoded fields + hex dump), plus a 15-minute summary report

---

## Hardware

```
┌─────────────────────────────────────────────────────┐
│                   Raspberry Pi 5                     │
│  USB ──────────────────────────────┐                 │
│  USB ──────────────────┐           │                 │
└────────────────────────┼───────────┼─────────────────┘
                         │           │
                  ┌──────┴──────┐  ┌─┴──────────┐
                  │  LilyGo T3  │  │  HackRF One │
                  │   v1.6.1    │  │  (optional) │
                  │  ESP32-PICO │  │             │
                  │  SX1276     │  │  1 MHz–6GHz │
                  │  SSD1306    │  │  wideband   │
                  │  OLED 128×64│  └─────────────┘
                  └─────────────┘
```

### LilyGo T3 v1.6.1

| Component | Detail |
|---|---|
| MCU | ESP32-PICO-D4, 240 MHz, dual core |
| LoRa | SX1276 — 137–1020 MHz |
| Display | SSD1306 OLED, 128×64, I²C |
| USB | USB-C → appears as `/dev/ttyACM0` |
| Power | USB or LiPo battery |

**Pin assignments (pre-wired on T3, no soldering needed):**

| Signal | GPIO |
|---|---|
| LoRa SCK | 5 |
| LoRa MISO | 19 |
| LoRa MOSI | 27 |
| LoRa NSS (CS) | 18 |
| LoRa RST | 23 |
| LoRa DIO0 | 26 |
| OLED SDA | 21 |
| OLED SCL | 22 |

### HackRF One (optional)

Used for initial wideband survey to identify active frequencies before configuring the LoRa scanner. Connect via USB. No additional wiring required.

---

## Software stack

```
┌─────────────────────────────────────────────────┐
│                 Raspberry Pi                     │
│                                                  │
│  lora_monitor.py  ←── Serial /dev/ttyACM0 ──┐   │
│       │                                      │   │
│       ├── parses # PACKET lines              │   │
│       ├── calls lora_decoder.py              │   │
│       ├── writes lora_alert.txt              │   │
│       └── OpenClaw cron (2 min)              │   │
│              │                               │   │
│              ▼                               │   │
│         Telegram                      LilyGo T3  │
│                                       LoRaCADScan │
│                                       .ino        │
└─────────────────────────────────────────────────┘
```

### Components

| File | Role |
|---|---|
| `scripts/LoRaCADScan.ino` | Arduino sketch — CAD scan + RX window + OLED |
| `scripts/lora_monitor.py` | Pi daemon — reads serial, triggers alerts |
| `scripts/lora_decoder.py` | Protocol decoder — LoRaWAN, LPP, Meshtastic... |
| `scripts/parse_sweep.py` | HackRF sweep CSV parser |
| `references/setup.md` | Step-by-step setup guide |
| `references/sx1276-cad.md` | SX1276 register reference for CAD |
| `references/hackrf-workflow.md` | HackRF + LilyGo combined workflow |

---

## Scan parameters

| Parameter | Default | Configurable |
|---|---|---|
| Frequency range | 433–445 MHz | `FREQ_START` / `FREQ_END` |
| Step | 50 kHz | `FREQ_STEP` |
| Bandwidths | 15.6 / 31.25 / 62.5 / 125 / 250 / 500 kHz | `BWS[]` array |
| Spreading factors | SF6–SF12 | `SF_MIN` / `SF_MAX` |
| RSSI gate | −130 dBm | `RSSI_MIN_DBM` |
| RX window | 10 seconds | `RX_WINDOW_MS` |
| Report interval | 15 minutes | `REPORT_INTERVAL_MS` |

---

## OLED screens

**Scan mode**
```
LoRa CAD Scanner v4
433.175 MHz
BW: 62k  SF:9  -136dBm
P:12  CAD:3  PKT:1
────────────────────
PKT 433.175 125k SF7
████████████░░░░░░░░  ← progress bar
```

**RX window** (CAD fired, waiting for packet)
```
[ >RX ON< ]          ← animated
433.175 MHz
BW: 62k  SF:9  -131dBm
[████████░░░░░░░░]   ← 10s countdown
Waiting pkt...  6s      )))
```

**Packet caught**
```
► PACKET CAUGHT! ◄
433.175  62k SF9
RSSI:-118 SNR:+6 len:23
────────────────────
1A 2B 3C 4D 5E 6F 7A 8B
9C AD BE CF D0 E1 F2 03
.+<M^o..........   4s
```

---

## Telegram alert example

```
🎯 LoRa PACKET CAUGHT!

📻 433.175 MHz  BW=125kHz  SF9
📶 RSSI: -118 dBm  SNR: +6 dB
📦 Length: 23 bytes

✅ Protocol: LoRaWAN (confidence 85%)
📋 LoRaWAN Unconfirmed Data Up | DevAddr=49:BE:7D:F1 | FCnt=42

  DevAddr: 49:BE:7D:F1
  FCnt: 42
  FPort: 2
  Hint: Possibly Cayenne LPP payload

HEX:
  40 F1 7D BE 49 00 2A 00
  02 01 67 00 E1 02 68 78
  2B 11 01 02 AB CD EF
```

---

## Supported protocols

| Protocol | Detection method |
|---|---|
| **LoRaWAN** | MHDR byte, frame structure, MIC position |
| **LoRaWAN Join Request** | AppEUI + DevEUI + DevNonce (23-byte exact) |
| **Cayenne LPP** | Channel/type/value triple parsing |
| **TTN Mapper** | lat+lon+alt+hdop (11-byte GPS format) |
| **Meshtastic** | dest/src node ID + packet ID header |
| **Plain Text** | ASCII printability ratio |
| **APRS-like** | Callsign `>` path `:` info pattern |
| **Unknown** | Entropy analysis + hint |

---

## Quick start

```bash
# 1. Flash LilyGo
mkdir -p ~/Arduino/LoRaCADScan
cp scripts/LoRaCADScan.ino ~/Arduino/LoRaCADScan/
arduino-cli lib install "LoRa" "U8g2"
arduino-cli compile --fqbn esp32:esp32:esp32 ~/Arduino/LoRaCADScan
arduino-cli upload  --fqbn esp32:esp32:esp32 --port /dev/ttyACM0 ~/Arduino/LoRaCADScan

# 2. Start Pi monitor
nohup python3 scripts/lora_monitor.py >> lora_monitor.log 2>&1 &

# 3. Add OpenClaw cron for Telegram delivery (every 2 min)
# See references/setup.md
```

See [`references/setup.md`](references/setup.md) for full setup including OpenClaw cron configuration.

---

## License

MIT
