<!-- GENERATED FILE: DO NOT EDIT DIRECTLY. -->
<!-- Source of truth: docs.httpeep.com/content/docs/cli/request.mdx -->
<!-- Generate with: node scripts/generate-httpeep-cli-skill-reference.mjs <references-dir> -->

# Request

The `request` subcommand sends an HTTP request through the HTTPeep proxy so it appears in the session list. This is useful for testing an endpoint without configuring a separate HTTP client to route through the proxy.

## Basic request

```bash
# Simple GET request
httpeep-cli request --method GET --url "https://api.example.com/v2/users"

# POST with headers and body
httpeep-cli request \
  --method POST \
  --url "https://api.example.com/v2/users" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer token123" \
  --body '{"name": "Alice"}'

# JSON output for scripting
httpeep-cli --format json request --method GET --url "https://api.example.com/v2/users"
```

| Flag | Description | Default |
|---|---|---|
| `--method <method>` | HTTP method | `GET` |
| `--url <url>` | Target URL | — |
| `-H`, `--header <header>` | HTTP header in `Key: Value` format (repeatable) | — |
| `--body <body>` | Request body (conflicts with `--body-file`) | — |
| `--body-file <path>` | Read request body from file (conflicts with `--body`) | — |

## HTTP version

Choose the preferred HTTP version. When requesting `http://` URLs with HTTP/2 preference, the client automatically falls back to HTTP/1.1.

```bash
# Default: auto-negotiate
httpeep-cli request --method GET --url "https://www.google.com"

# Prefer HTTP/2
httpeep-cli request --method GET --url "https://www.google.com" --http-version http2

# Force HTTP/1.1
httpeep-cli request --method GET --url "https://example.com" --http-version http1
```

| Value | Description |
|---|---|
| `auto` | Auto-negotiate (default) |
| `http1` | HTTP/1.1 only |
| `http2` | HTTP/2 preferred, falls back to HTTP/1.1 for plain HTTP |

## Redirects

By default, `request` does not follow redirects. Enable it when needed:

```bash
httpeep-cli request --method GET --url "https://google.com" \
  --follow-redirect \
  --max-redirects 10
```

| Flag | Description | Default |
|---|---|---|
| `--follow-redirect` | Follow HTTP redirects | — |
| `--max-redirects <n>` | Maximum number of redirects to follow | 10 |

## Proxy settings

You can route the request through an upstream proxy using either a complete URL or split parameters.

**Full proxy URL:**

```bash
httpeep-cli request --method GET --url "https://httpbin.org/get" \
  --proxy-url "http://user:pass@127.0.0.1:8800"
```

**Split parameters** (`--proxy-url` and split parameters are mutually exclusive):

```bash
httpeep-cli request --method GET --url "https://httpbin.org/get" \
  --proxy-protocol socks5h \
  --proxy-host 127.0.0.1 \
  --proxy-port 1080 \
  --proxy-username user \
  --proxy-password pass
```

| Flag | Description |
|---|---|
| `--proxy-url <url>` | Full proxy URL |
| `--proxy-protocol <proto>` | `http`, `https`, `socks5`, `socks5h` |
| `--proxy-host <host>` | Proxy host |
| `--proxy-port <port>` | Proxy port |
| `--proxy-username <user>` | Proxy username |
| `--proxy-password <pass>` | Proxy password |

## Temporary rules

Apply temporary rules to the request without modifying the global ruleset. All shortcut rule parameters are supported. See the [Rules](/cli/rules) page for a full explanation of each shortcut.

```bash
# Map remote domain to local service
httpeep-cli request --method GET --url "https://api.example.com/users" \
  --map-remote "api.example.com=http://127.0.0.1:3000"

# Serve a local file
httpeep-cli request --method GET --url "https://example.com/banner" \
  --map-local-file "example.com/banner=./fixtures/banner.json"

# Return an inline response
httpeep-cli request --method GET --url "https://api.example.com/health" \
  --inline-response "/health=503:text/plain:maintenance"

# Inject a fault
httpeep-cli request --method GET --url "https://api.example.com/orders" \
  --reject "api.example.com/orders=503"

# Simulate slow network
httpeep-cli request --method GET --url "https://api.example.com/feed" \
  --delay "api.example.com/feed=300" \
  --throttle "api.example.com/feed=req=100/200,res=150"
```

You can also pass full rule JSON or rule files:

```bash
httpeep-cli request --method GET --url "https://example.com" \
  --rule '{"id":"tmp-rule","description":"demo","enabled":true,"match":{}}'

httpeep-cli request --method GET --url "https://example.com" \
  --rule-file ./rule.yaml
```

## Save control

By default, the request and its response are saved as a new session. You can disable this:

```bash
httpeep-cli request --method GET --url "https://example.com" --no-save
```

> **Note:**
> The saved session can be inspected with `sessions list --keyword <domain>` or replayed with `replay --id <session_id>`.
