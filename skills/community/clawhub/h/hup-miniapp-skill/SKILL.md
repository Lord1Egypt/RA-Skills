---
name: hup-miniapp
description: Build, test, and list Hup mini apps — web apps that run inside Hup social posts and transact through the viewer's existing Hup wallet session via the Hup SDK bridge.
---

# Hup Mini App Builder

## Core Objective

Build mini apps for Hup (https://hup.social): single-page web apps that run inside a sandboxed
iframe embedded in a social post, and reach the viewer's wallet exclusively through the Hup SDK's
`postMessage` bridge. The viewer is already connected to Hup — a correct mini app inherits that
session and never opens a second wallet connection.

## Usage Rules and Triggers

Apply this skill when the user asks to:

- Build, scaffold, or debug a **Hup mini app** ("app inside a Hup post", "mint button in the feed").
- Port an existing **Farcaster / Base App mini app** to Hup.
- Diagnose an embed that renders but cannot connect, sign, or transact.
- Prepare an app for **listing** on the Hup apps directory or for embed review.

## Canonical Reference

The live, always-current specification is:

```
https://hup.social/miniapp-skill.md
```

Fetch it before building — it is the source of truth for the SDK surface and wallet policy. A
snapshot ships in `references/miniapp-guide.md` for offline work, and a complete working example
(connect, sign, send, policy checks) is in `references/demo-app.html`.

## Non-Negotiable Rules

1. **SDK-only wallet access.** Load `https://hup.social/miniapp-sdk.js` and use the provider it
   returns. Never bundle wagmi connectors, WalletConnect, RainbowKit, or read `window.ethereum` —
   self-connecting apps break on mobile and fail Hup's embed review.
2. **Respect the refused methods.** `eth_sign`, `eth_signTransaction`, and
   `wallet_addEthereumChain` are always rejected (error 4200). Use `personal_sign` or
   `eth_signTypedData_v4`. Never spoof `from` (rejected, 4100).
3. **Design to a fixed aspect ratio** declared at registration (`1:1`, `4:3`, `16:9`, `3:4`,
   `9:16`). Overflow scrolls inside the frame; the container never resizes.
4. **The server must allow framing.** No `X-Frame-Options`, no restrictive `frame-ancestors`.
5. **Handle the disconnected viewer.** `eth_requestAccounts` may return `[]` — render a
   "connect in Hup" state, never crash.
6. **Boot fast, degrade gracefully.** Nothing loads until the viewer presses Launch, and
   `hup.ready()` rejects standalone — show a sensible fallback outside Hup.

## Build Workflow

```text
1. Scaffold a single HTML page; load the SDK; await hup.ready() → context { user, chainId }.
2. Wire writes through provider.request() — each eth_sendTransaction is one Hup confirmation.
3. Test standalone: expect ready() to reject cleanly (this is correct behavior).
4. Deploy over https, then register on https://hup.social/apps → "List your app"
   (name, URL, category, embed shape; the URL's origin is pinned — messages from
   any other origin are dropped).
5. Request embed review from a Hup moderator. Every later edit pauses embedding
   until re-review — batch changes before updating a listing.
```

## Minimal Working Core

```html
<script src="https://hup.social/miniapp-sdk.js"></script>
<script>
  const ctx = await hup.ready()                       // rejects standalone / after 5s silence
  const provider = await hup.getProvider()            // EIP-1193, bridged to the Hup session
  const [account] = await provider.request({ method: 'eth_requestAccounts' })
  const hash = await provider.request({
    method: 'eth_sendTransaction',
    params: [{ from: account, to: CONTRACT, data: CALLDATA, value: '0x0' }],
  })
  hup.on('session', (s) => {/* viewer connected / disconnected / switched chain */})
</script>
```

Farcaster-compatible surface (`sdk.actions.ready()`, `sdk.wallet.getEthereumProvider()`,
`sdk.context`) rides the same transport — existing Farcaster mini apps generally run unmodified.

## Diagnostic Directives

| Symptom | Resolution |
| --- | --- |
| `SDK: no host` / `ready()` rejects | The app is standalone or the parent is not Hup — embed it in a Hup post to test the bridge. |
| SDK script 404 | Load from the host origin (`https://hup.social/miniapp-sdk.js`), not a relative path. |
| Empty embed box | The app's server denies framing — remove `X-Frame-Options` / `frame-ancestors`. |
| Handshake timeout while embedded | Frame URL origin differs from the registered App URL origin. |
| "App is not available for embedding" | Embed grant missing or paused by an edit — request (re-)review. |
| Error 4200 / 4100 | Refused method / mismatched `from` — see Non-Negotiable Rules 2. |
