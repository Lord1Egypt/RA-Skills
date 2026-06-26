# Security Baseline (OWASP / MASVS aligned)

Every bundle's `## Security` section must address the items below for its mode. The verify-lite scanner requires ≥ 3 concrete items; `quality:score` rewards 5+.

## Cross-platform invariants

1. **No plaintext secrets in the repo.** Tokens, API keys, signing keys live in env vars or OS keychain. The scanner rejects any of: `sk_live_*`, `ghp_*`, `AKIA*`, `xox[bapr]-*`, `AIza[0-9A-Za-z_-]{35}`, `BEGIN PRIVATE KEY`.
2. **No dynamic execution of remote strings.** No `eval`, no `new Function`, no `child_process.exec(userInput)`.
3. **Input validation at every system boundary.** Use `zod` / `pydantic` / Swift `Codable` / Kotlin `@Serializable` / ArkTS interfaces — never trust shape.
4. **Least privilege.** Permissions / entitlements / `allowlist` declared explicitly; no `dangerous` flags.
5. **HTTPS-only.** Bare `http://` rejected outside `localhost`.

## OWASP Top 10 mapping (server-side modes: A-10)

| Item | What we require |
|---|---|
| A01 Broken Access Control | Server-side role check on every action; deny-by-default |
| A02 Crypto Failures | bcrypt/scrypt/argon2 for passwords; `crypto.randomUUID()` for tokens; TLS via reverse proxy |
| A03 Injection | Parameterized queries only (Drizzle/Prisma); no string-concat SQL |
| A04 Insecure Design | Threat model documented in `S3` (data classification, attacker model) |
| A05 Misconfig | CSP, HSTS, X-Frame-Options DENY, SameSite=Lax cookies |
| A06 Vulnerable Components | Lockfile committed; CI runs `npm audit --omit=dev` |
| A07 Auth Failures | Rate-limit auth endpoints; session rotation on login; logout invalidates server-side |
| A08 Integrity | Subresource Integrity on CDN imports (if any); signed releases |
| A09 Logging | Structured JSON to stdout; never log secrets |
| A10 SSRF | Outbound URL allowlist; no fetch on user-supplied URLs without check |

## OWASP MASVS mapping (mobile modes: A-04, A-05, A-06, A-07, A-08)

| Control | Implementation |
|---|---|
| MSTG-STORAGE-1 | Secrets in Keychain / Keystore / `EncryptedSharedPreferences` / `flutter_secure_storage` / `expo-secure-store` — never `UserDefaults` / `SharedPreferences` / `AsyncStorage` |
| MSTG-CRYPTO-1 | Platform crypto only (`CryptoKit`, `javax.crypto`, `crypto`) — never custom |
| MSTG-NETWORK-1 | ATS / `network_security_config.xml` strict; no cleartext |
| MSTG-PLATFORM-2 | `WebView` disallows JS bridge with remote content unless absolutely necessary |
| MSTG-CODE-9 | Release builds: minify + obfuscate + R8 / ProGuard / Flutter `--obfuscate` |

## Desktop-specific (A-01, A-02, A-03)

- **Sandbox**: App Sandbox on macOS, MSIX capability declaration on Windows, Tauri allowlist scoped per-feature.
- **Path traversal**: every user-supplied path validated against `canonicalize` + an allowlist root before read/write.
- **Auto-update**: signed updates only; Tauri's built-in updater requires public-key verification.

## CLI-specific (A-12)

- **Argument validation**: every flag through `zod` / `pydantic`.
- **No shell=True**: subprocess invocations use array form, never string form with user input.
- **Quit fast on SIGINT**: don't leave half-written files; use `try/finally`.

## What the scanner enforces

| Pattern | Action |
|---|---|
| Plaintext API keys (regex matches above) | **Reject** the bundle |
| `eval(`, `new Function(`, `exec(...userInput`) | **Reject** the bundle |
| `## Security` section missing | **Reject** the bundle |
| `## Security` section with < 3 items | **Reject** in normal mode, warn in `--template` mode |

The scanner does **not** statically prove the described app is secure — that's the calling agent's job at Tier 1. The scanner only proves the bundle's contract is in place.
