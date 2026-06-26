# Anilist

AniList MCP — wraps AniList GraphQL API (free, no auth)

## search_anime

Search for anime by title. Returns title, episode count, status, score, genres, and synopsis. Use ge

## get_anime

Get full anime details by ID. Returns title, synopsis, episodes, duration, status, score, genres, st

## trending_anime

Get currently trending anime ranked by popularity. Returns title, status, score, episode count, and 

```json
{
  "mcpServers": {
    "anilist": {
      "url": "https://gateway.pipeworx.io/anilist/mcp"
    }
  }
}
```
