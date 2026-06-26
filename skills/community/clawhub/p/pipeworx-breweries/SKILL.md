---
name: pipeworx-breweries
description: Discover craft breweries across the US — search by name, city, or ID via Open Brewery DB
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🍺"
    homepage: https://pipeworx.io/packs/breweries
---

# Open Brewery DB

A comprehensive database of breweries across the United States. Search by name, browse by city, or pull full details for a specific brewery including address, phone, website, and brewery type (micro, nano, brewpub, etc.).

## Tools

- **`search_breweries`** — Find breweries by name or partial name. Returns up to 50 results with location and contact info.
- **`get_brewery`** — Full details for a specific brewery by its Open Brewery DB UUID.
- **`breweries_by_city`** — List breweries in a specific city (e.g., "Portland", "Denver", "Asheville").

## Scenarios

- Planning a brewery crawl in a specific city
- Building a craft beer finder feature for a travel app
- Looking up contact details or website for a brewery someone mentioned
- Analyzing the distribution of brewery types across cities

## Example: breweries in Portland

```bash
curl -s -X POST https://gateway.pipeworx.io/breweries/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"breweries_by_city","arguments":{"city":"Portland","limit":3}}}'
```

Each result includes: name, brewery type, street address, city, state, postal code, phone number, website URL, and coordinates.

## MCP client config

```json
{
  "mcpServers": {
    "pipeworx-breweries": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/breweries/mcp"]
    }
  }
}
```
