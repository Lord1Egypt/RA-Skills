---
name: open-meteo
description: "Get weather forecasts via Open-Meteo API (free, no API key). Use when: user asks about weather, temperature, rain probability, UV index, wind, or forecasts for any location. Provides current conditions, hourly forecasts, and 7-day daily forecasts with precipitation probability, feels-like temp, UV index, sunrise/sunset. Also generates Weather Strip SVG widget for the daily digest. Default weather skill — replaces wttr.in."
---

# Open-Meteo Weather

Free weather API. No API key needed. Returns JSON.

## Scripts

### weather.sh — Raw JSON Forecast Data

```
scripts/weather.sh <latitude> <longitude> [current|hourly|daily] [days] [units]
```

- `days`: 1-16 (default 3)
- `units`: `fahrenheit` (default) or `celsius`
- `current` mode returns both current snapshot and daily forecast

```bash
scripts/weather.sh 37.75 -122.43 current 3 fahrenheit
scripts/weather.sh 37.75 -122.43 hourly 2 fahrenheit
scripts/weather.sh 37.75 -122.43 daily 7 fahrenheit
```

### weather_strip.py — SVG Weather Strip Widget

Generates a Weather Strip-style interactive SVG visualization. Features:
- Smooth bezier curves for temperature and dew point
- Cloud cover area graph (semi-transparent, 0-100%)
- Rain amount bar graph (opaque light blue, 0-2 in/hr scale, shown when rain prob >50%)
- Rain probability line overlay
- UV index bar (yellow/orange/red at UV 3+)
- Sky gradient background (sky blue day → navy night, smooth sunrise/sunset transitions)
- Moon phase icon at sunset
- Fixed scrubber bar with scroll-to-read tooltip (shows all metrics)
- Multi-city support with time-range scheduling
- Fixed 0-110°F temperature scale
- 7-day daily forecast strip below hourly

```bash
# Single location
python3 scripts/weather_strip.py --lat 37.75 --lon -122.43 --days 7 \
  > /Users/dapkus/openclaw-apps/digest-app/static/weather-strip.html

# Standalone preview page
python3 scripts/weather_strip.py --lat 37.75 --lon -122.43 --days 7 \
  --output /Users/dapkus/openclaw-apps/digest-app/static/weather-strip-preview.html

# Multi-city with time ranges (for travel)
python3 scripts/weather_strip.py --schedule '[
  {"name":"SF","lat":37.75,"lon":-122.43,"ranges":[
    ["2026-03-01T00:00","2026-03-02T08:00"],
    ["2026-03-06T15:00","2026-03-07T23:00"]
  ]},
  {"name":"Palm Springs","lat":33.83,"lon":-116.55,"ranges":[
    ["2026-03-02T10:00","2026-03-06T13:00"]
  ]}
]' --days 7 > /Users/dapkus/openclaw-apps/digest-app/static/weather-strip.html
```

**Schedule format:** Each location has `name`, `lat`, `lon`, and either:
- `ranges`: list of `["start_iso", "end_iso"]` pairs (hour-level precision, skips transit gaps)
- `dates`: list of `"YYYY-MM-DD"` strings (whole days, simpler)

**Output:** Without `--output`, prints embeddable `<div>` to stdout. With `--output`, writes a full standalone HTML page.

### Digest Integration

The digest app reads `static/weather-strip.html` and includes it at the top of each digest page.

**Regenerate daily** as part of morning digest generation:
1. Generate weather strip → `static/weather-strip.html`
2. If travel scheduled, use `--schedule` with time ranges
3. Default: SF single-location

## Common Coordinates

| Location | Lat | Lon |
|---|---|---|
| San Francisco | 37.75 | -122.43 |
| New York | 40.71 | -74.01 |
| Los Angeles | 34.05 | -118.24 |
| London | 51.51 | -0.13 |
| Palm Springs | 33.83 | -116.55 |

For other cities:
```bash
curl -sf "https://geocoding-api.open-meteo.com/v1/search?name=CityName&count=1" | jq '.results[0] | {name, latitude, longitude}'
```

## WMO Weather Codes

| Code | Meaning |
|---|---|
| 0 | Clear sky |
| 1-3 | Mainly clear / Partly cloudy / Overcast |
| 45, 48 | Fog / Depositing rime fog |
| 51-55 | Drizzle: light / moderate / dense |
| 61-65 | Rain: slight / moderate / heavy |
| 71-75 | Snow: slight / moderate / heavy |
| 80-82 | Rain showers: slight / moderate / violent |
| 95, 96, 99 | Thunderstorm / with hail |

## Interpreting Results

- Parse JSON with `jq`
- `precipitation_probability_max` is the best "will it rain?" signal
- `apparent_temperature` = feels-like (wind chill + humidity)
- `uv_index_max` > 6 = recommend sunscreen
- Times are in the location's local timezone (auto-detected)

## Presentation

Summarize weather conversationally. Lead with what matters: temperature, rain chance, anything unusual. Don't dump raw JSON.
