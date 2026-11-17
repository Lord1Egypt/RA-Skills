---
name: Nginx
slug: nginx
version: 1.0.5
description: >-
  Configures and debugs nginx: reverse proxy, load balancing, SSL/TLS termination, caching,
  redirects, and static file serving. Use when writing or reviewing nginx.conf, server blocks,
  locations, upstreams, or proxy_pass, when a site behind nginx throws 502, 504, 413, 403, or a
  redirect loop, when WebSockets, SSE, or gRPC break through the proxy, when a certificate works
  in curl but warns in browsers, when requests hit the wrong location or the backend sees the
  wrong path, when tuning workers, buffers, gzip, or proxy cache, when rate limiting or blocking
  abuse, when proxying raw TCP/UDP, or when nginx runs in Docker or Kubernetes. Not for
  certificate issuance or renewal (ACME, Let's Encrypt) — that is the ssl skill.
homepage: https://clawic.com/skills/nginx
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: 🌐
    displayName: Nginx
    configPaths:
      - ~/Clawic/data/nginx/
---

User preferences and memory live in `~/Clawic/data/nginx/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/nginx/` or `~/clawic/nginx/`), move it to `~/Clawic/data/nginx/`.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/nginx/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| os_family | debian \| rhel \| alpine | debian | Selects package/config layout (sites-enabled vs conf.d), makes SELinux the first 502/403 suspect on rhel (`debug.md`), and sets module install paths |
| deployment | systemd \| docker \| kubernetes | systemd | Selects reload commands and resolver address; docker/kubernetes routes advice through `containers.md` |
| edge_position | standalone \| behind-cdn-lb | standalone | behind-cdn-lb turns on realip guidance, switches redirect logic from `$scheme` to `X-Forwarded-Proto`, and flags rate-limit keying on the LB address |

Preference areas to record as the user reveals them:

- **tooling** — OSS vs Plus, mainline vs stable channel, dynamic modules in use (brotli, headers-more, njs); governs which directives are assumed available
- **conventions** — config layout (conf.d vs sites-enabled vs single file), snippet/include organization, upstream and zone naming; governs where examples place directives
- **safety posture** — 302-before-301 rollout ramp, HSTS ramp speed, confirm-before-reload on production hosts; governs pacing in `redirects.md` and `ssl.md`
- **platform** — IPv6 listeners, HTTP/2/3 adoption, which CDN/LB sits in front; governs listen directives and header-trust guidance

## When To Use

- Writing or reviewing nginx config: server blocks, locations, proxy_pass, upstreams
- Debugging 502/504/413/403/redirect loops behind an nginx reverse proxy
- SSL/TLS termination, HTTP/2, WebSocket, gRPC, or SSE through nginx
- Tuning: workers, buffers, gzip, proxy cache, rate limiting
- Proxying raw TCP/UDP (databases, TLS passthrough, syslog) and operating nginx (upgrades, monitoring, log rotation)
- Not for certificate issuance/renewal itself (ACME, Let's Encrypt) — nginx consumes certs; issuance is the `ssl` skill

## Quick Reference

| Situation | Play |
|-----------|------|
| Random 502 after a container/backend redeploy | DNS cached at startup — use variable in `proxy_pass` + `resolver` (`proxy.md`) |
| 502 immediately vs 504 after ~60s | 502 = refused/reset/bad response; 504 = timeout. Different fixes (`proxy.md`) |
| 413 on uploads | `client_max_body_size` — default is 1m; raise in `http` or the exact `server`/`location` |
| WebSocket connects then dies, or never upgrades | Upgrade trio + timeout (`proxy.md`) |
| SSE/streaming arrives all at once | `proxy_buffering off` for that location (`proxy.md`) |
| gRPC calls fail through nginx, direct works | `grpc_pass`, not `proxy_pass` — trailers and HTTP/2 (`proxy.md`) |
| Wrong file served / 403 on aliased path | `root` vs `alias` semantics and the alias-traversal slash bug (`semantics.md`) |
| Request hits wrong location block | Re-derive with the matching algorithm below; `nginx -T` to see effective config |
| Backend receives wrong path (`/api/api/...` or missing prefix) | proxy_pass trailing-slash rules (below) |
| Browser cert warning, curl works | Missing intermediates — serve fullchain (`ssl.md`) |
| 80→443 redirect loop behind a CDN/LB | Trust `X-Forwarded-Proto`, don't redirect on `$scheme` alone (`ssl.md`) |
| Redirect fixed in config but browser still loops | Cached 301 — test in curl or a private window (`redirects.md`) |
| PHP blank page, "File not found", or browser downloads .php source | SCRIPT_FILENAME and location order (`fastcgi.md`) |
| nginx container exits instantly, or template renders empty values | Foreground mode and the envsubst collision (`containers.md`) |
| Proxy a database / route TLS by SNI without terminating / forward syslog | `stream {}` block, `ssl_preread` (`stream.md`) |
| Upgrade the nginx binary or a module without dropping connections | USR2/WINCH signal sequence (`operations.md`) |
| "Is nginx overloaded?" / capacity monitoring | `stub_status` and what its numbers mean (`operations.md`) |
| Slow under load, high CPU or connection errors | `performance.md` |
| Security headers vanished on some routes | `add_header` inheritance trap (`semantics.md`) |
| Config behaves unlike it reads (`if`, variables, includes, root/alias) | `semantics.md` |
| Anything else | Debugging Order below, then the closest file above |

Depth on demand: `debug.md` startup failures, status-code decoder, tracing · `proxy.md` 502/504, DNS trap, WebSocket, gRPC, buffering, retries · `semantics.md` root/alias, inheritance, `if`, variables, includes, server selection · `redirects.md` return/rewrite, status codes, canonical host · `ssl.md` chain, baseline, HSTS, OCSP, mTLS, HTTP/3 · `performance.md` workers, buffers, gzip, proxy cache · `security.md` rate/conn limits, auth, hardening · `fastcgi.md` PHP-FPM · `containers.md` Docker/K8s · `stream.md` TCP/UDP, TLS passthrough · `operations.md` signals, upgrades, monitoring, log rotation.

## Core Rules

1. `nginx -t && nginx -s reload` — never restart to apply config; reload is graceful (old workers finish in-flight requests). Test first: a bad config on restart takes the site down; on reload it's rejected.
2. Read the effective config with `nginx -T`, not the files — includes, inheritance, and distro defaults (`/etc/nginx/conf.d/*`) mean the file you're editing may not be what runs.
3. One canonical `Host` line: `proxy_set_header Host $host;`. Without it the backend sees the upstream name from `proxy_pass` — breaks virtual hosts, redirects, and anything that reads Host.
4. `proxy_set_header` in a location wipes ALL inherited proxy headers from server/http level, same for `add_header`. Inheritance is all-or-nothing per level: if you set one header in a location, re-declare the full set there.
5. Sizing: max concurrent proxied clients ≈ `worker_processes × worker_connections / 2` (each proxied request holds a client fd and an upstream fd). 4 workers × 1024 connections → ~2048 clients. Set `worker_rlimit_nofile` ≥ 2× worker_connections.
6. Never put logic in `if` beyond `return`/`rewrite` — `if` in location context creates a pseudo-location where other directives misbehave. Use `map` for conditionals.
7. Diagnose from the log split: log `$request_time` and `$upstream_response_time` together. High request_time + low upstream_time = slow client or buffering problem; both high = slow backend. Without both numbers you're guessing which side is slow.

## Location Matching (the real algorithm)

Common misreading is "regex beats prefix". Actual order:

1. Exact `= /path` — match ends immediately.
2. Find the LONGEST matching prefix (order in file irrelevant for prefixes).
3. If that prefix is marked `^~` — use it, skip regex entirely.
4. Otherwise try regex locations `~` / `~*` in FILE ORDER — first regex match wins.
5. No regex matched — fall back to the longest prefix from step 2.

Consequences:
- `location /api` also matches `/api-v2`, `/apiary` — prefix is string prefix, not path segment. Use `location /api/` plus `location = /api` if you need the segment.
- A short regex declared early beats your long careful prefix — `^~` on static asset prefixes is the standard defense.
- `location /api/` does not match `/api` (no trailing slash) — pair with exact match or accept the 404.

## proxy_pass Path Rules

- `proxy_pass http://backend;` (no URI part) → request path passed unchanged: `/api/users` → `/api/users`.
- `proxy_pass http://backend/;` (any URI part, even just `/`) → matched location prefix is REPLACED by that URI: `location /api/` + `.../` → `/api/users` becomes `/users`.
- URI part inside a regex location or inside `if` = config error at startup — rewrite instead, or drop the URI part.
- With a variable in `proxy_pass` (`set $up http://backend; proxy_pass $up;`) path handling changes again: nginx passes the URI as given in the directive; combine with `$request_uri` explicitly if needed.
- Verify with the backend's access log or `curl -v` against the backend directly — not by reasoning about the config.

## Proxy Headers & Real IP

Canonical block (re-declare wholesale wherever any `proxy_set_header` appears — rule 4):

```nginx
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
```

- `$host` = lowercase, no port; `$http_host` = raw header with port. APIs that generate absolute URLs usually need `$http_host`.
- `X-Forwarded-For` is client-spoofable. If nginx is behind a trusted LB/CDN, use the realip module: `set_real_ip_from <LB subnet>; real_ip_header X-Forwarded-For; real_ip_recursive on;` — otherwise rate limits and logs key on the LB's IP.
- Headers with underscores are silently dropped by default (`underscores_in_headers on` to keep) — a classic "auth works with curl -H, fails through nginx" cause.

## Upstream & Keepalive

```nginx
upstream backend {
    server 10.0.0.2:3000 max_fails=3 fail_timeout=10s;
    server 10.0.0.3:3000 max_fails=3 fail_timeout=10s;
    keepalive 32;
}
```

- `keepalive 32` does NOTHING alone. The trio: `keepalive N` in upstream + `proxy_http_version 1.1;` + `proxy_set_header Connection "";` in the location. Missing either latter directive = a new TCP (and TLS) handshake per request, silently.
- `keepalive N` = idle connections kept per worker, not a connection limit.
- Defaults: `max_fails=1 fail_timeout=10s`. `fail_timeout` is dual-purpose: the window for counting failures AND the ban duration. `max_fails=0` disables marking down entirely.
- These are passive checks (real requests fail first). Active health checks are nginx Plus only — in OSS, put a real health endpoint behind your monitoring instead.
- Server without a port = port 80 — a common surprise when the app listens on 3000.
- Retries: on error/timeout nginx tries the next upstream server. Non-idempotent methods (POST, PATCH, LOCK) are not retried since nginx >=1.9.13 unless you set `proxy_next_upstream non_idempotent` — do not set it for endpoints with side effects.

## try_files & Static

- SPA: `try_files $uri $uri/ /index.html;` — file, then directory (needs `index`), then internal fallback. Last arg is a redirect/code, not a checked file: `=404` to error instead.
- `try_files` + `proxy_pass` in one location: try_files controls; route to the proxy via a named location — `try_files $uri @app;` + `location @app { proxy_pass ...; }`. This is the canonical "static if present, else app" pattern.
- Static asset locations: `^~` prefix, `access_log off;`, `expires 30d;` + `add_header Cache-Control "public, immutable";` for hashed filenames (expires alone without Cache-Control gets ignored by some clients).
- `sendfile on; tcp_nopush on;` together — sendfile without tcp_nopush leaves the kernel optimization on the table.

## SSL/TLS Essentials

- `ssl_certificate` takes the FULLCHAIN (leaf + intermediates, leaf first, no root). Leaf-only "works" in browsers with cached intermediates and fails on fresh clients — the classic "works for me, warning for users".
- Baseline: `ssl_protocols TLSv1.2 TLSv1.3;` and start from the Mozilla SSL config generator (intermediate profile) rather than hand-picking ciphers.
- `ssl_ciphers` only governs ≤TLS1.2; TLS1.3 suites need `ssl_conf_command Ciphersuites` (OpenSSL) — a source of "my cipher config does nothing".
- `ssl_prefer_server_ciphers off` is the modern recommendation (client-hardware-aware selection); `on` was TLS1.2-era advice.
- `ssl_session_cache shared:SSL:10m;` — ~4000 sessions per MB, shared across workers. Skipping it costs a full handshake per returning client.
- Redirect loops, HSTS rollout, OCSP, client certs → `ssl.md`.

## Rate Limiting

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
location /api/ { limit_req zone=api burst=20 nodelay; limit_req_status 429; }
```

- `rate=10r/s` is enforced per-millisecond: 1 request per 100ms. Two instant requests without `burst` = second one rejected. Always pair rate with a burst sized for legitimate client behavior (a browser page load fires 10-30 parallel requests).
- `nodelay` = serve the burst immediately, refill over time; without it, burst requests queue and add latency.
- Default rejection status is 503 — set 429 so clients and monitoring can tell throttling from outage.
- Behind a CDN/LB without realip configured, `$binary_remote_addr` is the LB's address — you rate-limit everyone as one client.
- Zone sizing, tiered keys, connection/bandwidth limits → `security.md`.

## Debugging Order

1. `nginx -t` — config valid? `nginx -T` — what's actually loaded?
2. `tail -f` the error log; raise level only on the suspect vhost. Grep-to-cause:

| Error log message | Meaning |
|---|---|
| `connect() failed (111: Connection refused)` | Backend down or wrong port → 502 |
| `no live upstreams` | All upstream servers marked failed (max_fails tripped) → 502 |
| `upstream prematurely closed connection` | Backend crashed mid-response or app timeout shorter than nginx's → 502 |
| `upstream timed out (110)` | nginx waited `proxy_read_timeout` (default 60s) → 504 |
| `client intended to send too large body` | `client_max_body_size` (default 1m) → 413 |
| `worker_connections are not enough` | Connection budget exhausted → see Core Rule 5 |
| Anything else | Reproduce with `curl -v` against nginx AND directly against the backend; the diff localizes the fault |

3. A timeout in nginx does not cancel the backend request — the backend keeps burning CPU on a request nobody will read. Fix the slow endpoint, don't just raise the timeout.

## Output Gates

Before emitting an nginx config or config advice, verify:

- Apply instructions end with `nginx -t` then reload — never a restart?
- Every location that sets any `proxy_set_header` or `add_header` re-declares the full inherited set (rule 4)?
- `proxy_pass` URI part checked against the trailing-slash rules — the backend receives the path you intend?
- Upload-handling routes have `client_max_body_size` above the real payload size?
- New permanent redirects shipped as 302 first, 301 only after verification (`redirects.md` ramp)?
- If `edge_position` is behind-cdn-lb: realip configured before anything keys on client IP, and redirects read `X-Forwarded-Proto`?

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| `worker_processes auto` in containers | Reads host CPU count, not cgroup quota — 64 workers on a 2-CPU limit | Set explicitly to the container's CPU limit |
| Editing config, reloading, no change | Distro includes another file that wins | `nginx -T \| less`, find who owns the directive |
| Hostname in `proxy_pass` to dynamic infra | Resolved once at startup, cached forever | Variable + `resolver` (`proxy.md`) |
| `gzip on` for images/zip/woff2 | Recompressing compressed data: CPU spent, bytes gained | `gzip_types` with text formats only |
| `if` for routing logic | Pseudo-location; directives inside behave unpredictably | `map` + variable, or separate locations |
| Log rotation without signal | nginx keeps writing to the deleted inode; disk fills with no visible file | `nginx -s reopen` (USR1) in the rotate script (`operations.md`) |
| Reload "not taking" with WebSockets | Old workers stay alive until long-lived connections close | `worker_shutdown_timeout 30s;` to bound the drain |
| No `default_server` defined | First server block silently catches all unmatched Hosts | Explicit `listen 80 default_server; return 444;` catch-all (`semantics.md`) |

## Where Experts Disagree

- **Mainline vs stable channel.** The nginx team recommends mainline for most users; "stable" means fewer feature changes, not more reliability. Default: mainline from nginx.org repos when you control the host; pinned distro/stable inside images where reproducibility wins (`operations.md`).
- **conf.d vs sites-enabled.** Debian's symlink pattern adds an explicit enable/disable step; flat conf.d is simpler. Either works — the failure mode is mixing both and losing track of what's live; `nginx -T` is the referee (rule 2).
- **Terminate TLS at the CDN/LB or at nginx.** Edge termination centralizes cert management; nginx termination keeps encryption to the box. The boundary is compliance scope and who owns header trust — whoever terminates must set `X-Forwarded-Proto` and realip correctly (`ssl.md`).

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/nginx (install if the user confirms):

- `ssl` — certificate issuance, renewal, and TLS debugging beyond nginx directives
- `docker` — nginx in containers: images, networks, and the resolver at 127.0.0.11
- `caddy` — when automatic HTTPS and a simpler config beat nginx's control
- `vps` — server provisioning and hardening around the nginx install
- `dns` — records and propagation issues upstream of the proxy

## Feedback

- If useful, star it: https://clawic.com/skills/nginx
- Latest version: https://clawic.com/skills/nginx

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/nginx.
