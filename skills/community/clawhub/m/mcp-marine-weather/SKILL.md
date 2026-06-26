---
name: mcp-marine-weather
description: Marine weather forecasts via NOAA api.weather.gov — current conditions, multi-day forecasts, and marine weather warnings. No API key needed. Use when agents need wind, wave, temperature, or storm data for coastal/offshore planning.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - npx
    emoji: 🌊
---

# Marine Weather (NOAA)

Get marine weather conditions, forecasts, and alerts from the NOAA Weather API.

## Setup

```json
{
  "mcpServers": {
    "marine-weather": {
      "command": "npx",
      "args": ["-y", "@vbotholemu/mcp-marine-weather"]
    }
  }
}
```

## Tools

### `get_marine_weather`
Current conditions — temperature, wind speed/direction, humidity.

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| latitude  | number | yes      | Latitude (-90 to 90) |
| longitude | number | yes      | Longitude (-180 to 180) |

### `get_marine_forecast`
Multi-day forecast periods with detailed conditions.

| Parameter | Type   | Required |
|-----------|--------|----------|
| latitude  | number | yes      |
| longitude | number | yes      |

### `get_marine_alerts`
Active marine weather warnings — storms, wind advisories, surf, coastal flooding.

| Parameter | Type   | Required |
|-----------|--------|----------|
| latitude  | number | yes      |
| longitude | number | yes      |

## When to Use

- Sailing/charter trip planning
- Offshore activity safety checks
- Coastal event weather assessment
- Pre-departure weather briefings
