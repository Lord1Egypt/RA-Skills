---
name: pipeworx-citybikes
description: Real-time bike-sharing station data for 600+ networks worldwide — Citi Bike, Velib, Nextbike, and more
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🚲"
    homepage: https://pipeworx.io/packs/citybikes
---

# CityBikes

Real-time availability data for bike-sharing networks around the world. Covers 600+ systems including Citi Bike (NYC), Velib (Paris), Nextbike (Berlin), and many more. Check station availability, search by city, or list every network on the planet.

## Tools

| Tool | What it does |
|------|-------------|
| `list_networks` | Every bike-sharing network worldwide with city, country, and company info |
| `get_network` | All stations for a specific network with real-time bike/slot availability |
| `search_networks` | Find networks by city or country name (e.g., "New York", "France") |

## Ideal for

- Travel apps showing nearest available bikes in a city
- Urban mobility dashboards comparing bike-share systems
- Answering "are there bikes available near me?" when given a city
- Research on micro-mobility infrastructure across countries

## Example: Citi Bike NYC station availability

```bash
curl -s -X POST https://gateway.pipeworx.io/citybikes/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_network","arguments":{"id":"citi-bike-nyc"}}}'
```

Returns every station with: name, latitude, longitude, free bikes, empty slots, and timestamp.

## Common network IDs

| City | Network ID |
|------|-----------|
| New York | `citi-bike-nyc` |
| Paris | `velib` |
| London | `santander-cycles` |
| Berlin | `nextbike-berlin` |
| Chicago | `divvy` |

## Setup

```json
{
  "mcpServers": {
    "pipeworx-citybikes": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/citybikes/mcp"]
    }
  }
}
```
