---
name: pipeworx-flights
description: Live aircraft tracking — flights in a geographic area, individual aircraft by transponder, and airport arrivals/departures via OpenSky Network
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "✈️"
    homepage: https://pipeworx.io/packs/flights
---

# Flight Tracking (OpenSky Network)

Real-time flight data from the OpenSky Network. Track aircraft by transponder address, query all flights within a geographic bounding box, or pull arrival and departure lists for any airport. Free and open, no API key needed.

## Tools

| Tool | Description |
|------|-------------|
| `get_flights_in_area` | All aircraft currently in a lat/lon bounding box |
| `get_aircraft` | Track a specific aircraft by ICAO24 hex address (e.g., "a0b1c2") |
| `get_arrivals` | Recent arrivals at an airport by ICAO code (e.g., "KLAX") within a time range |
| `get_departures` | Recent departures from an airport by ICAO code within a time range |

## When to use

- "What planes are flying over Manhattan right now?" — define a bounding box around NYC
- Tracking a specific flight by its transponder code
- Building an airport dashboard showing recent arrivals and departures
- Aviation research or ADS-B data analysis

## Example: flights over London

```bash
curl -s -X POST https://gateway.pipeworx.io/flights/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_flights_in_area","arguments":{"lamin":51.3,"lomin":-0.5,"lamax":51.7,"lomax":0.3}}}'
```

Returns ICAO24 address, callsign, origin country, altitude, velocity, heading, and position for each aircraft.

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-flights": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/flights/mcp"]
    }
  }
}
```

## Notes

- Time ranges for arrivals/departures use Unix timestamps and are limited to 7-day windows
- The API updates aircraft positions roughly every 10 seconds
- Anonymous access is rate-limited; data may be slightly delayed
