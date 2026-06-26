---
name: jump-once-proxy
description: |
  Access overseas/external URLs via JumpOnce proxy service (jumptox.top).
  Use when: (1) needing to fetch content from websites blocked or unreachable from the current network,
  (2) accessing foreign APIs, (3) making HTTP requests through an overseas proxy,
  (4) user mentions overseas/proxy/jumptox/jump-once keywords.
  Supported exit server: Oracle Cloud Phoenix, USA (AS31898).
  Supports HTTP forwarding (structured and raw) and WebSocket relay.
---

# JumpOnce Proxy

Forward HTTP/WS requests through JumpOnce proxy to access overseas resources.

## Setup

### Get API Key

1. Register & login at [panel.jumptox.top](http://panel.jumptox.top)
2. Go to **Console → API Keys → Create**
3. Copy the key (starts with `jk_live_`)

### Configure

```bash
export JUMPONCE_API_KEY="jk_live_xxxxxxxxxxxx"
```

Or save it in workspace TOOLS.md for persistent access.

## Quick Usage

### Option A: Python SDK

```bash
pip install jump-once
```

```python
from jump import Client

client = Client(api_key="jk_live_xxxxxxxxxxxx")

# HTTP GET
result = client.http.forward(url="https://example.com/api")
print(result.status_code, result.body)

# HTTP POST
result = client.http.forward(
    url="https://api.example.com/data",
    method="POST",
    body='{"key": "value"}',
    headers={"Content-Type": "application/json"},
)
```

### Option B: Direct API Call

```python
import requests

resp = requests.post(
    "http://api.jumptox.top/api/v1/http/request",
    json={
        "url": "https://example.com/api",
        "method": "GET",
        "headers": {},
        "params": {},
        "timeout": 30,
    },
    headers={"Authorization": "Bearer jk_live_xxxxxxxxxxxx"},
)
print(resp.json())
```

### Option C: Bundled Script

```bash
python scripts/forward_request.py --url "https://example.com" --api-key "jk_live_xxx"
```

Use `--raw` flag for unparsed response, `--body` for POST data.

## Endpoints

- **Structured forward**: `POST /api/v1/http/request` — returns `{code, data: {statusCode, headers, body, elapsed}}`
- **Raw passthrough**: `POST /api/v1/http/raw` — returns target's raw response
- **WebSocket**: See [API Reference](references/api-reference.md) for channel management

## Limits

- HTTP body: 10 MB | Timeout: 120 s | Redirects: 5
- Allowed ports: 80, 443, 8080, 8443
- WS frame: 1 MB | WS idle: 30 min

Full API docs: [references/api-reference.md](references/api-reference.md)
