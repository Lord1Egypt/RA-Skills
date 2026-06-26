# Swiss Transport

Real-time Swiss public transport data: train, bus, and tram schedules from SBB and regional operators.

## search_stations

Find stations by name. Returns station ID, name, and coordinates.

## get_connections

Route planning between two locations. Returns departure/arrival times, duration, number of transfers, platform numbers, delays, and a breakdown of each journey section (which train/bus, intermediate stops).

## get_stationboard

Live departure board for any station. Shows the next departures with line name, category, destination, platform, and delay information.

## Example: Zurich to Bern connections

```bash
curl -X POST https://gateway.pipeworx.io/swisstransport/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_connections","arguments":{"from":"Zurich HB","to":"Bern","limit":3}}}'
```

## Example: departures from Geneva

```bash
curl -X POST https://gateway.pipeworx.io/swisstransport/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_stationboard","arguments":{"station":"Geneve","limit":5}}}'
```

```json
{
  "mcpServers": {
    "swisstransport": {
      "url": "https://gateway.pipeworx.io/swisstransport/mcp"
    }
  }
}
```
