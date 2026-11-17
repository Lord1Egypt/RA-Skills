# open_meteo — global weather forecast, archive, marine, air quality, pollen, flood

## What this source has

Open-Meteo is a free weather API that aggregates several open numerical models (ICON, GFS, ECMWF, ERA5, GEM) into a single JSON surface. Six distinct sub-services exposed here:

- **forecast**: ~16-day forecast at 1-11km resolution depending on region; hourly + daily granularity.
- **archive**: ERA5 reanalysis, 1940 → present at 0.25° resolution (~25km).
- **marine**: wave height, period, direction.
- **air_quality**: PM2.5, PM10, NO2, O3, SO2, CO + UV index, plus pollen as a separate variable group.
- **flood**: GloFAS-based river-discharge forecast.
- **pollen**: shorthand for the air-quality endpoint preset to pollen variables.

Each request takes lat/lon plus a list of variables under `hourly` or `daily`. No identifiers — coords are the key. Models update every few hours.

Use Open-Meteo for: any non-US weather (or US when you want hourly forecast detail), historical weather since 1940, climate-relevant time series. Pair with `noaa_nws` for US-official products.

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

## Limits

| | |
|---|---|
| Daily | 10,000 calls / day (non-commercial) |
| Monthly | — |
| Rate | 600 / hour, 60 / minute |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `forecast` | 16-day forecast | `latitude`, `longitude`, `hourly` or `daily` |
| `archive` | ERA5 historical (1940→) | `latitude`, `longitude`, `start_date`, `end_date`, `hourly` or `daily` |
| `marine` | Wave forecast | `latitude`, `longitude`, `hourly` |
| `air_quality` | Air pollutants + UV | `latitude`, `longitude`, `hourly` |
| `flood` | River discharge forecast | `latitude`, `longitude`, `daily` |
| `pollen` | Pollen variables (preset) | `latitude`, `longitude` |

## Worked examples

```bash
# 7-day temperature forecast, hourly, for Berlin
python3 scripts/reach.py query open_meteo forecast '{
  "latitude": 52.52,
  "longitude": 13.41,
  "hourly": "temperature_2m,precipitation,windspeed_10m",
  "forecast_days": 7
}'

# ERA5 archive for the same location, year 2023
python3 scripts/reach.py query open_meteo archive '{
  "latitude": 52.52,
  "longitude": 13.41,
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum"
}'

# Air quality + UV
python3 scripts/reach.py query open_meteo air_quality '{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "hourly": "pm2_5,pm10,ozone,uv_index"
}'

# Pollen forecast
python3 scripts/reach.py query open_meteo pollen '{
  "latitude": 48.86,
  "longitude": 2.35
}'
```

## Response shape

All sub-services share the same skeleton:

```json
{
  "latitude": 52.52, "longitude": 13.41,
  "generationtime_ms": 0.41,
  "utc_offset_seconds": 0, "timezone": "GMT", "timezone_abbreviation": "GMT",
  "elevation": 38.0,
  "hourly_units": {"time": "iso8601", "temperature_2m": "°C", ...},
  "hourly": {"time": ["2026-04-26T00:00", ...], "temperature_2m": [12.4, ...], ...},
  "daily_units": {...}, "daily": {...}
}
```

The `hourly` (or `daily`) object is a column-store: each variable is a parallel array, all aligned to the `time` array. Index `i` across the arrays gives one timestep.

## Pitfalls

- **Variable list is comma-separated, no spaces.** `temperature_2m,precipitation` — a space breaks the parser.
- **Per-variable units differ.** Always read `hourly_units` rather than assuming °C / mm / m/s.
- **Timezone defaults to GMT.** Pass `timezone: "auto"` to localize to the lat/lon's zone (and shift the `time` array accordingly).
- **Archive has a 5-day lag.** ERA5 reanalysis isn't real-time — `end_date` past ~5 days ago will succeed; today's date returns truncated.
- **Marine endpoint requires an ocean coord.** Inland lat/lon returns mostly nulls.
- **Pollen variables are sparse.** Pollen forecasts only cover Europe, North America, Australia, Japan well; tropical zones return nulls.
- **`forecast_days` max is 16**, default 7. `past_days` adds historical hours to a forecast call (up to 92).
- **Air-quality and forecast are different endpoints.** They share variable naming for things like `temperature_2m` but the air-quality endpoint adds pollutant variables. Don't try to mix them in one call.
- **Flood endpoint uses daily granularity only.**

## Source links

- API docs: https://open-meteo.com/en/docs
- Variable reference: https://open-meteo.com/en/docs (per-endpoint sections)
- Terms (non-commercial): https://open-meteo.com/en/terms
