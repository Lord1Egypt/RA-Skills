---
name: home-assistant-skill
version: "2.1.0"
description: >
  Control and query Home Assistant via natural language. Covers lights,
  switches, climate, temperature sensors, cameras, automations, energy
  monitoring, EV chargers, presence detection, door sensors, and home
  summaries. Credentials loaded from OpenClaw environment only.
author: openclaw-community
license: MIT
tags:
  - home-assistant
  - smart-home
  - lights
  - climate
  - cameras
  - automation
  - energy
  - iot
  - heating
  - telegram
  - latest

requires:
  env:
    - name: HOME_ASSISTANT_URL
      description: Your Home Assistant URL (e.g. http://homeassistant.local:8123)
    - name: HOME_ASSISTANT_TOKEN
      description: Long-lived access token (HA Profile > Security > Long-Lived Access Tokens)
  optional_env:
    - name: HOME_ASSISTANT_SSL_VERIFY
      description: Set to 'false' if using a self-signed certificate
    - name: HOME_ASSISTANT_CA_CERT
      description: Path to CA certificate file
  python_packages:
    - requests
    - urllib3

security:
  scope: owner-operated
  note: >
    Connects only to the Home Assistant instance you configure via
    HOME_ASSISTANT_URL. All credentials are user-supplied via openclaw.json
    env block. No data is sent to third parties.
  credential_handling: user-supplied-only
  network_access: user-own-home-assistant-only
---

# Home Assistant Integration v2.1 — OpenClaw Skill

Control and query your Home Assistant smart home in plain English through
Telegram or any OpenClaw channel.

## Setup

### 1. Create a Home Assistant Long-Lived Token

In Home Assistant: **Profile** (bottom-left) → **Security** → **Long-Lived Access Tokens** → **Create Token**

Copy the token immediately — it is only shown once.

### 2. Add credentials to openclaw.json

`json
{
  "env": {
    "HOME_ASSISTANT_URL":   "http://homeassistant.local:8123",
    "HOME_ASSISTANT_TOKEN": "your-long-lived-token-here"
  }
}
`

Using HTTPS with a self-signed certificate? Also add:

`json
"HOME_ASSISTANT_SSL_VERIFY": "false"
`

### 3. Restart OpenClaw

`ash
sudo systemctl restart openclaw
`

### 4. Test

Send your bot: home summary

## Security Notes

- Connects **only** to your configured HOME_ASSISTANT_URL — no third-party calls
- Create a dedicated HA user with only the permissions your agent needs
- Store credentials in openclaw.json with restricted permissions (chmod 600)
- Prefer HOME_ASSISTANT_CA_CERT over HOME_ASSISTANT_SSL_VERIFY=false for HTTPS

## What You Can Ask

| Phrase | What happens |
|---|---|
| home summary | Temperatures, lights on, heating status, active switches |
| what is the temperature? | All temperature sensors |
| 	urn off the living room lights | Calls light.turn_off |
| set the heating to 21 degrees | Calls climate.set_temperature |
| is the EV charger on? | Reads switch state |
| show me the front door camera | Returns snapshot URL |
| list all automations | Shows enabled/disabled automations |
| is anyone home? | Reads presence/person entity states |
| what is my energy consumption? | All power/energy sensors |
| 	urn on lights at 80% brightness | Service call with brightness attribute |

## Available Operations

The skill provides 15 Python snippets executed via the OpenClaw exec tool:

- _load_config — loads credentials from environment (always runs first)
- check_api — tests HA connectivity
- ha_summary_for_telegram — full home summary
- get_temperature_sensors — all temperature sensors
- get_lights — lights with brightness levels
- get_switches — all switches with state
- get_climate — thermostat/climate status
- call_service — control any HA device/service
- search_entities — find entities by keyword
- get_cameras — camera list with snapshot URLs
- camera_snapshot — download camera image
- get_automations — all automations with last-triggered
- 	rigger_automation — fire a specific automation
- get_energy — energy and power sensors
- send_notification — send via HA notify service

## Skill File

The full skill implementation is in home_assistant.json in this directory.
It contains all 15 snippets as Python code that the agent executes via
the Home Assistant REST API (/api/states, /api/services/*).

## Troubleshooting

**HOME_ASSISTANT_TOKEN not configured**
Check the HOME_ASSISTANT_TOKEN in your openclaw.json env block and restart OpenClaw.

**401 Unauthorized**
Token expired. Regenerate: HA → Profile → Security → Long-Lived Access Tokens.

**SSL certificate verify failed**
Add "HOME_ASSISTANT_SSL_VERIFY": "false" to your openclaw.json env block.

**Connection refused**
Check HOME_ASSISTANT_URL is correct and HA is running.
