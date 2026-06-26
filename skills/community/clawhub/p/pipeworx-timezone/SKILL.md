# Timezone

What time is it in Tokyo right now? Convert a meeting time from New York to London. List every IANA timezone string. Look up the timezone for an IP address.

## Tools

- **get_time_by_timezone** -- Current datetime in any IANA timezone (e.g., `America/New_York`, `Asia/Tokyo`)
- **list_timezones** -- All available IANA timezone strings
- **get_time_by_ip** -- Current datetime based on IP geolocation
- **convert_time** -- Convert a datetime between two timezones. Omit the time parameter to convert "right now."

## Example: convert meeting time

```bash
curl -X POST https://gateway.pipeworx.io/timezone/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"convert_time","arguments":{"from_timezone":"America/New_York","to_timezone":"Europe/London","time":"2025-04-15T09:00:00"}}}'
```

The response includes both datetimes, both UTC offsets, and the offset difference between the two zones.

```json
{
  "mcpServers": {
    "timezone": {
      "url": "https://gateway.pipeworx.io/timezone/mcp"
    }
  }
}
```
