---
name: pipeworx-zippopotam
description: ZIP and postal code lookup — get place names, states, and coordinates for postal codes in 60+ countries
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "📬"
    homepage: https://pipeworx.io/packs/zippopotam
---

# Zippopotam — Postal Code Lookup

Look up postal/ZIP codes in 60+ countries to get place names, state/province, coordinates, and country info. Or go the other direction: find postal codes for a city by country and state.

## Tools

- **`lookup_zipcode`** — Get place info for a ZIP/postal code. Provide the country code (e.g., "us", "gb", "de") and the postal code (e.g., "90210").
- **`lookup_city`** — Find postal codes for a city. Provide country code, state/province abbreviation, and city name.

## When to use

- Address validation — verify that a ZIP code maps to the expected city
- Populating city/state fields automatically after a user enters their ZIP code
- Finding all ZIP codes in a city for geographic analysis
- International postal code lookups across 60+ countries

## Example: look up Beverly Hills 90210

```bash
curl -s -X POST https://gateway.pipeworx.io/zippopotam/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"lookup_zipcode","arguments":{"country":"us","code":"90210"}}}'
```

```json
{
  "post_code": "90210",
  "country": "United States",
  "country_code": "US",
  "places": [{
    "name": "Beverly Hills",
    "state": "California",
    "state_code": "CA",
    "latitude": "34.0901",
    "longitude": "-118.4065"
  }]
}
```

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-zippopotam": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/zippopotam/mcp"]
    }
  }
}
```
