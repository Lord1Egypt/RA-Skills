# Home Assistant Skill for OpenClaw

Control your smart home through natural language via Home Assistant's REST API.

## Features

- **Device control** — Turn on/off/toggle switches, lights, climate devices
- **Light control** — Brightness, color temperature, RGB colors
- **Climate control** — Temperature, HVAC modes
- **Scene activation** — Trigger HA scenes
- **Entity search** — Find devices by name or domain
- **Alias system** — Map friendly names to entity IDs
- **History** — Query device state history
- **State verification** — Confirm state changes after commands

## Requirements

- Home Assistant instance (local or remote)
- Long-lived access token ([HA Profile → Security → Long-Lived Access Tokens](https://www.home-assistant.io/docs/authentication/#your-account-profile))
- Python 3 with `requests` module
- Network access to your HA instance

## Quick Start

```bash
# 1. Run setup (creates ~/.homeassistant.conf)
cd skills/home-assistant/scripts
./ha-setup.sh

# 2. Source the config
source ~/.homeassistant.conf

# 3. Use it
python3 ha-bridge.py search licht
python3 ha-bridge.py on kitchen_light
python3 ha-bridge.py light bedroom --brightness 128
```

## Alias System

Map friendly names to entity IDs in `scripts/aliases.json`:

```json
{
  "kitchen": "switch.kitchen_light_relay",
  "bedroom": "light.bedroom_led",
  "thermostat": "climate.living_room"
}
```

Then use aliases in any command:

```bash
python3 ha-bridge.py on kitchen
python3 ha-bridge.py light bedroom --brightness 200
python3 ha-bridge.py climate thermostat --temperature 21.5
```

## License

MIT
