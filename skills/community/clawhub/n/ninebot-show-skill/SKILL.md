---
name: ninebot-show-skill
description: Read-only Ninebot/九号 electric vehicle status and report skill. Query battery, range, charging, smart-service remaining days, location, monthly/today rides, recent ride details, and generate map or ride-track images through a locally authenticated ninecli session. Use when the user asks about 九号/Ninebot vehicle status, location, rides, smart service, daily reports, or vehicle visualizations.
compatibility: Requires a POSIX shell environment (Linux, macOS, WSL), Python 3, network access, and ninecli 0.1.7 installed by the setup script. Optional AMap Web Service key enables Chinese reverse geocoding and static maps.
metadata:
  version: "3.2.1"
  category: "automation"
  tags: "ninebot,ebike,vehicle,location,report"
  clawhub-slug: "ninebot-show-skill"
---

# Ninebot Show Skill

Read-only Agent Skill for Ninebot/九号 electric vehicles. It uses a locally authenticated `ninecli` session. Never ask the user to paste a Ninebot password, SMS verification code, access token, cookie, or BLE secret into chat.

## Use this skill for

- current battery percentage, estimated/precise range, charging state, battery voltage/temperature;
- smart-service validity and remaining days;
- current vehicle location;
- today/month riding distance, ride count, recent ride details;
- daily or evening vehicle reports;
- static location maps, ride tracks, and speed-distance charts.

## Safety and privacy

Treat these as sensitive: phone numbers, SN/serial numbers, VIN/frame numbers, Bluetooth MAC, Ninebot UID/MID, device IDs, tokens, cookies, BLE secrets, exact coordinates/addresses, and account/vehicle-linked service or ride IDs.

- Never place real values in public Skill files, examples, logs, screenshots, or archives.
- Never copy authentication material from HAR captures into this Skill.
- Default location privacy is `district`; district reverse-geocoding reduces coordinates to ~1 km precision before transmission. Only use `exact` when the user explicitly requests a full address.
- `--json` follows the same privacy mode. Coordinates appear only in `coordinates` mode.
- Do not emit map links containing `position=` unless the user explicitly requests one; use `locate.py --include-map-link` only with `exact` or `coordinates`.
- AMap reverse geocoding/static maps necessarily transmit coordinates and the configured AMap Web Service key to `restapi.amap.com`; OSM map tiles reveal the requested tile area to `tile.openstreetmap.org`; weather queries send the configured weather location to `wttr.in`. See `references/network-privacy.md`.
- Read the vehicle SN only from local configuration or an explicit runtime argument; do not hardcode it.
- Never output credential-grade fields such as `blue_secret`.
- Public examples must come from `references/example-data.md`.

## First-time setup

Run from the skill directory:

```bash
bash scripts/setup.sh
```

Then the user completes Ninebot authentication locally:

```bash
.venv/bin/ninecli login
.venv/bin/ninecli vehicles --json
```

Write the returned vehicle `wnumber` into:

```text
~/.config/ninebot-show-skill/config.json
```

Do not request that the user sends login credentials or tokens to the Agent.

## Main commands

Environment check:

```bash
scripts/run.sh --check
```

Generate a Chinese report:

```bash
scripts/run.sh
```

Machine-readable JSON:

```bash
scripts/run.sh --json
```

Hide location:

```bash
scripts/run.sh --privacy off
```

Coordinates only:

```bash
scripts/run.sh --privacy coordinates --no-weather --json
```

Location helper:

```bash
.venv/bin/python scripts/locate.py --privacy district
```

Static map:

```bash
.venv/bin/python scripts/map_shot.py
```

Recent ride visualization:

```bash
.venv/bin/python scripts/ride_plot.py
```

Specific ride track:

```bash
.venv/bin/python scripts/render_trail.py --out /tmp/track.png --ride <travel_id>
```

## Data sources

- `ninecli status <SN> --json`: current vehicle state.
- `ninecli battery <SN> --json`: main-battery information.
- `ninecli vehicles --json`: vehicle metadata. Only use non-secret report fields.
- `ninecli travel <SN> --month YYYYMM --json`: monthly aggregate and a limited ride list.
- `smart_service_surplus_days`: remaining smart-service days.
- `is_smart_service_expired`: smart-service expiration flag.

More detailed smart-service endpoints observed in traffic captures are encrypted and are **not** treated as supported unless the underlying CLI exposes them safely. Never embed HAR authentication headers or encrypted session material to imitate support.

## Location handling

Vehicle status/trail coordinates are treated as WGS-84. Convert to GCJ-02 before using AMap.

For Chinese reverse geocoding or AMap static maps, set either:

```text
AMAP_WEB_KEY=<your AMap Web Service key>
```

or `AMAP_WEBSERVICE_KEY`. Prefer process environment variables. An optional fallback file is `~/.config/ninebot-show-skill/.env` (or the path in `NINEBOT_ENV_FILE`). Never include a real `.env` in a public Skill archive.

## Limitations

- Monthly ride totals may be complete while the returned detailed ride list is limited to recent rides.
- `trail` does not reliably provide timestamps per point, so the speed chart uses distance as the horizontal axis.
- Some vehicle models omit BMS, motor, online-state, or other fields; report “未获取” instead of guessing.
- Smart-service support is currently limited to expiration state and remaining days unless `ninecli` adds more fields.

## Supporting files

Load these only when needed:

- `references/configuration.md` — configuration and privacy modes.
- `references/example-data.md` — safe public example values.
- `PRIVACY.md` — publication/privacy checklist.
- `README.md` — installation paths for Claude Code, Hermes, OpenClaw, and ClawHub.
