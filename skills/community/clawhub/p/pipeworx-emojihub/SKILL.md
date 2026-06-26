---
name: pipeworx-emojihub
description: Browse and fetch emojis by category or group — random picks, smileys, animals, food, flags, and more
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "😀"
    homepage: https://pipeworx.io/packs/emojihub
---

# EmojiHub

Need the right emoji? Pull random emojis, browse by category (smileys-and-people, animals-and-nature, food-and-drink, etc.), or filter by group for even more specific results. Returns emoji name, unicode character, and HTML entity.

## Tools

- **`random_emoji`** — A random emoji from any category
- **`get_by_category`** — Emojis from a specific category (e.g., "smileys-and-people", "travel-and-places")
- **`get_by_group`** — Emojis from a specific group within a category

## Good for

- Adding emoji reactions to chatbot responses
- Building emoji picker components with categorized data
- Random emoji for games or creative prompts
- Enriching social media tools with emoji suggestions

## Example

```bash
curl -s -X POST https://gateway.pipeworx.io/emojihub/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_by_category","arguments":{"category":"food-and-drink"}}}'
```

## Setup

```json
{
  "mcpServers": {
    "pipeworx-emojihub": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/emojihub/mcp"]
    }
  }
}
```
