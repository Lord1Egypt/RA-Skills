---
name: pipeworx-fruityvice
description: Nutritional data for fruits — calories, sugar, fat, protein, and carbs per 100g from Fruityvice
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🍎"
    homepage: https://pipeworx.io/packs/fruityvice
---

# Fruityvice

Look up nutritional facts for any fruit. Get calories, sugar, fat, protein, and carbohydrates per 100 grams. You can also filter fruits by nutritional ranges — perfect for finding low-sugar or high-protein fruit options.

## Tools

- **`get_fruit`** — Nutritional info for a specific fruit by name (e.g., "banana", "mango")
- **`list_fruits`** — Browse all available fruits with complete nutritional data
- **`get_by_nutrition`** — Filter fruits by a nutrient range (e.g., sugar between 5 and 10 grams)

## Example: look up a banana

```bash
curl -s -X POST https://gateway.pipeworx.io/fruityvice/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_fruit","arguments":{"name":"banana"}}}'
```

```json
{
  "name": "Banana",
  "family": "Musaceae",
  "genus": "Musa",
  "calories": 96,
  "fat": 0.2,
  "sugar": 17.2,
  "carbohydrates": 22,
  "protein": 1
}
```

## Setup

```json
{
  "mcpServers": {
    "pipeworx-fruityvice": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/fruityvice/mcp"]
    }
  }
}
```
