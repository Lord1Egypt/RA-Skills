---
name: pipeworx-nominatim
description: OpenStreetMap geocoding — forward/reverse geocoding and place lookups via the Nominatim API
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🗺️"
    homepage: https://pipeworx.io/packs/nominatim
---

# Nominatim Geocoding

Convert between addresses and coordinates using OpenStreetMap data. Forward geocode place names to lat/lon, reverse geocode coordinates to addresses, and look up specific OSM objects by ID.

## Tools

| Tool | Description |
|------|-------------|
| `search_address` | Free-form address search — returns coordinates, bounding box, and display name |
| `reverse_geocode` | Lat/lon to address (e.g., 48.8584, 2.2945 returns "Eiffel Tower, Paris") |
| `lookup` | Look up specific OpenStreetMap objects by their OSM ID |

## When to use

- Converting a user's typed address into coordinates for a map or weather API
- Identifying what's at a specific set of coordinates
- Resolving ambiguous place names to precise locations
- Building location-aware features without a paid geocoding service

## Example: where is the Sydney Opera House?

```bash
curl -s -X POST https://gateway.pipeworx.io/nominatim/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_address","arguments":{"query":"Sydney Opera House, Australia","limit":1}}}'
```

## Setup

```json
{
  "mcpServers": {
    "pipeworx-nominatim": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/nominatim/mcp"]
    }
  }
}
```

## Note

Nominatim has a usage policy of 1 request per second. The gateway respects this limit automatically.
