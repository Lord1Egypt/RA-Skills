# openaq — global air-quality measurements

## What this source has

OpenAQ aggregates real-time and historical air-quality data from government monitoring stations and research-grade sensors worldwide. ~15,000 locations across ~120 countries, with coverage densest in North America, Western Europe, and India. Pollutants tracked: PM2.5, PM10, O3, NO2, SO2, CO, BC, plus relative humidity and temperature where stations report them.

Each measurement has a sensor ID, location ID (a station may have multiple sensors), pollutant parameter, value, unit (µg/m³ or ppm depending on regulator), and timestamp. Coverage time range varies by station — some have 10+ years of history, others started this year.

Use OpenAQ for: current air quality at a point, historical pollution time series, comparing cities. Pair with `open_meteo` for forecasted air quality (different methodology — modelled vs measured); pair with `nominatim` for free-text location → coords first.

## Auth

| | |
|---|---|
| Required | none |
| Env var | `OPENAQ_KEY` |
| Account | optional (recommended for sustained use) |
| Account URL | https://docs.openaq.org/about/about |
| Plan tier | free |

If a key is desired, Reach is authorized to register at the URL above using `<agent-email>`. See `references/account_provisioning.md`. Anonymous access works but is rate-limited harder.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | 60 req/min anonymous; 2000 req/min with key |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `locations` | Find stations by area / parameter | none (use `coordinates`+`radius` or `bbox`) |
| `measurements` | Time-series readings | `locations_id` or `sensors_id` |
| `parameters` | List supported pollutants | none |

## Worked examples

```bash
# Find stations within 25km of a coord that measure PM2.5
python3 scripts/reach.py query openaq locations '{
  "coordinates": "40.7128,-74.0060",
  "radius": 25000,
  "parameters_id": 2,
  "limit": 20
}'

# Recent measurements for one location
python3 scripts/reach.py query openaq measurements '{
  "locations_id": 12345,
  "date_from": "2026-04-01T00:00:00Z",
  "date_to": "2026-04-26T00:00:00Z",
  "limit": 1000
}'

# Stations in a bounding box (Berlin)
python3 scripts/reach.py query openaq locations '{
  "bbox": "13.30,52.45,13.55,52.60",
  "limit": 50
}'

# Supported pollutants
python3 scripts/reach.py query openaq parameters '{}'
```

## Response shape

- `locations`: `{meta: {found, page, limit, ...}, results: [{id, name, locality, country: {id, code, name}, coordinates: {latitude, longitude}, sensors: [{id, name, parameter: {id, name, units, displayName}}], datetimeFirst, datetimeLast, isMobile, isMonitor, ...}]}`.
- `measurements`: `{meta, results: [{value, parameter: {id, name, units}, period: {datetimeFrom: {utc, local}, datetimeTo: {...}}, coordinates, sensorsId, locationsId}, ...]}`.
- `parameters`: `{results: [{id, name, units, displayName, description}, ...]}`. Use the `id` (e.g., 2 = PM2.5) in filters elsewhere.

## Pitfalls

- **v3 ≠ v2.** v3 changed schemas substantially: `locations_id` and `sensors_id` are distinct (a location has many sensors, one per pollutant); v2 conflated them. Don't reuse v2 IDs.
- **`parameters_id` filter** uses the integer ID, not the name. Look up via the `parameters` action: PM2.5=2, PM10=1, O3=3, NO2=5, SO2=6, CO=8.
- **`coordinates` is `lat,lon` as a string** — not lat/lon as separate params. `radius` is meters.
- **Units differ across stations.** µg/m³ for particulate; ppm/ppb for gases in some regulators, µg/m³ in others. Always read `parameter.units` per measurement before comparing.
- **`datetimeFrom`/`datetimeTo`** wraps both UTC and local — use UTC for comparisons across timezones.
- **Mobile vs fixed.** `isMobile: true` stations move (e.g., research vehicles). For consistent time series prefer `isMobile: false`.
- **Rate-limit response is 429** with a `Retry-After` header. Respect it — repeated 429s earn a temporary block.
- **Historical depth varies.** Some stations have minute-resolution; others hourly. Don't assume uniform sampling.

## Source links

- API docs: https://docs.openaq.org/
- v3 reference: https://api.openaq.org/docs
- About / data sources: https://openaq.org/about
