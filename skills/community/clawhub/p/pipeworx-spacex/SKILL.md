# SpaceX

Real-time and historical data from SpaceX launches, rockets, crew, and the Starlink constellation.

## What's available

- **get_latest_launch** -- The most recent SpaceX launch with success status, details, and media links (webcast, article, Wikipedia)
- **get_next_launch** -- Next upcoming launch with date and details
- **get_past_launches** -- Recent launches in reverse chronological order (configurable count)
- **get_rockets** -- All SpaceX rockets: Falcon 1, Falcon 9, Falcon Heavy, Starship. Includes cost per launch, success rate, and first flight date.
- **get_crew** -- SpaceX crew members with name, agency, status, and photo
- **get_starlink** -- Starlink satellite data sorted by most recent launch, including object name, launch date, and decay date

## Try it

```bash
curl -X POST https://gateway.pipeworx.io/spacex/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_latest_launch","arguments":{}}}'
```

## Configuration

```json
{
  "mcpServers": {
    "spacex": {
      "url": "https://gateway.pipeworx.io/spacex/mcp"
    }
  }
}
```
