# @blue-trianon/mcp-aviation-weather

MCP tool for aviation weather data — METAR reports, TAF forecasts, and nearby station discovery via the L402 API.

## Features

- Current METAR observations for any ICAO station
- Terminal Aerodrome Forecasts (TAF)
- Nearby station search by coordinates and radius
- Configurable base URL via environment variable
- Powered by L402 micropayments

## MCP Server Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "aviation-weather": {
      "command": "npx",
      "args": ["-y", "@blue-trianon/mcp-aviation-weather"],
      "env": {
        "NAUTDEV_BASE_URL": "https://api.nautdev.com"
      }
    }
  }
}
```

Or if installed globally:

```json
{
  "mcpServers": {
    "aviation-weather": {
      "command": "mcp-aviation-weather"
    }
  }
}
```

## Tools

### metar

Fetch current METAR weather observation for an aviation station.

| Parameter | Type   | Required | Description                          |
|-----------|--------|----------|--------------------------------------|
| station   | string | yes      | ICAO station identifier (e.g. KJFK) |

### taf

Fetch Terminal Aerodrome Forecast (TAF) for an aviation station.

| Parameter | Type   | Required | Description                          |
|-----------|--------|----------|--------------------------------------|
| station   | string | yes      | ICAO station identifier (e.g. KJFK) |

### nearby_stations

Find nearby aviation weather stations by coordinates.

| Parameter | Type   | Required | Description                              |
|-----------|--------|----------|------------------------------------------|
| lat       | number | yes      | Latitude (-90 to 90)                    |
| lon       | number | yes      | Longitude (-180 to 180)                 |
| radius    | number | no       | Search radius in nautical miles (default: 50) |

## Pricing

Requests are metered via L402 micropayments. See [Blue-Trianon-Ventures](https://github.com/Blue-Trianon-Ventures) for pricing details.

## License

MIT
