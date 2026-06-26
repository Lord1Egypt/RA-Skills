# LG Device Skill: Complete Example

This shows exactly what a successful device skill setup produces. Use this as a reference when creating new device skills.

---

## Example Setup Output

After running `setup.sh`:

```json
{
  "success": true,
  "apiServer": "https://api-kic.lgthinq.com",
  "profilesDir": "profiles",
  "devices": [
    {
      "id": "2f33f24132...",
      "name": "Living Room AC",
      "type": "RAC_056905_WW",
      "profilePath": "profiles/device_2f33f24132....json"
    }
  ]
}
```

---

## Generated lg_control.py (Abbreviated)

```python
import os, sys, json, time, requests
from dotenv import load_dotenv

# Load .env from project root (where skill is installed)
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path, override=False)

DEVICE_ID = os.getenv("LG_DEVICE_ID")

# API Server: env var > .api_server_cache > fallback
API_SERVER_CACHE = os.path.join(script_dir, ".api_server_cache")
if os.getenv("LG_API_SERVER"):
    BASE_URL = os.getenv("LG_API_SERVER")
elif os.path.exists(API_SERVER_CACHE):
    with open(API_SERVER_CACHE) as f:
        BASE_URL = f.read().strip()
else:
    BASE_URL = "https://api-kic.lgthinq.com"

def get_headers():
    return {
        "Authorization": f"Bearer {os.getenv('LG_PAT')}",
        "x-api-key": "v6GFvkweNo7DK7yD3ylIZ9w52aKBU0eJ7wLXkSR3",
        "x-client-id": "test-client-123456",
        "x-country": os.getenv("LG_COUNTRY"),
        "x-message-id": "fNvdZ1brTn-wWKUlWGoSVw",
        "Content-Type": "application/json"
    }

def control_property(category, property_name, value):
    # Fetch current state, build snapshot, send command
    ...

# Generated commands
def cmd_operation_airconoperationmode(value):
    return control_property('operation', 'airConOperationMode', value)

def cmd_temperature_cooltargettemperature(value):
    return control_property('temperature', 'coolTargetTemperature', float(value))

# CLI
if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "on":
        print(json.dumps(cmd_operation_airconoperationmode("POWER_ON")))
    elif cmd == "off":
        print(json.dumps(cmd_operation_airconoperationmode("POWER_OFF")))
    elif cmd == "status":
        print(json.dumps(get_status()))
```

---

## Generated SKILL.md

```markdown
---
name: lg-ac-livingroom
description: Control LG Living Room AC. Use for: (1) Power on/off, (2) Adjust temperature (16-30°C), (3) Change mode (cool/heat/dry/fan), (4) Check status.
---

# Living Room AC

## Commands

| Command | Description | Values |
|---------|-------------|--------|
| `on` | Turn AC on | - |
| `off` | Turn AC off | - |
| `status` | Get current state | - |
| `cooltargettemperature <val>` | Set temperature | 16-30 |
| `mode <val>` | Set mode | cool/heat/dry/fan/auto |

## Natural Language Mapping

| User Says | Action |
|-----------|--------|
| "turn on the AC" | `on` |
| "it's too hot" | `on` + `cooltargettemperature 22` |
| "set to 24 degrees" | `cooltargettemperature 24` |
| "turn off" | `off` |
| "check if AC is running" | `status` |

## Decision Logic

1. If device is `POWER_OFF` and user wants to change settings → turn on first
2. Wait 2 seconds after power-on before sending next command
3. Verify with `status` after changes

## Error Handling

| Error | Action |
|-------|--------|
| 401 | Check that `LG_PAT` is exported in the shell |
| 412 | Refresh state, retry |
| Device offline | Check device connectivity |
```

---

## File Structure

```
~/.openclaw/workspace/skills/lg-ac-livingroom/
├── SKILL.md        # Generated from profile
├── lg_control.py   # Generated from profile
├── lg_api_tool.py # Copied from universal skill
└── .env           # Only LG_DEVICE_ID
```

---

## Usage

### Direct Commands
```bash
python lg_control.py on
python lg_control.py cooltargettemperature 24
python lg_control.py status
python lg_control.py --help
```

### Via OpenClaw
- "OpenClaw, turn on the living room AC"
- "OpenClaw, set AC to 24 degrees"
- "OpenClaw, check AC status"
