---
name: hivehome
description: Control and query Hive Home (UK) smart heating, hot water, lights and devices via the unofficial API. Use when the user mentions Hive, Hive Home, Hive thermostat, smart heating, Hive app, British Gas Hive, or wants to automate or script Hive devices.
license: MIT
compatibility: Requires Python 3, pyhiveapi>=1.0.0, network access. Hive UK account (my.hivehome.com). For non-interactive use set HIVE_DEVICE_* env vars after first login.
homepage: https://github.com/yourusername/agent-skills
metadata:
  {"openclaw":{"homepage":"https://www.hivehome.com","requires":{"env":["HIVE_USERNAME","HIVE_PASSWORD"]}},"clawdbot":{"emoji":"🏠","requires":{"env":["HIVE_USERNAME","HIVE_PASSWORD"]},"primaryEnv":"HIVE_USERNAME","files":["scripts/*"]}}
---

# Hive Home (UK)

Control Hive thermostats, hot water, lights and other devices programmatically. Hive does **not** provide a public API; this skill uses the community **Pyhiveapi** library, which talks to the same backend as the Hive app.

**Prefer the bundled scripts** for common actions. Run `scripts/hive_control.py` from the skill directory (or `{baseDir}/scripts/hive_control.py` when the agent has the skill path). Only generate custom Pyhiveapi code when the user needs something the scripts do not support (e.g. lights, multi-zone by name, or custom logic).

**Important:** The API is unofficial. Never hardcode credentials or 2FA codes in prompts, logs or code. Use environment variables or a secure secret store.

## Bundled scripts

From the skill root (e.g. `hivehome/` or the skill directory loaded by your agent):

```bash
# Status (heating + hot water)
python scripts/hive_control.py status

# Heating
python scripts/hive_control.py set-temp 21
python scripts/hive_control.py mode heat
python scripts/hive_control.py mode schedule
python scripts/hive_control.py boost 30 21    # 30 min at 21°C
python scripts/hive_control.py boost-off

# Hot water
python scripts/hive_control.py hotwater-boost 30
python scripts/hive_control.py hotwater-boost-off
python scripts/hive_control.py hotwater-mode schedule
python scripts/hive_control.py hotwater-mode off

# Multiple zones (default zone 0)
python scripts/hive_control.py --zone 1 set-temp 20
```

Requires `HIVE_USERNAME`, `HIVE_PASSWORD`; for non-interactive use (e.g. agent runs) set `HIVE_DEVICE_GROUP_KEY`, `HIVE_DEVICE_KEY`, `HIVE_DEVICE_PASSWORD` after one interactive first-time login.

## Credentials

**Required env vars:** `HIVE_USERNAME`, `HIVE_PASSWORD`. For automation (no 2FA each run): `HIVE_DEVICE_GROUP_KEY`, `HIVE_DEVICE_KEY`, `HIVE_DEVICE_PASSWORD`.

**Where to set them:**
- **Generic / Cursor / CLI:** Set in your shell (`export HIVE_USERNAME=...`) or in a local `.env` file that is **not committed**. Run the script in an environment where these are set.
- **OpenClaw:** Set in `~/.openclaw/openclaw.json` under `skills.entries.hivehome.env`. OpenClaw injects these into the process for the agent run; they are not put in prompts or logs.
- **Other agents:** Use that agent’s recommended way to inject env vars or secrets so the skill’s scripts see them at runtime.

**Agent instruction:** If credentials are missing, do not ask the user to paste passwords or keys in chat. Tell them to set the required environment variables (or configure the skill in their agent’s config) and run the script again. See [references/CREDENTIALS.md](references/CREDENTIALS.md) for platform-specific notes.

## When to use this skill

- User asks to control Hive heating, thermostat, or hot water.
- User wants to script or automate Hive devices (heating, lights, plugs).
- User mentions Hive, British Gas Hive, or the Hive app in the context of automation or code.

## Prerequisites

- **Python 3** with **pyhiveapi>=1.0.0** (session API): `pip install "pyhiveapi>=1.0.0"`. If you see attribute or method errors, run `pip install -U pyhiveapi` and try again.
- **Hive account** (UK; my.hivehome.com). First-time login requires **SMS 2FA**; subsequent logins can use device credentials to avoid 2FA.

## Authentication

### First-time login (username + password + 2FA)

Hive enforces two-factor authentication. After initial login, capture **device credentials** for future runs so the user does not need to enter a 2FA code every time.

```python
import os
from pyhiveapi import Hive, SMS_REQUIRED

username = os.environ.get("HIVE_USERNAME")
password = os.environ.get("HIVE_PASSWORD")
if not username or not password:
    raise SystemExit("Set HIVE_USERNAME and HIVE_PASSWORD")

session = Hive(username=username, password=password)
login = session.login()

if login.get("ChallengeName") == SMS_REQUIRED:
    code = input("Enter 2FA code from SMS: ")
    session.sms2fa(code, login)

# Save these for next time (e.g. to env or a secure store)
device_data = session.auth.getDeviceData()
print("Store for device login:", device_data)

session.startSession()
# Now use session.heating, session.hotwater, session.light, etc.
```

### Device login (no 2FA after first time)

Use after the user has run first-time login and stored device credentials. Set `HIVE_DEVICE_GROUP_KEY`, `HIVE_DEVICE_KEY`, `HIVE_DEVICE_PASSWORD` (or pass them another secure way).

```python
import os
from pyhiveapi import Hive

session = Hive(
    username=os.environ["HIVE_USERNAME"],
    password=os.environ["HIVE_PASSWORD"],
    deviceGroupKey=os.environ["HIVE_DEVICE_GROUP_KEY"],
    deviceKey=os.environ["HIVE_DEVICE_KEY"],
    devicePassword=os.environ["HIVE_DEVICE_PASSWORD"],
)
session.deviceLogin()
session.startSession()
```

## Device lists

After `session.startSession()`, devices are in `session.deviceList` by type:

```python
heating = session.deviceList["climate"]
water_heaters = session.deviceList["water_heater"]
lights = session.deviceList["light"]
switches = session.deviceList["switch"]
sensors = session.deviceList["sensor"]
binary_sensors = session.deviceList["binary_sensor"]
```

Use the first (or chosen) device when calling the methods below.

## Heating (thermostat)

```python
if heating:
    zone = heating[0]
    # Read
    session.heating.getMode(zone)
    session.heating.getState(zone)
    session.heating.getCurrentTemperature(zone)
    session.heating.getTargetTemperature(zone)
    session.heating.getBoostStatus(zone)
    session.heating.getBoostTime(zone)
    session.heating.getOperationModes()  # e.g. SCHEDULE, HEAT, OFF

    # Write
    session.heating.setMode(zone, "SCHEDULE")
    session.heating.setMode(zone, "HEAT")
    session.heating.setTargetTemperature(zone, 21)
    session.heating.setBoostOn(zone, 30, 21)   # 30 min at 21°C
    session.heating.setBoostOff(zone)
```

## Hot water

```python
if water_heaters:
    hw = water_heaters[0]
    session.hotwater.getMode(hw)
    session.hotwater.getState(hw)
    session.hotwater.getBoost(hw)
    session.hotwater.setMode(hw, "OFF")
    session.hotwater.setMode(hw, "SCHEDULE")
    session.hotwater.setBoostOn(hw, 30)
    session.hotwater.setBoostOff(hw)
```

## Lights

```python
if lights:
    light = lights[0]
    session.light.getState(light)
    session.light.getBrightness(light)
    session.light.getColorTemp(light)
    session.light.getColor(light)
    # Set state (exact method names depend on pyhiveapi version; see reference)
```

## Quick reference

- **Modes (heating):** `SCHEDULE`, `HEAT`, `OFF` (and others per `getOperationModes()`).
- **Temperatures:** Use integers (e.g. `21` for 21°C). Check `session.heating.getMinTemperature(zone)` / `session.heating.getMaxTemperature(zone)` for limits.
- **Boost:** Heating boost takes (minutes, target_temp); hot water boost takes (minutes) only.

## Additional resources

- Full API surface, auth flow diagram and links: [references/REFERENCE.md](references/REFERENCE.md)
- Pyhiveapi: [GitHub](https://github.com/Pyhass/Pyhiveapi), [Session examples](https://pyhass.github.io/pyhiveapi.docs/docs/examples/session/)
- Home Assistant Hive integration (same backend): [home-assistant.io/integrations/hive](https://www.home-assistant.io/integrations/hive/)

## External endpoints

This skill ships **scripts** (`scripts/hive_control.py`) that call the **Pyhiveapi** Python library. The agent should run these scripts for common actions. When the user needs unsupported behaviour (e.g. lights), the agent may generate Pyhiveapi code. In all cases, only the following endpoints are used. No direct HTTP is made from the skill; Pyhiveapi encapsulates it.

| Purpose | Endpoint / host | Data sent |
|--------|------------------|-----------|
| Login (first time) | `beekeeper.hivehome.com` / `api.prod.bgchprod.info` (via Pyhiveapi) | Hive username, password; after 2FA, device registration |
| Device login | Same | Username, password, device group key, device key, device password |
| Device control (heating, hot water, lights, etc.) | Same | Session token; device IDs and command payloads (e.g. target temperature, mode) |

Credentials and 2FA codes must be supplied via environment variables or user input; the skill never contains or logs them. The bundled script includes a SECURITY MANIFEST header (env vars and endpoints used).

## Security and privacy

- **What leaves the machine:** Hive account credentials (username, password, and optionally device keys) and API requests (device state, setpoints, mode changes) are sent to Hive’s backend (Centrica/British Gas). The skill does not send data elsewhere.
- **What stays local:** Credentials should be stored only in the user’s environment or secret store; the skill instructs the agent never to hardcode or log them.
- **Autonomous invocation:** When this skill is enabled, the agent may suggest or generate code that calls the Hive API when the user asks about heating, thermostats, or Hive. The user controls whether to run that code and what credentials to provide.

## Trust statement

By using this skill, you send your Hive account credentials and device commands to Hive’s servers (beekeeper.hivehome.com / api.prod.bgchprod.info). Only install and use this skill if you trust that infrastructure and the Pyhiveapi library. This skill is not affiliated with Hive or British Gas.
