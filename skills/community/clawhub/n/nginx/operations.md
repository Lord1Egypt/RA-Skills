# Operations — Signals, Upgrades, Monitoring, Rotation

Running nginx as a service you're responsible for: process control, zero-downtime upgrades, capacity monitoring, log rotation, modules, and packaging. Config-content debugging lives in `debug.md`.

## Signals (the complete map)

| Signal | `nginx -s` | Effect |
|---|---|---|
| HUP | `reload` | Re-read config, start new workers, gracefully retire old ones |
| USR1 | `reopen` | Reopen log files — the log-rotation signal |
| QUIT | `quit` | Graceful shutdown: workers finish in-flight requests |
| TERM/INT | `stop` | Fast shutdown: in-flight requests dropped |
| USR2 | — | Spawn a NEW master with the new binary alongside the old |
| WINCH | — | Old master gracefully stops its workers (upgrade step 2) |

- `nginx -s` covers only the first four; USR2/WINCH go via `kill` to the master PID (`cat /var/run/nginx.pid`).
- Under systemd, prefer `systemctl reload nginx` over raw signals — the unit's ExecReload runs the test-then-signal sequence and systemd's state stays truthful. `systemctl restart` drops connections; reload never does (SKILL.md Core Rule 1).

## Zero-Downtime Binary Upgrade (USR2/WINCH)

Package managers restart the service (dropped connections). The signal sequence upgrades the BINARY with none:

1. Install the new binary at the same path (package upgrade without the restart, or manual copy).
2. `kill -USR2 <master-pid>` — new master + workers start from the new binary; old pid file becomes `nginx.pid.oldbin`. Both generations serve traffic.
3. `kill -WINCH $(cat /var/run/nginx.pid.oldbin)` — old workers drain gracefully.
4. Verify the new generation (curl the site, watch the error log). Then `kill -QUIT $(cat /var/run/nginx.pid.oldbin)`.
5. Rollback instead: `kill -HUP` the old master (it restarts its workers) and `-QUIT` the new one.

Long-lived connections (WebSocket) hold old workers alive through step 3 — same drain-bounding as reloads: `worker_shutdown_timeout`.

## Monitoring: stub_status

```nginx
location = /stub_status { stub_status; access_log off; allow 127.0.0.1; deny all; }
```

Output: `Active connections`, then `accepts handled requests`, then `Reading/Writing/Waiting`. The reads that matter:

- `handled < accepts` = connections DROPPED at the door — the worker_connections budget (SKILL.md Core Rule 5) is exhausted. This gap growing is your capacity alarm; equal counters are healthy.
- `requests / handled` = requests per connection. Near 1.0 means client keepalive is effectively off — check `keepalive_timeout` before buying capacity.
- `Waiting` = idle keepalive connections (normal); `Writing` climbing while requests don't = responses draining slowly — slow clients or buffering to temp files (`performance.md`).
- Counters are since-start and reset on restart (not reload) — monitoring must use deltas, not absolutes.
- Deeper request-level metrics come from the access log (`$request_time $upstream_response_time` — SKILL.md Core Rule 7); stub_status is connection-level only.

## Log Rotation

nginx holds log fds open — rotation must move the file, then signal USR1 to reopen; deleting without the signal leaves nginx writing to an invisible inode until the disk fills (SKILL.md Traps).

```
/var/log/nginx/*.log {
    daily
    rotate 14
    compress
    delaycompress
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 $(cat /var/run/nginx.pid)
    endscript
}
```

- `delaycompress` matters: workers may write to the rotated file for a moment after USR1; compressing immediately truncates those lines.
- Containers don't rotate: logs go to stdout/stderr and the runtime caps them (`containers.md`) — a logrotate config inside a container is dead weight.

## Dynamic Modules

- `load_module modules/ngx_stream_module.so;` goes in the MAIN context, above `events {}` — inside `http` it's an `unknown directive`-style startup failure.
- A module binary must be built for the EXACT nginx version running: version skew is the classic `worker process exited on signal 11` crash (`debug.md`, Worker Crashed). After every nginx upgrade, third-party modules (brotli, headers-more, ModSecurity) must be rebuilt or reinstalled from a matching package.
- `nginx -V` (capital V) lists compiled-in modules and build flags — the first check when a directive is "unknown": missing module, not a typo.

## Packaging & Versions

- Distro repos lag years behind; features gated by version floors used across this skill (`http2 on` >=1.25.1, `ssl_reject_handshake` >=1.19.4, upstream `keepalive_timeout` >=1.15.3) often need the official nginx.org repo, which ships both channels (mainline vs stable — SKILL.md, Where Experts Disagree).
- Distro packages also differ in LAYOUT: Debian adds `sites-available/sites-enabled` and a `www-data` user; nginx.org and RHEL packages use flat `conf.d/` and `nginx` user. Worker-user mismatch after switching packages = sudden 403s on files that worked (`debug.md`, Status Code Decoder).
- Pin the minor version in containers and record it with deploys — point releases change directive availability and defaults visibly (`containers.md`).

## Config Testing in CI

- `nginx -t` validates syntax AND the existence of every referenced file — certs, includes, dhparam. In CI that means testing inside a container of the SAME nginx version with certs mounted or dummy self-signed certs generated in the pipeline; a bare `nginx -t` on a runner without the cert paths fails on correct configs.
- `-t` does NOT catch runtime failures: unresolvable upstream hostnames at request time (variable + resolver form), missing backends, realip misconfiguration. Pair the syntax gate with one smoke request against a container running the rendered config.
- Reload-based deploys are atomic per worker generation: a reload that fails validation leaves the old config serving — which is exactly why deploy scripts must check `nginx -t`'s exit code and NOT fall back to restart on failure.
