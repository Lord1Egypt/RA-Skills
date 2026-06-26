---
name: pipeworx-dicebear
description: Generate unique avatar images from any seed text — 30+ styles including pixel art, initials, and abstract shapes
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "👤"
    homepage: https://pipeworx.io/packs/dicebear
---

# DiceBear Avatars

Generate deterministic, unique avatars from any seed string. Same seed always produces the same avatar. Choose from 30+ art styles including pixel art, bottts (robots), initials, adventurer, and more. Returns SVG URLs you can embed directly.

## Tools

- **`generate_avatar`** — Generate an avatar URL for a given style and seed. The seed can be a username, email, or any string.
- **`list_styles`** — Returns all available avatar styles with descriptions.

## When to use

- Default profile pictures for new users (deterministic = no database storage needed)
- Generating unique icons for items, categories, or projects
- Placeholder images during design prototyping
- Chat applications that need distinct avatars per participant

## Example

Generate a robot-style avatar for the seed "alice":

```bash
curl -s -X POST https://gateway.pipeworx.io/dicebear/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"generate_avatar","arguments":{"style":"bottts","seed":"alice"}}}'
```

```json
{
  "url": "https://api.dicebear.com/7.x/bottts/svg?seed=alice",
  "style": "bottts",
  "seed": "alice"
}
```

## Popular styles

`adventurer`, `avataaars`, `bottts`, `fun-emoji`, `icons`, `identicon`, `initials`, `lorelei`, `micah`, `miniavs`, `notionists`, `open-peeps`, `personas`, `pixel-art`, `rings`, `shapes`, `thumbs`

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-dicebear": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/dicebear/mcp"]
    }
  }
}
```
