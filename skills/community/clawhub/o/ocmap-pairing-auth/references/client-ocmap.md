# Client Implementation: OCMAP or Other Desktop App

This flow assumes a desktop app with a privileged main/backend process and an untrusted renderer/UI process.

## Principle

The renderer collects the code. The backend performs the cryptographic proof, calls the gateway, stores trust, and reconnects.

## Required client capabilities

- persistent device identity (ed25519 keypair or equivalent)
- websocket gateway client
- ability to sign a canonical payload
- secure local trust storage in backend/main process
- explicit auth state machine for onboarding and recovery

## Required exchange payload

Do not send only `code` and `deviceId`.

The client must send:

- `code`
- `deviceId`
- `publicKey`
- `signature`
- `signedAt`
- `nonce`
- optional metadata:
  - `displayName`
  - `platform`
  - `deviceFamily`
  - `clientId`
  - `clientMode`

## Required sequence

1. Load or create persistent device identity.
2. Collect `code`, `nonce`, and `bootstrapToken` from the Clawpodz pairing UI.
3. Open the websocket transport.
4. Send `connect` first with the short-lived bootstrap auth in `connect.auth`.
5. Wait until the handshake is complete.
6. Build the canonical signed payload using the nonce from `pairing.createCode`.
7. Call `pairing.exchangeCode` over the connected socket.
8. Persist `trust.deviceToken` in backend storage.
9. Reconnect or re-authenticate using the trusted token.
10. Transition auth state to connected.

## State model

Use explicit states:

- `UNPAIRED`
- `PAIRING_IN_PROGRESS`
- `PAIRED_CONNECTED`
- `PAIRED_DISCONNECTED`
- `REVOKED`

Do not show a generic `gateway not connected` dead-end when the real issue is `UNPAIRED` or `REVOKED`.

## Storage rules

Store trust in backend/main process storage only.

Examples:
- Electron main process file under userData
- OS keychain-backed secret store
- encrypted per-user app config

Do not persist the trusted token in:
- renderer localStorage
- renderer IndexedDB
- preload-exposed plain objects
- logs

## Common client-side mistakes

### 1. Calling pairing exchange before a valid connect-first handshake

Symptom:
- `gateway socket not open`
- `unauthorized: gateway token missing`

Fix:
- open the transport first
- send the short-lived bootstrap auth in `connect.auth`
- wait for handshake completion before exchange
- separate raw socket-open readiness from authenticated handshake readiness

### 2. Sending an incomplete pairing request

Symptom:
- server rejects exchange or cannot verify device proof

Fix:
- include `publicKey`, `signature`, `signedAt`, and `nonce`

### 3. Treating the pairing code as the long-lived credential

Fix:
- persist only the trusted device token returned by exchange

### 4. Keeping auto-connect disabled after pairing

Fix:
- after persisting trust, re-enable normal reconnect flow and reconnect

## Renderer / UI guidance

Renderer should expose:

- current auth state
- code entry UI
- pending progress state
- actionable error messages for expired/invalid/revoked cases
- local `Forget this device` action

Renderer should not have direct access to the trusted token.

## Suggested desktop test matrix

- app with no trust starts in `UNPAIRED`
- valid code pairs successfully
- restart reconnects automatically
- revoked server-side device transitions to `REVOKED` or `UNPAIRED`
- local forget-device clears trust and returns to `UNPAIRED`
- expired code produces a specific error state
