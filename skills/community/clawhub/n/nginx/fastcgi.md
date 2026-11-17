# FastCGI — PHP-FPM and Friends

`proxy_pass` speaks HTTP; PHP-FPM speaks FastCGI — `fastcgi_pass` or nothing works. Gunicorn/uvicorn/Node speak HTTP (use `proxy.md`); uWSGI in uwsgi mode uses `uwsgi_pass` with the same parameter pattern as below.

## The Minimal Correct PHP Block

```nginx
location ~ \.php$ {
    try_files $uri =404;      # the security line — see below
    include fastcgi_params;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    fastcgi_pass unix:/run/php/php8.3-fpm.sock;
}
```

- `fastcgi_params` vs `fastcgi.conf`: the distro's `fastcgi.conf` already contains the `SCRIPT_FILENAME` line; `fastcgi_params` does NOT. Including `fastcgi_params` without adding SCRIPT_FILENAME yourself = blank page or "File not found" — the single most common PHP-behind-nginx failure.
- `try_files $uri =404;` blocks the classic upload exploit: with PHP's `cgi.fix_pathinfo=1`, a request for `/uploads/avatar.jpg/x.php` can execute the "jpg" as PHP. The stat check refuses paths that aren't real files. Keep it even if php.ini is fixed — defense on both layers.
- Unix socket vs TCP: socket for same-host (no TCP overhead, permission-controlled); `fastcgi_pass php:9000;` when PHP-FPM is another container.

## Symptom → Cause

| Symptom | Cause | Check |
|---|---|---|
| Blank white page, 200 status | SCRIPT_FILENAME missing or wrong | `nginx -T \| grep -A2 SCRIPT_FILENAME` |
| "File not found" in browser, `Primary script unknown` in error log | SCRIPT_FILENAME resolves to a path PHP-FPM can't see — root mismatch, or in Docker the code isn't mounted at the SAME path in both containers | Path in the error log vs `ls` inside the PHP container |
| Browser downloads the .php source | Request never hit the PHP location — location order or a `^~` static prefix swallowing it | Matching algorithm in SKILL.md; this is also why code must never live in upload dirs |
| 502, error log `connect() ... failed (111)` | PHP-FPM down or socket path mismatch | `systemctl status php8.3-fpm`; compare `listen =` in the pool config against `fastcgi_pass` |
| 502, `connect() ... failed (13: Permission denied)` | Socket owned by a different user than the nginx worker | `listen.owner`/`listen.group` in the FPM pool = the worker user; on RHEL also SELinux (`debug.md`) |
| 502/latency under load, fine when quiet | FPM pool exhausted — `pm.max_children` reached, requests queue | FPM status page (`pm.status_path`) `listen queue` > 0; raise children within RAM budget: max_children ≈ available_ram / per-process RSS |
| 504 | `fastcgi_read_timeout` (default 60s) expired — long report/import scripts | Raise per-location, never globally; and remember the timeout doesn't stop the PHP process (SKILL.md, Debugging Order) |
| `upstream sent too big header` | Framework debug pages / huge session cookies | `fastcgi_buffer_size 16k;` (same mechanics as the proxy case in `proxy.md`) |

## PATH_INFO (front controllers and /index.php/route URLs)

```nginx
location ~ ^(?<script>.+\.php)(?<pathinfo>/.*)?$ {
    try_files $script =404;
    include fastcgi_params;
    fastcgi_param SCRIPT_FILENAME $document_root$script;
    fastcgi_param PATH_INFO $pathinfo;
    fastcgi_pass unix:/run/php/php8.3-fpm.sock;
}
```

Named captures beat `fastcgi_split_path_info` because `try_files` resets the split variables — the split-then-try_files combination silently sends an empty SCRIPT_FILENAME.

## Framework Routing

- The universal front-controller pair (Laravel, Symfony, WordPress pretty permalinks):
  `location / { try_files $uri $uri/ /index.php?$query_string; }` + the PHP location above.
- WordPress admin/uploads hardening: deny PHP under `/wp-content/uploads/` (`security.md`, Blocking Sensitive Paths).
- `fastcgi_intercept_errors on;` + `error_page` to serve your own 5xx instead of the framework's stack trace in production.

## FastCGI Cache (full-page cache for PHP sites)

Same engine and rules as the proxy cache in `performance.md` (`keys_zone`, `use_stale`, `cache_lock`, hit-rate verification) with `fastcgi_cache_*` names. The PHP-specific part is bypass logic — never serve cached pages to logged-in users:

```nginx
map "$http_cookie" $skip_cache {
    default               0;
    ~*wordpress_logged_in 1;
    ~*comment_author      1;
}
fastcgi_cache_bypass $skip_cache;   # don't serve from cache
fastcgi_no_cache     $skip_cache;   # don't store either
```

Add `$upstream_cache_status` to the log format before trusting any of it — `Set-Cookie` on every response yields a 0% hit rate that looks configured and does nothing.
