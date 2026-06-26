# httpstat ⚡

Pretty HTTP response statistics with timing waterfall. Like `curl -v` but readable.

## Features

- **Timing waterfall** — DNS, TCP, TLS, TTFB, transfer visualized as bars
- **TLS details** — version, cipher suite
- **Smart headers** — shows interesting response headers (Server, Cache-Control, CF-Ray, etc.)
- **Redirect following** — trace redirect chains with `--follow`
- **JSON output** — machine-readable timing data
- **Zero deps** — pure Python 3.10+, raw sockets for accurate timing

## Usage

```bash
# Basic request
python3 httpstat.py https://example.com

# POST with data
python3 httpstat.py https://httpbin.org/post -X POST -d '{"key":"value"}'

# Follow redirects
python3 httpstat.py http://github.com --follow

# JSON output for scripting
python3 httpstat.py https://example.com --json

# Custom headers
python3 httpstat.py https://api.example.com -H "Authorization: Bearer token"
```

## Output

```
  GET https://example.com
  200 OK

            DNS Lookup  ██  17ms
        TCP Connection  ████  29ms
         TLS Handshake  ██████  38ms
     Server Processing  ██████████████████████████  159ms
      Content Transfer  █  1ms
                        ────────────────────────────────────────
                 Total  244ms

  IP: 93.184.216.34
  TLS: TLSv1.3 (TLS_AES_128_GCM_SHA256)
  Body: 1,256 bytes

  Content-Type: text/html; charset=UTF-8
  Server: ECAcc (dcb/7F3B)
  Cache-Control: max-age=604800
```

## Options

| Flag | Description |
|------|-------------|
| `--method, -X` | HTTP method (GET, POST, etc.) |
| `--header, -H` | Add header (repeatable) |
| `--data, -d` | Request body |
| `--follow, -L` | Follow redirects |
| `--timeout, -t` | Timeout in seconds (default: 10) |
| `--json` | JSON output |

## Exit codes

- `0` — 2xx response
- `1` — error or 4xx/5xx response

## License

MIT
