# PHP-FPM — Pools, Sizing, and the 502/504 Family

FPM is a process manager: a master that owns the config and N worker children, each handling one request at a time, start to finish. Every symptom below follows from "one request occupies one whole process".

## Sizing the Pool

Formula, in this order:

1. Measure a warm worker's resident memory: `ps -o rss=,comm= -C php-fpm | sort -rn | head`. Take the high end, not the mean.
2. `pm.max_children = (RAM you will give PHP) / (peak worker RSS)`. On a 4 GB box reserving 1 GB for the OS, database client, and web server, with 80 MB workers: `3000 / 80 ≈ 37`.
3. Sanity-check against concurrency: `needed_children ≈ requests_per_second × average_seconds_per_request`. 50 rps at 120 ms needs ~6 concurrent workers; sizing for 37 then means headroom, not throughput.
4. Whichever number is SMALLER is your ceiling. Setting `max_children` above what RAM supports converts a slow site into an OOM-killed one.

- `memory_limit × pm.max_children` is the worst case a single pool can demand. If that product exceeds host RAM, you have configured an outage (`php-ini.md`).
- More workers than CPU cores is correct for I/O-bound PHP — workers spend most of their life waiting on the database. It is wrong for CPU-bound work, where they only add context switching.

## Process Manager Modes

| Mode | Behavior | Fits |
|---|---|---|
| `static` | `pm.max_children` processes, always alive | Predictable load, dedicated host — no fork latency, maximum memory use |
| `dynamic` | Between `pm.min_spare_servers` and `pm.max_spare_servers`, up to `max_children` | The general default |
| `ondemand` | Forks on arrival, idles out after `pm.process_idle_timeout` | Many low-traffic pools on one host; adds fork latency to the first request |

```ini
[app]
user = www-data
listen = /run/php/app.sock
listen.owner = www-data
listen.mode = 0660

pm = dynamic
pm.max_children = 37
pm.start_servers = 8
pm.min_spare_servers = 4
pm.max_spare_servers = 12
pm.max_requests = 500              ; recycle workers to bound leaks

request_terminate_timeout = 60s    ; > max_execution_time; the only limit that stops a blocked syscall
slowlog = /var/log/php/app.slow.log
request_slowlog_timeout = 5s       ; prints a PHP backtrace for anything slower

catch_workers_output = yes         ; without this, PHP output never reaches the FPM log
decorate_workers_output = no
clear_env = no                     ; FPM clears the environment by default

php_admin_value[memory_limit] = 256M
php_admin_value[error_log] = /var/log/php/app.error.log
```

- One pool per application and per unix user. Two sites in one pool share a memory budget, an OPcache, and a filesystem identity; a compromise of one reaches the other.
- `pm.max_requests` bounds leaks rather than fixing them, and it costs a fork per recycle. 500-1000 is a common range; a value low enough to be noticeable means you have a leak to find (`debugging.md`).
- `clear_env = no` is required for 12-factor configuration — by default FPM starts workers with a scrubbed environment and `getenv()` returns nothing. The alternative is explicit `env[KEY] = value` lines in the pool.

## 502 vs 504 vs 500

| Response | Meaning | First check |
|---|---|---|
| 502 Bad Gateway | The web server could not talk to FPM, or the worker died mid-request | FPM running? socket path and permissions match the nginx config? a worker segfaulted (check the FPM log for "exited on signal 11")? |
| 504 Gateway Timeout | Something upstream hit a time limit | nginx `fastcgi_read_timeout` vs FPM `request_terminate_timeout` vs PHP `max_execution_time` — the smallest one fires |
| 500 with an empty body | PHP fatal with `display_errors = Off` | The pool's `error_log`, then the PHP error log (`debugging.md`) |
| "server reached pm.max_children" in the FPM log | The pool is saturated | Requests are queuing; see the next section |

- Timeout ladder, ordered: `max_execution_time` (userland CPU only) < `request_terminate_timeout` (FPM kills the worker) < the web server's read timeout. Reversed, nginx gives up first and you never see a PHP diagnostic.
- A worker killed by `request_terminate_timeout` leaves no PHP stack trace by design. `slowlog` at a threshold below the terminate timeout captures the backtrace before the kill — configure both together.

## The Status Page

```ini
pm.status_path = /fpm-status     ; restrict it in the web server to localhost
ping.path = /fpm-ping
```

Read `listen queue`, `max listen queue`, `active processes`, and `max children reached`.

- `max children reached` above zero means the pool ran out of workers at some point: requests queued in the kernel backlog and users waited. Either the app got slower or the pool is undersized — check request duration before adding children.
- A persistently non-zero `listen queue` is saturation happening right now.
- `slow requests` counts what `request_slowlog_timeout` caught, which points straight at the log with the backtraces.

## Deploys

- `kill -USR2 <master-pid>` (or `systemctl reload php-fpm`) is a graceful reload: workers finish their current request, then the master starts new ones with the new config and a fresh OPcache.
- With `opcache.validate_timestamps = 0`, this reload IS the deploy — swapping files without it leaves every worker running the previous release (`performance.md`).
- Atomic release directories plus a symlink swap: point `root` at the symlink, and note that `realpath` caching plus OPcache can hold the OLD resolved path until the reload. Reload after the swap, always.
- Zero-downtime across a reload is a load-balancer property, not an FPM one; a single-node reload drops nothing that was already accepted but pauses acceptance briefly.

## nginx Pairing Notes

- `fastcgi_read_timeout` must exceed the PHP-side limits or nginx times out first and hides the real error.
- `fastcgi_buffering off` is required for streamed responses (server-sent events, progressive output); with buffering on, nginx holds the whole body.
- `client_max_body_size` must be at least `post_max_size`, or large uploads fail at nginx with a 413 before PHP ever sees them (`php-ini.md`).
- The `try_files $uri =404` guard before passing to FPM prevents path-info tricks from executing arbitrary uploaded files — the `nginx` skill covers the full location block.

## fastcgi_finish_request

`fastcgi_finish_request()` flushes the response and lets the worker keep running (FPM only). Useful for a fast response with a small tail of bookkeeping — but the worker stays OCCUPIED, so the work still counts against `pm.max_children`. Anything longer than a few hundred milliseconds belongs in a queue (`concurrency.md`).

## Related

- Directive precedence and pool-level overrides: `php-ini.md`
- Diagnosing the request that is stuck: `debugging.md`
- OPcache settings the reload interacts with: `performance.md`
