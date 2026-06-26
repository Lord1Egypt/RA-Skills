# Redaction Rules

Apply these rules before persisting any text to `{baseDir}/data` or `{baseDir}/reports`.

## Process

1. Redact first, save second.
2. Run replacements globally and case-insensitively when appropriate.
3. Preserve surrounding structure and meaning when possible.
4. If a value looks sensitive but does not match a known pattern, replace it with `[REDACTED_SUSPECTED_SECRET]`.

## Secret Patterns

- OpenAI-style API keys: `\bsk-[A-Za-z0-9]{16,}\b` -> `[REDACTED_API_KEY]`
- Bearer tokens: `(?i)\bBearer\s+[A-Za-z0-9._\-+/=]+\b` -> `Bearer [REDACTED_TOKEN]`
- JWTs: `\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9._-]+\.[A-Za-z0-9._-]+\b` -> `[REDACTED_JWT]`
- AWS access key IDs: `\bAKIA[0-9A-Z]{16}\b` -> `[REDACTED_AWS_ACCESS_KEY]`
- GitHub tokens: `\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b` -> `[REDACTED_GITHUB_TOKEN]`
- Slack tokens: `\bxox[baprs]-[A-Za-z0-9-]{10,}\b` -> `[REDACTED_SLACK_TOKEN]`
- Private key blocks: `-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----` -> `[REDACTED_PRIVATE_KEY_BLOCK]`
- Password-style assignments: `(?i)\b(password|passwd|pwd|secret)\s*[:=]\s*([^\s,;]+)` -> `$1=[REDACTED_SECRET]`
- Basic-auth URL credentials: `https?:\/\/[^\/\s:@]+:[^\/\s@]+@` -> `https://[REDACTED_CREDENTIALS]@`

## PII Minimization

- Replace emails with `[REDACTED_EMAIL]`.
- Replace phone numbers with `[REDACTED_PHONE]`.
- Replace personal home-directory fragments when not needed for evidence.

## Capture-Level Constraints

- `minimal`: store no raw message text.
- `snippets`: store one redacted excerpt per record, maximum 200 characters.
- `full`: store only redacted full text.

Never keep an unredacted copy in temporary or output files.
