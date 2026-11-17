# Errors, retries, and limits

## Error envelope

Branch on the stable `code`, never the mutable `message`. Validation failures may include `fields[]` with a path, code, and message.

- `400`: fix malformed input; do not retry unchanged.
- `401`: authenticate again or replace an expired/revoked credential.
- `403`: inspect `code`; check credential type, OAuth/PAT scopes, account role, payment readiness, and partner eligibility.
- `404`: verify the operation/path and caller access.
- `409`: re-read state and resolve the conflict.
- `422`: correct semantic validation using `fields[]`.
- `429`: honor server timing headers; do not retry immediately.
- `5xx`: retry only if the operation is idempotent or state proves it did not commit.

## Idempotency

- GET reads are safe to retry.
- PUT replacement is generally idempotent by shape.
- DELETE is generally safe to repeat when deleting an already-absent resource is a no-op.
- PATCH/add can append duplicates; read state before any retry.
- Registration, renewal, transfer, bids, payment, certificate order, and other billed POSTs must never be blindly retried.
- Domains v3 registration uses an idempotency key internally through `gddy`. Reuse the same logical attempt; poll the returned operation rather than starting a new purchase.

If a write times out after sending, assume the result is unknown. Inspect the resource, operation, account, or transaction before deciding whether another call is safe.

## Rate limits

Do not hardcode the older `60 requests/minute` value. GoDaddy documents rate limits as changeable and returns these headers:

- `RateLimit-Limit`
- `RateLimit-Remaining`
- `RateLimit-Reset`
- `Retry-After` on applicable rejections

Use `gddy api call ... --include` when rate information matters. On `429`, wait for the server-provided interval and add jitter for programmatic retries. Prefer bulk endpoints and sequential cursor pagination over parallel request bursts.

Current documentation: <https://developer.godaddy.com/en/docs/api-users/rate-limits>
