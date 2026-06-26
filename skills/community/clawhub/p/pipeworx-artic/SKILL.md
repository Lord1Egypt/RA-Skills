---
name: pipeworx-artic
description: Explore the Art Institute of Chicago's collection — artworks, artists, and exhibitions via the ARTIC public API
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🎨"
    homepage: https://pipeworx.io/packs/artic
---

# Art Institute of Chicago

One of the oldest and largest art museums in the United States, the Art Institute of Chicago holds nearly 300,000 works. Their public API exposes rich data about artworks, artists, and exhibitions — no API key required.

## Tools

| Tool | Description |
|------|-------------|
| `search_artworks` | Full-text search across the entire collection (e.g., "monet water lilies") |
| `get_artwork` | Fetch a detailed record for a single artwork by its ARTIC ID |
| `get_artist` | Biographical info and associated works for an artist by ID |
| `get_exhibitions` | Browse current and past exhibitions |

## When you'd use this

- Answering questions about specific paintings or artists in the ARTIC collection
- Pulling structured art data for educational apps or classroom tools
- Cross-referencing exhibitions when planning a trip to Chicago
- Feeding artwork descriptions into downstream analysis or summarization

## Try it out

Look up Grant Wood's *American Gothic* (artwork ID 6565):

```bash
curl -s -X POST https://gateway.pipeworx.io/artic/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_artwork","arguments":{"id":6565}}}'
```

Returns title, artist, date, medium, dimensions, image URL (via IIIF), description, and provenance.

## MCP client config

```json
{
  "mcpServers": {
    "pipeworx-artic": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/artic/mcp"]
    }
  }
}
```

## Notes

- Image URLs use the IIIF protocol — you can append size parameters to request specific dimensions
- Search supports up to 100 results per call
- All data is free and open-access
