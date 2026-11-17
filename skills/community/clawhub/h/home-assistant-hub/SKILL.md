---
name: "home-assistant-hub"
description: "Real-time Home Assistant monitoring, alert rules, TTS voice notifications on Echo devices, Telegram delivery, entity inspection. Service calls are HARD-DENIED by default — require explicit safe-domains opt-in."
homepage: https://github.com/openclaw/openclaw
metadata:
  {
    "openclaw":
      {
        "emoji": "🏡",
        "requires": { "bins": ["node"] },
        "permissions": [
          { "kind": "network", "direction": "outbound", "targets": ["Home Assistant API/WebSocket (HTTP + WSS)", "Telegram Bot API (HTTPS)", "Echo devices via HA notify service"], "reason": "Real-time monitoring of home device states, alert delivery to Telegram servers, and voice announcements on Echo devices require outbound network connections" },
          { "kind": "network", "direction": "local-bind", "targets": ["localhost:9123 (on-demand API)"], "reason": "Local HTTP API for ha-cmd.js service calls when configured. Disabled by default." },
          { "kind": "secrets", "direction": "local-read", "targets": ["config/hub.json"], "reason": "Reads HA long-lived bearer token, Telegram bot token, and chat ID. File is gitignored — never commit to version control" }
        ]
      },
  }
---

# ⚠️ SECURITY & PRIVACY WARNINGS — READ FIRST

## 🔴 Device Control — Hardened Defaults
This skill can invoke Home Assistant services to change physical device states. **Service calls are disabled by default.**

### ⛔ Always Blocked (never configurable)
The following domains are HARD-LOCKED in code and cannot be enabled:
- `lock.*` — door locks (physical security)
- `alarm_control_panel.*` — alarm systems (safety-critical)
- `cover.*` — blinds/doors/garage (privacy/security)

### ✅ Safe Domains — Explicit Opt-In Required
Service calls require domains to be listed in `call_safe_domains` in `config/hub.json`. **An empty list means all service calls are blocked.**

Default safe domains in the example config: `light`, `climate`, `scene`, `media_player`, `automation`, `notify`

To add a new domain, edit hub.json:
```json
"call_safe_domains": ["light", "climate", "scene", "media_player", "automation", "notify"]
```

### 🔍 Dry-Run Mode
Before executing any service call, use `--dry-run` to preview what would happen:
```bash
node scripts/ha-cmd.js call climate.set_temperature entity_id=climate.hvac temperature=22 --dry-run
# Output: Service URL + payload WITHOUT executing


## 📡 External Data Transmission
This skill transmits data to third-party services:
- **Telegram Bot API** — alert messages including occupancy, sensor states, routines → exposes household patterns and security-relevant information
- **Echo devices via HA** — TTS announcements broadcast inside the home environment
- **Home Assistant instance** — all device telemetry sent over network

**Do NOT include sensitive personal data in alert templates.** Notification content is visible on Telegram accounts and potentially logged by Telegram servers.

### 🚫 No Hardcoded Credentials
All credentials are loaded exclusively from `config/hub.json`. There are no hardcoded fallback tokens anywhere in the codebase. If `telegram_bot_token` or `telegram_chat_id` are missing, the deliverer will refuse to send (with a warning) rather than fall back to defaults.

## 🔐 Credential Sensitivity
All secrets (`ha_token`, `telegram_bot_token`, `telegram_chat_id`) are stored in `config/hub.json`. This file is gitignored but:
- The HA token is a **long-lived bearer token** with broad API access — treat it like a password
- Default `ha_url` uses plain HTTP → credentials transmitted in cleartext on the local network. Use HTTPS if possible.
- Rotate tokens regularly via HA → Profile → Long-Lived Access Tokens

## 🔧 Process Management
The hub runs as background processes (`nohup`, `disown`) that persist beyond your session. `pkill -f "ha-hub.js start"` can match multiple processes. Always verify process state before killing.

---

# Home Assistant Hub

Real-time monitoring of Home Assistant device states with configurable alert rules, TTS voice notifications on Echo devices via Parla entities, Telegram delivery for alerts and events, entity inspection (states, history, persons, areas), and controlled device management through direct service calls.

## Architecture Overview

```
┌───────────┐    HTTP/WS     ┌───────────────┐   JSON file   ┌─────────────────┐
│ Home      │ ◄──────────►  │  ha-hub.js    │ ───────────►  │ telegram-deliver│
│ Assistant │  polling or   │  background    │               │  background     │
│           │   WebSocket   │  monitoring   │               │  notification   │
└───────────┘               └───────────────┘               │  delivery       │
                                                            └────────┬────────┘
                                                                       │ HTTPS
                                                                 ┌─────▼──────┐
                                                                 │ Telegram API│
                                                                 └────────────┘

┌───────────┐    HTTP          ┌───────────────┐
│ ha-cmd.js │ ───────────────►  │ Home Assistant│   (on-demand, direct)
│ (CLI/API) │                   │ WebSocket     │
└───────────┘                   └───────────────┘
```

**Two background processes:**
| Process | Role | Frequency |
|---------|------|-----------|
| `ha-hub.js` | Connected to HA, monitors device states against alert rules | Polls every 10s (WS fallback) |
| `telegram-deliver.js` | Reads pending notification files and sends via Telegram | Checks every 30s |

## Permissions

| Permission | Direction | Targets | Reason |
|-----------|-----------|---------|---------|
| `network` | outbound | Home Assistant API/WebSocket (HTTP+WSS), Telegram Bot API (HTTPS), Echo devices via HA notify | Real-time home monitoring, alert delivery to third-party servers, voice announcements |
| `network` | local-bind | localhost:9123 (on-demand HTTP API) — **disabled by default** | Local service for ha-cmd.js when enabled in config |
| `secrets` | local-read | `config/hub.json` | HA long-lived bearer token + Telegram credentials. File is gitignored — never commit |

## Quick Start

```bash
cd skills/home-assistant-hub

# Test connection to HA (safe, read-only)
node scripts/ha-cmd.js info

# List entities containing "echo" or "parla" (safe, read-only)
node scripts/ha-cmd.js state list 2>&1 | grep -i echo

# Start the monitoring hub (background process)
node scripts/ha-hub.js start

# Check hub status
node scripts/ha-hub.js status

# Stop the hub
node scripts/ha-hub.js stop
```

## 📋 Safe Commands (Read-Only / Display)

These commands only **read** data from Home Assistant. No device state changes:

| Command | What it does | Data exposed |
|---------|-------------|-------------|
| `node scripts/ha-cmd.js info` | HA version, URL, OS, connected clients | System metadata |
| `node scripts/ha-cmd.js state` | All entity states at once | Full home telemetry snapshot |
| `node scripts/ha-cmd.js state get <id>` | Single entity state (e.g., `sensor.battery_level`) | One sensor value |
| `node scripts/ha-cmd.js state list <domain>` | Filter entities by domain (`light`, `binary_sensor`, etc.) | Domain-level inventory |
| `node scripts/ha-cmd.js scenes` | List all defined scenes | Scene configuration |
| `node scripts/ha-cmd.js persons` | List persons + presence states | Occupancy data — who is home |
| `node scripts/ha-cmd.js areas` | Areas with device counts | Home layout and device inventory |

## 🗣️ Voice Notifications (TTS)

Sends voice announcements to Echo devices via HA Parla entities. **This produces audible output in your physical environment.**

Use **comma-separated entity IDs** — do NOT pass a JSON array:

```bash
# Send to ALL configured Echo devices simultaneously
node scripts/ha-cmd.js call notify.send_message \
  entity_id="notify.echo_show_5_parla,notify.echo_pop_di_vincenzo_parla" \
  message="Ciao Vincenzo, la batteria è al 75 percento"

# Single device
node scripts/ha-cmd.js call notify.send_message \
  entity_id="notify.echo_show_5_parla" \
  message="La cena è pronta"
```

**Find Parla entity IDs:** `node scripts/ha-cmd.js state list 2>&1 | grep -i parla`

### Troubleshooting TTS
- **"400 Bad Request"** → wrong format. Use comma-separated string, not array.
- **"Success" but no audio** → verify: (1) Parla entities exist in HA, (2) an automation listens for `notify.send_message`, (3) Echo devices are online/unmuted.
- **Verify delivery:** check timestamp updated: `node scripts/ha-cmd.js state get notify.echo_show_5_parla | grep last_updated`

## 📋 Alert Rules

Configurable rules that detect device state changes and trigger notifications via Telegram or voice announcements.

### Add rule interactively
```bash
node scripts/ha-hub.js add-rule
```

### Add rules via JSON (stdin)
```bash
node scripts/ha-hub.js add-rules << 'EOF'
[
  {
    "name": "Garage aperto",
    "entity_id": "binary_sensor.garage_door",
    "condition": "state",
    "value": "on",
    "cooldown": 300,
    "title": "Garage",
    "template": "Il garage è aperto!"
  },
  {
    "name": "Batteria bassa",
    "entity_id": "sensor.battery_level",
    "condition": "below",
    "value": "20",
    "cooldown": 600,
    "title": "🪫 Batteria",
    "template": "Batteria al {{state}}% — serve attenzione"
  }
]
EOF
```

### List rules
```bash
node scripts/ha-hub.js rules
```

### Rule conditions

| Condition | Meaning | Example value |
|-----------|---------|-------------|
| `state` | State equals value | `on`, `home`, `open` |
| `not_state` | State not equals value | `away` |
| `above` | Numeric state above threshold | `25` |
| `below` | Numeric state below threshold | `10` |
| `changed` | Always trigger on any change | — |

## 📱 Telegram Integration

Alerts are delivered to a Telegram chat when configured. **⚠️ Data is transmitted externally to Telegram servers.** Alert content includes entity states, occupancy information, and home status. Avoid including sensitive personal data in alert templates.

```bash
node scripts/telegram-deliver.js start   # Start delivery process
node scripts/telegram-deliver.js status  # Check delivery status
node scripts/telegram-deliver.js stop    # Stop delivery process
```

Telegram settings in `config/hub.json`:
```json
"telegram_bot_token": "your_bot_token",
"telegram_chat_id": "your_chat_id",
"notification_channel": "telegram"   // or: "both" (Telegram + Echo)
```

### Notification flow
1. HA device state changes (e.g., battery drops to 19%)
2. `ha-hub.js` detects change against active alert rules
3. Matching rule writes a JSON file to `notifications/` directory
4. `telegram-deliver.js` picks up the new file and sends to Telegram
5. File is moved to `delivered/` on successful delivery

## 🔧 On-Demand Commands (`ha-cmd.js`)

All commands run from the skill directory:
```bash
cd skills/home-assistant-hub
```

### Safe (read-only / display) commands:

| Command | Description |
|---------|-------------|
| `node scripts/ha-cmd.js info` | HA version, URL, OS |
| `node scripts/ha-cmd.js state` | All entity states |
| `node scripts/ha-cmd.js state get <id>` | Specific entity (e.g., sensor.battery) |
| `node scripts/ha-cmd.js state list <domain>` | Filter by domain (light, binary_sensor...) |
| `node scripts/ha-cmd.js scenes` | List all defined scenes |
| `node scripts/ha-cmd.js persons` | List persons + presence states |
| `node scripts/ha-cmd.js areas` | Areas with device counts |

### ⚠️ Control commands (state-changing) — DISABLED BY DEFAULT:

Service calls require explicit domain opt-in in `config/hub.json` via `call_safe_domains`. **No service is callable unless its domain is listed there.** Dangerous domains (`lock`, `alarm_control_panel`, `cover`) are hard-locked and cannot be enabled.

| Command | Description |
|---------|-------------|
| `node scripts/ha-cmd.js call <service> [key=value ...] --dry-run` | Preview what would be called (no execution) |
| `node scripts/ha-cmd.js call <service> [key=value ...]` | Execute service — **only if domain is in call_safe_domains** |

#### Examples (understand the impact before running):

```bash
# TTS announcement on Echo devices
node scripts/ha-cmd.js call notify.send_message \
  entity_id="notify.echo_show_5_parla" message="Prova vocale"

# Turn on a light — changes physical environment
node scripts/ha-cmd.js call light.turn_on entity_id=light.living_room

# Set thermostat temperature — affects comfort
node scripts/ha-cmd.js call climate.set_temperature \
  entity_id=climate.hvac temperature=22

# Activate a scene (multi-device action)
node scripts/ha-cmd.js call scene.turn_on entity_id=scene.movie_time

# Trigger an automation
node scripts/ha-cmd.js call automation.trigger entity_id=automation.my_automation
```

## 🔑 Hub Config (`config/hub.json`)

Use `hub.example.json` as a template:

```bash
cp config/hub.example.json config/hub.json
# Edit hub.json with your credentials — NEVER commit this file!
```

```json
{
  "ha_url": "http://homeassistant.local:8123",       // use https:// if available
  "ha_token": "your-long-lived-token",               // treat as password
  "poll_interval": 10,                                // seconds between polls
  "rules": [...],                                     // alert rules (see above)
  "notification_channel": "telegram",                 // or: "both"
  "quiet_hours": {                                    // suppress alerts during sleep
    "enabled": true,
    "start": "22:30",
    "end": "08:30"
  },
  "on_demand": {                                      // local API port for ha-cmd.js (disabled by default)
    "enabled": false,
    "port": 9123
  },
  "call_safe_domains": ["light", "climate", "scene", "media_player", "automation", "notify"]
  "telegram_bot_token": "...",
  "telegram_chat_id": "...",
  "echo_devices": {
    "all_devices_announce_id": "",                    // legacy: Alexa announce group (unused)
    "echo_pop_device_id": "notify.echo_pop_di_vincenzo_parla",
    "echo_show_device_id": "notify.echo_show_5_parla"
  }
}
```

## 🔕 Quiet Hours

Suppress alerts during sleep in `config/hub.json`:

```json
"quiet_hours": {
  "enabled": true,
  "start": "22:00",
  "end": "08:00"
}
```

Rules during quiet hours are silently suppressed. To override (e.g., urgent alert), call `notify.send_message` directly — it bypasses rules entirely.

## 📁 Architecture

```
skills/home-assistant-hub/
├── SKILL.md              ← this file (read first!)
├── config/
│   ├── hub.json          ← runtime config (secrets, gitignored)
│   └── hub.example.json  ← template with safe defaults
├── scripts/
│   ├── ha-hub.js         ← WebSocket + polling monitoring engine
│   ├── telegram-deliver.js ← Telegram notification delivery daemon
│   └── ha-cmd.js         ← on-demand read-only + service call CLI (with allowlist enforcement)
├── notifications/        ← pending notification JSON files (gitignored)
├── delivered/            ← successfully delivered notifications (gitignored)
├── logs/                 ← daily rotation logs (gitignored)
├── references/
│   └── setup.md          ← detailed setup guide
├── start.sh              ← portable quick-start script
├── daemon.sh             ← persistent daemon wrapper
└── .gitignore
```

## 🚨 Troubleshooting Quick Reference

| Problem | Solution |
|---------|----------|
| HA connection fails | Check token in HA → Profile → Long-Lived Access Tokens |
| No alerts firing | Verify entity IDs with `ha-cmd.js state list` + grep |
| WS fails but polling works | Normal — hub auto-fallbacks to polling mode |
| Duplicate alerts | Increase `cooldown` in rule config (seconds) |
| **TTS no audio** | Use comma-separated Parla entities. Verify entities exist first with `state list`. |
| Telegram not delivering | Check bot_token and chat_id in hub.json; restart telegram-deliver |
| **"Service domain blocked"** | Add the domain to `call_safe_domains` in hub.json (see Security section above) |
