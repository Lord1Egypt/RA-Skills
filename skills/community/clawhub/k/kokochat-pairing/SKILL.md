---
name: kokochat-pairing
version: 0.4.1
description: "Generate a KokoChat connection code using OpenClaw's official `openclaw qr` device-pair flow. Use when the user asks to pair KokoChat, generate a KokoChat connection code, or sends a KokoChat `kokochat.pairingRequest` payload. The script brings up the KokoChat relay tunnel and runs `openclaw qr` so the GATEWAY signs a short-lived bootstrapToken; after the phone redeems it, inspect `openclaw devices list` to verify the actual device scopes and approve/keep/revoke according to the owner's consent."
author: komako-workshop
license: Apache-2.0
tags: [latest, kokochat, pairing, device, gateway, relay]
triggers:
  - kokochat pairing
  - pair kokochat
  - generate kokochat connection code
  - kokochat 配对
  - KokoChat 连接码
  - kokochat.pairingRequest
metadata:
  openclaw:
    emoji: "📱"
    requires:
      bins: [node, openclaw]
      capabilities:
        - network
      platforms:
        - linux
        - darwin
        - windows
---

# kokochat-pairing

KokoChat is a mobile client for this OpenClaw Gateway. KokoChat pairs as a real
Gateway device through OpenClaw's **official** `openclaw qr` device-pair flow:
the generator brings up the KokoChat relay tunnel, runs `openclaw qr`, and the
**Gateway** mints a short-lived bootstrapToken. The phone completes the
device-pair handshake and the Gateway issues the real device token. This skill
never self-signs a token or writes `paired.json` directly — that self-signing is
exactly what a careful OpenClaw flags as a backdoor.

The generated setup code uses the KokoChat relay tunnel url (so the phone can
reach this Gateway through NAT). Do not hand out LAN or bare public Gateway urls.

KokoChat product features only need `operator.read` + `operator.write` (read
sessions/history, send messages). The actual device-token scopes are signed by
OpenClaw's official `openclaw qr` / device-pair flow and may vary by OpenClaw
version or Gateway policy. After pairing, inspect `openclaw devices list`; if
the granted scopes exceed what the owner wants to grant, stop and revoke the
device. KokoChat itself does not need `operator.admin`, `operator.approvals`, or
`operator.talk.secrets`.

## Generating A Connection Code

Run this from the skill directory. A pairing request is optional (older app
builds may include one; the `openclaw qr` flow does not need it):

```bash
node ./generate-kokochat-code.mjs
```

Return only the generated KokoChat connection code in a fenced code block.

## Inspect / Approve The Phone Device (after the user pastes the code)

The setup code carries a gateway-signed bootstrapToken. When the user pastes it
into KokoChat, the phone redeems it through OpenClaw's official device-pair
flow. Depending on the OpenClaw version/gateway policy, the phone may create a
**pending** device request or may already appear as paired. Inspect first (the
operator is verifying a device the owner asked to pair — no patching, no
self-signing):

```bash
openclaw devices list             # confirm the KokoChat phone + actual scopes
openclaw devices approve --latest # only if it is pending and the owner accepts
```

If the phone is already paired, do not run approve. Inspect the actual scopes
with `openclaw devices list`; pairing is complete only if the owner accepts
them. If the scopes or device identity do not match expectations, stop and
recommend revoking/removing the device.

## If The User Did Not Trigger Pairing From The App

Ask them to open KokoChat's "我 / 配对" page, then either run the install +
generate command it shows, or paste back the connection code you return here.

## Output Format

````markdown
这是新的 KokoChat 连接码：

```
<raw setup code from generate-kokochat-code.mjs>
```
````

## Do Not

- Do not print the raw `gateway.auth.token`.
- Do not generate a token-only or self-signed setup code; the generator goes
  through `openclaw qr` so the Gateway signs the token.
- Do not widen scopes beyond `operator.read` + `operator.write`.
- Do not patch OpenClaw internals (e.g. message-handler) to skip device
  approval; use `openclaw devices approve` instead.
