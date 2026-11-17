# Open-Meteo — Other APIs

All Open-Meteo APIs share the same conventions as the Forecast API: `GET` with
query parameters, no API key, `latitude`/`longitude` required, parallel-array
JSON responses with `*_units`, `timezone=auto` supported, errors as
`{"error": true, "reason": "..."}`. Examples verified against the live API.

## Contents

- [Geocoding API](#geocoding-api)
- [Historical Weather API (Archive)](#historical-weather-api-archive)
- [Air Quality API](#air-quality-api)
- [Marine Weather API](#marine-weather-api)
- [Elevation API](#elevation-api)
- [Flood API](#flood-api)
- [Climate Change API](#climate-change-api)
- [Ensemble Forecast API](#ensemble-forecast-api)

## Geocoding API

`GET https://geocoding-api.open-meteo.com/v1/search`

| Parameter | Meaning |
|---|---|
| `name` | Place name. 1–2 chars = exact match; ≥3 chars = fuzzy match |
| `count` | Number of results, 1–100 (default 10) |
| `language` | Lowercase code (`en`, `zh`, `ja`, `de`, `fr`...) — localizes result names |
| `format` | `json` (default) or `protobuf` |

Response fields per result: `id` (GeoNames ID), `name`, `latitude`, `longitude`,
`elevation`, `timezone`, `population`, `country`, `country_code` (ISO-3166),
`admin1`–`admin4` (administrative areas, largest to smallest), `feature_code`
(GeoNames code, e.g. `PPLC` = capital city, `AIRP` = airport).

Notes:
- Matches localities (cities, towns, districts), **not street addresses**.
- When there is no match, the response has no `results` key at all — check with
  `"results" in data`, not for an empty list.
- Results are ordered by relevance/population; filter by `country_code` or
  `admin1` when the name is ambiguous.

## Historical Weather API (Archive)

`GET https://archive-api.open-meteo.com/v1/archive`

Reanalysis data (ERA5 and better regional models) from **1940 to ~5 days ago**,
worldwide, hourly resolution.

| Parameter | Meaning |
|---|---|
| `start_date`, `end_date` | Required, `YYYY-MM-DD` |
| `hourly`, `daily` | Same variable names as the Forecast API (no `precipitation_probability` — this is measured-past data, not a forecast) |
| Units/timezone params | Same as Forecast API |

```
GET https://archive-api.open-meteo.com/v1/archive?latitude=25.05&longitude=121.53
    &start_date=2025-07-01&end_date=2025-07-02
    &daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto
```

```json
{
  "daily": {
    "time": ["2025-07-01", "2025-07-02"],
    "temperature_2m_max": [36.5, 36.4],
    "temperature_2m_min": [25.9, 26.0],
    "precipitation_sum": [0.0, 0.0]
  }
}
```

Choosing between forecast `past_days` and the archive:
- Last few days/weeks → forecast endpoint with `past_days` (up to 92).
- Anything older, or multi-year analysis → archive endpoint.
- The most recent ~5 days are missing from the archive (reanalysis delay).

## Air Quality API

`GET https://air-quality-api.open-meteo.com/v1/air-quality`

Supports `current` and `hourly` (no `daily`). Forecast up to 7 days
(`forecast_days`, default 5).

Key variables: `pm2_5`, `pm10` (μg/m³), `carbon_monoxide`, `nitrogen_dioxide`,
`sulphur_dioxide`, `ozone` (μg/m³), `us_aqi` (0–500), `european_aqi` (0–100+),
`uv_index`, `dust`, `aerosol_optical_depth`. Pollen (Europe only, in season):
`alder_pollen`, `birch_pollen`, `grass_pollen`, `mugwort_pollen`,
`olive_pollen`, `ragweed_pollen`.

```
GET https://air-quality-api.open-meteo.com/v1/air-quality?latitude=25.05&longitude=121.53
    &current=pm2_5,pm10,us_aqi&timezone=auto
```

```json
{"current": {"time": "2026-07-03T15:00", "pm2_5": 25.2, "pm10": 28.9, "us_aqi": 124}}
```

US AQI bands: 0–50 good, 51–100 moderate, 101–150 unhealthy for sensitive
groups, 151–200 unhealthy, 201–300 very unhealthy, 301+ hazardous.

## Marine Weather API

`GET https://marine-api.open-meteo.com/v1/marine`

Coordinates must be at sea (nearest ocean grid cell is used — the returned
coordinates can shift noticeably toward open water).

Variables (available in `current`, `hourly`, and as `daily` max/dominant
aggregations): `wave_height` (m), `wave_direction` (°), `wave_period` (s),
plus `wind_wave_*` and `swell_wave_*` variants of the same three, and
`sea_surface_temperature` (°C, current/hourly), `ocean_current_velocity`,
`ocean_current_direction`.

```
GET https://marine-api.open-meteo.com/v1/marine?latitude=25.15&longitude=121.75
    &current=wave_height,wave_direction,wave_period,sea_surface_temperature&timezone=auto
```

```json
{"current": {"wave_height": 0.64, "wave_direction": 119, "wave_period": 5.95,
             "sea_surface_temperature": 30.4}}
```

## Elevation API

`GET https://api.open-meteo.com/v1/elevation?latitude=25.05&longitude=121.53`

Returns terrain elevation from a 90 m DEM: `{"elevation": [12.0]}`.
Accepts up to 100 comma-separated coordinate pairs per call.

## Flood API

`GET https://flood-api.open-meteo.com/v1/flood`

River discharge forecasts (GloFAS, ~5 km grid). `daily` variables:
`river_discharge` (m³/s), plus `river_discharge_mean`, `_median`, `_max`,
`_min`, `_p25`, `_p75` ensemble statistics. `forecast_days` up to 210;
historical from 1984 via `start_date`/`end_date`. Values represent the nearest
river within the grid cell, not the exact coordinate.

## Climate Change API

`GET https://climate-api.open-meteo.com/v1/climate`

Downscaled CMIP6 climate projections, **daily** data from 1950 to 2050.

| Parameter | Meaning |
|---|---|
| `start_date`, `end_date` | Required (up to 2050-12-31) |
| `models` | Required. E.g. `EC_Earth3P_HR`, `MRI_AGCM3_2_S`, `CMCC_CM2_VHR4`, `FGOALS_f3_H`, `HiRAM_SIT_HR`, `MPI_ESM1_2_XR`, `NICAM16_8S` — request several and average for robustness |
| `daily` | `temperature_2m_max`, `temperature_2m_min`, `temperature_2m_mean`, `precipitation_sum`, `rain_sum`, `snowfall_sum`, `wind_speed_10m_max`, `relative_humidity_2m_max`, `shortwave_radiation_sum`, etc. |

Use for long-term trends ("how much hotter will summers be in 2040"), never for
actual forecasts.

## Ensemble Forecast API

`GET https://ensemble-api.open-meteo.com/v1/ensemble`

Runs every ensemble member of a model (e.g. `models=icon_seamless` → 40
members) for uncertainty estimation. Same hourly variables as the Forecast
API; the response repeats each variable as `temperature_2m`,
`temperature_2m_member01`, `temperature_2m_member02`, ... Responses get large
quickly — request few variables and short ranges.
