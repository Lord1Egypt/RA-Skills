---
name: pipeworx-geo
description: Geographic utilities — geocoding, reverse geocoding, country info, timezone lookup, and sunrise/sunset times
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "📍"
    homepage: https://pipeworx.io/packs/geo
---

# Geographic Utilities

A Swiss-army knife for location data. Convert addresses to coordinates (and back), look up country details, check the local timezone, and get sunrise/sunset times — all from free public APIs, no keys needed.

## Tools

| Tool | Description |
|------|-------------|
| `geocode` | Address or place name to lat/lon coordinates (e.g., "Eiffel Tower, Paris") |
| `reverse_geocode` | Lat/lon coordinates to a human-readable address |
| `get_country` | Country details by name or ISO code — population, capital, languages, currencies |
| `get_timezone` | Current timezone and local time for any lat/lon |
| `get_sunrise_sunset` | Sunrise, sunset, golden hour, and day length for a location and date |

## Reach for this when

- A user gives a place name and you need coordinates for another API
- Converting GPS coordinates to a street address
- Answering "what time is it in Tokyo right now?"
- Calculating daylight hours for a specific location and date
- Looking up country metadata (capital, population, languages)

## Example: geocode the Colosseum

```bash
curl -s -X POST https://gateway.pipeworx.io/geo/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"geocode","arguments":{"query":"Colosseum, Rome, Italy"}}}'
```

Returns latitude (41.8902), longitude (12.4922), and display name.

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-geo": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/geo/mcp"]
    }
  }
}
```
