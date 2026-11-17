# Security — Injection, Escaping, Secrets, and Untrusted Input

Rule that orders everything below: validate on the way IN against an allowlist, escape on the way OUT for the specific context. Escaping at input is how you get double-escaped HTML in the database and an unescaped value in the email template.

## SQL Injection

- Bind every value; allowlist every identifier. Placeholders cannot substitute table names, column names, `ORDER BY` directions, or `LIMIT` on some drivers.

```php
$dir = ['asc' => 'ASC', 'desc' => 'DESC'][$input] ?? 'ASC';   // allowlist, not escaping
$sql = "SELECT * FROM invoices WHERE tenant_id = ? ORDER BY created_at {$dir}";
```

- `PDO::ATTR_EMULATE_PREPARES` is ON by default for MySQL: the driver interpolates values client-side using the CONNECTION charset. Combined with a DSN that omits `charset=utf8mb4`, this has been a real injection vector for multibyte charsets. Set emulation to `false` and put the charset in the DSN (`database.md`).
- `IN (?)` cannot bind a list — build the placeholders: `implode(',', array_fill(0, count($ids), '?'))`.
- `PDO::quote()` is a last resort, is driver-specific, and does not help with identifiers.
- ORM escape hatches (`whereRaw`, DQL string fragments) reopen the hole; anything raw takes bound parameters too.

## XSS — Escape Per Context

| Destination | Function |
|---|---|
| HTML body, quoted attribute | `htmlspecialchars($s, ENT_QUOTES \| ENT_SUBSTITUTE, 'UTF-8')` |
| Unquoted attribute | Do not. Quote the attribute, then use the row above |
| Inside `<script>` | `json_encode($v, JSON_HEX_TAG \| JSON_HEX_AMP \| JSON_HEX_APOS \| JSON_HEX_QUOT)` |
| URL path or query value | `rawurlencode($v)` |
| `href`/`src` value | Allowlist the scheme (`https`, `mailto`) before escaping — `javascript:` survives HTML escaping |
| CSS value | Do not interpolate user data into CSS; map to a class name |
| Shell argument | `escapeshellarg($v)` — and prefer `proc_open` with an argument array (`concurrency.md`) |
| HTML the user is allowed to write | A parser-based sanitizer with an allowlist; never a regex |

- `ENT_SUBSTITUTE` matters: without it, invalid UTF-8 makes `htmlspecialchars` return an EMPTY string, and the page silently loses content.
- On `php >=8.1` the default flags escape single quotes; on older versions the default did not, so any code relying on defaults must be audited when the floor is below 8.1.
- Templating engines that auto-escape (Twig, Blade) only cover the HTML context — `|raw` and JS blocks are still yours.
- Content-Security-Policy is the second layer, never the first.

## Passwords and Tokens

- `password_hash($p, PASSWORD_DEFAULT)` and `password_verify()`. Never a raw hash function, never a hand-rolled salt.
- Pin and measure the cost factor rather than trusting the default, which has been raised across 8.x releases: choose the highest `['cost' => N]` that keeps hashing near 100 ms on your production hardware, and re-measure after a hardware change.
- bcrypt silently truncates at 72 BYTES (not characters) and stops at a null byte. A passphrase policy above that length needs Argon2id (`PASSWORD_ARGON2ID`, available when compiled in) or a pre-hash step.
- `password_needs_rehash($hash, PASSWORD_DEFAULT, $opts)` on every successful login, then re-hash the plaintext you still hold — the only moment you can upgrade an algorithm.
- Tokens, session IDs, password-reset links, API keys: `random_bytes(32)` or `random_int()`. `uniqid()` is a formatted timestamp; `mt_rand()` and `shuffle()` come from a seeded PRNG. Both are predictable.
- Compare secrets with `hash_equals($known, $given)` — constant-time, and immune to the `"0e…" == "0e…"` collapse (`types.md`).
- Store reset tokens hashed, with an expiry and single use. A database leak otherwise hands over live account access.

## File Uploads

- `$_FILES['f']['type']` and the filename extension are both client-supplied. Determine the type with `finfo_file(finfo_open(FILEINFO_MIME_TYPE), $tmp)` and cross-check it against an allowlist of extensions you generate.
- Check `$_FILES['f']['error'] === UPLOAD_ERR_OK` first; `UPLOAD_ERR_INI_SIZE`, `UPLOAD_ERR_PARTIAL`, and `UPLOAD_ERR_NO_TMP_DIR` all arrive as a present-but-broken entry.
- If the POST body exceeds `post_max_size`, `$_POST` AND `$_FILES` are EMPTY with no error at all — detect it by an empty `$_POST` on a POST request with a non-zero `CONTENT_LENGTH` (`php-ini.md`).
- `move_uploaded_file()` (which verifies the file really came from an upload), never `copy`/`rename` on the temp path.
- Store outside the document root, with a generated name; serve through a script that sets `Content-Type` and `Content-Disposition`. An uploaded `.php` inside the webroot is remote code execution; so is `.phtml`, and so is a file the web server maps by a secondary extension (`avatar.php.jpg` under a misconfigured `AddHandler`).
- Images: re-encode rather than trust. Passing user files to an image library that shells out (older ImageMagick delegates) has its own history.

## Deserialization and Dynamic Code

- `unserialize()` on untrusted input instantiates arbitrary classes and triggers their `__wakeup`/`__destruct` — a POP chain to RCE with only the classes already in your vendor directory. Use `json_decode`. If you cannot, `unserialize($s, ['allowed_classes' => false])`.
- `include`/`require` with any user-controlled component is file inclusion; keep `allow_url_include = Off` and resolve through a fixed map of allowed names, never string concatenation.
- `eval`, `create_function` (removed), `preg_replace` with `/e` (removed), `assert()` on a string argument (removed) — none belong in application code.
- `extract($_POST)` and `$$variable` create attacker-named variables (`arrays.md`).
- `call_user_func($_GET['fn'])` is remote function invocation; dispatch through an explicit map.

## Paths and Files

```php
$base = realpath('/var/app/storage');
$path = realpath($base . '/' . $userPath);
if ($path === false || !str_starts_with($path, $base . DIRECTORY_SEPARATOR)) {
    throw new RuntimeException('path escapes storage root');
}
```

- The trailing separator in the prefix check is not optional: without it `/var/app/storage-public` passes.
- `basename()` is not containment — it strips directories but a symlink inside the directory still escapes.
- Reject null bytes and normalize before validating, never after (`strings.md`).

## HTTP-Layer Concerns

- CSRF: a per-session token in every state-changing form, compared with `hash_equals`. `SameSite=Lax` cookies block the simplest cross-site POST but not same-site subdomain attacks, and not GET-triggered state changes — which should not exist.
- Session fixation: `session_regenerate_id(true)` on login and on any privilege change; `session.use_strict_mode = 1` so an attacker-supplied session ID is never adopted (`sessions.md`).
- Open redirect: validate the target against an allowlist of paths or hosts; `parse_url` and check the host, do not `str_starts_with($url, '/')` alone (`//evil.com` is a protocol-relative absolute URL).
- SSRF: user-supplied URLs fetched server-side reach `169.254.169.254`, `localhost`, and the private ranges. Resolve the hostname, reject private and link-local addresses, disable `CURLOPT_FOLLOWLOCATION` or re-validate every hop (`http.md`).
- Header injection through `header()` is blocked for newlines by the engine, but a value reflected into a cookie, a redirect target, or an email header via `mail()`'s `$additional_params` is not.
- Mass assignment: build the entity from an explicit list of allowed fields, never from the whole request array.

## Configuration and Secrets

- Secrets in environment variables or a secret manager, never in a file under the document root. `.env` files must be outside the webroot or blocked by the server — a readable `.env` is the whole application.
- `expose_php = Off`, `display_errors = Off`, `log_errors = On` in production (`php-ini.md`).
- Composer supply chain: commit `composer.lock`, run `composer audit` in CI, and keep `allow-plugins` explicit — an install script runs with your developer's privileges (`composer.md`).
- `disable_functions` is a hardening layer, not a boundary; it is bypassable and it breaks legitimate tooling. Prefer running PHP as an unprivileged user with no write access to its own code directory.
- XML: modern libxml2 disables external entity loading by default, so XXE now mostly appears where code explicitly passes `LIBXML_NOENT`. Do not pass it.

## Red Flags in a Review

| Signal | Action |
|---|---|
| String interpolation inside an SQL string | Stop; bind the value before anything else in the review |
| `unserialize(` on request data | Treat as RCE until proven otherwise |
| `md5`/`sha1` next to `password` | Migrate to `password_hash` with a login-time rehash |
| `==` next to `token`, `hash`, `signature` | Replace with `hash_equals` |
| `@` before a filesystem or network call | Ask what failure it is hiding |
| `EMULATE_PREPARES` unset, DSN without `charset` | Fix both together |
| Any user value reaching `include`, `eval`, `exec`, `system` | Redesign the dispatch |

## Related

- Driver-level settings and transaction safety: `database.md`
- Session hardening in full: `sessions.md`
- Uploads, downloads, and outbound requests: `http.md`
