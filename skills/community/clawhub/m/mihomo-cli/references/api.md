# Mihomo API Reference

Base URL: `http://<external-controller>`

Authentication: `Authorization: Bearer <secret>` (if configured)

## Core Endpoints

### System Info
- `GET /version` - Get version info
- `GET /configs` - Get running configuration
- `GET /memory` - Get memory usage
- `POST /restart` - Restart mihomo

### Proxies
- `GET /proxies` - List all proxies with delay history
- `GET /proxies/{name}` - Get specific proxy info
- `GET /proxies/{name}/delay?url=...&timeout=...` - Test proxy delay
- `PUT /proxies/{name}` - Switch proxy (for selector groups)

### Groups
- `GET /group` - List all policy groups
- `GET /group/{name}` - Get group info
- `GET /group/{name}/delay` - Test all proxies in group

### Traffic & Logs
- `GET /traffic` - WebSocket stream of traffic stats
- `GET /logs?level=debug|info|warning|error` - WebSocket stream of logs
- `GET /connections` - List active connections
- `DELETE /connections/:id` - Close specific connection

### Providers
- `GET /providers/proxies` - List all proxy providers
- `GET /providers/proxies/{name}` - Get provider info
- `POST /providers/proxies/{name}/healthcheck` - Health check all
- `POST /providers/proxies/{name}/proxies/{proxy}/healthcheck` - Check specific

### Rules
- `GET /rules` - List all rules
- `GET /providers/rules` - List rule providers

### Cache
- `POST /cache/dns/flush` - Flush DNS cache
- `POST /cache/fakeip/flush` - Flush FakeIP cache

### DNS
- `GET /dns/query?domain=...&type=...` - Query DNS

### Debug
- `GET /debug/gc` - Trigger GC
- `GET /debug/pprof` - Get pprof data

## Response Format

### Proxy Object
```json
{
  "name": "Proxy Name",
  "type": "Shadowsocks",
  "alive": true,
  "history": [
    {"time": "2024-01-01T00:00:00Z", "delay": 100}
  ],
  "extra": {
    "http://www.gstatic.com/generate_204": {
      "alive": true,
      "history": [...]
    }
  }
}
```

### Group Object
```json
{
  "name": "GLOBAL",
  "type": "Selector",
  "now": "🇭🇰 Hong Kong",
  "all": ["Proxy1", "Proxy2"],
  "history": []
}
```

## Common Operations

### Get Best Proxy (by delay)
```bash
curl -H "Authorization: Bearer $SECRET" \
  http://localhost:9090/proxies | \
  jq '.proxies | to_entries | 
    map(select(.value.history | length > 0)) | 
    sort_by(.value.history[-1].delay) | 
    .[0].key'
```

### Switch Group
```bash
curl -X PUT -H "Authorization: Bearer $SECRET" \
  -H "Content-Type: application/json" \
  -d '{"name":"Proxy Name"}' \
  http://localhost:9090/proxies/GLOBAL
```

### Test Specific Proxy
```bash
curl -H "Authorization: Bearer $SECRET" \
  "http://localhost:9090/proxies/$(echo 'Proxy Name' | jq -sRr @uri)/delay?url=http://www.gstatic.com/generate_204&timeout=5000"
```