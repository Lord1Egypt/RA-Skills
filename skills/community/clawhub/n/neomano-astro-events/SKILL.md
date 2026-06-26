---
name: neomano-astro-events
description: Astronomy visibility helper for a given location (lat/lon). Lists what you can see tonight and in the next days: Moon phase and rise/set, planet visibility windows, and optional ISS passes. Use when the user asks for astronomical events visible from their coordinates/city.
metadata: {"clawdbot":{"emoji":"🔭","requires":{"bins":["python3"]}}}
---

## Inputs

- Location: `lat`, `lon` (or city).
- Timezone (IANA) or UTC offset (default: infer/ask; Ecuador mainland is UTC-5).
- Horizon constraints (optional): open/urban.

## One-time setup

Create venv and install deps:

```bash
python3 {baseDir}/scripts/bootstrap_venv.py
```

Note: the `.venv/` directory is intentionally not shipped in the skill package; each user creates it locally.

## Run

```bash
python3 {baseDir}/scripts/run.py tonight --lat -2.039958 --lon -79.892266 --tz "America/Guayaquil"
python3 {baseDir}/scripts/run.py next --lat -2.039958 --lon -79.892266 --tz "America/Guayaquil" --days 7
```

## Privacy / offline-by-design

This skill computes everything **locally**.

- No paid APIs.
- No external astronomy services.
- It only downloads **public datasets** (free):
  - JPL ephemeris file (DE421) used by Skyfield.
  - ISS TLE text from Celestrak (for ISS passes).

## What it outputs

- Twilight window (astronomical dusk → dawn)
- Moon phase + rise/set
- Planets: best viewing window (altitude above horizon)
- ISS passes (rise / culminate / set) for the next hours
