# Boardgames

Boardgames MCP — wraps Board Game Atlas API (public demo client_id, free)

## search_games

Search for board games by name. Returns title, year, player count, playtime, rating, price, and desc

## get_game

Get full details for a specific board game by ID (from search_games results). Returns name, year, pl

## hot_games

Get the most popular board games ranked by current buzz. Returns title, year, player count, playtime

```json
{
  "mcpServers": {
    "boardgames": {
      "url": "https://gateway.pipeworx.io/boardgames/mcp"
    }
  }
}
```
