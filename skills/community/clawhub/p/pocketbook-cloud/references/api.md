# PocketBook Cloud API notes

This skill is unofficial and not affiliated with PocketBook International SA. Consumer Cloud endpoints can change without notice.

Current interoperability behavior used by the helper:

- Provider discovery: `GET /api/v1.0/auth/login`
- Password login: `POST /api/v1.0/auth/login/{provider}`
- Token refresh: `POST /api/v1.0/auth/renew-token`
- Account check: `GET /api/v1.0/user`
- Library: `GET /api/v1.0/books` with `limit` / `offset`
- Upload: `PUT /api/v1.1/files/{filename}`
- Delete: `POST /api/v1.1/fileops/delete/?fast_hash=...`
- Note index: `GET /api/v1.0/notes?fast_hash=...`
- Note detail: `GET /api/v1.0/notes/{uuid}?fast_hash=...`
- Downloads use the per-book `link` returned by the library response. The helper deliberately does not attach PocketBook Authorization to that URL.

`fast_hash` is the stable cloud-side book identifier used for notes and file operations. User-facing resolution also considers book id, title, author, filename, ISBN, and format.

The PocketBook browser client credentials embedded by the helper are public browser-client interoperability values, not user credentials. User passwords and account tokens must never be committed or logged.

## Compatibility boundary

Endpoint-specific parsing lives in `scripts/pocketbook_lib/api.py`. Required response shapes fail closed when critical fields disappear or change type; unknown additional fields are tolerated. Sanitized examples used by credential-free contract tests live under `tests/fixtures/`.

API response bodies are bounded before JSON parsing. Ambient proxy environment variables are disabled for authenticated API requests. Download URLs are treated as untrusted input and use a separate pinned HTTPS transport that validates public addresses and TLS hostname identity on every redirect hop.
