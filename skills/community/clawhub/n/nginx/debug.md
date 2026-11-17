# Debugging — Symptom to Cause

Work symptom-first. The universal first three: `nginx -t` (is the config valid?), `nginx -T` (what is actually loaded?), `tail -f` the error log while reproducing with `curl -v`. 502/504 chains live in `proxy.md`; this file covers everything else.

## Won't Start / Dies at Startup

| Error log line | Cause | Fix |
|---|---|---|
| `bind() ... failed (98: Address already in use)` | Another listener owns the port — often Apache, or a stale nginx master from a crashed upgrade | `ss -ltnp \| grep :80` names the holder; stop it or kill the stale master |
| `bind() ... failed (13: Permission denied)` | Ports <1024 need root or `CAP_NET_BIND_SERVICE` — hits unprivileged containers and rootless setups | Listen ≥1024 (see `containers.md`) or grant the capability |
| `[emerg] unknown directive "..."` | Module not compiled in or not loaded (stream, headers-more, brotli) | `nginx -V` lists build modules; dynamic modules need `load_module` in the MAIN context, before `events` |
| `[emerg] cannot load certificate` | Wrong path, or key unreadable — the master reads certs as root, so this is usually a typo or a moved file | `ls -l` the exact path from the message; on renewal scripts, check the symlink target |
| `SSL_CTX_use_PrivateKey_file ... key values mismatch` | Cert and key from different generations | Compare `openssl x509 -noout -modulus` vs `openssl rsa -noout -modulus` (`ssl.md`) |
| `[warn] conflicting server name` | Two blocks claim the same `server_name` — nginx starts anyway and the FIRST wins | Not fatal, but your "new" vhost may never receive a request; deduplicate |
| `[emerg] "stream" directive is not allowed here` | `stream {}` placed inside `http {}` | It is a sibling of `http` at top level (`stream.md`) |

## SELinux (RHEL/CentOS/Fedora — the distro-specific 502/403)

Config is correct, same setup works on Debian, error log shows `(13: Permission denied)`:

- Proxying to any port: `setsebool -P httpd_can_network_connect 1` — SELinux blocks outbound connections from nginx by default.
- Serving files outside `/usr/share/nginx`: `chcon -R -t httpd_sys_content_t /srv/www` (or a `semanage fcontext` rule to survive relabels).
- Confirm attribution before flipping booleans: `ausearch -m avc -ts recent` shows the denial. `os_family: rhel` in config makes this the first suspect.

## Status Code Decoder (nginx-specific meanings)

| Code | Meaning | First move |
|---|---|---|
| 400 instantly, some clients only | Oversized request headers (big cookies, SSO tokens) | Raise `large_client_header_buffers`; on HTTP/2-heavy traffic see `ssl.md` |
| 403 on files that exist | Worker user can't read the path (check EVERY parent dir has `x`), a `deny` rule, or a directory request with no `index` and `autoindex off` | `sudo -u www-data cat <file>` reproduces the permission case in one command |
| 404 on files that exist | Wrong `root`/`alias` resolution or location mismatch | Re-derive with the matching algorithm (SKILL.md); `root` vs `alias` semantics in `semantics.md` |
| 405 on POST to a static file | The static handler only serves GET/HEAD — common with SPA forms and health checks that POST | Route the path to the backend, or `error_page 405 =200 $uri;` if serving the file is genuinely intended |
| 413 | `client_max_body_size` (default 1m) | Raise it in the exact `server`/`location` that handles uploads |
| 444 | No response sent at all — nginx closed the connection | Deliberate: your `default_server` catch-all is eating the request; the client used the wrong Host |
| 494–497 | nginx-internal TLS/header errors: 494 header too large, 495/496 client-cert failure, 497 plain HTTP sent to the HTTPS port | 497 = someone hardcoded `http://host:443`; 495/496 → mTLS in `ssl.md` |
| 499 (log only) | CLIENT gave up before the response — nginx never sent one | See below |
| 502 / 504 | Upstream failure vs upstream timeout | `proxy.md` — different fixes |

## The 499 Spike

499 means the client closed first. It is a symptom of someone ELSE's timeout being shorter than your response time:

- Uniform ~10s or ~30s gaps between request and 499 → an LB/CDN in front timing out; align its timeout above your `proxy_read_timeout` or fix the slow endpoint.
- 499s on one endpoint only → that endpoint is slow; users navigate away. Profile it — the 499 count is your abandonment metric.
- 499 storms during deploys → clients retrying against draining workers; bound the drain with `worker_shutdown_timeout`.

## Sporadic 502 on a Healthy Backend (the keepalive race)

`upstream prematurely closed connection` at random, low rate, backend logs show nothing: the backend closed an idle keepalive connection at the same instant nginx reused it. Node's default idle timeout is 5s; gunicorn's 2s.

- Fix: make the backend's idle timeout LONGER than nginx's reuse window, or set `keepalive_timeout` in the `upstream` block (nginx >=1.15.3) below the backend's value.
- Verify the diagnosis, don't guess: rate correlates with traffic troughs (idle connections), not peaks.

## Worker Crashed

`worker process exited on signal 11` — nearly always a third-party dynamic module built for a different nginx version; modules must be rebuilt for the EXACT version (`operations.md`). Confirm by removing `load_module` lines one at a time.

## Deeper Tracing

- Per-request correlation: add `$request_id` to `log_format` and `proxy_set_header X-Request-ID $request_id;` — one ID across nginx and backend logs turns "which request was that" into a grep.
- `error_log /path debug;` needs a binary built `--with-debug` (`nginx -V` to check); scope it to one server block, not `http`, or the log drowns you.
- One-client debug: `debug_connection <your-ip>;` in `events {}` — debug-level logging for that IP only, safe on production.
- `worker_connections are not enough` / `Too many open files (24)` → the connection budget and `worker_rlimit_nofile` math in SKILL.md Core Rule 5.

## When You Are Truly Stuck

`curl -v` against nginx AND directly against the backend, same path and headers; the diff between the two responses names the layer. Then reduce: comment out includes until the behavior flips — the include that flips it owns the bug.
