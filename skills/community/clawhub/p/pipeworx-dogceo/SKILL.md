---
name: pipeworx-dogceo
description: Random dog photos by breed — 120+ breeds with sub-breeds from the Dog CEO API
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🐕"
    homepage: https://pipeworx.io/packs/dogceo
---

# Dog CEO

Need a dog picture? This pack serves random dog images from a collection of 120+ breeds. Get a completely random dog, filter by breed, or browse the full breed list with sub-breeds.

## Tools

| Tool | Description |
|------|-------------|
| `random_image` | A random dog image URL from any breed |
| `list_breeds` | All breeds and their sub-breeds |
| `breed_images` | Multiple random images for a specific breed (default 3) |
| `random_breed_image` | A single random image for a specific breed |

## Perfect for

- "Show me a golden retriever" requests
- Placeholder images during UI development
- Dog breed identification apps that need reference photos
- Pet-themed chatbot responses

## Example

```bash
curl -s -X POST https://gateway.pipeworx.io/dogceo/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"breed_images","arguments":{"breed":"labrador","count":3}}}'
```

Returns 3 image URLs of Labrador Retrievers.

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-dogceo": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/dogceo/mcp"]
    }
  }
}
```
