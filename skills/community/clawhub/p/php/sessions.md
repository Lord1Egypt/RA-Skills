# Sessions — Locking, Expiry, and Not Being Hijacked

## The Lock Nobody Expects

`session_start()` acquires an EXCLUSIVE lock on the session record and holds it until the script ends or you close it. Every other request carrying the same session ID blocks, waiting.

- Symptom: a dashboard firing six parallel AJAX calls takes the SUM of their durations instead of the maximum. Nothing in the code looks serial.
- Fix: `session_write_close()` immediately after the last write. Reads from `$_SESSION` still work afterward (the array stays populated in memory); only further WRITES are lost.

```php
session_start();
$userId = $_SESSION['user_id'] ?? null;
session_write_close();          // release the lock before the slow part
$report = $reporting->build($userId);
```

- Endpoints that never touch the session should not start one at all. Auto-starting sessions globally (`session.auto_start = 1`) serializes the entire application per user.
- The `files` handler locks with `flock`; Redis and Memcached handlers have their own locking behavior — phpredis, for example, exposes `session.lock_*` settings and can be configured with a lock timeout and retries. Switching handlers changes the failure mode, not the existence of the problem.

## Expiry: Two Clocks

| Setting | Controls | Default |
|---|---|---|
| `session.cookie_lifetime` | How long the BROWSER keeps the cookie; `0` means until the browser closes | 0 |
| `session.gc_maxlifetime` | How long the SERVER considers the data valid, in seconds | 1440 (24 minutes) |

- Users "randomly logged out after about twenty minutes idle" is `gc_maxlifetime` (1440 seconds), not the cookie. Raise the server side too, or the cookie outlives the data it points at.
- Garbage collection is probabilistic: `session.gc_probability / session.gc_divisor` chance per request. On low-traffic sites, expired data can survive for a long time; on Debian and Ubuntu, PHP's own GC is disabled in favor of a system cron that cleans the DEFAULT `save_path` — point `save_path` somewhere custom and nothing ever cleans it.
- Sessions do not expire "on schedule": a file older than `gc_maxlifetime` is deleted the next time a GC pass happens to run. Enforce a real timeout in the application with an absolute and an idle timestamp inside `$_SESSION`.

## Hardening

```ini
session.use_strict_mode = 1     ; reject session IDs the server never issued
session.use_only_cookies = 1    ; never accept an ID from the URL
session.cookie_httponly = 1     ; unreadable from JavaScript
session.cookie_secure = 1       ; HTTPS only
session.cookie_samesite = Lax   ; blocks the simplest cross-site POST
session.name = __Host-sid       ; the __Host- prefix pins path and host, with Secure
```

- `use_strict_mode = 0` (the default on many builds) lets an attacker set an arbitrary session ID in the victim's browser and then use it — classic session fixation. Turning it on is the single most important line here.
- `session_regenerate_id(true)` on login and on every privilege change. The `true` deletes the old record; under parallel requests that can log the user out of an in-flight tab, which is why frameworks keep a brief grace window instead.
- Bind the session to a fingerprint that does not change legitimately: user agent is stable enough, IP is not (mobile networks roam). A mismatch means destroy the session, not just log it.
- Logging out means all three: clear `$_SESSION`, `session_destroy()`, and expire the cookie with `setcookie(session_name(), '', ['expires' => time() - 42000, …])`. Skipping the third leaves a cookie pointing at a dead ID, which combined with weak strict-mode settings is a fixation vector.
- On shared hosting, the default `save_path` is a directory every account can read. Set a private path, or use a database or Redis handler (`security.md`).

## Storage Handlers

- `files` — the default; simple, and the lock is a real filesystem lock. Does not work across multiple web servers unless the path is shared, and a shared NFS `save_path` has unreliable locking.
- `redis`/`memcached` — the standard multi-node choice. Memcached can EVICT a session under memory pressure, which logs users out at random; Redis with `maxmemory-policy noeviction` for the session database avoids it.
- Database — auditable and transactional, but every request now writes a row; use it when you need to enumerate or revoke sessions.
- Custom handlers implement `SessionHandlerInterface`. Implementing `validateId()` is what makes `use_strict_mode` work for your handler, and it is the method people forget.

## Data Inside the Session

- Store identifiers, not objects. A serialized object requires its class to be loadable on the next request, and a deploy that renames or moves the class produces `__PHP_Incomplete_Class` on every existing session (`oop.md`).
- Never store authorization decisions ("is_admin") without re-checking them; a role revoked in the database stays true in the session until it expires.
- Keys containing `|` break the default `php` serialize handler; `session.serialize_handler = php_serialize` handles them correctly. Numeric-only keys have similar problems — use plain identifier-shaped keys.
- Sessions are not a cache. Flash messages and a user id belong there; a 2 MB search result read on every request does not, because it is deserialized on every single request under a lock.

## Alternatives

- Signed stateless cookies (JWT or a signed payload) remove the lock and the shared store, at the cost of revocation: a token stays valid until it expires, whatever the database says. Short lifetimes plus a refresh token, or a revocation list — which reintroduces the shared store you were avoiding.
- The honest boundary: server-side sessions when you need instant revocation and server-controlled state; stateless tokens when you need many services to verify identity without a shared session store.

## Related

- Fixation, CSRF, and cookie flags in context: `security.md`
- Cookie mechanics and proxies: `http.md`
- Session ini directives and precedence: `php-ini.md`
