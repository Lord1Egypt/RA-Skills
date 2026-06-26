---
name: pipeworx-carbon
description: UK national carbon intensity data — real-time, historical, and generation mix from the Carbon Intensity API
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🌱"
    homepage: https://pipeworx.io/packs/carbon
---

# UK Carbon Intensity

How clean is the UK electricity grid right now? This pack pulls from the official Carbon Intensity API (carbonintensity.org.uk) maintained by National Grid ESO. Get real-time and historical carbon intensity forecasts plus the current generation fuel mix.

## Tools

| Tool | Purpose |
|------|---------|
| `get_intensity` | Current national carbon intensity — forecast gCO2/kWh, actual value, and index (very low to very high) |
| `get_intensity_by_date` | Carbon intensity data for a specific date (format YYYY-MM-DD) |
| `get_generation_mix` | Current electricity generation breakdown by fuel type (wind, solar, gas, nuclear, etc.) |

## When this is useful

- Smart home systems deciding when to run appliances (charge EVs when intensity is low)
- Sustainability dashboards showing real-time grid carbon data
- Research comparing UK grid decarbonization over time
- Answering "how green is UK electricity right now?"

## Example

```bash
curl -s -X POST https://gateway.pipeworx.io/carbon/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_generation_mix","arguments":{}}}'
```

Returns something like:

```json
{
  "from": "2024-03-15T10:00Z",
  "to": "2024-03-15T10:30Z",
  "mix": [
    { "fuel": "wind", "percentage": 38.2 },
    { "fuel": "nuclear", "percentage": 15.1 },
    { "fuel": "gas", "percentage": 22.4 },
    { "fuel": "solar", "percentage": 8.7 }
  ]
}
```

## Setup

```json
{
  "mcpServers": {
    "pipeworx-carbon": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/carbon/mcp"]
    }
  }
}
```
