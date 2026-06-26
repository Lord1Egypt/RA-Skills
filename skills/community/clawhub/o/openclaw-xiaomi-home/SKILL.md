---
name: openclaw-xiaomi-home
description: Your OpenClaw can now control your smart home. It connects to your Xiaomi/Mijia devices through Home Assistant and lets you control lights, AC, locks, sensors and more with plain text or voice commands. Ask things like "turn on the living room light", "set AC to 26 degrees", "is the front door locked?", or "what's the bedroom temperature?" and your AI assistant handles it instantly. Triggers: "turn on the light", "set AC temperature", "is the door locked?", "check the temperature", "lock the door", "turn everything off".

NOTE: Requires Home Assistant (Docker, localhost:8123) and Xiaomi devices paired with Mi Home.

Required credentials:
- `HA_TOKEN`: Long-Lived Access Token from Home Assistant, stored in `.env` (gitignored). Used as Bearer token to authenticate MCP server requests. Never sent to any external service.

Security:
- MCP server only accepts requests from localhost
- All MCP calls require "Authorization: Bearer <HA_TOKEN>" header
- HA_TOKEN is never transmitted to any service other than your local Home Assistant
- No data collection or exfiltration — purely local device control
---

# Xiaomi Home Control

**Your OpenClaw can now control your smart home.** Connect to Xiaomi/Mijia devices through Home Assistant and control everything with plain text or voice.

## What It Does

Just tell your AI what you want:

```
"Turn on the living room light"
"Set bedroom AC to 26 degrees"
"Is the front door locked?"
"What's the temperature?"
"Lock all doors"
"Turn off all lights"
```

Done. No apps. No switching. No pointing and clicking.

## What You Can Control

| Category | Examples |
|----------|---------|
| 💡 Lights | Turn on/off, adjust brightness |
| ❄️ Air Conditioning | Set temperature, mode, fan speed |
| 🔐 Door Locks | Lock/unlock from anywhere |
| 🌡️ Sensors | Temperature, humidity, motion |
| 💨 Fans & Humidifiers | On/off, speed control |
| 🪟 Blinds & Curtains | Open/close |
| 🤖 Robot Vacuums | Start, stop, return to charger |

Works with **1837+ Xiaomi/Mijia devices** via the official Xiaomi Home integration.

## Setup (One Time)

```bash
# 1. Start Home Assistant
docker compose up -d

# 2. Connect your Xiaomi devices
# (open localhost:8123 → add Xiaomi Home integration)

# 3. Install the control server
cd scripts/ha-mcp-server && npm install

# 4. Done
```

Full guide in README.md.

## How It Works

```
You → "Turn on the light"
  ↓
OpenClaw AI
  ↓
Home Assistant (your local server)
  ↓
Xiaomi Device
```

All on **your local network** — no cloud, no subscription.

## Why It's Better

| Before | After |
|--------|-------|
| Open app → find device → tap | Just say what you want |
| One device at a time | Control everything at once |
| Can't do it remotely | Through AI assistant from anywhere |
| Remember which app for which device | Describe it in plain English |

## Privacy

- Everything stays on your home network
- No cloud dependency after setup
- No data collection or tracking
- Runs on your own hardware

## Example Commands

```
"Turn on the living room light"
"Dim the bedroom to 30%"
"Set AC to cool mode at 24 degrees"
"Is the door locked?"
"Lock the front door"
"What's the living room temperature?"
"Turn off all lights"
"Open the blinds"
"Start the vacuum"
```
