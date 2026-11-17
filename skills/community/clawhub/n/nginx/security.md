# Security — Rate Limits, Auth, and Hardening

TLS configuration lives in `ssl.md`; this file is abuse control, access control, and surface reduction.

## Rate Limiting (beyond the base block)

The canonical `limit_req` block, per-millisecond enforcement, burst sizing, 429 vs 503, and the LB-keying trap live in SKILL.md, Rate Limiting. The parts that come up next:

- Zone sizing: ~16k states per MB of zone; when the zone fills, nginx evicts oldest states — a 10m zone handles ~160k distinct client IPs.
- Tiered keys: `map` an API token or path to different zones; `limit_req` accepts multiple zones per location (all must pass).
- Whitelisting: `map` trusted IPs/health-checkers to an empty string as the zone key — an empty key is never limited; cleaner than `if` gymnastics.
- `limit_req_dry_run on;` logs would-be rejections without enforcing — the safe way to calibrate rate and burst against real traffic before turning a limit on.

## Connection & Bandwidth Limits

- `limit_conn_zone $binary_remote_addr zone=perip:10m;` + `limit_conn perip 20;` — caps concurrent connections; the tool against slow-POST floods and download hogs, orthogonal to request rate.
- `limit_rate 1m;` throttles response bandwidth per connection; `limit_rate_after 10m;` serves the first bytes full-speed (video seeking stays snappy, bulk scraping doesn't).
- Slowloris posture on public edges: `client_header_timeout 10s; client_body_timeout 10s;` (defaults 60s hold sockets open for a minute per drip-fed request) + `reset_timedout_connection on;`.

## Access Control

- `allow`/`deny` evaluate `$remote_addr` — behind a proxy without realip you are allowing the LB, not the client. Order matters: first match wins, so `allow 10.0.0.0/8; deny all;`.
- Basic auth: `auth_basic "restricted"; auth_basic_user_file /etc/nginx/htpasswd;` — generate entries with `htpasswd -B` (bcrypt); the tool's default crypt() hashes are brute-forceable.
- IP-or-password: `satisfy any;` + allow rules + auth_basic — office IPs skip the prompt, everyone else authenticates.
- Method restriction: `limit_except GET POST { deny all; }` — inside it, allow/deny/auth apply to the excluded methods; blocks TRACE/DELETE probes on read-only routes.

## auth_request (subrequest authentication)

The pattern behind oauth2-proxy and forward-auth gateways: nginx asks an auth service before serving each request.

```nginx
location /private/ {
    auth_request /_auth;
    auth_request_set $auth_user $upstream_http_x_user;
    proxy_set_header X-User $auth_user;
    proxy_pass http://backend;
}
location = /_auth {
    internal;
    proxy_pass http://auth-service/verify;
    proxy_pass_request_body off;
    proxy_set_header Content-Length "";
    proxy_set_header X-Original-URI $request_uri;
}
```

- Auth service semantics: 2xx = allow, 401/403 = deny (forwarded to the client), anything else = 500.
- `proxy_pass_request_body off` + empty Content-Length are mandatory — the subrequest must not re-upload the body.
- Auth-gated file downloads: backend returns `X-Accel-Redirect` to an `internal;` location — the auth check runs once, nginx serves the file (`proxy.md`, Header Details).

## Blocking Sensitive Paths

- `location ~ /\.(?!well-known) { deny all; }` — blocks `.git`, `.env`, `.htpasswd` (exposed `.git` directories are a recurring real-world source-code leak) while keeping `/.well-known/` for ACME challenges.
- Block PHP execution in upload dirs even on non-PHP sites that once ran WordPress: `location ~* /uploads/.*\.php$ { deny all; }` — the FastCGI-side defense is in `fastcgi.md`.
- `secure_link` for expiring signed URLs: `secure_link $arg_md5,$arg_expires; secure_link_md5 "$secure_link_expires$uri secret";` — download links that die, without an app roundtrip.

## Surface Reduction

- `server_tokens off;` — hides the version in headers and error pages ("nginx" remains; hiding it entirely needs headers-more). Scanners fingerprint versions to pick exploits; don't hand them the number.
- Unknown-Host and IP-scan traffic: the `default_server` + `return 444` + `ssl_reject_handshake` catch-all — canonical block in `semantics.md`, Server Selection.
- Security headers (`X-Content-Type-Options nosniff`, `X-Frame-Options SAMEORIGIN` or CSP `frame-ancestors`, HSTS from `ssl.md`): keep the set in one included snippet, because any `add_header` in a location wipes inherited ones (`semantics.md`).

## CORS (do it once, correctly)

- Echo, don't wildcard, when credentials are involved: `Access-Control-Allow-Origin: *` is invalid with cookies. `map $http_origin $cors { ~^https://(app|admin)\.example\.com$ $http_origin; default ""; }` then `add_header Access-Control-Allow-Origin $cors always;`.
- Preflights never reach your backend logic gate: `if ($request_method = OPTIONS) { return 204; }` inside the API location, with the CORS headers present on that return path too.
- The `always` flag is not optional — without it, 4xx/5xx responses lack CORS headers, and the browser masks your API's real error as "CORS failure".

## What nginx OSS Does Not Give You

- No WAF: ModSecurity and NAXSI bolt on; native tools are rate/conn limits, `map`-based blocklists, and `geo` (CIDR→variable lookups, efficient at thousands of ranges: `geo $blocked { default 0; 203.0.113.0/24 1; }`).
- No active health checks and no dynamic upstream API (both Plus features) — design around passive checks (`proxy.md`, Retries & Failover).
