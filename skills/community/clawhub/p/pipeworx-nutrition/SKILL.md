---
name: pipeworx-nutrition
description: Nutrition MCP — wraps Open Food Facts API (free, no auth)
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/nutrition
---

# pipeworx-nutrition

Nutrition MCP — wraps Open Food Facts API (free, no auth). Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `search_products`
- `get_product`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-nutrition": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/nutrition/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/nutrition](https://pipeworx.io/packs/nutrition)
