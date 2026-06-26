---
name: homeassistant
description: Control Home Assistant entities via REST API. Use when the user asks to control lights, climate, switches, or other HA entities. Supports climate (thermostat), light, switch, and sensor queries.
version: 1.0.0
metadata:
  clawdbot:
    emoji: "🏠"
    requires:
      bins: ["curl", "jq"]
---

# Home Assistant Skill

Control your Home Assistant instance via REST API. Supports climate control, lights, switches, and sensor queries.

## Purpose

This skill provides read and write access to your Home Assistant entities:
- **Climate**: Set temperature, HVAC mode, query current state
- **Lights**: Turn on/off, set brightness, color
- **Switches**: Toggle on/off
- **Sensors**: Query current values
- **Services**: Call any HA service

## Setup

Credentials are stored in `~/.openclaw/credentials/homeassistant.json`:

```json
{
  "url": "http://192.168.2.82:8123",
  "token": "LONG_LIVED_ACCESS_TOKEN"
}
```

To generate a long-lived access token:
1. Open Home Assistant → Profile (bottom left)
2. Scroll to "Long-Lived Access Tokens"
3. Click "Create Token"
4. Name it "clawd" and copy the token

## Commands

All commands use the HA REST API. Output is human-readable by default, add `json` for raw output.

### Climate Control

Set thermostat temperature and mode:

```bash
# Set temperature (auto-selects cool/heat based on setpoint vs current)
bash scripts/climate.sh set <entity_id> <temperature>

# Set specific mode (cool, heat, auto, off)
bash scripts/climate.sh mode <entity_id> <mode>

# Get current climate state
bash scripts/climate.sh status <entity_id>
bash scripts/climate.sh status <entity_id> json
```

**Examples:**
```bash
# Set to 73°F cooling
bash scripts/climate.sh set climate.living_room 73 cool

# Turn off thermostat
bash scripts/climate.sh mode climate.living_room off

# Check current temperature
bash scripts/climate.sh status climate.living_room
```

### List Entities

Find entity IDs for climate, lights, switches:

```bash
# List all climate entities
bash scripts/entities.sh climate

# List all light entities
bash scripts/entities.sh light

# List all switch entities
bash scripts/entities.sh switch

# List all entities of a domain
bash scripts/entities.sh all
```

### Light Control

```bash
# Turn on
bash scripts/light.sh on light.living_room

# Turn off
bash scripts/light.sh off light.living_room

# Set brightness (0-255)
bash scripts/light.sh brightness light.living_room 128

# Set color (RGB)
bash scripts/light.sh color light.living_room 255 0 0

# Get state
bash scripts/light.sh status light.living_room
```

### Switch Control

```bash
# Toggle switch
bash scripts/switch.sh toggle switch.bedroom_fan

# Turn on/off
bash scripts/switch.sh on switch.bedroom_fan
bash scripts/switch.sh off switch.bedroom_fan
```

### Sensor Query

```bash
# Get sensor value
bash scripts/sensor.sh get sensor.temperature_outside
bash scripts/sensor.sh get sensor.humidity_living_room json
```

### Call Service

Direct service call for advanced use:

```bash
# Generic service call
bash scripts/service.sh call <domain> <service> <entity_id> '[{"key": "value"}]'

# Example: Set temperature via climate.set_temperature
bash scripts/service.sh call climate set_temperature climate.living_room '{"temperature": 73}'
```

## Entity Discovery

If you don't know the entity ID:

```bash
# Find all climate entities
bash scripts/entities.sh climate

# Find entities by name (fuzzy search)
bash scripts/entities.sh search thermostat
bash scripts/entities.sh search temperature
```

## Common Workflows

1. **"Make it cold" / "Turn on AC"** → Find climate entity → Set to cool mode at desired temp
2. **"Turn off the lights"** → List light entities → Turn off specific or all
3. **"What's the temperature?"** → Query temperature sensor
4. **"Set thermostat to 73"** → Set climate entity to 73°F

## Error Handling

If the command fails:
- Check HA is reachable: `curl -s http://192.168.2.82:8123`
- Verify token is valid (regenerate if needed)
- Confirm entity ID exists: `bash scripts/entities.sh climate`

## Notes

- HA URL: `http://192.168.2.82:8123` (from MEMORY.md)
- All calls use long-lived access token (no OAuth refresh needed)
- Climate mode mappings: `cool`, `heat`, `auto`, `off`, `heat_cool`
- Temperature unit follows HA configuration (°F for US)

## Reference

- [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest/)
- [Climate Integration](https://www.home-assistant.io/integrations/climate/)