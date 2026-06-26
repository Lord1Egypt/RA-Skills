# @velocibot/mcp-marine-weather

MCP tool for marine weather forecasts using the NOAA Weather API (api.weather.gov).

## Features

- Current marine conditions (temperature, wind speed/direction)
- Multi-day forecast periods
- Active marine weather warnings and alerts
- Filters alerts for marine-relevant events (storms, wind, surf, coastal flooding)
- No API key required (uses NOAA public API)

## MCP Server Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "marine-weather": {
      "command": "npx",
      "args": ["-y", "@velocibot/mcp-marine-weather"]
    }
  }
}
```

Or if installed globally:

```json
{
  "mcpServers": {
    "marine-weather": {
      "command": "mcp-marine-weather"
    }
  }
}
```

## Tool: marine_forecast

**Input:**
| Parameter | Type   | Required | Description              |
|-----------|--------|----------|--------------------------|
| lat       | number | yes      | Latitude (-90 to 90)    |
| lon       | number | yes      | Longitude (-180 to 180) |

**Example - BVI Waters:**
```json
{
  "lat": 18.4286,
  "lon": -64.6185
}
```

**Output:**
```json
{
  "conditions": {
    "summary": "Partly Cloudy",
    "temperature": 82,
    "temperatureUnit": "F",
    "windSpeed": "15 mph",
    "windDirection": "E",
    "detailed": "Partly cloudy with east winds around 15 mph...",
    "period": "This Afternoon"
  },
  "forecast": [
    {
      "name": "Tonight",
      "temperature": 76,
      "windSpeed": "10 mph",
      "windDirection": "E",
      "forecast": "Mostly Clear"
    }
  ],
  "warnings": [
    {
      "event": "Small Craft Advisory",
      "headline": "Small Craft Advisory until 6 PM",
      "severity": "Moderate"
    }
  ]
}
```

## Coverage

This tool uses the NOAA Weather API which covers the United States and its territories, including:
- US Virgin Islands
- Puerto Rico
- Guam
- American Samoa
- All US coastal waters

## License

MIT
