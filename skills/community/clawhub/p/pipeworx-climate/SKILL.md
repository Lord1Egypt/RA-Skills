---
name: pipeworx-climate
description: Long-range climate projections from Open-Meteo — temperature trends from 1950 to 2050 with multi-model comparison
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🌍"
    homepage: https://pipeworx.io/packs/climate
---

# Climate Projections

What will the climate look like in 2040? This pack uses the Open-Meteo Climate API to retrieve long-term temperature projections for any location on Earth, spanning 1950 to 2050. Compare outputs across multiple climate models.

## Tools

- **`get_climate_projection`** — Temperature data for a location using the EC_Earth3P_HR model. Provide latitude, longitude, start date, and end date.
- **`compare_models`** — Run the same query across multiple climate models simultaneously to see how projections diverge.

## Use cases

- Visualizing how average temperatures in a specific city have changed since 1950
- Comparing climate model outputs for a research paper
- Building climate risk assessments for real estate or agriculture
- Answering "will summers in London be hotter in 2045?"

## Example: temperature trend for Tokyo

```bash
curl -s -X POST https://gateway.pipeworx.io/climate/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_climate_projection","arguments":{"latitude":35.6762,"longitude":139.6503,"start_date":"2020-01-01","end_date":"2050-12-31"}}}'
```

Returns daily temperature projections with min, max, and mean values.

## Setup

```json
{
  "mcpServers": {
    "pipeworx-climate": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/climate/mcp"]
    }
  }
}
```

## Tips

- Date range must fall between 1950-01-01 and 2050-12-31
- The `compare_models` tool is heavier — use smaller date ranges for faster responses
- Latitude/longitude in decimal degrees (e.g., Tokyo: 35.6762, 139.6503)
