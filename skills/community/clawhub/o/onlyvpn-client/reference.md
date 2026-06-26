# OnlyVPN CLI — full reference

## Invocation (read first)

**Prerequisite:** The **main OnlyVPN client must be running** before any `vpn-cli` / `vpn-cli.exe` command will work.

- **Windows:** start **`onlynet.exe`** from the install directory first (default **`C:\Program Files\onlynet\onlynet.exe`**). Then use **`vpn-cli.exe`** with the same arguments as in this document (e.g. `"C:\Program Files\onlynet\vpn-cli.exe" status`).
- **macOS:** from the **unzipped** package, locate **`Onlynet.app`**, then start the main binary inside the bundle: **`Onlynet.app/Contents/MacOS/OnlyNet`** (or `open path/to/Onlynet.app`). After that, use **`vpn-cli`** with the same arguments (e.g. `vpn-cli status`). If the app was moved to **Applications**, the binary is typically **`/Applications/Onlynet.app/Contents/MacOS/OnlyNet`**.

Section titles below show **`vpn-cli`** for brevity; substitute **`vpn-cli.exe`** on Windows.

## Success responses (examples)

### Status — `vpn-cli status`

Returns current connection state, node, and traffic-related fields as JSON.

```json
{
  "code": 200,
  "message": "ok",
  "data": {
    "connected": true,
    "subscription": "link.com",
    "node": "hk-01",
    "server_ip": "203.0.113.10",
    "started_at": "2026-03-27T10:00:00Z"
  }
}
```

### Subscription — add — `vpn-cli sub add "https://link.com..."`

```json
{
  "code": 200,
  "message": "subscription added",
  "data": {
    "name": "link.com",
    "url": "https://link.com/subscribe"
  }
}
```

### Subscription — update — `vpn-cli sub update`

```json
{
  "code": 200,
  "message": "subscriptions updated",
  "data": {
    "total": 2,
    "details": [
      { "name": "link.com", "nodes": 58, "status": "ok" },
      { "name": "backup.com", "nodes": 32, "status": "ok" }
    ]
  }
}
```

### Subscription — list — `vpn-cli sub list`

```json
{
  "code": 200,
  "message": "ok",
  "data": [
    {
      "name": "link.com",
      "url": "https://link.com/subscribe",
      "node_count": 58,
      "updated_at": "2026-03-27T10:02:00Z"
    },
    {
      "name": "backup.com",
      "url": "https://backup.com/sub",
      "node_count": 32,
      "updated_at": "2026-03-27T09:58:00Z"
    }
  ]
}
```

### Subscription — remove — `vpn-cli sub remove "link.com"`

```json
{
  "code": 200,
  "message": "subscription removed"
}
```

### Subscription — nodelist — `vpn-cli sub nodelist "link.com"`

```json
{
  "code": 200,
  "message": "ok",
  "data": {
    "subscription": "link.com",
    "nodes": [
      {
        "name": "hk-01",
        "address": "hk-01.link.com:443",
        "region": "HK",
        "latency_ms": 42
      },
      {
        "name": "jp-02",
        "address": "jp-02.link.com:443",
        "region": "JP",
        "latency_ms": 68
      }
    ]
  }
}
```

### Control — connect — `vpn-cli connect sub "link.com" node "hk-01"`

```json
{
  "code": 200,
  "message": "connected",
  "data": {
    "subscription": "link.com",
    "node": "hk-01",
    "server_ip": "203.0.113.10",
    "local_ip": "10.8.0.2",
    "latency_ms": 45,
    "best_mode": false
  }
}
```

### Control — connect best — `vpn-cli connect --best`

```json
{
  "code": 200,
  "message": "connected with best node",
  "data": {
    "subscription": "link.com",
    "node": "sg-03",
    "latency_ms": 31,
    "best_mode": true
  }
}
```

### Control — disconnect — `vpn-cli disconnect`

```json
{
  "code": 200,
  "message": "disconnected",
  "data": {
    "was_connected": true,
    "disconnected_at": "2026-03-27T10:05:00Z"
  }
}
```

### General — help — `vpn-cli --help`

```json
{
  "code": 200,
  "message": "ok",
  "data": {
    "command": "vpn-cli",
    "usage": "vpn-cli <command> [options]",
    "commands": [
      "status",
      "sub add|update|list|remove|nodelist",
      "connect",
      "disconnect"
    ]
  }
}
```

### General — version — `vpn-cli --version`

```json
{
  "code": 200,
  "message": "ok",
  "data": {
    "name": "vpn-cli",
    "version": "1.3.2",
    "build": "20260327",
    "platform": "windows-amd64"
  }
}
```

## Error responses

Unified failure shape:

```json
{
  "code": 1001,
  "message": "subscription not found",
  "error": {
    "type": "SUBSCRIPTION_NOT_FOUND",
    "details": "No subscription named 'link.com'",
    "hint": "Run `vpn-cli sub list` to check available subscription names."
  },
  "request_id": "7c9f3c2f-5d2f-4bf6-8df1-4d0900f2f8d1",
  "ts": "2026-03-27T10:20:00Z"
}
```

| Field | Meaning |
| --- | --- |
| `code` | Error code (failure when not success) |
| `message` | Short user-facing message |
| `error.type` | Machine-readable type (often `SCREAMING_SNAKE_CASE`) |
| `error.details` | Detailed description |
| `error.hint` | Optional remediation |
| `request_id` | Optional trace id |
| `ts` | Error time (UTC, ISO8601) |

**Convention (documented by product):** success may be represented as `code = 0` in some materials; examples in this doc often use `200`. Implementations should treat documented success values as success for the given build.

### Suggested error codes and `error.type` values

| Code | `error.type` | Meaning |
| --- | --- | --- |
| 1001 | `SUBSCRIPTION_NOT_FOUND` | Subscription not found |
| 1002 | `NODE_NOT_FOUND` | Node not found |
| 1003 | `INVALID_ARGUMENT` | Invalid argument / parameter error |
| 1004 | `NETWORK_ERROR` | Network / connection anomaly |
| 1005 | `AUTH_REQUIRED` | Authentication / permission issue |
| 1006 | `ALREADY_CONNECTED` | Already connected |
| 1007 | `NOT_CONNECTED` | Not connected |
| 1099 | `INTERNAL_ERROR` | Internal / unknown error |

All subcommands (`status`, `sub`, `connect`, `disconnect`, `help`, `version`) may return this error format on failure.
