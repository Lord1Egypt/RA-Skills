# Sunrise & Sunset

When does the sun rise in Tokyo? What time is golden hour in Reykjavik on the summer solstice?

This pack returns precise sunrise, sunset, dawn, dusk, solar noon, golden hour, first light, last light, and day length for any location on Earth.

## Two tools

**get_times** -- Today's sun times for a latitude/longitude.

**get_times_date** -- Sun times for a specific date at a latitude/longitude.

## Example: sunrise in New York today

```bash
curl -X POST https://gateway.pipeworx.io/sunrisesunset/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_times","arguments":{"lat":40.7128,"lng":-74.006}}}'
```

## Example: summer solstice in Reykjavik

```bash
curl -X POST https://gateway.pipeworx.io/sunrisesunset/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_times_date","arguments":{"lat":64.1466,"lng":-21.9426,"date":"2025-06-21"}}}'
```

```json
{
  "mcpServers": {
    "sunrisesunset": {
      "url": "https://gateway.pipeworx.io/sunrisesunset/mcp"
    }
  }
}
```
