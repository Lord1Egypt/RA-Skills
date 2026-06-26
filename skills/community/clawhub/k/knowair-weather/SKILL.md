---
name: knowair-air-quality
description: Get comprehensive air quality forecast from monitoring stations with up to 15-day coverage via the Caiyun Weather API. Returns AQI, PM2.5, PM10, O3, NO2, SO2, CO values with trend analysis, best/worst periods, and health recommendations. Use when the user asks about air quality, AQI, PM2.5, pollution forecast, smog, air pollution, or is it safe to exercise outdoors.
license: MIT-0
compatibility: Requires python3 and internet access.
argument-hint: "For example: check air quality at 116.3176,39.9760, or air quality forecast for Shanghai"
allowed-tools: ["Bash(python3:*)", "Read"]
metadata:
  openclaw:
    emoji: "💨"
    primaryEnv: CAIYUN_TOKEN
    requires:
      env:
        - CAIYUN_TOKEN
      bins:
        - python3
---

# KnowAir Air Quality — Station-Based AQI Forecast

Query comprehensive air quality forecasts from monitoring stations with up to 15-day coverage using the Caiyun Weather API.

## Prerequisites

1. A valid Caiyun Weather API token set as `CAIYUN_TOKEN` environment variable, or stored in `~/.config/knowair/token`.
2. Coordinates (longitude, latitude) for the target location.

## Quick Start

```bash
python3 scripts/query_air_quality.py --lng 116.3176 --lat 39.9760
```

## Workflow

1. **Resolve coordinates** — convert city name to coordinates if needed.
2. **Run the script**:
   ```bash
   python3 scripts/query_air_quality.py --lng <LNG> --lat <LAT>
   ```
3. **Present results** — summarize current AQI level, pollutant trends, best/worst periods, and health advice.

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--lng` | Longitude (-180 to 180) | Required |
| `--lat` | Latitude (-90 to 90) | Required |
| `--hours` | Forecast hours (1-360) | `120` |
| `--detail-level` | Display density 0-6 (0=auto) | `0` |
| `--lang` | Output language: `en` or `zh` | `en` |

## Defaults

- Hours: 120 (5 days)
- Detail level: auto (0)
- Language: `en`

## Failure Handling

- Missing token → exit code 2 with setup instructions.
- API error → exit code 1 with error details.
- Station data unavailable → falls back to API forecast data.
