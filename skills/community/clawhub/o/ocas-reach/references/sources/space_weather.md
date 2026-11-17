# space_weather — NASA DONKI + Open Notify

## What this source has

A composite source combining two APIs for space weather and orbital data:

1. **NASA DONKI** (Space Weather Database Of Notifications, Knowledge, Information) — Solar flares, coronal mass ejections, geomagnetic storms, and interplanetary shocks. Events are classified and timestamped.
2. **Open Notify** — Real-time ISS (International Space Station) location.

Use space_weather for: solar event tracking, geomagnetic storm alerts (relevant for satellite operations, power grids, communications), ISS position, and general space situational awareness.

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

Both APIs are free and require no authentication.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | throttle to <1/sec |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `cme` | Coronal Mass Ejections | none (date range optional) |
| `gst` | Geomagnetic Storms | none (date range optional) |
| `ips` | Interplanetary Shocks | none (date range optional) |
| `iss_location` | ISS current position | none |

## Worked examples

```bash
# Get recent coronal mass ejections
python3 scripts/reach.py query space_weather cme '{}'

# Get geomagnetic storms in a date range
python3 scripts/reach.py query space_weather gst '{"startDate": "2024-01-01", "endDate": "2024-01-15"}'

# Get current ISS position
python3 scripts/reach.py query space_weather iss_location '{}'

# Get interplanetary shocks
python3 scripts/reach.py query space_weather ips '{}'
```

## Response shape

**DONKI events** (CME, GST, IPS) return arrays of event objects:

```json
[
  {
    "activityID": "2024-01-01T00:00:00-CME-001",
    "startTime": "2024-01-01T00:00:00",
    "sourceLocation": "N20W30",
    "activeRegionNumber": "13550",
    "linkedEvents": [...]
  }
]
```

**ISS location** returns:

```json{
  "message": "success",
  "timestamp": 1705286400,
  "iss_position": {
    "latitude": "45.2134",
    "longitude": "-122.4321"
  }
}
```

## Pitfalls

- **NASA DONKI uses DEMO_KEY by default** if no key is provided. For production use, register for a free NASA API key.
- **Date format is YYYY-MM-DD.** No time component for DONKI date range queries.
- **ISS location updates every 5 seconds** but the API has low rate limit. Don't poll frequently.
- **Event data lags real-time by hours to days.** DONKI events are analyzed and posted after detection, not instant.
- **This is a composite source.** CME/GST/IPS query NASA DONKI; ISS location queries Open Notify. The base_url switches per action.

## Source links

- NASA DONKI: https://ccmc.gsfc.nasa.gov/DONKI/
- NASA API portal: https://api.nasa.gov/
- Open Notify: http://open-notify.org/
