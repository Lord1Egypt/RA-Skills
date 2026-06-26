---
name: pipeworx-imgflip
description: Top 100 meme templates from Imgflip — names, dimensions, and image URLs ready for captioning
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "😂"
    homepage: https://pipeworx.io/packs/imgflip
---

# Imgflip Meme Templates

Get the top 100 meme templates from Imgflip, ranked by popularity. Each template includes its name, image URL, width, height, and box count (number of text areas). Useful for meme generators, content tools, or just browsing what's popular.

## Tools

- **`get_memes`** — Returns all 100 top meme templates with id, name, url, width, height, and box_count

## Use cases

- Building a meme generator that needs popular templates
- Displaying trending meme formats in a social content tool
- Picking a random meme template for a fun conversation feature
- Reference data for meme identification

## Example

```bash
curl -s -X POST https://gateway.pipeworx.io/imgflip/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_memes","arguments":{}}}'
```

Returns templates like "Drake Hotline Bling", "Distracted Boyfriend", "Two Buttons", etc.

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-imgflip": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/imgflip/mcp"]
    }
  }
}
```
