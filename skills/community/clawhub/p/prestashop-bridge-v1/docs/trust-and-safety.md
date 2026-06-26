# Trust and Safety

## Hard guarantees
- JWT RS256 only
- HMAC-SHA256 on every protected request
- strict timestamp window of ±30 seconds
- strict JSON schema validation
- MySQL-backed job truth
- double-layer idempotency

## Explicit non-goals
- no direct filesystem control
- no direct database control
- no synchronous heavy writes
- no exactly-once promise at transport level

## Operational safety rules
- `202 Accepted` is never a business success signal
- retries must preserve the same `X-Request-ID`
- rate limiting applies before expensive downstream work
- failed jobs are retained in MySQL DLQ for 90 days
