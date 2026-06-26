# Radio

Discover internet radio stations from around the world. The Radio Browser database indexes tens of thousands of live streams across every genre and country.

## Available commands

- **search_stations** -- Find stations by name, sorted by popularity
- **get_top_stations** -- Most-voted stations globally or filtered by country
- **list_countries** -- All countries with station counts
- **list_tags** -- Top genres and tags by station count

## Example: find jazz stations

```bash
curl -X POST https://gateway.pipeworx.io/radio/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_stations","arguments":{"query":"jazz","limit":5}}}'
```

Each station result includes a direct stream URL, codec, bitrate, country, language, and tags -- everything needed to start playing.

## Popular use cases

- Build a radio discovery feature for a music app
- Find stations by country for localization projects
- Get stream URLs for background audio in creative coding

## Setup

```json
{
  "mcpServers": {
    "radio": {
      "url": "https://gateway.pipeworx.io/radio/mcp"
    }
  }
}
```
