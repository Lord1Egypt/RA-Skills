---
name: pipeworx-chess
description: Chess.com player profiles, game stats, match archives, and leaderboards from the public API
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "♟️"
    homepage: https://pipeworx.io/packs/chess
---

# Chess.com

Pull player profiles, ratings across all time controls, historical game archives, and global leaderboards from Chess.com's public API. No authentication needed.

## Tools

| Tool | Description |
|------|-------------|
| `get_player` | Public profile for a Chess.com username (e.g., "hikaru", "magnuscarlsen") |
| `get_stats` | Ratings and win/loss/draw counts for bullet, blitz, rapid, and daily |
| `get_games` | Game archive for a specific month — includes PGN, time control, and results |
| `get_leaderboards` | Top players globally across all time controls |

## When to use

- Looking up a player's current rating or recent performance
- Analyzing game archives for a specific player and month
- Comparing ratings across time controls for coaching conversations
- Displaying leaderboard rankings in a chess community tool

## Example: Hikaru's blitz stats

```bash
curl -s -X POST https://gateway.pipeworx.io/chess/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_stats","arguments":{"username":"hikaru"}}}'
```

Returns ratings, win/loss/draw for each time control, plus best rating achieved and date.

## MCP client config

```json
{
  "mcpServers": {
    "pipeworx-chess": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/chess/mcp"]
    }
  }
}
```
