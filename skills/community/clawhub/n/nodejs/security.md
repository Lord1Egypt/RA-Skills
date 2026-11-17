# Security — Untrusted Input, Secrets, and Supply Chain

## Untrusted Input Reaching a Dangerous Sink

| Sink | Exact defense |
|---|---|
| Shell (`exec`) | `execFile(bin, [args])` — array arguments never touch a shell; with `spawn`, keep `shell: false` (the default). Quoting user input for a shell is the losing move |
| Filesystem path | `const p = path.resolve(root, userInput); if (p !== root && !p.startsWith(root + path.sep)) reject` — a prefix check without the separator lets `/data-evil` pass a `/data` guard |
| Object keys in a merge | Block `__proto__`, `constructor`, and `prototype`, or keep user-keyed data in a `Map`/`Object.create(null)`. `JSON.parse` itself is safe — the recursive merge afterwards is not |
| Regex | Bound input length and avoid nested quantifiers; `(a+)+` on a crafted string backtracks exponentially and blocks the whole process (ReDoS) |
| `eval` / `new Function` | No safe form on user-reachable strings. Parse data, do not execute it |
| Outbound URL (SSRF) | Resolve the hostname, reject private and link-local ranges — including the cloud metadata address 169.254.169.254 — and disable redirects, or re-check after each hop |
| Deserialization | Never revive arbitrary types from user JSON; validate against a schema and construct your own objects |
| Anything else | Validate at the boundary against an allowlist, then pass typed values inward — validation deep in the call stack is validation that some caller skipped |

- Path traversal has a second door: symlinks. After resolving, `realpath` the result and repeat the containment check when the tree is user-writable (→ `filesystem.md`).
- Null bytes and Unicode normalization defeat naive filename filters; reject unexpected characters rather than stripping them, since stripping can produce a new valid path.
- `node:vm` is NOT a sandbox — its own documentation says so. Isolate untrusted code at the process or container level, with its own user, memory limit, and timeout (→ `concurrency.md`).

## Secrets

- Never in argv: `ps` shows arguments to every user on the box, and process listings end up in crash reports and support tickets.
- Environment variables are readable by anything that can inspect the process and are frequently dumped by error reporters; mounted files with restrictive permissions are strictly better where the platform allows it.
- Redact at the logger with a field list, not at each call site: `authorization`, `cookie`, `set-cookie`, `password`, `token`, `secret`, and whole request bodies on auth routes (→ `production.md`).
- Never log an entire config object or `process.env`, including in a "temporary" debug line — those are the lines that survive into production.
- Compare secrets in constant time (`crypto.timingSafeEqual` on equal-length buffers); `===` on a token leaks length and prefix through timing.
- Rotate on the assumption of eventual exposure: a secret that cannot be rotated without a deploy will not be rotated.

## Crypto Basics That Get Wrong

- Passwords: a memory-hard KDF (`crypto.scrypt`, or argon2/bcrypt from userland), never a bare hash. Node's `scrypt` is available in core and async — the sync variant blocks the loop (SKILL.md rule 1), and heavy KDF work competes for the 4 libuv threads (rule 3).
- Randomness: `crypto.randomBytes`/`crypto.randomUUID` for anything security-relevant. `Math.random()` is predictable and has produced real token-guessing vulnerabilities.
- Do not invent encryption schemes: use an authenticated mode (AES-GCM), never reuse a nonce with the same key, and store the algorithm and version alongside the ciphertext so rotation is possible later.
- Verify signatures and JWTs with an explicit algorithm allowlist — accepting the token's own `alg` header is how `none` and key-confusion attacks work.

## Process and Platform Hardening

- Run as a non-root numeric UID with a read-only filesystem where possible; a Node service that must write usually needs one tmpfs path, not a writable root (→ `production.md`).
- Set a memory limit and a heap ceiling (SKILL.md rule 8): an unbounded process is a denial-of-service target using nothing but a large request body.
- Cap request bodies, upload sizes, and JSON depth at the edge; deeply nested JSON is a parser CPU attack even when small (→ `http.md`).
- Rate-limit by an identity you actually trust — behind a proxy, `X-Forwarded-For` is client-controlled unless you trust only known proxy IPs and read the right position.
- The permission model (`--permission`, experimental as of Node 24) restricts filesystem, child-process, and worker access from the runtime side: useful defense in depth, not a substitute for process isolation (→ `runtime.md`).

## Supply Chain

- Risk concentrates in install scripts and transitive dependencies: `npm ci --ignore-scripts` where the build allows it, and pin a vulnerable transitive dep with `overrides` rather than waiting for upstream (→ `packages.md`).
- Lockfiles must be committed and reviewed; an unexplained lockfile change is the cheapest place to catch a dependency swap.
- Prefer fewer dependencies over audited ones: every package is an install-time code execution and a maintainer account that can be phished.
- Scan at two points — CI (blocks bad builds) and the registry or runtime inventory (catches advisories published after the build). CI-only scanning approves artifacts that rot in place.
- Enable 2FA and provenance on publish; a package with a single unprotected write token is one phishing email from an incident.

## Error Surface

- Return generic messages plus a correlation id to clients; the stack, the query, and the driver error stay in the logs (→ `errors.md`).
- Distinguish "not found" from "not allowed" only when the distinction is not itself a leak — for private resources, both should look the same to an unauthorized caller.
- Turn off framework debug pages and verbose errors in production by setting `NODE_ENV=production` explicitly; a missing value quietly leaves development behavior enabled.
