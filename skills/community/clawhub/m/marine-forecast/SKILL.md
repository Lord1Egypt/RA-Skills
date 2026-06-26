---
name: marine-forecast
description: "Marine and sailing weather via Open-Meteo. Waves, swell, sea temperature, wind, tides, ocean currents, and sailing assessments. Free, no API key, global coverage."
homepage: https://open-meteo.com/en/docs/marine-weather-api
metadata: {"clawdbot":{"emoji":"🌊","requires":{"bins":["curl"]}}}
---

# Marine Forecast

Marine and sailing weather using Open-Meteo Marine API + Weather API. Free, no API key required, works worldwide.

Two APIs are used together — replace `LAT`, `LON`, and `TZ` in all commands:
- **Marine API** (`marine-api.open-meteo.com`) — waves, swell, sea temp, currents, tides
- **Weather API** (`api.open-meteo.com`) — wind, gusts, air temp, pressure, visibility

Find coordinates for any location using web search or the user's input. Use the nearest timezone (IANA format, e.g. `Europe/London`, `America/New_York`, `Atlantic/Canary`).

## Current conditions

Sea state:
```bash
curl -s "https://marine-api.open-meteo.com/v1/marine?latitude=LAT&longitude=LON&current=wave_height,wave_direction,wave_period,swell_wave_height,swell_wave_direction,swell_wave_period,sea_surface_temperature&timezone=TZ"
```

Wind and atmosphere:
```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=LAT&longitude=LON&current=temperature_2m,wind_speed_10m,wind_direction_10m,wind_gusts_10m,apparent_temperature,pressure_msl,cloud_cover,visibility&timezone=TZ"
```

Run both and combine the results into a single briefing.

## Hourly forecast

Marine (up to 16 days, adjust `forecast_days`):
```bash
curl -s "https://marine-api.open-meteo.com/v1/marine?latitude=LAT&longitude=LON&hourly=wave_height,wave_direction,wave_period,swell_wave_height,swell_wave_direction,swell_wave_period,swell_wave_peak_period,wind_wave_height,wind_wave_direction,sea_surface_temperature,ocean_current_velocity,ocean_current_direction,sea_level_height_msl&forecast_days=3&timezone=TZ"
```

Wind (up to 16 days):
```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=LAT&longitude=LON&hourly=wind_speed_10m,wind_direction_10m,wind_gusts_10m,temperature_2m,pressure_msl,visibility,cloud_cover,precipitation_probability&forecast_days=3&timezone=TZ"
```

## Daily summary

Marine:
```bash
curl -s "https://marine-api.open-meteo.com/v1/marine?latitude=LAT&longitude=LON&daily=wave_height_max,wave_direction_dominant,wave_period_max,swell_wave_height_max,swell_wave_direction_dominant,swell_wave_period_max&forecast_days=7&timezone=TZ"
```

Weather:
```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=LAT&longitude=LON&daily=wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_probability_max&forecast_days=7&timezone=TZ"
```

## Tides (sea level)

```bash
curl -s "https://marine-api.open-meteo.com/v1/marine?latitude=LAT&longitude=LON&hourly=sea_level_height_msl&forecast_days=3&timezone=TZ"
```

High/low tide: find local maxima and minima in the `sea_level_height_msl` array. Sea level includes tidal signal + inverted barometer effect.

## Ocean currents

```bash
curl -s "https://marine-api.open-meteo.com/v1/marine?latitude=LAT&longitude=LON&hourly=ocean_current_velocity,ocean_current_direction&forecast_days=3&timezone=TZ"
```

## Presenting results

Always present marine data as a structured sailing briefing:

### Current conditions format

```
Sea:    [wave_height]m waves, [wave_period]s period, from [direction]
Swell:  [swell_wave_height]m from [direction], [swell_wave_period]s period
Wind:   [wind_speed] km/h [direction], gusts [wind_gusts] km/h
Temp:   Air [temperature]C (feels [apparent_temperature]C), Sea [sea_surface_temperature]C
Sky:    [cloud_cover]% cloud, [visibility/1000]km visibility
```

### Sailing assessment

Rate conditions based on the data:
- **Calm** — waves < 0.5m, wind < 12 km/h (Beaufort 0-2)
- **Light** — waves 0.5-1m, wind 12-19 km/h (Beaufort 3)
- **Moderate** — waves 1-2m, wind 20-38 km/h (Beaufort 4-5)
- **Rough** — waves 2-3m, wind 39-49 km/h (Beaufort 6)
- **Very Rough** — waves 3-4m, wind 50-61 km/h (Beaufort 7)
- **Dangerous** — waves > 4m or wind > 62 km/h (Beaufort 8+)

Flag warnings:
- Small craft advisory: wind gusts > 50 km/h or wave height > 3m
- Gale warning: sustained wind > 62 km/h or wave height > 5m
- Suggest activity suitability: sailing, diving, fishing, swimming, surfing

### Beaufort scale

| Force | km/h | Description | Sea State |
|-------|------|-------------|-----------|
| 0 | 0-1 | Calm | Flat |
| 1 | 2-5 | Light air | Ripples |
| 2 | 6-11 | Light breeze | Small wavelets |
| 3 | 12-19 | Gentle breeze | Large wavelets |
| 4 | 20-28 | Moderate breeze | Small waves |
| 5 | 29-38 | Fresh breeze | Moderate waves |
| 6 | 39-49 | Strong breeze | Large waves |
| 7 | 50-61 | Near gale | Breaking waves |
| 8 | 62-74 | Gale | High waves |
| 9 | 75-88 | Severe gale | Very high waves |
| 10 | 89-102 | Storm | Exceptionally high waves |

### Wind direction conversion

Convert degrees to compass: divide by 22.5, round, index into `[N, NNE, NE, ENE, E, ESE, SE, SSE, S, SSW, SW, WSW, W, WNW, NW, NNW]`.

Quick reference: 0=N, 45=NE, 90=E, 135=SE, 180=S, 225=SW, 270=W, 315=NW.

## Units

| Measurement | Unit |
|-------------|------|
| Wave height | meters (m) |
| Wave period | seconds (s) |
| Wind speed | km/h |
| Temperature | Celsius (C) |
| Current velocity | km/h |
| Directions | degrees (0=N, 90=E, 180=S, 270=W) |
| Sea level | meters relative to MSL |
| Visibility | meters |
| Pressure | hPa |

Users may prefer knots for wind. Convert: `knots = km/h * 0.539957`. Add `&wind_speed_unit=kn` to the weather API URL to get knots directly.

## Popular sailing locations (reference)

| Region | Example | Lat | Lon |
|--------|---------|-----|-----|
| Canary Islands | Las Palmas | 28.1 | -15.4 |
| Balearics | Palma de Mallorca | 39.57 | 2.65 |
| Greek Islands | Piraeus | 37.94 | 23.65 |
| Croatia | Split | 43.51 | 16.44 |
| Caribbean | St. Maarten | 18.04 | -63.05 |
| South Pacific | Tahiti | -17.53 | -149.57 |
| Southeast Asia | Phuket | 7.88 | 98.39 |
| East Africa | Zanzibar | -6.16 | 39.19 |
| Australia | Sydney | -33.87 | 151.21 |
| US East Coast | Annapolis | 38.97 | -76.49 |
| UK | Solent | 50.77 | -1.30 |
| Scandinavia | Gothenburg | 57.71 | 11.97 |

## Data sources

- ECMWF WAM (European Centre for Medium-Range Weather Forecasts)
- NOAA GFS Wave (Global Forecast System)
- DWD GWAM/EWAM (German Weather Service)
- Resolution: 5-25 km depending on region and model
- Updates: multiple times per day
- Forecast range: up to 16 days (`forecast_days=16`)

## Notes

- All data is JSON. Parse with `jq` if available, otherwise read raw JSON.
- Hourly data returns large arrays. For quick checks, use `current` parameters. For planning, use `daily`. Use `hourly` only when the user needs detailed breakdowns.
- Combine marine + weather API calls to give a complete picture. Neither alone is sufficient for a full sailing briefing.
- Sea level data approximates tides but does not label high/low explicitly. Derive from local maxima/minima in the hourly array.
- For coastal areas, data accuracy depends on proximity to the nearest grid point. Open ocean coverage is excellent; harbors and bays may be less precise.

Docs: https://open-meteo.com/en/docs/marine-weather-api
