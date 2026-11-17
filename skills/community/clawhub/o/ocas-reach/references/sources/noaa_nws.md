# noaa_nws — official US National Weather Service forecasts and alerts

## What this source has

The api.weather.gov endpoint is the National Weather Service's public REST surface. It serves the official US forecasts (the same product the NWS publishes), active alerts (warnings, watches, advisories), current observations from ASOS/AWOS stations, marine forecasts, and gridded model output. US territories and coastal waters are included.

Forecasts come in two granularities: 7-day daily/twice-daily summaries and hourly forecasts ~6.5 days out. Alerts use the Common Alerting Protocol (CAP) — each alert has an `id`, geographic codes (UGCs/SAME), severity, urgency, and effective/expires timestamps.

Use NWS for: authoritative US forecasts, severe-weather alerts (tornado, flash flood, hurricane), point observations from official stations. Pair with `open_meteo` for non-US locations or for archival weather; pair with `usgs_earthquake` for seismic events.

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

NWS requires every request carry a `User-Agent` identifying the caller with a contact. Reach sends `ocas-reach (<agent-email>)` automatically.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | no documented hard cap; informally "be reasonable" — keep below 5 req/sec |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `points` | Resolve a lat/lon to gridpoint metadata | `lat`, `lon` |
| `forecast` | 7-day forecast for a gridpoint | `office`, `x`, `y` |
| `alerts` | Active alerts (filterable) | none |
| `observations` | Latest observation at a station | `station_id` |

## Worked examples

```bash
# Step 1: resolve a coordinate to its gridpoint
python3 scripts/reach.py query noaa_nws points '{"lat": 40.7128, "lon": -74.0060}'
# → {properties: {gridId: "OKX", gridX: 33, gridY: 35, forecastHourly: "...", ...}}

# Step 2: fetch the 7-day forecast for that gridpoint
python3 scripts/reach.py query noaa_nws forecast '{"office": "OKX", "x": 33, "y": 35}'

# Active tornado warnings nationwide
python3 scripts/reach.py query noaa_nws alerts '{"event": "Tornado Warning", "status": "actual"}'

# Active alerts for Texas (state code)
python3 scripts/reach.py query noaa_nws alerts '{"area": "TX"}'

# Latest observation at JFK ASOS
python3 scripts/reach.py query noaa_nws observations '{"station_id": "KJFK"}'
```

## Response shape

- `points`: `{properties: {gridId, gridX, gridY, forecast, forecastHourly, forecastGridData, observationStations, relativeLocation: {properties: {city, state}}, county, fireWeatherZone, timeZone, radarStation}}`. The `gridId/gridX/gridY` triple feeds the next call.
- `forecast`: `{properties: {updated, units, forecastGenerator, generatedAt, periods: [{number, name, startTime, endTime, isDaytime, temperature, temperatureUnit, windSpeed, windDirection, icon, shortForecast, detailedForecast}, ...]}}`. Periods are typically 12-hourly (Day/Night).
- `alerts`: GeoJSON FeatureCollection — `{features: [{properties: {id, areaDesc, sent, effective, expires, ends, status, messageType, severity, certainty, urgency, event, headline, description, instruction, response, parameters, sender, senderName}, geometry: ...}]}`.
- `observations`: `{properties: {timestamp, temperature: {value, unitCode}, dewpoint, windDirection, windSpeed, barometricPressure, relativeHumidity, visibility, cloudLayers: [...]}}`.

## Pitfalls

- **Forecast lookup is a 2-step dance.** You can't go straight from lat/lon to forecast — `points` first, then plug `gridId`/`gridX`/`gridY` into `forecast`. Cache the gridpoint per location; gridpoints don't change.
- **`gridId` (a.k.a. `office`) is a 3-letter forecast-office code** like `OKX` (NYC), `LWX` (DC). The forecast endpoint accepts it under the path param named `office`.
- **Active alerts only.** The `alerts` action returns currently-effective alerts. There's a separate path for historical alerts not wrapped here.
- **`area` filter takes 2-letter state codes**, not zone IDs. For zone-level filtering use `zone` with NWS zone IDs (NYC003 etc.).
- **Units default to US.** Add `units: "si"` (or `"us"`) on forecast for explicit control. Temperatures still come back with `unitCode` like `wmoUnit:degF`.
- **Stations vs gridpoints.** `observations` requires an ICAO/station ID (`KJFK`, `KLAX`), not lat/lon. Get the nearest station list from the `observationStations` URL on `points`.
- **`User-Agent` rule is enforced.** Anonymous-looking UAs return 403.
- **Forecast endpoint can return 503 during model runs.** Retry with backoff — usually clears in 30 seconds.

## Source links

- API docs: https://www.weather.gov/documentation/services-web-api
- OpenAPI spec: https://api.weather.gov/openapi.json
- Terms: https://www.weather.gov/disclaimer
