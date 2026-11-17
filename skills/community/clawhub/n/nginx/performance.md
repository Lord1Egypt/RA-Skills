# Performance: Tuning That Actually Moves Numbers

## Workers & Connections

- `worker_processes auto` reads host CPUs via sysconf — in a container with a 2-CPU cgroup limit on a 64-core host you get 64 workers thrashing. Set it to the cgroup quota explicitly.
- Budget: concurrent proxied clients ≈ workers × worker_connections / 2 (client fd + upstream fd per request). The formula and worked example live in SKILL.md Core Rule 5 — keep numbers consistent with it.
- Raising `worker_connections` without `worker_rlimit_nofile` ≥ 2× just moves the failure from "worker_connections are not enough" to EMFILE.
- `multi_accept on` and `worker_cpu_affinity` are micro-tuning: measure before and after or don't touch them; neither fixes a saturated backend.

## Buffers

- `client_body_buffer_size` (default 8k/16k) smaller than typical uploads → every upload spills to a disk temp file, silently. If your API takes 1MB JSON bodies, set 1m and watch the temp-file warnings disappear.
- Same spill for proxy responses: see buffering in `proxy.md`.
- `client_max_body_size` (default 1m) is a hard 413, not a buffer — the number users hit first on any upload feature.
- Fewer, larger buffers beat many tiny ones — buffer memory is per-connection, so 1000 connections × oversized buffers is how nginx "leaks" memory without leaking.

## Gzip

```nginx
gzip on;
gzip_comp_level 5;           # 4-6 zone; above 6 = CPU up, bytes barely down
gzip_min_length 256;         # tiny payloads can GROW when compressed
gzip_types text/plain text/css application/json application/javascript image/svg+xml;
gzip_vary on;                # without it, caches/CDNs may serve gzip to non-gzip clients
gzip_proxied any;            # default OFF for proxied requests — behind a LB, gzip silently never fires
```

- `gzip on` alone compresses only `text/html` — the `gzip_types` line is what makes it real.
- Never add already-compressed types (jpg, png, woff2, zip): CPU spent to make files slightly larger.
- `gzip_proxied` is the invisible one: responses to requests carrying `Via` aren't compressed by default.
- Pre-compress static assets at build time (`gzip_static on;` + `.gz` files) — zero runtime CPU, better ratios.

## Proxy Cache

```nginx
proxy_cache_path /var/cache/nginx keys_zone=app:10m max_size=1g inactive=60m use_temp_path=off;
location / {
    proxy_cache app;
    proxy_cache_key $scheme$host$uri$is_args$args;
    proxy_cache_valid 200 10m;
    proxy_cache_use_stale error timeout updating;
    proxy_cache_lock on;
    add_header X-Cache-Status $upstream_cache_status;
}
```

- `proxy_cache_lock on` + `use_stale updating` = thundering-herd protection: one request refreshes, everyone else gets the stale copy. Without these, cache expiry under load sends a request stampede to the backend.
- `proxy_cache_valid 10m;` without status codes applies to 200, 301, AND 302 — cached redirects are a classic "users stuck on old URL" bug. List codes explicitly.
- Key design: including `$args` means every UTM-tagged URL is a separate cache entry (cache blowup); excluding it serves one variant for genuinely different queries. Decide per route, not globally.
- Backend `Set-Cookie` responses are not cached by default — an app that cookies every response has a 0% hit rate. Check `X-Cache-Status` before assuming the cache works.
- `inactive=60m` evicts unused entries by time; `max_size` by space; an entry can be "valid" yet evicted by either — they're independent.

## Static Files & FD Cache

- `sendfile on; tcp_nopush on;` as a pair; `tcp_nodelay on` matters for keepalive's last packets. This trio is the standard block — the win is real but bounded; don't expect it to fix application latency.
- `open_file_cache max=10000 inactive=30s; open_file_cache_valid 60s;` — caches fds and stat() results; the caveat is deploys via file-swap can serve stale metadata for up to `valid` seconds.
- `expires` + `Cache-Control` together for assets (SKILL.md, try_files section). For hashed filenames, `immutable` eliminates revalidation requests entirely.

## Logging Cost

- `access_log` is a synchronous write per request. `access_log /var/log/nginx/access.log main buffer=64k flush=5s;` batches it — trade: up to one buffer of logs lost on crash.
- `access_log off;` on static/asset and health-check locations — health checks alone can be a majority of log lines. Conditional form: `map $request_uri $loggable { /healthz 0; default 1; }` + `access_log ... if=$loggable;`.
- The log format that pays for itself: add `$request_time $upstream_response_time $upstream_cache_status` — the three numbers behind every "nginx is slow" diagnosis (split explained in SKILL.md Core Rule 7).
