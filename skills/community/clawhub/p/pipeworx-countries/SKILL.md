---
name: pipeworx-countries
description: World country data — search by name, code, region, language, or currency via REST Countries API v3.1
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🌐"
    homepage: https://pipeworx.io/packs/countries
---

# REST Countries

Comprehensive data for every country in the world. Look up population, capital, languages, currencies, flag emoji, and geographic details. Search by name, ISO code, region, spoken language, or currency.

## Tools

| Tool | Description |
|------|-------------|
| `search_countries` | Search countries by name (partial matches work) |
| `get_country_by_code` | Lookup by ISO 3166-1 alpha-2 (e.g., "US") or alpha-3 (e.g., "USA") code |
| `countries_by_region` | List all countries in a region: africa, americas, asia, europe, oceania |
| `countries_by_language` | Countries where a given language is spoken (e.g., "spanish") |
| `countries_by_currency` | Countries using a given currency (e.g., "eur", "usd") |

## Use cases

- Building country selector dropdowns with flags and calling codes
- Answering "what countries speak French?" or "which countries use the Euro?"
- Enriching location data with population, timezone, and regional info
- Geographic research comparing countries by area, population density, or income

## Example: countries that speak Arabic

```bash
curl -s -X POST https://gateway.pipeworx.io/countries/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"countries_by_language","arguments":{"language":"arabic"}}}'
```

Returns each country's name, capital, region, population, and flag emoji.

## Setup

```json
{
  "mcpServers": {
    "pipeworx-countries": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/countries/mcp"]
    }
  }
}
```
