---
name: mcp-aviation-weather
description: Aviation weather data — METAR observations, TAF forecasts, and nearby station discovery via L402 API. Use for flight planning, airport weather checks, and aviation safety briefings.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - npx
      env:
        - L402_API_BASE_URL
    emoji: ✈️
---

# Aviation Weather (L402)

METAR reports, TAF forecasts, and nearby station search for aviation weather.

## Setup

```json
{
  "mcpServers": {
    "aviation-weather": {
      "command": "npx",
      "args": ["-y", "@vbotholemu/mcp-aviation-weather"],
      "env": {
        "L402_API_BASE_URL": "https://api.nautdev.com"
      }
    }
  }
}
```

## Tools

### `get_metar`
Current METAR observation for any ICAO station.

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| station   | string | yes      | ICAO station code (e.g., KJFK) |

### `get_taf`
Terminal Aerodrome Forecast.

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| station   | string | yes      | ICAO station code |

### `find_stations`
Find nearby weather stations by coordinates.

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| latitude  | number | yes      | Latitude |
| longitude | number | yes      | Longitude |
| radius_nm | number | no       | Search radius in nautical miles |

## When to Use

- Pre-flight weather briefings
- Airport condition monitoring
- Flight planning and routing
- Aviation safety assessments
