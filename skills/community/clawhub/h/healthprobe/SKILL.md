---
name: healthprobe
description: "Probe any URL and check if it's up. Returns the HTTP status code, response latency in milliseconds, and a healthy/not-healthy verdict. Configurable timeout. Useful for checking if an API is available before calling it."
metadata: {"openclaw":{"emoji":"💓","requires":{"bins":["python"]},"install":[{"id":"pip","kind":"uv","packages":["fastapi","uvicorn","pydantic","httpx"]}]}}
---

# HealthProbe

Check if a URL is up before you call it.

## Start the server

```bash
uvicorn healthprobe.app:app --port 8009
```

## Probe a URL

```bash
curl -s -X POST http://localhost:8009/v1/probe \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' | jq
```

Returns `healthy` (true if 2xx), `status_code` (HTTP code or -1 on error), `latency_ms`, and `error` (if connection failed).

## With custom timeout

```bash
curl -s -X POST http://localhost:8009/v1/probe \
  -H "Content-Type: application/json" \
  -d '{"url": "https://slow-api.example.com", "timeout_ms": 1000}' | jq '.healthy'
```

Timeout range: 100ms to 30,000ms (default: 5,000ms).
