---
name: pipeworx-nhtsa
description: Decode VINs and look up vehicle makes/models via the NHTSA Vehicle Product Information Catalog
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🚗"
    homepage: https://pipeworx.io/packs/nhtsa
---

# NHTSA Vehicle Data

Decode Vehicle Identification Numbers (VINs) into make, model, year, body type, engine, and safety features. Also browse all registered vehicle makes and look up available models by make and year.

## Tools

- **`decode_vin`** — Decode a 17-character VIN into structured vehicle attributes
- **`get_makes`** — All vehicle makes (brands) registered with NHTSA
- **`get_models`** — Vehicle models for a specific make and model year (e.g., Toyota 2022)

## When to use

- A user provides a VIN and wants to know the car details
- Building a vehicle lookup feature for insurance or auto parts
- Browsing what models a manufacturer offers in a given year
- Verifying vehicle information from a bill of sale or registration

## Example: decode a VIN

```bash
curl -s -X POST https://gateway.pipeworx.io/nhtsa/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"decode_vin","arguments":{"vin":"1HGBH41JXMN109186"}}}'
```

Returns: make, model, year, body class, drive type, engine displacement, fuel type, plant city, and more.

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-nhtsa": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/nhtsa/mcp"]
    }
  }
}
```
