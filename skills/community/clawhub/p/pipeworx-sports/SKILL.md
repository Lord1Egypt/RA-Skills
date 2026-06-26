# Sports

Live scores, standings, team info, and player data across football, basketball, baseball, hockey, and more via TheSportsDB.

## Tools at a glance

- `search_teams` -- Find teams by name. Returns sport, league, country, stadium, description, badge image.
- `search_players` -- Find players by name. Returns team, nationality, position, bio, thumbnail.
- `get_league_table` -- Current season standings for any league (wins, draws, losses, goals, points).
- `get_last_events` -- Last 15 results for a team with scores.
- `get_next_events` -- Next 15 upcoming fixtures for a team.

## Example: Premier League standings

```bash
curl -X POST https://gateway.pipeworx.io/sports/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_league_table","arguments":{"league_id":"4328","season":"2024-2025"}}}'
```

## Useful league IDs

| League | ID |
|--------|-----|
| English Premier League | 4328 |
| La Liga | 4335 |
| Serie A | 4332 |
| NBA | 4387 |
| NFL | 4391 |
| MLB | 4424 |

## Useful team IDs

- Arsenal: 133604
- Manchester United: 133612
- Real Madrid: 133738
- LA Lakers: 134867

```json
{
  "mcpServers": {
    "sports": {
      "url": "https://gateway.pipeworx.io/sports/mcp"
    }
  }
}
```
