# Pairing Protocol Contract

Use this file as the source of truth for the server/client contract.

## Goal

Allow a user to enroll a desktop client once with a short-lived code generated in OpenClaw Control UI, then reconnect automatically on future launches using trusted device credentials.

## Model

The pairing code is not the long-lived credential.

The pairing code authorizes a one-time exchange. The exchange returns or mints the normal OpenClaw trusted-device token for that device identity.

## Gateway methods

### `pairing.createCode`

Server-only/admin UI call.

**Request**

```json
{}
```

Optional future field:

```json
{ "scopes": ["ocmap.connect"] }
```

**Response**

```json
{
  "pairingId": "uuid",
  "code": "ABCD-EFGH",
  "nonce": "uuid-or-random-string",
  "bootstrapToken": "short-lived-bootstrap-auth",
  "bootstrapExpiresAtMs": 1770000180000,
  "scopes": ["ocmap.connect"],
  "createdAt": 1770000000000,
  "expiresAt": 1770000300000,
  "status": "active"
}
```

Notes:
- TTL should be 2-5 minutes.
- Code should be short and human-enterable.
- Nonce is required for signed exchange.
- `bootstrapToken` is required for first-time connect auth so the client can obey OpenClaw's connect-first handshake rule.

### `pairing.exchangeCode`

Desktop/client call. Requires a successful websocket connect + handshake first.

Before calling `pairing.exchangeCode`, the client should use the short-lived bootstrap auth from `pairing.createCode` in the initial `connect.auth` payload so the gateway accepts the first connection without asking the user for a long-lived gateway token.

**Request**

```json
{
  "code": "ABCD-EFGH",
  "deviceId": "sha256-public-key-fingerprint",
  "publicKey": "base64url-ed25519-public-key",
  "signature": "base64url-signature",
  "signedAt": 1770000000000,
  "nonce": "same nonce returned by createCode",
  "displayName": "OpenClaw Multi-Agent Desktop",
  "platform": "win32",
  "deviceFamily": "desktop",
  "clientId": "ocmap-desktop",
  "clientMode": "desktop"
}
```

**Signature payload**

The signature should cover the same canonical device-auth payload the server verifies. In the current implementation that is a v3 payload shaped like:

- `deviceId`
- `clientId`
- `clientMode`
- `role = "operator"`
- `scopes = []`
- `signedAtMs`
- `token = ""`
- `nonce`
- `platform`
- `deviceFamily`

The exact builder/helper should be shared or mirrored between server and client.

**Success response**

```json
{
  "ok": true,
  "trust": {
    "deviceId": "...",
    "deviceToken": "long-lived-trusted-device-token",
    "role": "operator",
    "scopes": [],
    "issuedAt": 1770000000000,
    "trustedDevice": {
      "deviceId": "...",
      "displayName": "OpenClaw Multi-Agent Desktop",
      "publicKeyFingerprint": "...",
      "scopes": [],
      "issuedAt": 1770000000000,
      "lastSeenAt": 1770000000000
    }
  }
}
```

Legacy/fallback clients may also look for `token`, `gatewayToken`, or `authToken`, but `trust.deviceToken` is the clean target shape.

**Failure response semantics**

Return structured codes in error details:

- `PAIRING_DISABLED`
- `CODE_INVALID`
- `CODE_EXPIRED`
- `CODE_ALREADY_USED`
- `DEVICE_REVOKED`

### `pairing.revokeDevice`

Server/admin UI call.

**Request**

```json
{ "deviceId": "..." }
```

**Response**

```json
{ "deviceId": "..." }
```

## Handshake sequence

1. User generates pairing in OpenClaw Control UI.
2. OpenClaw returns `code`, `nonce`, and `bootstrapToken`.
3. Client opens websocket and sends `connect` first.
4. Client includes the bootstrap auth in `connect.auth`.
5. Gateway accepts the handshake.
6. Client calls `pairing.exchangeCode` with full signed device proof.
7. Gateway returns `trust.deviceToken`.
8. Client stores trust and reconnects normally on future launches.

## State machine

Recommended client auth states:

- `UNPAIRED`
- `PAIRING_IN_PROGRESS`
- `PAIRED_CONNECTED`
- `PAIRED_DISCONNECTED`
- `REVOKED`

## Security requirements

- Single use per code.
- Mark code used immediately on successful exchange.
- Rate-limit bad attempts.
- Reject code reuse.
- Reject stale `signedAt` values.
- Reject `deviceId` mismatch versus `publicKey`.
- Reject invalid signature.
- Keep trust token out of renderer/browser state.
