---
name: open-meteo-api
description: Fetch weather forecasts, current conditions, historical weather, and air quality with the free Open-Meteo API (no API key). Use for any weather, temperature, rain, wind, UV, sunrise/sunset, air quality, or climate data task, even if Open-Meteo isn't mentioned.
---

# Open-Meteo API

Open-Meteo is a free, open-source weather API. **No API key, no signup** for
non-commercial use (fair-use limit ~10,000 requests/day). It blends national
weather models (NOAA GFS, DWD ICON, ECMWF, Météo-France, JMA...) and
auto-selects the best model per location.

## Fastest path: bundled script

For the common case — current conditions and a daily forecast for a place —
run the bundled zero-dependency script (Python 3.8+, stdlib only) instead of
composing API calls by hand:

```bash
python3 scripts/get_weather.py "Taipei"                 # current + 3-day forecast
python3 scripts/get_weather.py "Paris" --country FR     # disambiguate place name
python3 scripts/get_weather.py --lat 25.05 --lon 121.53 # skip geocoding
python3 scripts/get_weather.py "Tokyo" --days 7 --json  # raw JSON for parsing
python3 scripts/get_weather.py "Denver" --fahrenheit
```

It geocodes, fetches, and decodes WMO weather codes into readable text.
Exit codes: 0 success, 1 place not found, 2 API/network error.

Call the API directly (below) for anything the script doesn't cover: hourly
data, specific variables (UV, soil, radiation...), historical weather, air
quality, marine, or non-Python environments.

## Typical workflow (direct API)

Most user questions name a **place**, but the API takes **coordinates**:

1. **Geocode** the place name → latitude/longitude (Geocoding API below).
   Skip this step if coordinates are already known.
2. **Fetch weather** from the forecast (or other) endpoint.
3. **Interpret** `weather_code` using the WMO table below.

## Quick reference

| Task | Endpoint |
|---|---|
| Forecast / current weather | `https://api.open-meteo.com/v1/forecast` |
| Place name → coordinates | `https://geocoding-api.open-meteo.com/v1/search` |
| Historical weather (1940→now) | `https://archive-api.open-meteo.com/v1/archive` |
| Air quality (PM2.5, AQI, pollen) | `https://air-quality-api.open-meteo.com/v1/air-quality` |
| Marine (waves, sea temp) | `https://marine-api.open-meteo.com/v1/marine` |
| Elevation lookup | `https://api.open-meteo.com/v1/elevation` |

All endpoints: `GET` with query parameters, JSON responses, HTTPS, CORS enabled.
See `references/other-apis.md` for historical/air-quality/marine/elevation/flood/climate details.

## Forecast API

`GET https://api.open-meteo.com/v1/forecast`

Key parameters:

| Parameter | Meaning |
|---|---|
| `latitude`, `longitude` | Required. WGS84 decimal degrees. |
| `current` | Comma-separated variables for current conditions |
| `hourly` | Comma-separated hourly variables |
| `daily` | Comma-separated daily aggregations (**requires `timezone`**) |
| `timezone` | `auto` (recommended — resolves from coordinates) or IANA name like `Asia/Taipei`. Default is GMT. |
| `forecast_days` | 0–16 (default 7) |
| `past_days` | 0–92 — include recent past days in the same response |
| `start_date`, `end_date` | `YYYY-MM-DD`, alternative to forecast_days/past_days |
| `temperature_unit` | `celsius` (default) or `fahrenheit` |
| `wind_speed_unit` | `kmh` (default), `ms`, `mph`, `kn` |
| `precipitation_unit` | `mm` (default) or `inch` |

Most-used variables (full list in `references/weather-variables.md`):

- **current**: `temperature_2m`, `relative_humidity_2m`, `apparent_temperature`,
  `precipitation`, `weather_code`, `wind_speed_10m`, `wind_direction_10m`, `is_day`
- **hourly**: `temperature_2m`, `precipitation_probability`, `precipitation`,
  `weather_code`, `wind_speed_10m`, `relative_humidity_2m`, `cloud_cover`, `uv_index`
- **daily**: `weather_code`, `temperature_2m_max`, `temperature_2m_min`,
  `precipitation_sum`, `precipitation_probability_max`, `sunrise`, `sunset`,
  `uv_index_max`, `wind_speed_10m_max`

### Example: current weather

```
GET https://api.open-meteo.com/v1/forecast?latitude=25.05&longitude=121.53
    &current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m
    &timezone=auto
```

```json
{
  "latitude": 25.06, "longitude": 121.52,
  "timezone": "Asia/Taipei", "utc_offset_seconds": 28800, "elevation": 12.0,
  "current_units": {"temperature_2m": "°C", "wind_speed_10m": "km/h", "weather_code": "wmo code"},
  "current": {
    "time": "2026-07-03T15:00", "interval": 900,
    "temperature_2m": 31.8, "relative_humidity_2m": 63,
    "apparent_temperature": 37.6, "precipitation": 0.0,
    "weather_code": 1, "wind_speed_10m": 5.1
  }
}
```

### Example: 3-day daily forecast

```
GET https://api.open-meteo.com/v1/forecast?latitude=25.05&longitude=121.53
    &daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,sunrise,sunset
    &timezone=auto&forecast_days=3
```

```json
{
  "daily_units": {"temperature_2m_max": "°C", "precipitation_sum": "mm"},
  "daily": {
    "time": ["2026-07-03", "2026-07-04", "2026-07-05"],
    "weather_code": [95, 95, 96],
    "temperature_2m_max": [33.6, 33.5, 33.2],
    "temperature_2m_min": [26.0, 25.7, 26.1],
    "precipitation_sum": [1.5, 4.3, 4.2],
    "precipitation_probability_max": [100, 99, 82],
    "sunrise": ["2026-07-03T05:08", "..."],
    "sunset": ["2026-07-03T18:47", "..."]
  }
}
```

**Response shape**: hourly/daily data comes as **parallel arrays** — `time[i]`
pairs with `temperature_2m_max[i]`. Units for every requested variable are
echoed in `*_units`. Timestamps are ISO 8601 in the requested timezone
(local time when `timezone=auto`), **without** a UTC offset suffix.

## Geocoding API

`GET https://geocoding-api.open-meteo.com/v1/search?name=Taipei&count=5&language=en&format=json`

Parameters: `name` (place name, fuzzy for ≥3 chars), `count` (1–100, default 10),
`language` (lowercase code: `en`, `zh`, `ja`, `de`...).

```json
{
  "results": [
    {
      "id": 1668341, "name": "Taipei",
      "latitude": 25.05306, "longitude": 121.52639,
      "country": "Taiwan", "country_code": "TW",
      "admin1": "Taiwan", "timezone": "Asia/Taipei", "population": 7871900
    }
  ]
}
```

Pick the first result unless the user's context suggests otherwise (check
`country`/`admin1` when names are ambiguous, e.g. Paris TX vs Paris FR; results
are ordered by relevance and population). **No `results` key at all** means no
match — retry with a simpler query (city name only, no district/street; the
geocoder matches localities, not addresses).

## WMO weather codes

`weather_code` values (WMO 4677 subset) — condensed table:

| Code | Meaning |
|---|---|
| 0 | Clear sky |
| 1 / 2 / 3 | Mainly clear / partly cloudy / overcast |
| 45 / 48 | Fog / depositing rime fog |
| 51 / 53 / 55 | Drizzle: light / moderate / dense |
| 56 / 57 | Freezing drizzle: light / dense |
| 61 / 63 / 65 | Rain: slight / moderate / heavy |
| 66 / 67 | Freezing rain: light / heavy |
| 71 / 73 / 75 | Snowfall: slight / moderate / heavy |
| 77 | Snow grains |
| 80 / 81 / 82 | Rain showers: slight / moderate / violent |
| 85 / 86 | Snow showers: slight / heavy |
| 95 | Thunderstorm |
| 96 / 99 | Thunderstorm with slight / heavy hail |

## Code examples

```python
import requests

def get_weather(place: str) -> dict:
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": place, "count": 1}, timeout=10,
    ).json()
    if "results" not in geo:
        raise ValueError(f"Place not found: {place}")
    loc = geo["results"][0]
    r = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": loc["latitude"], "longitude": loc["longitude"],
            "current": "temperature_2m,weather_code,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "timezone": "auto",
        }, timeout=10,
    )
    r.raise_for_status()
    return r.json()
```

```javascript
const geo = await (await fetch(
  `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(place)}&count=1`
)).json();
const { latitude, longitude } = geo.results[0];
const weather = await (await fetch(
  `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}` +
  `&current=temperature_2m,weather_code&timezone=auto`
)).json();
```

## Errors

Errors return HTTP 400 with `{"error": true, "reason": "<message>"}` — e.g.
missing `longitude`, an unknown variable name, or an out-of-range date. Read
`reason`; it states exactly which parameter is wrong.

## Practical tips

- Request **only the variables you need** — response size and quota cost scale
  with variable count and day range.
- Always pass `timezone=auto` when using `daily` (required) or showing times to
  a user; otherwise times are GMT and daily aggregation boundaries are wrong.
- "Will it rain?" → prefer `precipitation_probability` (hourly) or
  `precipitation_probability_max` (daily) over raw `precipitation` amounts.
- Yesterday/last week → use `past_days` on the forecast endpoint. Older than
  ~3 months → use the **archive** endpoint (see `references/other-apis.md`).
  Archive data lags real time by ~5 days.
- The returned `latitude`/`longitude` are the model grid cell center (~1–11 km
  grid), so they differ slightly from the request — that's normal.
- `interval` in `current` is the data refresh interval in seconds; current
  conditions are model data, not station readings.
- Batch multiple locations in one call: `latitude=25.05,24.14&longitude=121.53,120.68`
  returns a JSON array of result objects.
- Free tier is non-commercial use only; commercial use needs a paid API key
  (`&apikey=` on `customer-` prefixed endpoints). No key is needed otherwise.

For the complete variable catalog read `references/weather-variables.md`;
for historical, air-quality, marine, elevation, flood, climate, and ensemble
endpoints read `references/other-apis.md`.
