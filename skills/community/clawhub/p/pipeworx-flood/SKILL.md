---
name: pipeworx-flood
description: River discharge and flood forecasts for any location — up to 92 days ahead via Open-Meteo
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🌊"
    homepage: https://pipeworx.io/packs/flood
---

# Flood Forecasts

Get daily river discharge predictions for any location on Earth, up to 92 days into the future. The Open-Meteo Flood API provides discharge volumes in cubic meters per second, plus comprehensive forecasts with mean, median, and maximum discharge values.

## Tools

- **`get_river_discharge`** — Daily discharge forecast for a location (lat/lon). Default 7 days, max 92.
- **`get_flood_forecast`** — Comprehensive forecast including mean, max, and additional discharge metrics. Default 16 days.

## When this matters

- Early warning systems for communities near rivers
- Insurance and risk assessment for flood-prone areas
- Agricultural planning that depends on river levels
- Emergency preparedness — checking if a river near coordinates is expected to surge

## Example: Danube river near Vienna

```bash
curl -s -X POST https://gateway.pipeworx.io/flood/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_flood_forecast","arguments":{"latitude":48.2082,"longitude":16.3738,"forecast_days":16}}}'
```

Returns daily discharge values with date and cubic meters per second.

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-flood": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/flood/mcp"]
    }
  }
}
```
