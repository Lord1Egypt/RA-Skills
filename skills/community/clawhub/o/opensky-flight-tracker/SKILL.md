---
name: flight-tracker
description: >
  Use this skill when the user asks about live flight positions, aircraft
  tracking by callsign or flight number, or flights currently overhead a
  location. Trigger phrases: flight numbers (EK203, QR42, BA117),
  "where is my flight", "what's flying over me", "track flight",
  "is [flight] in the air", any aircraft callsign.
metadata:
  clawdbot:
    emoji: "✈️"
    requires:
      bins: ["flight-tracker"]
    install:
      - id: pip
        kind: pip
        package: flight-tracker-cli
        bins: ["flight-tracker"]
        label: "Install flight-tracker-cli (pip)"
---

# Flight Tracker Skill

No API key or setup required — works out of the box.

## Commands

### Track an aircraft by callsign

```bash
flight-tracker aircraft EK203
flight-tracker aircraft QR42 --format json
flight-tracker aircraft BAW117 --format summary
```

Shows live position, altitude, speed, heading, and vertical rate for a single aircraft. The aircraft must be currently airborne.

**Callsign format:** Always uppercase. OpenSky uses radio callsigns which usually match the ICAO airline prefix + flight number (e.g. `EK203`, `QR42`, `BAW117`). Note that the radio callsign may differ from the ticket flight number — for example, British Airways flight BA117 uses callsign `BAW117`.

### Aircraft overhead a location

```bash
flight-tracker overhead --lat 25.2048 --lon 55.3657
flight-tracker overhead --lat 51.4775 --lon -0.4614 --radius 100
flight-tracker overhead --lat 40.6413 --lon -73.7781 --format json
```

Shows all airborne aircraft within a radius (default 50 km) of the given coordinates. Results sorted by altitude descending.

## Rate Limits

The OpenSky free tier allows one request every 10 seconds. The CLI handles rate limiting automatically with exponential backoff retries (configurable via `--retries`).

## Output Format

All commands default to `--format summary` which prints a human-readable table. Use `--format json` when piping output to another tool or agent — this outputs clean JSON to stdout with no extra decoration.

## Global Options

- `--retries N` — Number of retries on failure (default: 3)
- `--timeout N` — Request timeout in seconds (default: 20)
