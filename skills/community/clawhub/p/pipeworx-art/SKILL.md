---
name: pipeworx-art
description: Search and explore 500,000+ artworks in the Metropolitan Museum of Art's open-access collection
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🖼️"
    homepage: https://pipeworx.io/packs/art
---

# Metropolitan Museum of Art

The Met's collection spans 5,000 years of art from every corner of the world. This pack connects to their open-access API, giving you structured data on paintings, sculptures, textiles, photographs, and more — complete with high-resolution image URLs, provenance, and exhibition history.

## Available tools

- **`search_artworks`** — Full-text search across the collection. Returns the first 5 matching objects with details like artist, date, medium, and image URL.
- **`get_artwork`** — Deep dive into a single object by its Met Museum ID. Returns everything: dimensions, credit line, gallery location, provenance, classification, and more.
- **`get_departments`** — Lists all curatorial departments (e.g., Egyptian Art, European Paintings, Asian Art).

## Scenarios where this fits

1. A user asks "show me Impressionist paintings at the Met" — use `search_artworks` with query `"impressionism"`
2. Generating educational content about ancient Egyptian artifacts
3. Building an art recommendation feature and need structured metadata
4. Comparing works across departments or time periods

## Example: finding Van Gogh works

```bash
curl -s -X POST https://gateway.pipeworx.io/art/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_artworks","arguments":{"query":"van gogh sunflowers"}}}'
```

You'll get back objects including titles, dates, artist nationality, medium, and direct links to high-res images on the Met's CDN.

## Output shape

Each artwork includes:
- `title`, `artist`, `date`, `medium`
- `department`, `culture`, `period`
- `image_url` (public domain where available)
- `object_url` (link to the Met's website)

## Setup

```json
{
  "mcpServers": {
    "pipeworx-art": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/art/mcp"]
    }
  }
}
```
