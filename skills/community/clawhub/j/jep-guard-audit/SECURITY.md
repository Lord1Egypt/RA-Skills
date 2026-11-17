# Security profile v1 — migration required

This release changes authentication and validation. It is a locally tested repair candidate, not an independently certified protocol implementation. Do not treat older dummy signatures as valid data.

## HTTP services

Run on loopback: `uvicorn skill.api:app --host 127.0.0.1 --port 8000 --limit-concurrency 16 --timeout-keep-alive 5`.
For remote use, terminate TLS and enforce request-rate/read-time limits at a trusted reverse proxy. The service bounds request bodies to 256 KiB and JSON nesting to 20. It does not supply an internet-facing rate limiter.

`JEP_CLIENTS` is an operator-controlled JSON object mapping SHA-256 hexadecimal bearer-token digests to `{ "tenant": "team-a", "issuers": ["agent-a"], "permissions": [...] }`. Generate tokens from at least 32 random bytes. Send the original token in `Authorization: Bearer ...`. Do not store tokens in source or send them to a third party. Missing authentication configuration returns 503; unauthenticated callers cannot operate the API. Keep environment configuration accessible only to the service account.

Permissions are explicit: `audit:write`, `audit:read`, `audit:export`, `consensus`, `check`, and `draft:judge`, `draft:delegate`, `draft:terminate`, `draft:verify`. Grant only the permissions required for that service. The audit service partitions data by the authenticated tenant, not a client-supplied tenant identifier.

## Signed events

`JEP_TRUSTED_KEYS` maps approved issuer IDs to objects mapping key IDs to base64url-encoded raw 32-byte Ed25519 public keys. Keys are configured out of band; headers cannot supply new trusted keys. Rotate/revoke keys through operator configuration. Revoking a key will cause existing audit records signed by that key to fail current verification.

The compact JWS protected header is exactly `{"alg":"EdDSA","typ":"JEP+JWS","kid":"key-id"}`. Payload bytes are RFC 8785 JCS of `{"context": context, "event": complete_event_without_signature}`. Include all dataclass fields, including null fields. Sign the full event after timestamp, ID and payload are final. `skill.security.sign_event` and `verify_event` implement this profile. The context is `{"purpose":"audit" or "consensus", "tenant":"team-a", "session":"round-id"}`. A signature is rejected in a different session, purpose or tenant. Private keys stay with the issuer.

This profile uses a signed FriendlyEvent envelope for audit and a signed COEEvent envelope for consensus. The mapped JEP-looking structure is a projection; its sig is not a JWS over the projection. Do not claim general JEP-04/JAC-01 wire interoperability. `JEPCodec.encode` serializes the complete projection, including its signature; it is not the unsigned signing input. Use the security helpers instead.

Signed statements establish issuer provenance, not the truth of the statement or legal compliance. Services store or compute evidence; they do not execute the events' described actions.

## Installation and validation

Use Python 3.12 and `pip install --require-hashes -r requirements.txt`. Exact transitive versions and package hashes are included. Package names are standard registry dependencies; Uvicorn is distinct from Gunicorn and is not renamed to suppress an automated similarity warning.

Run this package's tests with `python -m pytest tests`. In the combined repair repository, also run `python -m pytest tests` at the repository root after installing pytest and httpx. Test-only signing keys are generated in memory; no private keys or tokens are shipped.

## Audit behavior

SQLite stores signed input, the ingestion digest and replay identifiers in a private directory. Default path: `~/.jep-audit/events.sqlite3`; override with `JEP_AUDIT_DB`. The directory must be mode 0700 and file mode 0600. Back up the database securely. No remote persistence or automatic deletion occurs. Capacity limits are 128 events per batch and 1,000 per session. Operator-configured tenant reservations additionally bound each tenant across all sessions by event count and stored UTF-8 body bytes. The sum of all reservations cannot exceed 100,000 events or 256 MiB of event bodies. A full tenant cannot borrow another tenant's reservation. Quota checks and batch writes are one SQLite transaction; rejected batches consume no capacity. No records or replay identifiers are automatically deleted.

IDs must be canonical UUIDv4. Timestamps must include a timezone and arrive within ±300 seconds. Batches are atomic. Reading a chain is deterministic; historical timestamps are not reclassified as expired. References resolve to earlier records, parent hashes use `sha256:` plus the complete projected event digest. Client fault extensions cannot waive missing parents. Empty sessions are not valid chains. R001 checks subsequent signed verification; warnings do not establish action success.

## Tenant storage reservations (2.0.1)

Set `JEP_AUDIT_TENANT_QUOTAS` before starting the service. It is an operator-controlled JSON object, not an HTTP request field. For example:

```json
{
  "team-a": {"max_events": 10000, "max_bytes": 16777216},
  "team-b": {"max_events": 10000, "max_bytes": 16777216}
}
```

Use exactly the tenant names assigned in `JEP_CLIENTS`. All credentials for one tenant share that tenant's reservation, including writes to new session IDs. Unknown tenants cannot ingest. Read/export permissions continue to be enforced separately. Each budget must be a positive integer; at most 128 tenants can be configured. Combined event budgets must be at most 100,000 and combined body-byte budgets at most 268,435,456. Without this variable, only `local` is reserved, with 10,000 events and 16 MiB. Python callers may supply the same operator policy through `AuditEngine(..., tenant_quotas=...)`.

The complete policy is stored in SQLite. Every writer must use exactly that policy; workers with conflicting settings fail at startup and policy changes detected during ingestion stop writes. Changing a policy requires an operator-reviewed offline migration with all writers stopped. There is no request endpoint or automatic expansion of budgets. A quota rejection returns HTTP 429. A tenant without a reservation is rejected without allocating storage. Existing reads and exports remain available when a tenant is full.

### Upgrade from 2.0.0

Stop **all** 2.0.0 processes first: old writers do not enforce these reservations and must not share the database with 2.0.1. Make a private backup that retains every event, nonce and ingestion digest. Choose reservations for every tenant already present in the database and every tenant allowed to write. On first startup, 2.0.1 verifies existing row counts and UTF-8 body sizes against these budgets before recording the policy. Over-quota or unconfigured historical tenants cause startup to fail without deleting their records. Do not delete history or reset the database to bypass the check; use a reviewed migration that retains replay-protection evidence.

These reservations isolate retained audit data, not CPU, I/O bandwidth or total disk consumption. The byte budget counts stored event bodies, including signatures; SQLite pages, indexes, journals, backups and other programs use additional space. Provision filesystem headroom/quotas and operator monitoring separately. Enforce per-tenant request rates and timeouts at a trusted gateway for shared deployments. No automatic archival, eviction or replay-history pruning is supplied.

A same-issuer prior judgment is required for delegation/termination authority in this profile. Signed verification statements do not prove an external execution happened. Export labels are legacy categories, not statutory certification or prescribed retention periods. Raw exports are redacted technical summaries and need `audit:export`. External anchoring is required to detect database deletion, rollback or truncation by the host owner.
