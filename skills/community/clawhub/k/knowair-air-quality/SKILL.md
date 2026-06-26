---
name: knowair-forecast
description: Get hourly (up to 360 hours) and daily (up to 15 days) weather forecasts by latitude and longitude via the Caiyun Weather API. Returns temperature trends, weather conditions, precipitation probability, wind, humidity, and life indices. Supports configurable detail levels. Use when the user asks about weather forecast, tomorrow's weather, weekly forecast, hourly forecast, will it rain, temperature trend, or future weather.
license: MIT-0
compatibility: Requires python3 and internet access.
argument-hint: "For example: show the 7-day forecast for Beijing, or hourly forecast for 121.4737,31.2304"
allowed-tools: ["Bash(python3:*)", "Read"]
metadata:
  openclaw:
    emoji: "📅"
    primaryEnv: CAIYUN_TOKEN
    requires:
      env:
        - CAIYUN_TOKEN
      bins:
        - python3
---

# KnowAir Forecast — Hourly & Daily Weather Forecasts

Query detailed hourly and daily weather forecasts for any location using the Caiyun Weather API.

## Prerequisites

1. A valid Caiyun Weather API token set as `CAIYUN_TOKEN` environment variable, or stored in `~/.config/knowair/token`.
2. Coordinates (longitude, latitude) for the target location.

## Quick Start

```bash
python3 scripts/query_forecast.py --lng 116.3176 --lat 39.9760 --type daily --days 7
```

## Workflow

1. **Resolve coordinates** — convert city name to longitude and latitude if needed.
2. **Choose forecast type** — `hourly` or `daily`.
3. **Run the script**:
   ```bash
   python3 scripts/query_forecast.py --lng <LNG> --lat <LAT> --type <TYPE>
   ```
4. **Present results** — highlight temperature ranges, precipitation probability, and notable weather changes.

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--lng` | Longitude (-180 to 180) | Required |
| `--lat` | Latitude (-90 to 90) | Required |
| `--type` | `hourly` or `daily` | `daily` |
| `--hours` | Hours to forecast (1-360, hourly mode) | `48` |
| `--days` | Days to forecast (1-15, daily mode) | `7` |
| `--detail-level` | Display density 0-6 (0=auto, 1=every hour, etc.) | `0` |
| `--lang` | Output language: `en` or `zh` | `en` |

## Defaults

- Forecast type: `daily`
- Days: 7, Hours: 48
- Detail level: auto (0)
- Language: `en`

## Failure Handling

- Missing token → exit code 2 with setup instructions.
- API error → exit code 1 with error details.
- Network unreachable → suggest the user check connectivity.

## Additional Resources

- [examples.md](examples.md) — usage examples
