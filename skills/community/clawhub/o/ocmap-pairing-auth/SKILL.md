---
name: ocmap-pairing-auth
description: Implement one-time pairing-code authentication between an OpenClaw gateway and a desktop or remote client such as OCMAP. Use when adding or updating pairing.createCode / pairing.exchangeCode / pairing.revokeDevice, short-lived bootstrap auth for connect-first handshakes, trusted-device persistence, the OpenClaw Control UI Clawpodz tab, client-side signed device proof, or recovery/revocation flows for persistent trusted device enrollment.
---

# OCMAP Pairing Auth

Implement the feature as a thin pairing-code layer on top of OpenClaw's existing signed device identity and trusted-device token flow. Do not invent a second long-lived auth system.

## Workflow

1. Read `references/protocol.md` first.
2. If working on OpenClaw gateway or Control UI, read `references/server-openclaw.md`.
3. If working on OCMAP or another desktop client, read `references/client-ocmap.md`.
4. Keep server and client aligned on the exact request/response contract before wiring UI.

## Required design

- Generate a short-lived one-time code on the server.
- Also mint a short-lived bootstrap auth value during `pairing.createCode`.
- Preserve OpenClaw's connect-first rule:
  - client must send the bootstrap value during `connect.auth`
  - complete handshake normally
  - only then call `pairing.exchangeCode`
- Bind exchange to a device identity proof:
  - `deviceId`
  - `publicKey`
  - `signature`
  - `signedAt`
  - `nonce`
- On success, mint or reuse the normal OpenClaw trusted-device token path.
- Persist trust on the client outside the renderer/UI process.
- Support revoke on the server and forget-device on the client.
- Return structured error codes instead of generic failures.

## Non-negotiable rules

- Keep pairing codes short-lived: 2-5 minutes.
- Make bootstrap auth values short-lived as well.
- Make codes single-use.
- Rate-limit failed exchange attempts.
- Never expose the long-lived trusted token in renderer/browser UI state.
- Do not require manual approval after a successful code exchange; the code exchange is the approval.
- Do not bypass OpenClaw's existing device token verification model; extend it.
- Do not bypass OpenClaw's connect-first handshake rule just to make pairing work.

## OpenClaw implementation checklist

- Add gateway methods:
  - `pairing.createCode`
  - `pairing.exchangeCode`
  - `pairing.revokeDevice`
- Return `code`, `nonce`, and short-lived bootstrap auth from `pairing.createCode`.
- Store pairing-code state separately from generic device pending/paired records.
- Surface Clawpodz pairing UI in its own Control UI tab under Integrations, with recent pairings and trusted desktop clients there.
- Keep generic paired devices / nodes / exec approvals in the Devices tab.
- Add feature-flag or config gating for rollout.
- Return structured failure codes such as:
  - `PAIRING_DISABLED`
  - `CODE_INVALID`
  - `CODE_EXPIRED`
  - `CODE_ALREADY_USED`
  - `DEVICE_REVOKED`

## Client implementation checklist

- Use the returned bootstrap auth during `connect.auth` so the client can satisfy the connect-first handshake.
- Open the websocket and complete the gateway handshake before attempting pairing exchange.
- Submit the full signed payload; `code + deviceId` alone is insufficient.
- After exchange, persist the returned trusted-device token in main/backend storage.
- Reconnect using the stored token and transition auth state cleanly.
- Distinguish `UNPAIRED`, `PAIRING_IN_PROGRESS`, `PAIRED_CONNECTED`, `PAIRED_DISCONNECTED`, and `REVOKED`.

## Validation

Run this matrix before calling the feature done:

- Fresh pair with valid code succeeds.
- Reuse same code fails with `CODE_ALREADY_USED`.
- Expired code fails with `CODE_EXPIRED`.
- Invalid signature/public key/device mismatch fails with `CODE_INVALID`.
- Restart client after success reconnects automatically.
- Revoke device on server forces client back to unpaired/revoked flow.
- Gateway restart does not lose trusted device records.

## References

- Server details: `references/server-openclaw.md`
- Client details: `references/client-ocmap.md`
- Protocol contract: `references/protocol.md`
