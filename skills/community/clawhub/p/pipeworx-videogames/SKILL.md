# Video Games

Browse and search free-to-play games across PC and browser platforms. Powered by the FreeToGame database.

## What can I do?

**list_games** -- Browse the full catalog. Filter by platform (`pc`, `browser`), category (`mmorpg`, `shooter`, `strategy`, `moba`, `racing`, `sports`, `sandbox`, `open-world`, `survival`, `pvp`, `zombie`, `tower-defense`, `horror`, `mmofps`), and sort order (`release-date`, `popularity`, `alphabetical`, `relevance`).

**get_game** -- Full details for a game by ID: description, genre, developer, publisher, release date, screenshots, system requirements, and game URL.

**filter_games** -- Advanced filtering by dot-separated tags like `3d.mmorpg.fantasy` or `shooter.pvp` with optional platform filter.

## Example: popular PC shooters

```bash
curl -X POST https://gateway.pipeworx.io/videogames/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"list_games","arguments":{"platform":"pc","category":"shooter","sort_by":"popularity"}}}'
```

## Example: get Valorant details

Valorant's FreeToGame ID is 452:

```bash
curl -X POST https://gateway.pipeworx.io/videogames/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_game","arguments":{"id":452}}}'
```

```json
{
  "mcpServers": {
    "videogames": {
      "url": "https://gateway.pipeworx.io/videogames/mcp"
    }
  }
}
```
