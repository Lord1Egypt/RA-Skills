---
name: pipeworx-httpcat
description: HTTP status code cat images — get a cat photo for any status code plus a reference of all common codes
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🐈"
    homepage: https://pipeworx.io/packs/httpcat
---

# HTTP Cats

Every HTTP status code deserves a cat. This pack returns cat image URLs from http.cat for any status code, plus a handy reference list of all common HTTP codes with their meanings.

## Tools

- **`get_status_cat`** — Get the http.cat image URL for a specific HTTP status code (e.g., 404, 418, 500)
- **`list_codes`** — Reference list of common HTTP status codes with human-readable descriptions

## Perfect for

- Making error messages more fun in documentation or Slack alerts
- Teaching HTTP status codes in a memorable way
- Adding personality to API monitoring dashboards
- "What does a 418 status code mean?" — it means I'm a Teapot, obviously

## Example

```bash
curl -s -X POST https://gateway.pipeworx.io/httpcat/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_status_cat","arguments":{"code":404}}}'
```

```json
{
  "code": 404,
  "description": "Not Found",
  "image_url": "https://http.cat/404"
}
```

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-httpcat": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/httpcat/mcp"]
    }
  }
}
```
