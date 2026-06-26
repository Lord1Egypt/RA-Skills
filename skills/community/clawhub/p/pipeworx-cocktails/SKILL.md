---
name: pipeworx-cocktails
description: Cocktail recipes from TheCocktailDB — search by name, browse by ingredient, or discover a random drink
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🍸"
    homepage: https://pipeworx.io/packs/cocktails
---

# Cocktail Recipes

Shaken or stirred? This pack wraps TheCocktailDB to give you cocktail recipes with full ingredient lists, measurements, and instructions. Search by name, filter by ingredient, or let fate decide with a random cocktail.

## Tools

| Tool | Description |
|------|-------------|
| `search_cocktails` | Search cocktails by name (e.g., "margarita", "old fashioned") |
| `get_cocktail` | Full recipe by TheCocktailDB ID — ingredients, measurements, instructions, and image |
| `random_cocktail` | A random cocktail with complete recipe details |
| `cocktails_by_ingredient` | Find all cocktails using a specific ingredient (e.g., "vodka", "lime juice") |

## Reach for this when

- Someone asks "what can I make with gin and tonic water?"
- Building a cocktail discovery feature for a bar or restaurant app
- Need a random drink suggestion for a party menu
- Want full ingredient lists and preparation instructions for a specific cocktail

## Example: what can I make with rum?

```bash
curl -s -X POST https://gateway.pipeworx.io/cocktails/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"cocktails_by_ingredient","arguments":{"ingredient":"rum"}}}'
```

Returns a list of cocktails (Mojito, Daiquiri, Mai Tai, etc.) with names, thumbnails, and IDs you can pass to `get_cocktail` for the full recipe.

## MCP client config

```json
{
  "mcpServers": {
    "pipeworx-cocktails": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/cocktails/mcp"]
    }
  }
}
```
