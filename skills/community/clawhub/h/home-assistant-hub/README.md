# ⚠️ SECURITY & PRIVACY WARNINGS — READ BEFORE INSTALLING

## 🔴 Live Device Control — Hardened Defaults
This skill can invoke Home Assistant services to change physical device states. **Service calls are DISABLED BY DEFAULT.**

### Always Blocked (never configurable)
The following domains are HARD-LOCKED in code:
- `lock.*` → door locks (physical security)
- `alarm_control_panel.*` → alarm systems (safety-critical)
- `cover.*` → blinds/doors/garage (privacy/security)

### Safe Domains — Explicit Opt-In Required
Service calls require domains to be listed in `call_safe_domains` in `config/hub.json`. **An empty list blocks all service calls.**

Default safe domains: `light`, `climate`, `scene`, `media_player`, `automation`, `notify`

### Dry-Run Mode
Always use `--dry-run` first to preview what would be called:
```bash
node scripts/ha-cmd.js call climate.set_temperature entity_id=climate.hvac temperature=22 --dry-run
# Shows: Service URL + payload WITHOUT executing

## 📡 External Data Transmission
This skill sends data to third-party services (Telegram Bot API, Echo devices). Alert messages include occupancy status, sensor states, and routines. Do not include sensitive personal information in alert templates. Notification content is visible on Telegram accounts and potentially logged by Telegram servers.

## 🔐 Credential Sensitivity
All secrets (`ha_token`, `telegram_bot_token`, `telegram_chat_id`) are stored in `config/hub.json`. The HA token is a long-lived bearer token with broad API access — treat it like a password. Default URL uses plain HTTP; use HTTPS if possible to prevent credential exposure on the local network.

---

# Home Assistant Hub

Real-time monitoring of Home Assistant device states with configurable alert rules, TTS voice notifications on Echo devices via Parla entities, Telegram delivery for alerts and events, entity inspection (states, history, persons, areas), and controlled device management through direct service calls.

## What It Does

1. **Monitor** home device states in real-time (polling + WebSocket)
2. **Alert** when conditions change (battery, garage, temperature, occupancy) — delivered via Telegram or voice announcements on Echo devices
3. **Inspect** entities: states, history, persons, areas, scenes
4. **Control** Home Assistant services directly through `ha-cmd.js` calls

### Example use cases

- 🔋 **Battery monitoring**: alerts when charge drops below 20% or exceeds 95% (full charge alert)
- 🏠 **Security monitoring**: garage door open/close, window sensors, motion detection
- 🌡️ **Comfort monitoring**: temperature/humidity thresholds, HVAC status
- 💡 **Device control**: turn lights on/off, set thermostat, activate scenes *(use with caution)*
- 📢 **Voice announcements**: TTS broadcasts to Echo devices via Parla entities

## How It Works

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

### Two background processes

| Process | What it does | Frequency |
|---------|-------------|-----------|
| **ha-hub.js** | Connected to HA, monitors device states against alert rules | Polls every 10s (WebSocket with polling fallback) |
| **telegram-deliver.js** | Reads pending notification files and sends via Telegram | Checks every 30s |

### Notification flow

1. HA device state changes (e.g., battery drops to 19%)
2. `ha-hub.js` detects the change against active alert rules
3. Matching rule writes a JSON file to `notifications/` directory
4. `telegram-deliver.js` picks up the new file and sends via Telegram Bot API
5. File is moved to `delivered/` on success

### On-demand command flow (ha-cmd.js)

1. Run: `node scripts/ha-cmd.js state list light`
2. Receive device states from HA (read-only)

Or for control actions (requires domain opt-in in hub.json):
1. Preview: `node scripts/ha-cmd.js call light.turn_on entity_id=light.living_room --dry-run`
2. Execute: `node scripts/ha-cmd.js call light.turn_on entity_id=light.living_room`

## Quick Start

```bash
# 1. Setup (copy config template)
cp config/hub.example.json config/hub.json
# Edit hub.json with your credentials — NEVER commit this file!

# 2. Test connection to HA
node scripts/ha-cmd.js info

# 3. Add alert rules (interactive or via JSON)
node scripts/ha-hub.js add-rule              # interactive prompt
node scripts/ha-hub.js add-rules << 'EOF'    # via JSON stdin
[{"name":"Low battery","entity_id":"sensor.battery_level","condition":"below","value":"20","cooldown":600,"title":"🪫 Battery","template":"Battery at {{state}}% — low"}]
EOF

# 4. Start the monitoring hub (background process)
node scripts/ha-hub.js start

# 5. Check status
node scripts/ha-hub.js status

# 6. Stop when done
node scripts/ha-hub.js stop
```

## Alert Rules

### Add rule interactively
```bash
node scripts/ha-hub.js add-rule
```

### Add rules via JSON (stdin)
```bash
node scripts/ha-hub.js add-rules << 'EOF'
[
  {
    "name": "Garage opened",
    "entity_id": "binary_sensor.garage_door",
    "condition": "state",
    "value": "on",
    "cooldown": 300,
    "title": "Garage",
    "template": "The garage door is open!"
  },
  {
    "name": "Low battery",
    "entity_id": "sensor.battery_level",
    "condition": "below",
    "value": "20",
    "cooldown": 600,
    "title": "🪫 Battery",
    "template": "Battery at {{state}}% — low"
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
|-----------|---------|---------------|
| `state` | State equals value | `on`, `home`, `open` |
| `not_state` | State not equals value | `away` |
| `above` | Numeric state above threshold | `25` |
| `below` | Numeric state below threshold | `10` |
| `changed` | Always trigger on any change | — |

### Rule fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Human-readable rule identifier |
| `entity_id` | Yes* | Single entity ID to monitor |
| `entities` | Yes* | Array of entity IDs (alternative) |
| `condition` | Yes | Condition type (see table above) |
| `value` | Condition-dependent | Threshold or target value |
| `cooldown` | No | Seconds between alerts (default 300) |
| `title` | No | Alert title in notification |
| `template` | No | Custom message template with `{{state}}` variable |

*Either `entity_id` or `entities` required.

## Voice Notifications (TTS)

Send voice announcements to Echo devices via Parla entities. **This produces audible output inside your home environment.**

```bash
# All Echo devices simultaneously
node scripts/ha-cmd.js call notify.send_message \
  entity_id="notify.echo_show_5_parla,notify.echo_pop_di_vincenzo_parla" \
  message="Dinner is ready"

# Single device
node scripts/ha-cmd.js call notify.send_message \
  entity_id="notify.echo_show_5_parla" \
  message="Hello"
```

Echo device IDs are configured in `config/hub.json` under `echo_devices`. Find available Parla entities:
```bash
node scripts/ha-cmd.js state list 2>&1 | grep -i parla
```

## Telegram Integration

Notifications delivered to a Telegram chat when configured. **⚠️ Alert messages are transmitted externally to Telegram servers and may expose household occupancy patterns.**

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

## On-Demand Commands (`ha-cmd.js`)

### Safe commands (read-only / display only)

| Command | Description | Data exposed |
|---------|-------------|--------------|
| `node scripts/ha-cmd.js info` | HA version, URL, OS, connected clients | System metadata |
| `node scripts/ha-cmd.js state` | All entity states snapshot | Full home telemetry |
| `node scripts/ha-cmd.js state get <id>` | Single entity state | One sensor value |
| `node scripts/ha-cmd.js state list <domain>` | Filter by domain (light, binary_sensor...) | Domain inventory |
| `node scripts/ha-cmd.js scenes` | List all defined scenes | Scene configuration |
| `node scripts/ha-cmd.js persons` | Persons + presence states | **Occupancy data** — who is home |
| `node scripts/ha-cmd.js areas` | Areas with device counts | Home layout, device inventory |

### ⚠️ Control commands (state-changing) — DISABLED BY DEFAULT

The `call` subcommand invokes Home Assistant services. **Execution is blocked unless the domain is listed in `call_safe_domains` in hub.json.** Dangerous domains are hard-locked and cannot be enabled.

| Command | Description |
|---------|-------------|
| `node scripts/ha-cmd.js call <service> [key=value ...] --dry-run` | Preview service call (no execution) |
| `node scripts/ha-cmd.js call <service> [key=value ...]` | Execute — **only if domain is in call_safe_domains** |

#### Examples:

```bash
# TTS announcement (produces audible output)
node scripts/ha-cmd.js call notify.send_message \
  entity_id="notify.echo_show_5_parla" message="Test"

# Turn on a light — changes physical environment
node scripts/ha-cmd.js call light.turn_on entity_id=light.living_room

# Set thermostat temperature — affects comfort
node scripts/ha-cmd.js call climate.set_temperature \
  entity_id=climate.hvac temperature=22

# Activate a scene (multi-device action)
node scripts/ha-cmd.js call scene.turn_on entity_id=scene.movie_time
```



## Hub Config (`config/hub.json`)

Use `hub.example.json` as a template:

```bash
cp config/hub.example.json config/hub.json
# Edit hub.json with your credentials — NEVER commit this file!
```

```json
{
  "ha_url": "http://homeassistant.local:8123",       // use https:// if available
  "ha_token": "your-long-lived-token",               // treat as password — broad API access
  "poll_interval": 10,                                // seconds between polls (WebSocket fallback)
  "rules": [...],                                     // alert rules (see above)
  "notification_channel": "telegram",                 // or: "both"
  "quiet_hours": {                                    // suppress alerts during sleep
    "enabled": true,
    "start": "22:00",
    "end": "08:00"
  },
  "call_safe_domains": ["light", "climate", "scene", "media_player", "automation", "notify"],
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

## 🚨 Troubleshooting

| Problem | Solution |
|---------|----------|
| Connection fails | Check token in HA → Profile → Long-Lived Access Tokens |
| No alerts firing | Verify entity IDs with `node scripts/ha-cmd.js state list` + grep |
| WS fails but polling works | Normal — hub auto-fallbacks to polling mode |
| Duplicate alerts | Increase `cooldown` in rule config (seconds) |
| TTS no audio | Use comma-separated Parla entities. Verify with `state list`. |
| Telegram not delivering | Check bot_token and chat_id in hub.json; restart telegram-deliver |

## Directory Structure

```
skills/home-assistant-hub/
├── SKILL.md              ← skill description (read first)
├── README.md             ← this file (user-facing documentation)
├── config/
│   ├── hub.json          ← runtime config (secrets - gitignored, never commit)
│   └── hub.example.json  ← template with safe defaults
├── scripts/
│   ├── ha-hub.js         ← monitoring engine (WebSocket + polling)
│   ├── telegram-deliver.js ← notification delivery daemon
│   └── ha-cmd.js         ← on-demand CLI: read-only commands + service calls
├── notifications/        ← pending notifications (gitignored)
├── delivered/            ← successfully delivered notifications (gitignored)
├── logs/                 ← daily rotation logs (gitignored)
├── references/
│   └── setup.md          ← detailed installation guide
├── start.sh              ← portable quick-start script
├── daemon.sh             ← persistent background daemon wrapper
└── .gitignore
```
