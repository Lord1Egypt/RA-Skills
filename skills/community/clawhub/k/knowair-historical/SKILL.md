---
name: knowair-historical
description: Get historical weather data up to 72 hours back via the Caiyun Weather API. Returns past temperature, weather conditions, precipitation, wind, humidity, apparent temperature, and air quality at regular intervals. Use when the user asks about past weather, yesterday's weather, what was the temperature earlier, recent weather history, or weather data from the past few hours/days.
license: MIT-0
compatibility: Requires python3 and internet access.
argument-hint: "For example: what was the weather yesterday at 116.3176,39.9760, or past 24 hours in Shanghai"
allowed-tools: ["Bash(python3:*)", "Read"]
metadata:
  openclaw:
    emoji: "📜"
    primaryEnv: CAIYUN_TOKEN
    requires:
      env:
        - CAIYUN_TOKEN
      bins:
        - python3
---

# KnowAir Historical — Past Weather Data

Query historical weather data for up to 72 hours back using the Caiyun Weather API.

## Prerequisites

1. A valid Caiyun Weather API token set as `CAIYUN_TOKEN` environment variable, or stored in `~/.config/knowair/token`.
2. Coordinates (longitude, latitude) for the target location.

## Quick Start

```bash
python3 scripts/query_historical.py --lng 116.3176 --lat 39.9760 --hours 24
```

## Workflow

1. **Resolve coordinates** — convert city name to coordinates if needed.
2. **Run the script**:
   ```bash
   python3 scripts/query_historical.py --lng <LNG> --lat <LAT> --hours <HOURS>
   ```
3. **Present results** — summarize temperature range, weather changes, and notable events in the past period.

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--lng` | Longitude (-180 to 180) | Required |
| `--lat` | Latitude (-90 to 90) | Required |
| `--hours` | Hours to look back (1-72) | `24` |
| `--lang` | Output language: `en` or `zh` | `en` |

## Defaults

- Hours back: 24
- Language: `en`

## Failure Handling

- Missing token → exit code 2 with setup instructions.
- API error → exit code 1 with error details.
