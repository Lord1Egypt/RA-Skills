# Security — Untrusted Input, Secrets, Crypto, and Dependencies

Go's standard library gets several security defaults right (contextual HTML escaping, TLS 1.2 minimum for clients, memory safety) and leaves the rest to you. These are the decisions that matter, in the order they get exploited.

## Randomness and Secrets

- `crypto/rand` for anything an attacker must not predict: tokens, session IDs, password reset links, nonces, salts. `math/rand` is deterministic from its seed and its output stream is reconstructible from a few samples — auto-seeding (`go >=1.20`) and `math/rand/v2` (`go >=1.22`) make it *unpredictable to you*, not to an attacker.
- Token generation: `b := make([]byte, 32); rand.Read(b)` with `crypto/rand`, then `base64.RawURLEncoding.EncodeToString(b)`. 32 bytes is the standard size for a session or API token.
- Compare secrets with `subtle.ConstantTimeCompare(a, b) == 1`. `==` on strings short-circuits at the first differing byte, which leaks the prefix length through timing.
- Passwords: a memory-hard KDF (`golang.org/x/crypto/argon2` or `bcrypt`), never SHA-256, never with a global salt. Store the parameters alongside the hash so they can be raised later.
- Secrets come from the environment or a mounted file, never from a command-line argument (visible in the process list) and never from a source constant. `git`-committed keys survive rotation because history is forever.
- Go cannot reliably zero a secret in memory: the GC may have copied the string already, and strings are immutable. Use `[]byte` and clear it when it matters, and accept this as a limit rather than a solved problem.

## Injection

| Surface | Wrong | Right |
|---|---|---|
| SQL | `fmt.Sprintf("... WHERE id = %s", id)` | Placeholders (`database.md`); identifiers validated against an allowlist |
| Shell | `exec.Command("sh", "-c", userInput)` | `exec.Command("git", "checkout", ref)` — an argument slice, no shell (`cli.md`) |
| HTML | `text/template` | `html/template`, which escapes per context (HTML, attribute, JS, URL, CSS) |
| Paths | `filepath.Join(root, userPath)` | Containment check below, or `os.Root` (`go >=1.24`) |
| URLs | String concatenation of user input | `url.URL` + `url.Values.Encode()` |
| Log lines | Raw user input into a log message | Structured attributes, which quote values (`logging.md`) |

- `html/template` escapes based on where the value lands in the parsed document — that context awareness is the whole point, and it is lost the moment you wrap a value in `template.HTML`, which means "trusted, do not escape". Every `template.HTML` on user data is an XSS.
- `filepath.Join` **cleans** the path, resolving `..` — so `Join("/data", "../etc/passwd")` yields `/etc/passwd` with no error. Containment requires an explicit check:

```go
p := filepath.Join(root, name)
if !strings.HasPrefix(p, filepath.Clean(root)+string(os.PathSeparator)) {
    return errors.New("path escapes root")
}
```

That still does not stop a symlink inside `root` pointing out of it. `os.Root` (`go >=1.24`) resolves every operation within the root and is the real answer where available.

## Untrusted Input Limits

- Bound every body before parsing: `r.Body = http.MaxBytesReader(w, r.Body, 1<<20)`. Without it, `io.ReadAll` or `json.Unmarshal` will happily allocate whatever the client sends (`http.md`, `json.md`).
- Bound decompression too: a 1 KB gzip payload can expand to gigabytes. Wrap the decompressed reader in `io.LimitReader`.
- Archive extraction (`archive/zip`, `archive/tar`) is the classic path-traversal sink — entry names can contain `..` and absolute paths. Validate every entry name against the destination root before creating anything, and cap the total extracted size and file count.
- Deeply nested JSON or XML can exhaust the stack. Size limits handle most of it; a depth limit handles the rest.
- Regexp is safe from catastrophic backtracking (RE2 is linear-time), but a huge input against a complex pattern is still linear in a large number — bound the input (`strings.md`).
- Integer conversion: `int32(userSuppliedInt64)` truncates silently. Validate the range before converting, especially for sizes and offsets.

## TLS

- Defaults are sane: modern cipher suites, and a `MinVersion` of TLS 1.2 for clients — and, from `go >=1.22`, for servers too (before that, a zero-value server config accepted TLS 1.0/1.1; the `tls10server=1` GODEBUG still reverts it). Set `MinVersion: tls.VersionTLS12` (or `tls.VersionTLS13`) explicitly anyway: it is the only form that survives an older toolchain, a GODEBUG set elsewhere in the environment, and a config copied into a `go <1.22` module.
- `InsecureSkipVerify: true` disables certificate verification entirely — it is not "skip the hostname check", it accepts any certificate from anyone. For a private CA, load it into a `RootCAs` pool instead.
- Custom `RootCAs`: `x509.SystemCertPool()` then `AppendCertsFromPEM` — starting from an empty pool silently drops every public CA.
- mTLS: `ClientAuth: tls.RequireAndVerifyClientCert` plus a `ClientCAs` pool. `RequireAnyClientCert` accepts unverified certificates and is almost never what was meant.
- Certificate expiry is an outage with a date on it. Alert on remaining validity, do not discover it from a pager.

## HTTP Hardening

- Server timeouts are the DoS defense, and all of them default to unlimited — `ReadHeaderTimeout` above all (`http.md`).
- Security headers on HTML responses: `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Strict-Transport-Security` on HTTPS. Set them in one middleware so no route can forget.
- CORS: an explicit origin allowlist. Reflecting the request's `Origin` header with `Access-Control-Allow-Credentials: true` grants every site authenticated access to your API.
- Cookies: `HttpOnly`, `Secure`, `SameSite=Lax` or `Strict`, and a scoped `Path`. The zero-value `http.Cookie` has none of them.
- Never expose `net/http/pprof` publicly — importing it registers on `http.DefaultServeMux`, so serving that mux publishes heap dumps and command-line arguments (`debugging.md`).
- Errors returned to clients say what to do; stack traces, SQL text, and internal hostnames go to the log, not the response body.

## Dependencies and Supply Chain

- `govulncheck ./...` (golang.org/x/vuln) reports vulnerabilities that your code **actually reaches** in the call graph, which is why its output is short enough to act on where a plain dependency scan is not. Run it in CI.
- `go.sum` plus the checksum database verifies module content. A `checksum mismatch` is either a retagged release or tampering — investigate, never bypass with `GOFLAGS=-mod=mod` or `GONOSUMDB` (`modules.md`).
- `GOPRIVATE` for internal paths, so private module names never leak to the public proxy and checksum database as lookups.
- Pin the toolchain and dependencies in CI; a build that silently upgrades is a build that can silently be compromised.
- Every dependency ships in your binary. The stdlib covers HTTP, TLS, JSON, SQL, templating, and crypto — an added module for any of those is a supply-chain surface accepted in exchange for convenience.

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| `math/rand` for tokens | Predictable session IDs | `crypto/rand` |
| `==` on a secret or MAC | Timing oracle | `subtle.ConstantTimeCompare` |
| `text/template` for HTML | XSS on every user field | `html/template` |
| `template.HTML(userInput)` | Escaping deliberately disabled | Never on untrusted data |
| `filepath.Join(root, userPath)` alone | Path traversal | Prefix check, or `os.Root` |
| `InsecureSkipVerify: true` to fix a cert error | Accepts any certificate from anyone | Add the CA to `RootCAs` |
| Unbounded `io.ReadAll` on a request body | Memory exhaustion from one client | `MaxBytesReader` + `LimitReader` |
| Secrets in `ENV` layers of an image | Readable by anyone who can pull it | Mounted secret files |
| `%+v` on a struct with credentials into a log | Secret in the log store | `LogValue()` redaction (`logging.md`) |

## Back To SKILL.md

Input bounds at the HTTP layer: `http.md`. Placeholders and identifiers: `database.md`. Dependency verification: `modules.md`.
