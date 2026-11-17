---
name: openmeteo-daybrief
description: "One-day weather brief from Open-Meteo (no API key): high/low, rain hours, sunset, and dry daylight windows to get outside, optionally fitted into free gaps in your calendar."
homepage: https://open-meteo.com
metadata:
  {
    "openclaw":
      {
        "emoji": "🌤️",
        "requires": { "bins": ["node"] },
      },
  }
---

# openmeteo-daybrief

Use this skill when the user asks about today's or tomorrow's weather, whether to bring an
umbrella, or when there is a good time to go outside. Use it in morning briefings.

## Run

```bash
{baseDir}/scripts/daybrief --lat <latitude> --lon <longitude> --tz <IANA timezone> --date today
```

Options:

- `--date today|tomorrow|YYYY-MM-DD` (default `today`)
- `--units fahrenheit|celsius` (default `fahrenheit`)
- `--gaps-file <path>`: a JSON file with a `gaps` array of `{ "local": "HH:MM-HH:MM" }` free
  slots (for example the output of a calendar tool). Outdoor windows are then limited to those slots.
- `A3_LAT`, `A3_LON`, `A3_TZ` environment variables are used when the flags are omitted.
- `DAYBRIEF_API_URL`: forecast endpoint (default `https://api.open-meteo.com/v1/forecast`), for a
  self-hosted Open-Meteo or to rehearse an outage.
- `DAYBRIEF_CACHE_DIR`: where the last good forecast is kept (default: the system temp directory).
  The request is retried up to three times before the cache is used.

The command prints JSON:

```json
{ "date": "2026-11-16", "condition": "moderate rain", "high": 67.1, "low": 53.6, "unit": "°F",
  "precipChanceMax": 80, "rainHours": "14:00-16:59", "sunrise": "06:26", "sunset": "16:49",
  "outdoorWindows": [{ "start": "08:00", "end": "14:00" }], "gapsConsidered": false }
```

## How to answer

- Lead with condition, high/low, and rain hours, in one or two short lines.
- Suggest the best outdoor window. If `gapsConsidered` is true, say it fits the user's free time.
- If `rainHours` is set, mention an umbrella. If `outdoorWindows` is empty, say so plainly.
- If `cached` is true, Open-Meteo was unreachable and this is the last forecast fetched at
  `fetchedAt` (at most 24 hours old). Use it and say it is the earlier forecast.
- On `{"error": ...}`, say weather is unavailable right now. Do not guess a forecast.

## Notes

- Data: Open-Meteo forecast API (free for non-commercial use, no key, no account).
- No personal data leaves the machine except the coordinates you pass.
