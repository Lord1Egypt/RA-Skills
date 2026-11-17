# airnow — EPA AirNow Air Quality API

## What this source has

The US EPA's AirNow API provides official Air Quality Index (AQI) data for the United States. Data includes:

- Current AQI observations by ZIP code or lat/lon
- Forecast AQI by ZIP code
- Historical AQI data
- Pollutant-specific data (PM2.5, Ozone, PM10, CO, SO2, NO2)

Use airnow for: checking current air quality in any US location, air quality forecasts, health-related air quality queries, and complementing Open-Meteo's global air quality with official US government data.

## Auth

| | |
|---|---|
| Required | yes (free key) |
| Account | required |
| Signup URL | https://docs.airnowapi.org/ |

Free key required. Registration is instant (email-based). Key is issued immediately.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | 1000/hour (free tier) |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `observation_zip` | Current AQI by ZIP code | `zipCode`, `API_KEY` |
| `observation_latlon` | Current AQI by lat/lon | `latitude`, `longitude`, `API_KEY` |
| `forecast` | AQI forecast by ZIP code | `zipCode`, `API_KEY` |

## Worked examples

```bash
# Current air quality by ZIP code
python3 scripts/reach.py query airnow observation_zip '{"zipCode": "94102", "distance": "25", "API_KEY": "'$AIRNOW_KEY'"}'

# Current air quality by lat/lon
python3 scripts/reach.py query airnow observation_latlon '{"latitude": "37.7749", "longitude": "-122.4194", "distance": "25", "API_KEY": "'$AIRNOW_KEY'"}'

# Air quality forecast
python3 scripts/reach.py query airnow forecast '{"zipCode": "94102", "date": "2024-01-15", "API_KEY": "'$AIRNOW_KEY'"}'
```

## Response shape

Returns an array of AQI observations:

```json
[
  {
    "DateObserved": "2024-01-15",
    "HourObserved": 14,
    "LocalTimeZone": "PST",
    "ReportingArea": "San Francisco",
    "StateCode": "CA",
    "Latitude": 37.7749,
    "Longitude": -122.4194,
    "ParameterName": "PM2.5",
    "AQI": 42,
    "Category": {
      "Number": 1,
      "Name": "Good"
    }
  }
]
```

## Pitfalls

- **US only.** AirNow covers only the United States and territories. For global air quality, use Open-Meteo or OpenAQ.
- **ZIP code must be valid US ZIP.** International postal codes are not supported.
- **Distance parameter controls search radius.** Default is 25 miles. Increase for rural areas.
- **Forecast dates must be within 5 days.** Only short-term forecasts are available.
- **AQI is pollutant-specific.** Each observation covers one pollutant. Multiple pollutants may be returned for the same location/time.
- **Key is required.** Unlike most Reach sources, AirNow requires a free API key. Store in `~/.hermes/.env` as `AIRNOW_KEY`.

## Source links

- AirNow API docs: https://docs.airnowapi.org/
- AQI explanation: https://www.airnow.gov/aqi/aqi-basics/
- Signup: https://docs.airnowapi.org/
