# Security Model

## Authentication
- OAuth2 Client Credentials
- JWT algorithm: RS256
- token TTL: 3600 seconds
- scopes: `bridge:read`, `bridge:write`

## Request signing
String to sign:
`METHOD + "\n" + URI + "\n" + TIMESTAMP + "\n" + REQUEST_ID + "\n" + BODY_SHA256`

Exact sample values:
- method: `POST`
- uri: `/v1/jobs/products/update`
- timestamp: `1710950400`
- request id: `f47ac10b-58cc-4372-a567-0e02b2c3d479`
- body sha256: `37abd647733fbd18a3f11fb5a082fe59c62719d9fe833aec96b28ccea36b70ba`
- signature: `448e251d1c71078b07a10baf4094fd2686bcebef97761c4729a921f71798554c`

## Timestamp window
Requests outside ±30 seconds are rejected.

## Network isolation
Only approved source IPs may reach the Bridge in MVP.
