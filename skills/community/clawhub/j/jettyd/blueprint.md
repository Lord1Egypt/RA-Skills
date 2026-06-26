# jettyd + OpenClaw Blueprint

**The complete setup for AI agents that talk to physical hardware.**

This blueprint documents how to connect OpenClaw (or any AI agent stack) to real IoT devices using [jettyd](https://jettyd.com) as the middleware layer.

---

## What this gives you

After following this blueprint, you can ask your AI agent:

> *"What's the temperature in the greenhouse?"*  
> *"Turn on the irrigation relay for 30 seconds."*  
> *"Alert me if humidity drops below 40%."*

And it will work — because your ESP32 is speaking directly to your AI agent.

---

## Architecture

```
[ESP32 device]
    │  jettyd firmware (MIT open source)
    │  - Self-registers on first boot
    │  - Publishes telemetry via MQTT
    │  - Receives commands
    │  - Runs JettyScript rules on-device
    ▼
[jettyd platform]  ←→  [OpenClaw agent]
  api.jettyd.com           MCP server or REST
  mqtt.jettyd.com          skill or LangChain tool
```

---

## Part 1 — Hardware setup (15 minutes)

### What you need
- ESP32-S3, C3, or C6 dev board (~$5)
- USB cable for flashing
- ESP-IDF 5.x installed

### Steps

```bash
# 1. Clone the template
git clone https://github.com/jettydiot/jettyd-firmware-template my-device
cd my-device

# 2. Fetch the SDK
make setup

# 3. Configure — edit sdkconfig.defaults:
#    CONFIG_JETTYD_FLEET_TOKEN="your-fleet-token-here"
#    CONFIG_JETTYD_WIFI_SSID="YourNetworkName"
#    CONFIG_JETTYD_WIFI_PASSWORD="YourNetworkPassword"

# 4. Build and flash
rm -f sdkconfig
idf.py build flash monitor
```

On first boot you'll see:
```
I (13600) jettyd:   Jettyd running
I (13600) jettyd:   Drivers: 0
```

Your device is now provisioned. ✓

---

## Part 2 — Platform account (5 minutes)

1. Sign up at [jettyd.com](https://jettyd.com) → free tier (5 devices)
2. Get your API key from `api.jettyd.com/v1/api-keys`
3. Create a fleet token at `api.jettyd.com/v1/fleet-tokens`
4. Put the fleet token in `sdkconfig.defaults` (step 1 above)

**Test it:**
```bash
curl https://api.jettyd.com/v1/devices \
  -H "Authorization: Bearer YOUR_API_KEY"
# → [{"id": "...", "name": "device-abc", "status": "online"}]
```

---

## Part 3 — Connect to OpenClaw (5 minutes)

### Option A: MCP server (Claude Desktop / Cursor)

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "jettyd": {
      "command": "npx",
      "args": ["@jettyd/mcp"],
      "env": {
        "JETTYD_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Restart Claude Desktop. Now ask: *"What jettyd devices do I have?"*

### Option B: OpenClaw skill

The jettyd skill is installed at `~/.openclaw/workspace/skills/jettyd/`.

Configure in `~/.openclaw/openclaw.json`:
```json
{
  "skills": {
    "entries": {
      "jettyd": {
        "apiKey": "your-api-key-here",
        "baseUrl": "https://api.jettyd.com/v1"
      }
    }
  }
}
```

Use the CLI directly:
```bash
node ~/.openclaw/workspace/skills/jettyd/scripts/jettyd-cli.js list
node ~/.openclaw/workspace/skills/jettyd/scripts/jettyd-cli.js device DEVICE_ID
node ~/.openclaw/workspace/skills/jettyd/scripts/jettyd-cli.js command DEVICE_ID relay.on
```

### Option C: LangChain tool

See `examples/langchain_tool.py` in this directory for a complete LangChain integration.

```python
from jettyd_tool import JettydTool
tools = [JettydTool(api_key="your-key")]
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
agent.run("What is the temperature on my greenhouse sensor?")
```

---

## Part 4 — Add sensors (10 minutes)

Edit `jettyd-sdk/jettyd/src/driver_registry.c`:

```c
#include "dht22.h"

void jettyd_register_drivers(void)
{
    // DHT22 temperature + humidity on GPIO 4
    dht22_config_t air = { .pin = 4 };
    dht22_register("air", &air);
}
```

Rebuild and flash. Readings appear in the device shadow within 60 seconds.

**Available drivers:** DHT22, DS18B20, BME280, HC-SR04, INA219, soil moisture, relay, LED, button, PWM

---

## Part 5 — Automations with JettyScript (5 minutes)

Push rules to your device over the air — no reflashing:

```bash
curl -X PUT https://api.jettyd.com/v1/devices/DEVICE_ID/config \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "rules": [{
      "id": "temp-alert",
      "when": {
        "type": "threshold",
        "sensor": "air.temperature",
        "op": ">",
        "value": 30,
        "debounce": 30
      },
      "then": [{
        "action": "publish_alert",
        "params": {"severity": "warning", "message": "Too hot!"}
      }]
    }]
  }'
```

Subscribe a webhook to forward alerts to Slack, email, or anywhere:
```bash
curl -X POST https://api.jettyd.com/v1/webhooks \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Slack alerts",
    "url": "https://hooks.slack.com/...",
    "events": ["device.alert.warning", "device.alert.critical"]
  }'
```

---

## Part 6 — Dashboard

`app.jettyd.com` — login with your account to see device status, live readings, and send commands from the browser.

---

## Available tools summary

| Interface | Best for |
|-----------|----------|
| MCP server (`@jettyd/mcp`) | Claude Desktop, Cursor, Continue |
| OpenClaw skill | OpenClaw agents (this setup) |
| LangChain tool | Python agent stacks |
| REST API | Any HTTP client |
| Dashboard | Browser / visual overview |

---

## Resources

- Firmware SDK: [github.com/jettydiot/jettyd-firmware](https://github.com/jettydiot/jettyd-firmware) (MIT)
- Template: [github.com/jettydiot/jettyd-firmware-template](https://github.com/jettydiot/jettyd-firmware-template)
- MCP server: [github.com/jettydiot/jettyd-mcp](https://github.com/jettydiot/jettyd-mcp) / `npx @jettyd/mcp`
- Docs: [docs.jettyd.com](https://docs.jettyd.com)
- Waitlist: [jettyd.com](https://jettyd.com)

---

*Built in Johannesburg 🦞 — the IoT dock for AI agents.*
