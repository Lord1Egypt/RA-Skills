---
name: jrv-http-client
description: Make HTTP requests from the command line with support for auth (Bearer, Basic, API key), custom headers, JSON/form body, response formatting, timing, and history logging. A curl replacement with agent-friendly output.
---

# jrv-http-client

A developer-friendly HTTP client for agents and scripts. Supports all HTTP methods, authentication, request bodies, pretty-printed responses, timing, and request history — all without needing curl flags memorized.

## Quick Start

```bash
# Simple GET request
python3 scripts/http_client.py GET https://httpbin.org/get

# POST with JSON body
python3 scripts/http_client.py POST https://httpbin.org/post --json '{"name": "test"}'

# POST with form data
python3 scripts/http_client.py POST https://httpbin.org/post --form "name=test&value=42"

# PUT request
python3 scripts/http_client.py PUT https://api.example.com/users/1 --json '{"role": "admin"}'

# DELETE request
python3 scripts/http_client.py DELETE https://api.example.com/users/1

# Bearer token auth
python3 scripts/http_client.py GET https://api.example.com/me --bearer "mytoken123"

# Basic auth
python3 scripts/http_client.py GET https://api.example.com/data --auth "user:password"

# API key header
python3 scripts/http_client.py GET https://api.example.com/data --api-key "X-API-Key:abc123"

# Custom headers
python3 scripts/http_client.py GET https://api.example.com/ --header "Accept: application/json" --header "X-App: myapp"

# Follow redirects
python3 scripts/http_client.py GET https://example.com/ --follow

# Show only status code
python3 scripts/http_client.py GET https://api.example.com/health --status-only

# Output response to file
python3 scripts/http_client.py GET https://example.com/data.json --output response.json

# Timeout
python3 scripts/http_client.py GET https://slow.api.example.com/ --timeout 10

# Show request timing
python3 scripts/http_client.py GET https://httpbin.org/get --timing

# Output as JSON (for scripting)
python3 scripts/http_client.py GET https://httpbin.org/get --output-json
```

## Commands

| Option | Description |
|--------|-------------|
| `GET/POST/PUT/DELETE/PATCH/HEAD` | HTTP method |
| `<url>` | Target URL |
| `--json <body>` | JSON request body (sets Content-Type: application/json) |
| `--form <data>` | Form-encoded body (key=value&key2=val2) |
| `--bearer <token>` | Bearer token Authorization header |
| `--auth <user:pass>` | Basic auth |
| `--api-key <Header:value>` | Custom API key header |
| `--header <H: V>` | Add custom header (repeatable) |
| `--follow` | Follow redirects (default: no) |
| `--timeout N` | Request timeout in seconds (default: 30) |
| `--status-only` | Print only the HTTP status code |
| `--output <file>` | Save response body to file |
| `--output-json` | Output full response as JSON (status, headers, body, timing) |
| `--timing` | Show request/response timing |
| `--no-verify` | Skip TLS certificate verification |
| `--verbose` | Show request headers sent |

## Response Format

By default, responses are pretty-printed:
- JSON responses are syntax-highlighted and indented
- Other responses show raw text
- Status line and response headers are always shown

## Exit Codes

- `0` — HTTP 2xx response
- `1` — HTTP 4xx/5xx response
- `2` — Network error, timeout, or usage error

## Use Cases

- **API testing**: Quick endpoint checks without Postman
- **Health monitoring**: Check if an API returns 200
- **Auth testing**: Test Bearer/Basic/API key auth flows
- **Webhook debugging**: Send test payloads to webhook endpoints
- **CI scripts**: Trigger API actions or check health in pipelines
