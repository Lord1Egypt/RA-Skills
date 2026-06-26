# Home Assistant Skill for OpenClaw

Control your Home Assistant instance via REST API with natural language commands.

## Features

- **Climate Control**: Set thermostat temperature, HVAC mode, query current state
- **Lights**: Turn on/off, set brightness, color
- **Switches**: Toggle on/off
- **Sensors**: Query current values
- **Entity Discovery**: Find entity IDs by domain or fuzzy search

## Requirements

- Home Assistant instance (local or remote)
- Long-lived access token from HA profile
- `curl` and `jq` installed

## Setup

1. Generate a long-lived access token in Home Assistant:
   - Profile (bottom left) → Long-Lived Access Tokens → Create Token
   - Name it "clawd" or similar

2. Create credentials file at `~/.openclaw/credentials/homeassistant.json`:

```json
{
  "url": "http://your-ha-host:8123",
  "token": "YOUR_LONG_LIVED_ACCESS_TOKEN"
}
```

## Usage

### Climate

```bash
# Set temperature (auto-selects cool/heat)
bash scripts/climate.sh set climate.living_room 73

# Set specific mode
bash scripts/climate.sh mode climate.living_room cool

# Get status
bash scripts/climate.sh status climate.living_room
```

### Lights

```bash
bash scripts/light.sh on light.living_room
bash scripts/light.sh off light.living_room
bash scripts/light.sh brightness light.living_room 128
bash scripts/light.sh color light.living_room 255 0 0
```

### Switches

```bash
bash scripts/switch.sh toggle switch.bedroom_fan
bash scripts/switch.sh on switch.bedroom_fan
```

### Sensors

```bash
bash scripts/sensor.sh get sensor.temperature_outside
```

### Entity Discovery

```bash
bash scripts/entities.sh climate
bash scripts/entities.sh light
bash scripts/entities.sh search thermostat
```

## OpenClaw Integration

Add to your `MEMORY.md`:

```markdown
| Home Assistant | `~/.openclaw/workspace/skills/homeassistant/scripts/` — Climate, lights, switches, sensors |
```

## License

MIT