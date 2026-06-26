# JumpOnce API Reference

## Base URL

```
http://api.jumptox.top
```

## Authentication

All requests require `Authorization: Bearer jk_live_xxxxxxxxxxxx` header.

Two token types:
- **API Key** — `jk_live_` prefix, for SDK/programmatic use
- **JWT Token** — from login, for web panel

## HTTP Forwarding

### Structured Forward

```
POST /api/v1/http/request
```

Request body:
```json
{
  "url": "https://httpbin.org/get",
  "method": "GET",
  "headers": { "X-Custom": "value" },
  "params": { "foo": "bar" },
  "timeout": 30,
  "followRedirects": true,
  "verifySSL": true
}
```

Response:
```json
{
  "code": 200,
  "data": {
    "statusCode": 200,
    "headers": { "...": "..." },
    "body": { "...": "..." },
    "elapsed": 234.5,
    "finalUrl": "https://httpbin.org/get"
  }
}
```

### Raw Passthrough

```
POST /api/v1/http/raw
```

Same request body as structured forward, but returns the target server's raw response without wrapping.

## WebSocket Forwarding

### Create Channel

```
POST /api/v1/ws/channel
```

```json
{
  "targetUrl": "wss://stream.example.com/ws",
  "autoReconnect": true,
  "pingInterval": 30
}
```

Returns `{ channelId, wsUrl }`.

### Connect Relay

```
GET /api/v1/ws/connect/{channelId}
```

### Manage

- `GET /api/v1/ws/channels` — list active channels
- `DELETE /api/v1/ws/channel/{channelId}` — close channel

## Error Codes

| Status | Meaning |
|--------|---------|
| 400 | Bad request parameters |
| 401 | Unauthorized (invalid/expired token) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Resource not found |
| 429 | Rate limited or quota exceeded |
| 502 | Target unreachable (SSRF block or network error) |

## Limits

| Item | Limit |
|------|-------|
| HTTP body | 10 MB max |
| HTTP timeout | 120 s max |
| HTTP redirects | 5 max |
| Target ports | 80, 443, 8080, 8443 |
| WS frame | 1 MB max |
| WS idle timeout | 30 min |
