---
name: pipeworx-musicbrainz
description: MusicBrainz MCP — wraps MusicBrainz Web Service v2 (free, no auth)
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/musicbrainz
---

# pipeworx-musicbrainz

MusicBrainz MCP — wraps MusicBrainz Web Service v2 (free, no auth). Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `search_artists`
- `get_artist`
- `search_releases`
- `get_release`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-musicbrainz": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/musicbrainz/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/musicbrainz](https://pipeworx.io/packs/musicbrainz)
