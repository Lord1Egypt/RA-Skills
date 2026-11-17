# Reverse Proxy: Traps and Diagnosis

## 502 vs 504 (decide before touching config)

- 502 Bad Gateway = nginx reached a conclusion fast: connection refused, reset, or a malformed/oversized response. Look for `connect() failed`, `no live upstreams`, `upstream prematurely closed`, or `upstream sent too big header` in the error log.
- 504 Gateway Timeout = nginx waited out `proxy_read_timeout` (default 60s). The backend is alive but slow — raising the timeout hides the symptom; profile the endpoint.
- `upstream sent too big header` → raise `proxy_buffer_size` (default 4k/8k, one memory page). Common with large cookies or JWT-stuffed headers; 16k usually suffices.
- Timeout defaults all 60s: `proxy_connect_timeout` (cap it at 2-5s — 60s to learn a host is down is absurd), `proxy_read_timeout`, `proxy_send_timeout`. read_timeout is between successive reads, not total response time.

## The DNS Trap (dynamic backends, Docker, K8s)

`proxy_pass http://api.internal:3000;` resolves ONCE at config load and caches forever. Backend gets a new IP (container restart, autoscaling, blue/green) → nginx keeps hitting the corpse → 502s until reload.

Fix — variable forces runtime resolution:

```nginx
resolver 127.0.0.11 valid=10s;   # Docker's embedded DNS; use your VPC resolver otherwise
set $upstream http://api.internal:3000;
proxy_pass $upstream;
```

- `valid=10s` overrides record TTL; without `resolver`, variable-based proxy_pass fails at request time.
- Cost: variable form skips `upstream` blocks — no keepalive pool, no load-balancing directives. If you need both, reload nginx on deploys instead.
- With a URI-rewriting need in variable form, append explicitly: `proxy_pass $upstream$request_uri;`.

## Keepalive to Upstreams (the silent no-op)

All three or nothing:

```nginx
upstream backend { server 10.0.0.2:3000; keepalive 32; }
location / {
    proxy_http_version 1.1;          # default is 1.0 — no keepalive
    proxy_set_header Connection "";  # default forwards "close"
    proxy_pass http://backend;
}
```

Symptom of the missing pieces: works fine, but TIME_WAIT sockets pile up and TLS upstreams show handshake CPU. `keepalive 32` = idle conns kept per worker; size it near your steady concurrent request count per worker, not your total.

## WebSocket

```nginx
map $http_upgrade $connection_upgrade { default upgrade; '' close; }
location /ws/ {
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection $connection_upgrade;
    proxy_pass http://backend;
    proxy_read_timeout 3600s;
}
```

- Missing `proxy_http_version 1.1` = handshake fails, often reported as "WebSocket closes immediately".
- The `map` (vs hardcoded `Connection "upgrade"`) lets the same location serve normal HTTP and WS.
- Idle sockets die at `proxy_read_timeout` (60s default) — either raise it or have the app ping more often than the timeout.
- Every proxy hop in a chain (CDN → LB → nginx) needs the upgrade headers; the failure point is whichever hop forgot.
- Reload keeps old workers alive until WS connections close — bound with `worker_shutdown_timeout`.

## gRPC

```nginx
server {
    listen 443 ssl;
    http2 on;                          # gRPC requires HTTP/2 on the client leg
    location /myapp.Service/ {
        grpc_pass grpc://10.0.0.2:50051;   # grpcs:// for TLS to the backend
        grpc_read_timeout 300s;
    }
}
```

- `proxy_pass` breaks gRPC even over HTTP/2-to-client: gRPC status arrives in HTTP TRAILERS, which the HTTP proxy path doesn't forward — `grpc_pass` or nothing works (same rule shape as FastCGI: right module for the protocol).
- Locations route on the gRPC path `/package.Service/Method` — per-service locations and rate limits work exactly like REST routes.
- Long-lived server streams die at `grpc_read_timeout` (default 60s) — clients see `UNAVAILABLE (14)`; same fix pattern as WebSocket idle timeouts.
- nginx-generated errors (bad gateway, timeouts) surface to gRPC clients as transport failures, not grpc-status — a client seeing `UNAVAILABLE` with nothing in the backend log means the failure is at nginx; check its error log first.

## Buffering & Streaming

- `proxy_buffering on` (default) buffers the whole response before the client sees byte one. Correct for normal pages; fatal for SSE and streamed responses ("events arrive in one lump at the end").
- Streaming location: `proxy_buffering off;` + long `proxy_read_timeout` + ensure no `proxy_cache` on the route. Also disable response buffering in any second proxy layer.
- Per-response alternative: backend sends `X-Accel-Buffering: no` header — works with buffering globally on, keeps the default for everything else. Prefer this when only some endpoints stream.
- Buffering on + response larger than `proxy_buffers` = spill to disk temp files (`proxy_max_temp_file_size`, default 1024m). Watch for `an upstream response is buffered to a temporary file` warnings — that's disk I/O on your hot path.

## Retries & Failover

- `proxy_next_upstream error timeout;` (default) retries the next server on connect failure/timeout. Since nginx >=1.9.13, non-idempotent methods (POST, PATCH, LOCK) are NOT retried — adding `non_idempotent` reintroduces double-charge/double-write risk; only for endpoints with idempotency keys.
- `proxy_next_upstream_tries 2` and `proxy_next_upstream_timeout 10s` bound the retry storm; unbounded retries across a large upstream pool turn one slow request into N.
- `fail_timeout=10s max_fails=3`: 3 failures within 10s bans the server for 10s (same value, both roles). During the ban with all servers down → `no live upstreams` → instant 502 without even trying.
- `ip_hash` hashes only the first three octets of IPv4 — clients behind one /24 (corporate NAT) all land on one server. `hash $cookie_sessionid consistent` or `least_conn` distribute better when sessions allow.

## Header Details

- `Host $host` vs `Host $http_host`: `$host` strips the port and lowercases; apps generating absolute URLs on nonstandard ports need `$http_host`.
- `X-Forwarded-For` handling: `$proxy_add_x_forwarded_for` appends; writing `$remote_addr` overwrites the chain. Appending means the value is client-controlled — backends must take the LAST trusted hop, not the first entry.
- Response header `X-Accel-Redirect` from the backend triggers an internal redirect to a protected location — the pattern for auth-gated file downloads (`internal;` on the file location).
