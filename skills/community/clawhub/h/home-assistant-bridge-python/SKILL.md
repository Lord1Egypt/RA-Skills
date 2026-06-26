---
name: home-assistant
description: Control Home Assistant devices, read sensors, and manage automations using the Python Bridge. Use when the user wants to interact with their smart home - turning lights on/off, adjusting thermostats, reading sensor data, checking device states, or creating/modifying automations. Works with any Home Assistant instance accessible via REST API.
---

# Home Assistant Skill (Python Bridge)

Integration with Home Assistant via Python Bridge for reliable smart home control.

## Prerequisites

- Home Assistant instance running (local or remote)
- Long-lived access token from HA profile
- Network connectivity to HA instance
- Python 3 with `requests` module

## Configuration

**One-time setup:**
```bash
cd /root/.openclaw/workspace/skills/home-assistant/scripts
./ha-setup.sh
```

This creates `~/.homeassistant.conf` with your HA_URL and HA_TOKEN.

**Load configuration:**
```bash
source ~/.homeassistant.conf
```

## Core Commands

All commands go through `ha-bridge.py`. Aliases are supported everywhere — use friendly names instead of entity IDs.

### Device Control

```bash
python3 ha-bridge.py on <entity|alias>          # Turn on
python3 ha-bridge.py off <entity|alias>         # Turn off
python3 ha-bridge.py toggle <entity|alias>      # Toggle
python3 ha-bridge.py on <entity> --verify       # Turn on + verify state after 3s
```

**Examples:**
```bash
python3 ha-bridge.py on kitchen                 # Alias → switch.kitchen_light_relay
python3 ha-bridge.py off tv --verify            # Turn off + verify
python3 ha-bridge.py toggle bedroom             # Toggle bedroom light
```

### Light Control

```bash
python3 ha-bridge.py light <entity|alias> --brightness <0-255>
python3 ha-bridge.py light <entity|alias> --color-temp <mireds>
python3 ha-bridge.py light <entity|alias> --rgb "255,0,0"
```

**Examples:**
```bash
python3 ha-bridge.py light bedroom --brightness 128
python3 ha-bridge.py light kitchen --rgb "255,200,100"
```

### Climate Control

```bash
python3 ha-bridge.py climate <entity|alias> --temperature <value>
python3 ha-bridge.py climate <entity|alias> --mode <heat|cool|auto|off>
```

### Scene Activation

```bash
python3 ha-bridge.py scene <scene_entity>
```

### Read States

```bash
python3 ha-bridge.py states                     # All entities (JSON)
python3 ha-bridge.py state <entity|alias>       # Specific entity (JSON)
```

### Search Entities

```bash
python3 ha-bridge.py search <query>             # Search by name or entity_id
python3 ha-bridge.py search licht               # Find all "licht" entities
python3 ha-bridge.py search temp --domain sensor  # Only sensors matching "temp"
```

### History

```bash
python3 ha-bridge.py history <entity|alias>              # Last 24h
python3 ha-bridge.py history kitchen --hours 48           # Last 48h
```

### Aliases

```bash
python3 ha-bridge.py aliases                    # Show all configured aliases
```

Aliases are stored in `scripts/aliases.json`. Edit directly to add/change/remove.

### Services

```bash
python3 ha-bridge.py services                   # List all available HA services
```

## Alias System

Aliases map friendly names to entity IDs. Stored in `scripts/aliases.json`:

```json
{
  "kitchen": "switch.kitchen_light_relay",
  "bedroom": "light.bedroom_led_strip",
  "thermostat": "climate.living_room"
}
```

Use aliases anywhere an entity ID is expected.

## Aliases

Aliases are stored in `scripts/aliases.json`. Copy `scripts/aliases.example.json` as starting point:

```bash
cp scripts/aliases.example.json scripts/aliases.json
```

Then edit with your own device mappings. Use `python3 ha-bridge.py search <query>` to find entity IDs.

## Status Delay Note

Home Assistant needs 1-3 seconds to update state after a command. Use `--verify` to auto-check after 3 seconds.

## File Structure

```
skills/home-assistant/
├── SKILL.md                          # This file
├── README.md                         # Human-readable docs
├── scripts/
│   ├── ha-bridge.py                  # Main bridge (all commands)
│   ├── ha-setup.sh                   # One-time setup
│   ├── aliases.json                  # Your alias mappings (create from example)
│   └── aliases.example.json          # Example alias mappings
└── references/
    └── finding-entities.md           # How to find entity IDs
```
