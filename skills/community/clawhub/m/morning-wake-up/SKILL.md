---
name: morning-wake-up
description: >
  Morning wake-up automation that fetches today's weather and matches it to a
  Sonos playback preset. Use when the user asks for a morning routine, wake-up
  automation, weather-based music selection, or daily alarm with Sonos.
  Triggers on phrases like "morning wake-up", "wake me up", "morning routine",
  "weather-based music", "daily alarm with music".
---

# Morning Wake-Up

Automate a morning wake-up flow: fetch weather → match preset → play on Sonos.

## Prerequisites

- Weather skill (Open-Meteo, no API key)
- Sonos CLI (`sonos`) installed and speakers on local network
- At least one Sonos favorite configured per weather category

## Weather-to-Preset Mapping

| Weather Category | WMO Codes | Default Sonos Favorite |
|---|---|---|
| sunny | 0, 1 | `Morning Sunshine` |
| cloudy | 2, 3, 45, 48 | `Cloudy Morning` |
| rain | 51–67, 80–82 | `Rainy Day` |
| snow | 71–77, 85–86 | `Winter Morning` |
| storm | 95–99 | `Storm Chaser` |

Override defaults by editing `scripts/presets.json`.

## Manual Run

```bash
# From the skill directory
bun scripts/wake-up.ts --location "Shanghai" --speaker "Living Room"
```

Parameters:
- `--location` (required): City name or "lat,lon"
- `--speaker` (required): Sonos speaker name
- `--volume` (optional, default 15): Start volume (0–100)
- `--units` (optional, default "celsius"): "celsius" or "fahrenheit"

## Scheduled Automation (cron)

Set up a daily cron job via OpenClaw:

```
cron add — schedule: "0 7 * * *" — payload: "Run morning-wake-up for location Shanghai on speaker Living Room"
```

The agent reads this skill, then executes the wake-up script.

## How It Works

1. **Fetch weather** — calls Open-Meteo API for current conditions at the given location
2. **Map weather code** — translates WMO code to a category using `presets.json`
3. **Play on Sonos** — opens the matching Sonos favorite and sets volume

## Troubleshooting

- `sonos discover` fails → see sonoscli skill troubleshooting (Local Network permission, sandbox mode)
- No matching favorite → falls back to the first available Sonos favorite
- Weather API unreachable → uses last known category if cached, otherwise defaults to `cloudy`
