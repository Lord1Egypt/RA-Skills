# Security Rules (CodeGuard Integration)

Security rules are statically copied from the `cisco/software-security` tile (CodeGuard framework v1.2.5). These rules are baked into NextSteps at publish time — no runtime dependency.

**Update policy**: When `cisco/software-security` releases a new version, re-publish the NextSteps tile to incorporate updated rules. The `^1.2.0` dependency in tile.json allows compatible updates.

## Rule 1 — No Hardcoded Credentials

**NEVER** generate a next step that includes or encourages hardcoded credentials.

- Violation: "Add your API key `sk-abc123` to the config file"
- Correct: "Set up environment variable for your API key"

Applies to: passwords, API keys, tokens, secrets, private keys, connection strings.

Detection: If a suggestion contains a string matching common secret patterns (`sk-`, `ghp_`, `xox-`, `AKIA`, `-----BEGIN`, `password=`, `secret=`), discard and regenerate.

## Rule 2 — Secure Crypto Recommendations

When suggesting cryptography-related next steps, only recommend current algorithms.

- **Allowed**: AES-256, SHA-256/384/512, RSA-2048+, Ed25519, ChaCha20-Poly1305, Argon2
- **Disallowed**: MD5, SHA-1, DES, 3DES, RC4, RSA-1024, ECB mode

Violation: "Add MD5 hash verification for uploads"
Correct: "Add SHA-256 hash verification for uploads"

## Rule 3 — Safe File Operations

When suggesting file operations, never recommend:
- Writing to system directories without confirmation
- Recursive deletion without safeguards
- File permissions that are world-writable (e.g., `chmod 777`)

Reframe as safe alternatives:
- "Clean up build artifacts with `rm -rf dist/`" → "Clean up build artifacts (review contents of `dist/` first)"
- "Set permissions to 777" → "Set appropriate file permissions (consider 644 for files, 755 for directories)"

## Rule 4 — Dependency Security

When suggesting dependency-related next steps:
- Prefer: "Run `npm audit` to check for vulnerabilities" over "Install [package] to fix it"
- Never suggest pinning to a known-vulnerable version
- Include security review as a step when suggesting new dependencies: "Add X dependency (check its security advisories first)"

## Rule 5 — .gitignore Enforcement

On every activation, if `.nextsteps/` directory exists and is NOT in `.gitignore`:
- Include as a high-priority suggestion: "Add `.nextsteps/` to .gitignore — personal preference data shouldn't be committed"
- Category: ✅ Quick Win
- This overrides normal slot allocation — it takes a guaranteed slot until resolved

Additional .gitignore checks:
- If `.env` files detected and not in .gitignore → suggest adding
- If `node_modules/` exists and not in .gitignore → suggest adding
- If common secret files detected (*.pem, *.key) and not in .gitignore → suggest adding

## Rule 6 — No Suggestion Should Bypass Security

Self-review gate: before presenting any suggestion, verify it does not:
1. Encourage disabling security features (e.g., "disable CORS", "set --no-verify")
2. Suggest running untrusted code without sandboxing
3. Recommend storing sensitive data in plaintext
4. Propose network operations without TLS
5. Encourage ignoring security warnings or audit results

If a generated suggestion fails this check:
- Discard and regenerate
- If all 3 regeneration attempts fail, replace with a security-related Quick Win from the project context

## Implementation Notes

- These rules are applied during the **self-review gate** (Step 5 of the generation pipeline in SKILL.md)
- Security violations are a hard fail — the suggestion is discarded, not softened
- Maximum 3 regeneration attempts per suggestion before falling back to a safe alternative
- Security rules take precedence over all other generation rules (including user customization)
- Users CANNOT disable security rules through customization — they are not configurable
