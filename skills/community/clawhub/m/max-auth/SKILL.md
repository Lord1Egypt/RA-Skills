---
name: max-auth
description: Security authentication gate for OpenClaw sensitive actions. Deploys a local Node.js auth server with biometric passkeys (WebAuthn/Touch ID/Face ID) and master password. Supports session-scoped auth per channel/session key, secure one-time secret submission URLs, and a browser UI in Portuguese, English, and Spanish.
---

# Max Auth

A lightweight self-hosted authentication server for OpenClaw. It protects sensitive agent actions with biometric passkeys and a master password, supports independent auth per session/channel, and can collect secrets via one-time HTTPS forms so credentials never need to appear in chat.

## Features

- 🔑 Biometric passkeys via WebAuthn
- 🔐 Master password using PBKDF2 + salt
- ⏱ 2-hour session tokens
- 🔒 Session-scoped auth per `sessionKey` (`telegram:6314900956`, `discord:channel:123`, etc.)
- 🔗 Delegated grants between sessions
- 🧾 Audit log at `~/.max-auth/audit.log`
- 🌍 Browser UI localized in Portuguese, English, and Spanish
- 🕳️ One-time secure secret forms (`request_secret` / `retrieve_secret`)
- 🔌 OpenClaw plugin tools: `check_auth`, `require_auth`, `request_secret`, `retrieve_secret`

## Requirements

- Node.js 18+
- HTTPS reverse proxy in front of the local auth server for WebAuthn browser flows

## Quick Setup

```bash
mkdir -p ~/.max-auth && cd ~/.max-auth
cp <skill-path>/assets/auth-server.js .
cp <skill-path>/assets/package.json .
npm install

node auth-server.js set-password 'your_strong_password'
node auth-server.js
```

By default the server runs on `127.0.0.1:8456`.
Use `references/api.md` for systemd, proxying, and HTTP API details.

## Session-scoped auth

Each channel/session has its own auth state.

Examples:
- `telegram:6314900956`
- `discord:channel:1488653811185881133`
- `global`

Typical check:

```bash
curl -s "http://127.0.0.1:8456/status?session=telegram%3A6314900956"
```

If auth is missing, direct the user to:

```text
https://your-host/auth?session=telegram%3A6314900956
```

## Secure secret handoff

Use this when the user needs to give a password/token/API key without leaking it into chat.

Flow:
1. Agent calls `request_secret` with a label + field definitions
2. User opens the returned HTTPS URL and submits the form in the browser
3. Agent polls with `retrieve_secret`
4. Values are returned once and then consumed/deleted from memory

The values are stored in memory only, expire automatically, and are not written to the chat transcript.

## When to require auth

Require auth before:
- deleting files/data
- package installs
- system configuration changes
- sending messages/emails to third parties
- mutating external APIs

Do not require auth for ordinary read/search/list/fetch operations.

## References

- `references/api.md` — setup + HTTP API
- `references/integration.md` — agent integration patterns
