# php.ini — Which Setting Wins, and Why Yours Did Not

"I changed the setting and nothing happened" has exactly three causes: you edited a file this SAPI does not read, a later layer overrode it, or the directive cannot be changed at that level.

## Find the Truth First

```
php --ini                      # CLI: loaded file + scanned directory + parsed files
php-fpm -i | head -20          # FPM's own view (different from CLI, almost always)
<?php phpinfo();               # the running web SAPI — the only authoritative web answer
php -i | grep -i memory_limit  # "Local Value" vs "Master Value" shows what overrode what
```

The CLI and the web SAPI load DIFFERENT ini files on nearly every distribution (`/etc/php/8.3/cli/php.ini` vs `/etc/php/8.3/fpm/php.ini`). Editing one and testing the other is the most common wasted hour in PHP operations.

## Precedence, Lowest to Highest

1. Compiled-in defaults
2. `php.ini` for the SAPI
3. `conf.d/*.ini`, loaded in filename order — this is why extension configs are numbered (`10-opcache.ini`, `20-xdebug.ini`)
4. FPM pool: `php_value[...]` and `php_admin_value[...]` (`fpm.md`)
5. Web-server-level directives (`.htaccess` `php_value` under mod_php)
6. `.user.ini` in the script's directory, for `PHP_INI_USER`/`PHP_INI_PERDIR` directives only
7. `ini_set()` at runtime, for `PHP_INI_ALL` directives only

- `php_admin_value` in an FPM pool cannot be overridden by `ini_set()` — that is the difference from `php_value`, and the right tool for `memory_limit` ceilings you do not want a script to raise.
- `.user.ini` is CACHED: changes take up to `user_ini.cache_ttl` (300 seconds by default) to appear. Under FPM, `.htaccess`-style directives do not work at all; `.user.ini` is the replacement.
- Directive changeability is listed per setting in the manual as `PHP_INI_ALL` / `PERDIR` / `SYSTEM`. `upload_max_filesize` is PERDIR, so `ini_set('upload_max_filesize', …)` silently does nothing. Most `opcache.*` settings are SYSTEM and need a restart.

## Settings That Change Behavior You Will Notice

| Directive | Default-ish | What it actually does |
|---|---|---|
| `memory_limit` | 128M | Per-process ceiling. Real host requirement is this × `pm.max_children` (`fpm.md`) |
| `max_execution_time` | 30 (0 on CLI) | Counts CPU time in userland only — not time inside system calls on Unix |
| `post_max_size` | 8M | Exceeded ⇒ `$_POST` AND `$_FILES` arrive EMPTY, with no error |
| `upload_max_filesize` | 2M | Must be ≤ `post_max_size`, which must leave room for the other fields |
| `max_file_uploads` | 20 | Files past the 20th vanish silently from `$_FILES` |
| `max_input_vars` | 1000 | Form fields past the 1000th are DROPPED silently — the classic giant-form bug |
| `date.timezone` | UTC | Unset means UTC with no warning; every `date()` in the app inherits it (`datetime.md`) |
| `default_charset` | UTF-8 | The implicit encoding for `htmlspecialchars` and `mb_*` (`strings.md`) |
| `precision` / `serialize_precision` | 14 / -1 | Why a float prints as `0.3` and JSON-encodes differently (`types.md`) |
| `pcre.backtrack_limit` | 1000000 | Exceeded ⇒ `preg_match` returns `false` silently (`strings.md`) |
| `zend.assertions` | 1 dev / -1 prod | `-1` compiles assertions out entirely; cannot be raised at runtime (`errors.md`) |
| `session.gc_maxlifetime` | 1440 | Server-side session expiry in seconds — usually what logs users out, not the cookie (`sessions.md`) |
| `output_buffering` | varies | Non-zero lets `header()` work after output, and hides where output started |

## Production Baseline

```ini
display_errors = Off
display_startup_errors = Off
log_errors = On
error_reporting = E_ALL
error_log = /var/log/php/error.log     ; must be writable by the FPM user
expose_php = Off
zend.assertions = -1
opcache.enable = 1
opcache.validate_timestamps = 0        ; with an FPM reload in the deploy (performance.md)
session.cookie_httponly = 1
session.cookie_secure = 1
session.cookie_samesite = Lax
session.use_strict_mode = 1
```

- `error_reporting = E_ALL` with `display_errors = Off` is the correct pair: everything is recorded, nothing is shown. Reducing `error_reporting` in production means the log will not contain the deprecation that breaks the next upgrade (`versions.md`).
- An unwritable `error_log` path fails silently and you get a blank page with an empty log — check `ls -l` as the FPM user (`debugging.md`).

## Development Baseline

```ini
display_errors = On
error_reporting = E_ALL
zend.assertions = 1
opcache.enable = 1
opcache.validate_timestamps = 1
opcache.revalidate_freq = 0            ; see edits immediately
xdebug.mode = develop,debug            ; off in any shared or perf-tested environment
```

## Per-Environment Without Editing php.ini

- One-off: `php -d memory_limit=1G script.php` — highest precedence for that invocation, ideal for a migration that legitimately needs more.
- Per pool: `php_admin_value[memory_limit] = 512M` in the FPM pool file, so one heavy application does not raise the ceiling for every other pool on the host.
- Per script: `ini_set('memory_limit', '512M')` works only for `PHP_INI_ALL` directives and only if no `php_admin_value` locked it.
- In containers, ship a single `conf.d/99-app.ini` with your overrides rather than editing the base image's `php.ini` — it survives base-image upgrades and is diffable.

## Extensions

- `php -m` lists loaded modules; `php --ri opcache` prints one extension's configuration and runtime state.
- Load order matters when extensions interact: opcache must load before Xdebug or the debugger's behavior gets strange. That is what the numeric prefixes in `conf.d` are for.
- `ext-mbstring`, `ext-intl`, `ext-pcntl`, `ext-pdo_mysql` are the ones most often missing on a fresh server and each fails as a "call to undefined function" long after startup (`versions.md`).

## Related

- Pool-level overrides and worker limits: `fpm.md`
- Which of these settings governs a symptom you are chasing: `debugging.md`
- OPcache tuning in depth: `performance.md`
