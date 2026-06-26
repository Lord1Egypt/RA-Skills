---
name: knowair-minutely
description: Get minute-level precipitation forecast for the next 2 hours via the Caiyun Weather API. Returns precipitation intensity at 1-minute intervals and 30-minute probability data. Best for major cities in China. Use when the user asks about rain in the next hour, will it rain soon, should I bring an umbrella, precipitation forecast, or minute-level rain prediction.
license: MIT-0
compatibility: Requires python3 and internet access.
argument-hint: "For example: will it rain in the next 2 hours at 116.3176,39.9760, or check precipitation in Beijing"
allowed-tools: ["Bash(python3:*)", "Read"]
metadata:
  openclaw:
    emoji: "🌧️"
    primaryEnv: CAIYUN_TOKEN
    requires:
      env:
        - CAIYUN_TOKEN
      bins:
        - python3
---

# KnowAir Minutely — Minute-Level Precipitation Forecast

Query minute-level precipitation forecast for the next 2 hours using the Caiyun Weather API. Best coverage for major cities in China.

## Prerequisites

1. A valid Caiyun Weather API token set as `CAIYUN_TOKEN` environment variable, or stored in `~/.config/knowair/token`.
2. Coordinates (longitude, latitude) for the target location.

## Quick Start

```bash
python3 scripts/query_minutely.py --lng 116.3176 --lat 39.9760
```

## Workflow

1. **Resolve coordinates** — convert city name to coordinates if needed.
2. **Run the script**:
   ```bash
   python3 scripts/query_minutely.py --lng <LNG> --lat <LAT>
   ```
3. **Present results** — tell the user when rain starts/stops and the intensity, using the API's natural language description.

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--lng` | Longitude (-180 to 180) | Required |
| `--lat` | Latitude (-90 to 90) | Required |
| `--lang` | Output language: `en` or `zh` | `en` |

## Defaults

- Language: `en`

## Failure Handling

- Missing token → exit code 2 with setup instructions.
- API error → exit code 1 with error details.
- Data unavailable for location → inform user that minutely data is mainly available for China.
