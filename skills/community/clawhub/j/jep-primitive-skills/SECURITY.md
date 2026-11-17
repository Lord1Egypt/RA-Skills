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

## Primitive behavior

The four endpoints construct unsigned draft events only. `success` means draft construction succeeded. Responses explicitly include `draft=true` and `signature_valid=false`. They do not delegate real authority, stop a process or independently verify evidence. The caller's issuer must be assigned to its authenticated identity, and each operation needs the matching `draft:*` permission.

Prefilled signatures are rejected because timestamp/nonce construction would invalidate them. To sign an audit/consensus event, construct the complete input dataclass for that service, then use `sign_event` from that service's security profile. Do not copy a draft projection's signature or claim it is a verified event. The adapter copies extensions and does not invent an orphan-fault exception for termination.
