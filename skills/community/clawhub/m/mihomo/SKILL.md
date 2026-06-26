---
name: mihomo
description: |
  Manage mihomo (Clash Meta) proxy instances via REST API. Use when user mentions mihomo, clash, proxy switching, 
  or needs to: (1) Check proxy status/version, (2) Switch proxy nodes, (3) Test proxy delays, (4) Manage connections, 
  (5) Reload config or restart, (6) Flush DNS/FakeIP cache, (7) Monitor traffic/logs.
---

# Mihomo Proxy Management

Control mihomo instances via REST API.

## Connection Info

Default values, override with user-provided:
- **Host**: `http://127.0.0.1:9090`
- **Secret**: Ask user if not provided

Store connection in environment for session:
```bash
MIHOMO_URL="http://host:9090"
MIHOMO_SECRET="your-secret"
```

## Common Operations

### Check Status

```bash
# Version
curl -s -H "Authorization: Bearer $MIHOMO_SECRET" "$MIHOMO_URL/version"

# All proxies
curl -s -H "Authorization: Bearer $MIHOMO_SECRET" "$MIHOMO_URL/proxies" | jq '.proxies | keys'

# Active connections count
curl -s -H "Authorization: Bearer $MIHOMO_SECRET" "$MIHOMO_URL/connections" | jq '.connections | length'
```

### Switch Proxy

```bash
# Switch node in a group
curl -X PUT -H "Authorization: Bearer $MIHOMO_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"name":"节点名"}' \
  "$MIHOMO_URL/proxies/策略组名"
```

### Test Delay

```bash
# Test specific proxy
curl -s -H "Authorization: Bearer $MIHOMO_SECRET" \
  "$MIHOMO_URL/proxies/节点名/delay?url=https://www.gstatic.com/generate_204&timeout=5000"

# Test all proxies in group
curl -s -H "Authorization: Bearer $MIHOMO_SECRET" \
  "$MIHOMO_URL/group/策略组名/delay?url=https://www.gstatic.com/generate_204&timeout=5000"
```

### Manage Connections

```bash
# List connections
curl -s -H "Authorization: Bearer $MIHOMO_SECRET" "$MIHOMO_URL/connections" | jq '.connections[] | {id, metadata}'

# Close all
curl -X DELETE -H "Authorization: Bearer $MIHOMO_SECRET" "$MIHOMO_URL/connections"
```

### Cache & Config

```bash
# Flush DNS cache
curl -X POST -H "Authorization: Bearer $MIHOMO_SECRET" "$MIHOMO_URL/cache/dns/flush"

# Flush FakeIP cache
curl -X POST -H "Authorization: Bearer $MIHOMO_SECRET" "$MIHOMO_URL/cache/fakeip/flush"

# Reload config
curl -X PUT -H "Authorization: Bearer $MIHOMO_SECRET" "$MIHOMO_URL/configs?force=true"

# Restart mihomo
curl -X POST -H "Authorization: Bearer $MIHOMO_SECRET" "$MIHOMO_URL/restart"
```

## API Reference

For complete endpoint list, see [references/api.md](references/api.md).