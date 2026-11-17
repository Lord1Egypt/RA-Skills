# weather — consolidated US weather (NWS + SPC + METAR) + global (Open-Meteo)

## What this source has

A single consolidated source that wraps 4 US government and open weather APIs behind one interface:

- **conditions**: Current observed conditions from the nearest NWS ASOS/AWOS station — temperature, dewpoint, wind, visibility, pressure, sky cover, raw METAR.
- **forecast**: Official NWS 7-day or hourly forecast — detailed periods with temperature, wind, precipitation chance.
- **alerts**: Active NWS warnings, watches, and advisories filtered by lat/lon point or 2-letter state code.
- **metar**: Raw and decoded METAR for any ICAO station (KPDX, KOKC, EGLL, etc.) via aviationweather.gov.
- **brief**: One-call overview — conditions + 3-period forecast + alert count. Optimized for "how's the weather" conversational queries.
- **global**: Current conditions worldwide via Open-Meteo — works for any lat/lon, not just US. Supports US (°F/mph) and metric (°C/kmh) units.
- **severe**: SPC Day 1 categorical outlook (TSTM, MRGL, SLGT, ENH, MDT, HIGH) + active tornado/severe thunderstorm watches. Optional state filter reduces results.

Use `weather` as the default for all weather queries. Pair with individual `noaa_nws` or `open_meteo` sources only if you need raw API shapes or archival access.

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

All endpoints carry the ocas-reach User-Agent automatically.

## Limits

| | |
|---|---|
| Daily | — (no documented cap) |
| Monthly | — |
| Rate | NWS/SPC: keep below 5 req/sec; Open-Meteo: 600/hr, 60/min |

## Endpoints

```bash
python3 scripts/reach.py query weather <action> '<params_json>'
```

| Action | Purpose | Required params |
|---|---|---|
| `conditions` | Current observed conditions | `lat`, `lon` |
| `forecast` | 7-day or hourly forecast | `lat`, `lon` |
| `alerts` | Active warnings/watches | `lat`+`lon` OR `state` |
| `metar` | Raw + decoded METAR | `station` |
| `brief` | Conditions + forecast + alerts overview | `lat`, `lon` |
| `global` | Worldwide current weather | `lat`, `lon` |
| `severe` | SPC outlook + watches | none (optional: `state`) |

## Worked examples

```bash
# Current conditions in Portland, OR
python3 scripts/reach.py query weather conditions '{"lat": 45.5152, "lon": -122.6784}'

# 7-day forecast for Oklahoma City
python3 scripts/reach.py query weather forecast '{"lat": 35.4676, "lon": -97.5164}'

# Active alerts for Texas
python3 scripts/reach.py query weather alerts '{"state": "TX"}'

# Quick briefing for Chicago
python3 scripts/reach.py query weather brief '{"lat": 41.8781, "lon": -87.6298}'

# Current weather in London (Open-Meteo)
python3 scripts/reach.py query weather global '{"lat": 51.5074, "lon": -0.1278}'

# METAR for JFK
python3 scripts/reach.py query weather metar '{"station": "KJFK"}'

# SPC severe outlook + watches
python3 scripts/reach.py query weather severe '{}'

# SPC outlook + Oklahoma alerts
python3 scripts/reach.py query weather severe '{"state": "OK"}'
```

## Response shape

**conditions** — `{station, station_name, timestamp, temperature_c, dewpoint_c, wind_speed_kmh, wind_direction_deg, wind_gust_kmh, barometric_pressure_pa, visibility_m, text_description, raw_metar}`

**forecast** — `{periods: [{name, start, end, temperature, temperature_unit, wind_speed, wind_direction, short_forecast, detailed_forecast, precip_chance}], location: {lat, lon}}`

**alerts** — `{count, alerts: [{event, severity, urgency, certainty, headline, description, onset, expires, sender_name, area_desc}]}`

**metar** — `{station, raw, temperature_c, dewpoint_c, wind_dir_deg, wind_speed_kt, wind_gust_kt, visibility_mi, altimeter_inhg, flight_category, clouds, observation_time}`

**brief** — `{conditions: {…}, forecast_periods: [3 items], alert_count: N, alerts_summary: [headlines], location: {lat, lon}}`

**global** — `{current: {temperature_2m, relative_humidity_2m, apparent_temperature, precipitation, weather_code, wind_speed_10m, wind_direction_10m, wind_gusts_10m, surface_pressure}, units: {…}, location: {lat, lon}}`

**severe** — `{day1_outlook: [{label, label2, stroke}], active_watches: [...], state_alerts: {…} (if state param given)}`

## Pitfalls

- **conditions/forecast need NWS gridpoint resolution.** The connector calls `/points/{lat},{lon}` first internally. This adds one internal HTTP call per request.
- **All US-only.** The `conditions`, `forecast`, `alerts`, and `severe` actions only work for US locations (including territories). Use `global` for international.
- **METAR uses ICAO codes.** 4-letter station IDs only — `KPDX` not `PDX`, `EGLL` not `LHR`.
- **Alerts: `state` takes 2-letter codes.** `TX` not `Texas`. Mutually exclusive with lat/lon — pick one.
- **brief makes 3 internal API calls.** It chains `conditions` + `forecast` + `alerts`. More expensive than single actions but fewer round-trips than calling them separately.
- **global defaults to US units.** Pass `units: "metric"` for °C/kmh. Default is `us` (°F/mph).
- **severe SPC GeoJSON is always CONUS.** The Day 1 outlook covers the continental US. Alaska/Hawaii outlooks come from separate SPC endpoints not yet wired.
- **`weather_code` in global output is a WMO code.** 0=clear, 1-3=cloudy, 45-48=fog, 51-55=drizzle, 61-65=rain, 71-77=snow, 80-82=showers, 95-99=thunderstorm. Don't assume Fahrenheit.

## Source links

- API docs: https://www.weather.gov/documentation/services-web-api
- SPC products: https://www.spc.noaa.gov/products/
- METAR: https://aviationweather.gov/api/data/metar
- Open-Meteo: https://open-meteo.com/en/docs
- Plugin source (reference): https://github.com/FahrenheitResearch/hermes-weather-plugin
