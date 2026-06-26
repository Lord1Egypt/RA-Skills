---
name: pipeworx-movies
description: Movies MCP — wraps iTunes Search API (movies, free, no auth) and TVmaze API (TV shows, free, no au
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/movies
---

# pipeworx-movies

Movies MCP — wraps iTunes Search API (movies, free, no auth) and TVmaze API (TV shows, free, no au. Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `search_movies`
- `search_tv_shows`
- `get_tv_show`
- `get_tv_schedule`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-movies": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/movies/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/movies](https://pipeworx.io/packs/movies)
