---
name: jettyd
description: Interact with IoT devices via the jettyd platform — read sensors, send commands, manage rules, and list devices
version: 1.1.2
tags:
  - iot
  - esp32
  - sensors
  - automation
  - mqtt
metadata:
  author: jettyd
  license: MIT
  homepage: https://jettyd.com
  api_base: https://api.jettyd.com/v1
  openclaw:
    requires:
      env:
        - JETTYD_API_KEY
      config:
        - path: skills.entries.jettyd.apiKey
          description: API key for jettyd platform (alternative to JETTYD_API_KEY env var)
      bins:
        - node
    network:
      - host: api.jettyd.com
        description: jettyd IoT platform API
    fileAccess:
      - path: ~/.openclaw/openclaw.json
        access: read
        description: Reads API key from OpenClaw config if JETTYD_API_KEY env var is not set
---

# jettyd IoT Skill

Interact with IoT devices via the jettyd platform. Read sensor data, send commands, manage rules, and list devices.

## When to use

Use this skill when the user asks about:
- Device status, online/offline, last seen
- Sensor readings: temperature, humidity, distance, voltage, current
- Controlling actuators: relay, LED, PWM
- Pushing JettyScript rules (threshold alerts, automations)
- Webhook subscriptions for device events
- Anything involving their ESP32 or jettyd devices

## Config

Reads API key from `~/.openclaw/openclaw.json`:
```json
{
  "skills": {
    "entries": {
      "jettyd": {
        "apiKey": "tk_xxxx",
        "baseUrl": "https://api.jettyd.com/v1"
      }
    }
  }
}
```

Or from env: `JETTYD_API_KEY`

## CLI

All operations go through `scripts/jettyd-cli.js`.

```bash
node skills/jettyd/scripts/jettyd-cli.js <command> [args]
```

## Commands

| Command | Description |
|---------|-------------|
| `list` | List all devices with status |
| `device <id>` | Device detail + all sensor readings |
| `telemetry <id> [metric] [period]` | Historical readings (1h/6h/24h/7d) |
| `command <id> <action> [params]` | Send command to device |
| `push_config <id> <json_or_file>` | Push JettyScript rules |
| `webhooks` | List webhook subscriptions |
| `create_webhook <name> <url> <events...>` | Create webhook |

## Example prompts

**"What devices do I have?"**
→ `node .../jettyd-cli.js list`

**"What's the temperature on my greenhouse sensor?"**
→ `node .../jettyd-cli.js list` to find device ID, then `device <id>`

**"Turn on the relay on device abc123"**
→ `node .../jettyd-cli.js command abc123 relay.on`

**"Blink the LED 3 times"**
→ `node .../jettyd-cli.js command abc123 led.blink '{"count":3,"interval_ms":300}'`

**"Alert me if temperature goes above 30°C"**
→ Compose JettyScript JSON and run `push_config <id> <json>`

**"Show me temperature history for the last 24 hours"**
→ `node .../jettyd-cli.js telemetry abc123 temperature 24h`

## push_rules — JettyScript rule format

Use `push_config <id> <json>` to deploy rules to a device. Rules run on the jettyd cloud and fire webhooks / alerts when conditions are met.

**Temperature alert example** — alert when temperature exceeds 30 °C:

```json
{
  "rules": [
    {
      "id": "temp-high-alert",
      "trigger": {
        "type": "threshold",
        "metric": "temperature",
        "operator": ">",
        "value": 30
      },
      "cooldown_seconds": 300,
      "actions": [
        {
          "type": "alert",
          "severity": "warning",
          "message": "Temperature is {{temperature}}°C — above threshold of 30°C"
        }
      ]
    }
  ]
}
```

Push it:

```bash
node skills/jettyd/scripts/jettyd-cli.js push_config <device-id> '{"rules":[...]}'
# or from a file:
node skills/jettyd/scripts/jettyd-cli.js push_config <device-id> ./rules.json
```

Supported trigger operators: `>` `<` `>=` `<=` `==` `!=`
Supported action types: `alert` `webhook` `command`
