# Stream — TCP/UDP Proxying and TLS Passthrough

`stream {}` is a sibling of `http {}` at top level, never inside it (nginx won't start otherwise — `debug.md`). It proxies raw connections: databases, TLS passthrough, syslog, MQTT, game servers. No locations, no headers, no URIs — routing happens at connect time.

## Minimal TCP Proxy

```nginx
stream {
    upstream pg { server 10.0.0.5:5432 max_fails=3 fail_timeout=10s; }
    server {
        listen 15432;
        proxy_pass pg;
        proxy_timeout 30m;
        proxy_connect_timeout 3s;
    }
}
```

- `proxy_timeout` (default 10m) closes the session after that much IDLE time in either direction — the cause of "database connection resets after exactly 10 minutes idle". Size it above your pool's idle keepalive, or enable TCP keepalives with `so_keepalive=on` on the listen.
- Same `ip:port` cannot be listened on by both `stream` and `http` — the second context to load fails with "address already in use" from inside nginx itself.
- Load balancing: `least_conn` and `hash $remote_addr consistent` work in stream; passive health only, same `max_fails` semantics as HTTP upstreams (SKILL.md, Upstream & Keepalive).

## Client IP at the TCP Layer

There are no X-Forwarded-* headers in a TCP stream — the backend sees nginx's IP, full stop. Consequences and fixes:

- Postgres `pg_hba.conf`, Redis ACLs, MySQL host grants now match nginx's address, not the client's. Auth rules silently widen to "anyone who can reach nginx".
- `proxy_protocol on;` prepends the PROXY protocol header carrying the real client IP — but the backend MUST be configured to expect it (another nginx, HAProxy, Dovecot, and Postfix can; Postgres and MySQL cannot). A backend not expecting it sees the header as protocol garbage: instant connection errors on every request.
- Receiving side: nginx behind an LB that sends PROXY protocol needs `listen ... proxy_protocol;` plus `set_real_ip_from` — without the listen flag, every connection fails with a parse error.

## TLS Passthrough by SNI (route without terminating)

Route TLS connections by hostname while the backend keeps its own certs — multi-tenant boxes, mail servers, "nginx in front but app terminates TLS":

```nginx
stream {
    map $ssl_preread_server_name $backend {
        app.example.com   10.0.0.2:443;
        mail.example.com  10.0.0.3:993;
        default           10.0.0.2:443;
    }
    server {
        listen 443;
        ssl_preread on;
        proxy_pass $backend;
    }
}
```

- `ssl_preread on` reads the ClientHello without decrypting; `$ssl_preread_server_name` is the SNI. No `ssl_certificate` here — nginx never terminates.
- The `map` needs a `default` — a client without SNI (old tools, raw IP scans) otherwise gets dropped with nothing in the access log.
- Passthrough and termination on the same port is an either/or per server block: if you need "terminate for site A, pass through for site B", passthrough-route in `stream` to a local `http` listener on another port (e.g. 8443) for the terminated sites.
- HTTP-level features are unavailable on passthrough traffic by definition: no realip headers, no caching, no rate limiting by URL — only connection-level limits work.

## UDP

```nginx
server {
    listen 514 udp;
    proxy_pass syslog_pool;
    proxy_responses 0;
    proxy_timeout 1s;
}
```

- `proxy_responses` defines the "session": 0 = fire-and-forget (syslog, statsd) — nginx doesn't hold state waiting for replies; 1 = request/reply (DNS). Wrong value = session-table growth or dropped replies.
- UDP "sessions" are synthetic (tuple + timeout) — a low `proxy_timeout` keeps the state table small on high-volume fire-and-forget traffic.

## Logging & Diagnosis

- `access_log` in stream needs its own `log_format` — HTTP variables don't exist; the useful set: `$remote_addr $status $bytes_sent $bytes_received $session_time $upstream_addr`.
- Stream `$status` is coarse (2xx/4xx/5xx-like codes, e.g. 200 session OK, 502 upstream unreachable) — diagnosis leans on the error log and on `$upstream_addr` showing WHICH backend was tried.
- Test TCP proxying with `nc -v host port` or `openssl s_client` (for passthrough, check the cert served is the BACKEND's — if you see nginx's default cert, a `http` listener caught the port instead).

## Mail Proxy (boundary note)

`mail {}` is a third top-level context (IMAP/POP3/SMTP proxying with an HTTP auth backend) — distinct from stream and rarely the right tool: the common "nginx in front of a mail server" need is TLS/SNI passthrough, covered above. Reach for `mail {}` only when you need per-user backend routing via its auth_http protocol.
