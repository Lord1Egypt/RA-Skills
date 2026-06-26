# Rick and Morty

Wubba lubba dub dub! Query the Rick and Morty universe -- characters, locations, and episodes from all seasons of the show.

## Commands

| Tool | What it does |
|------|-------------|
| `search_characters` | Find characters by name (returns status, species, gender, origin, location, episode count) |
| `get_character` | Full character details by ID |
| `get_location` | Location details by ID (name, type, dimension, resident count) |
| `get_episode` | Episode details by ID (name, air date, episode code, character count) |

## Example: look up Rick Sanchez

```bash
curl -X POST https://gateway.pipeworx.io/rickmorty/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_character","arguments":{"id":1}}}'
```

## Handy IDs

- Character 1: Rick Sanchez
- Character 2: Morty Smith
- Location 1: Earth (C-137)
- Episode 1: Pilot (S01E01)

```json
{
  "mcpServers": {
    "rickmorty": {
      "url": "https://gateway.pipeworx.io/rickmorty/mcp"
    }
  }
}
```
