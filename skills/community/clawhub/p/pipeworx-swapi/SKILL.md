# Star Wars API

A long time ago in a galaxy far, far away... all the data from the Star Wars universe became available via MCP.

Search for characters, look up planets, inspect starships, and get film details from the original six films.

## Tools

**search_people** -- Search characters by name. Try "Luke", "Darth", or "Leia". Returns physical attributes, birth year, gender, and homeworld.

**get_planet** -- Planet by ID. Tatooine is 1. Returns climate, terrain, population, gravity, orbital data.

**get_starship** -- Starship by ID. The Millennium Falcon is 10, Death Star is 9. Returns model, manufacturer, crew capacity, cargo, hyperdrive rating, and speed.

**get_film** -- Film by ID. A New Hope is 1. Returns title, episode number, director, producer, release date, and the full opening crawl.

## Example: look up Tatooine

```bash
curl -X POST https://gateway.pipeworx.io/swapi/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_planet","arguments":{"id":1}}}'
```

## Quick reference

| Thing | ID |
|-------|-----|
| Luke Skywalker | search "Luke" |
| Tatooine | Planet 1 |
| Millennium Falcon | Starship 10 |
| Death Star | Starship 9 |
| A New Hope | Film 1 |
| The Empire Strikes Back | Film 2 |

```json
{
  "mcpServers": {
    "swapi": {
      "url": "https://gateway.pipeworx.io/swapi/mcp"
    }
  }
}
```
