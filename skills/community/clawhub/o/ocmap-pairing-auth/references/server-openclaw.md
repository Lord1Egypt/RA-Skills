# Server Implementation: OpenClaw

Implement the pairing system as an extension of existing OpenClaw device pairing and device token logic.

## Principle

Do not build a second auth backend. Pairing-code exchange should end by creating or rotating the same trusted device token model OpenClaw already uses.

## Existing primitives to reuse

Look for or reuse helpers around:

- device identity derivation from public key
- device signature verification
- existing trusted paired-device storage
- existing device token issuance / rotation / revocation
- gateway method scope enforcement
- Control UI device/pairing panels

## Recommended files / areas

Typical OpenClaw touchpoints:

- gateway protocol schemas
- gateway method registration list
- gateway method scopes
- server method handlers for devices/pairing
- infra storage for pairing codes
- Control UI devices controller + view + navigation

## Server responsibilities

### 1. Pairing-code storage

Store code records separately from normal device pending requests.

Track at least:

- `pairingId`
- `code`
- `nonce`
- `createdAt`
- `expiresAt`
- `usedAt`
- `usedByDeviceId`
- `failedAttempts`
- `status`

### 2. Create code

When `pairing.createCode` is called:

- verify feature flag / config gate
- create a short-lived human-readable code
- generate a nonce
- issue a short-lived bootstrap auth token using OpenClaw's existing bootstrap-token infrastructure
- persist the record
- return code + nonce + bootstrap auth + expiry metadata

### 3. Exchange code

When `pairing.exchangeCode` is called:

- require that the websocket has already connected successfully using the short-lived bootstrap auth
- verify feature flag / config gate
- look up code record
- reject missing/expired/used/revoked codes
- normalize and validate the public key
- derive `deviceId` from the public key and compare
- rebuild the canonical signature payload and verify signature
- call into existing device-pairing approval logic with `silent: true`
- auto-approve the synthetic pending request
- read back the issued trusted-device token
- mark the code used
- return trust material

### 4. Revoke trusted device

When `pairing.revokeDevice` is called:

- remove or revoke the trusted device record
- ensure next client startup cannot silently reconnect

### 5. Control UI

Expose this in a dedicated Clawpodz surface under Integrations:

- create pairing
- show pairing code and pairing nonce separately inside one modal
- show bootstrap auth in the same modal for first-time desktop connect
- show expiry/use/expired status for recent codes
- show trusted OCMAP / Clawpodz devices
- revoke trusted device

Keep generic paired devices, node bindings, and exec approvals in the Devices tab instead of mixing them into the Clawpodz pairing surface.

## Feature flag / rollout

Gate the feature behind config or env during rollout.

Examples:
- env var like `OCMAP_PAIRING_V1=1`
- later: a proper OpenClaw config flag surfaced in the dashboard

Prefer config-backed rollout for reusable deployments.

## Suggested server-side test matrix

- create code returns nonce and expiry
- exchange valid code succeeds once
- same code reused fails
- expired code fails
- invalid signature fails
- mismatched deviceId/publicKey fails
- revoke device removes future reconnect ability
- trusted devices survive gateway restart

## Common server-side mistakes

- Returning a pairing code but not the nonce the client must sign.
- Issuing a completely separate token type with separate verification logic.
- Not marking codes used atomically.
- Not recording which device consumed the code.
- Letting renderer/UI directly see or store the long-lived trusted token.
