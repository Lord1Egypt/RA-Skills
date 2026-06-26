# Mihomo API Reference

## Authentication

All API requests require Authorization header:

```bash
curl -H "Authorization: Bearer ${secret}" http://${host}:${port}/endpoint
```

## Endpoints

### System

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/version` | GET | Get mihomo version |
| `/configs` | GET | Get current config |
| `/configs?force=true` | PUT | Reload config |
| `/restart` | POST | Restart mihomo |
| `/upgrade` | POST | Upgrade mihomo |

### Monitoring

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/logs?level=info` | GET/WS | Real-time logs |
| `/traffic` | GET/WS | Real-time traffic (kbps) |
| `/memory` | GET/WS | Memory usage (kb) |
| `/connections` | GET/WS | Active connections |
| `/connections` | DELETE | Close all connections |
| `/connections/{id}` | DELETE | Close specific connection |

### Proxies

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/proxies` | GET | List all proxies |
| `/proxies/{name}` | GET | Get proxy details |
| `/proxies/{name}` | PUT | Select proxy `{"name":"节点名"}` |
| `/proxies/{name}/delay?url=...&timeout=5000` | GET | Test proxy delay |

### Groups

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/group` | GET | List all groups |
| `/group/{name}` | GET | Get group details |
| `/group/{name}/delay?url=...&timeout=5000` | GET | Test group delay |

### Providers

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/providers/proxies` | GET | List all proxy providers |
| `/providers/proxies/{name}` | GET | Get provider details |
| `/providers/proxies/{name}` | PUT | Update provider |

### Cache

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/cache/fakeip/flush` | POST | Flush fakeip cache |
| `/cache/dns/flush` | POST | Flush DNS cache |

### DNS Query

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/dns/query?name=example.com&type=A` | GET | DNS lookup |

## Common Examples

### Get version
```bash
curl -H "Authorization: Bearer $SECRET" http://host:9090/version
```

### List all proxies
```bash
curl -H "Authorization: Bearer $SECRET" http://host:9090/proxies | jq .
```

### Switch proxy in group
```bash
curl -X PUT -H "Authorization: Bearer $SECRET" \
  -H "Content-Type: application/json" \
  -d '{"name":"香港01"}' \
  http://host:9090/proxies/自动选择
```

### Test proxy delay
```bash
curl -H "Authorization: Bearer $SECRET" \
  "http://host:9090/proxies/香港01/delay?url=https://www.gstatic.com/generate_204&timeout=5000"
```

### Reload config
```bash
curl -X PUT -H "Authorization: Bearer $SECRET" \
  "http://host:9090/configs?force=true"
```

### Flush DNS cache
```bash
curl -X POST -H "Authorization: Bearer $SECRET" \
  http://host:9090/cache/dns/flush
```

### Get active connections
```bash
curl -H "Authorization: Bearer $SECRET" http://host:9090/connections | jq '.connections | length'
```

### Close all connections
```bash
curl -X DELETE -H "Authorization: Bearer $SECRET" http://host:9090/connections
```