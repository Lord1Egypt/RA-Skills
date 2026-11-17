# Config Semantics: Where nginx Doesn't Behave Like It Reads

## Root vs Alias

- `root /var/www;` + `location /img/` → serves `/var/www/img/photo.png` (location APPENDED to root).
- `alias /var/www/images/;` + `location /img/` → serves `/var/www/images/photo.png` (location REPLACED).
- Slash discipline: with `alias`, location and alias must both end in `/` or both not. Mismatch = doubled or malformed paths.
- Security: `location /img` (no trailing slash) + `alias /var/www/images/` lets `/img../secret` resolve to `/var/www/images/../secret` — the classic alias path-traversal. Always the trailing slash on BOTH, or use `root`.
- `alias` inside a regex location requires a capture: `location ~ ^/img/(.+)$ { alias /var/www/images/$1; }`.
- Default preference: `root` in the `server` block, overridden per-location only when the filesystem layout truly diverges. `alias` is the exception tool, not the default.

## add_header / proxy_set_header Inheritance

Inheritance is per-directive-family and all-or-nothing: a level inherits ALL parent `add_header` lines OR, if it declares even one of its own, NONE.

- Symptom: security headers (HSTS, CSP) set at server level vanish exactly on the routes that set `Cache-Control` in a location.
- Fix: keep the common set in an included snippet and `include` it in every location that adds headers — do not rely on inheritance for anything security-relevant.
- Same model for `proxy_set_header`: one custom header in a location silently drops Host/X-Forwarded-* from the server level. Backend suddenly seeing wrong Host after adding one header = this.
- `add_header ... always;` controls something different: whether the header applies to 4xx/5xx responses (default: only 2xx/3xx). Error pages missing CORS headers = missing `always`.

## if Is a Pseudo-Location

- `if` in location context creates an implicit nested location; content-phase directives inside it (`try_files`, `proxy_pass` with URI, etc.) misbehave in documented-but-surprising ways.
- Safe inside `if`: `return`, `rewrite ... last/break`, `set`. Treat everything else as unsupported.
- Multiple `if` blocks never combine as AND — each evaluates independently. AND logic: chain `map`s or concatenate variables (`set $flag "${a}${b}"; if ($flag = "11") {...}`).
- `set` executes at rewrite phase regardless of location matched later — the variable is set even when "its" location doesn't serve the request.
- Default: any condition on host/URI belongs in `server_name`/`location`; any condition on other request data belongs in `map`. `if` is the last resort for return/rewrite only.

## Variables

- `$uri` = decoded and normalized (`/foo%20bar` → `/foo bar`, `//` collapsed, rewrites applied); `$request_uri` = raw client bytes with query string. Proxying with `$uri` re-encodes and can change semantics; passing raw upstream wants `$request_uri`.
- Undefined variable = empty string plus an error-log warning, never a config error — typos in variable names fail silently at runtime.
- `$args`/`$arg_name` for query access; `$host` (normalized) vs `$http_host` (raw with port) — the distinction that breaks absolute-URL generation, detailed in `proxy.md`.
- `map` is evaluated lazily and once per use — a `map` with hundreds of entries costs nothing until the variable is read. Default tool for any lookup table; `if` chains are the antipattern.

## try_files Details

- `try_files $uri /index.html;` without `$uri/` skips directory resolution — `/docs` 404s even though `/docs/index.html` exists.
- Only the LAST argument is special (internal redirect or `=code`); all earlier ones are stat() checks. `try_files $uri =404;` is the cheap "file or 404".
- Each listed path is a filesystem syscall per request — a 6-fallback try_files on a hot path is measurable; `open_file_cache` (performance.md) amortizes it.
- With `proxy_pass` in the same location, try_files decides and proxy_pass never fires — the working pattern is the named-location fallback in SKILL.md (try_files & Static).

## Includes & File Layout

- `include conf.d/*.conf` loads alphabetically — ordering-sensitive directives (regex locations, maps, default_server) can change behavior when a file is renamed. Prefix ordering-critical files numerically (`00-maps.conf`).
- Include of a nonexistent explicit path = nginx won't start; a glob matching nothing = silently fine. Both facts are exploited by deploy scripts and both bite.
- Relative include paths resolve against the configuration prefix (nginx.conf's directory), not the including file.
- `sites-enabled` symlink pattern (Debian): the config that runs is the symlink target — `nginx -T` is the truth when editing "the" file changes nothing (SKILL.md Core Rule 2).

## Server Selection

- Request Host matched against `server_name`s: exact, then leading-wildcard (`*.example.com`), then trailing-wildcard, then regex in order. No match → the `default_server` for that listen ip:port — or, if none declared, the FIRST server block in include order (which is why renaming a config file once broke someone's routing).
- `server_name _;` is not a wildcard — it's just an intentionally never-matching name, only useful inside a `default_server` block.
- Explicit hardening default: `server { listen 80 default_server; listen 443 ssl default_server; ssl_reject_handshake on; return 444; }` — unknown Hosts and IP-scanners get nothing (444 = close without response), and your real certs aren't served to strangers. `ssl_reject_handshake` needs nginx >=1.19.4; older versions must supply a dummy self-signed cert instead.
