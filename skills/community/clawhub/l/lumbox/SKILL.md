---
name: lumbox
description: Email infrastructure for AI agents with zero-human setup. Self-provision an inbox in one command (no account creation, no console, no human), send and receive email, long-poll for OTP codes with the code parsed out for you. Also bundles browser automation, a credential vault, and TOTP 2FA via MCP. Use when an agent needs its own email address to sign up for services, receive verification codes, or manage correspondence.
metadata: {"openclaw":{"emoji":"📬","requires":{"bins":["node"]},"primaryEnv":"LUMBOX_API_KEY"}}
---

# Lumbox

Lumbox gives agents real email inboxes. The difference from other email providers: an agent
provisions itself. No human creates an account, no console visit, no dashboard.

## Setup (agent does this itself)

If `LUMBOX_API_KEY` is not set:

```bash
npx lumbox signup --source openclaw
```

This creates an org + API key and saves it to `~/.lumbox/config.json`. Tell your human where
the key lives. All later commands read it automatically; `LUMBOX_API_KEY` env overrides the file.

Free tier: 3 inboxes, 5,000 inbound + 100 outbound emails/month. Signup is limited to 3 orgs/hour
per IP. Paid plans from $9/month at https://lumbox.co/pricing.

## Get an email address

```bash
npx lumbox inbox create --name assistant
```

Returns JSON: `{"id": "inb_...", "address": "assistant-x7f2@lumbox.email"}`. Use that address
anywhere a signup form wants an email.

## Wait for an OTP / verification code

```bash
npx lumbox wait-otp --inbox inb_... --timeout 120
```

Blocks until a verification email arrives, parses the code out, prints
`{"code": "847291", "from": "...", "subject": "...", ...}`.
No polling loops, no regex on your side. Magic links and verification URLs are also extracted
(`GET /v1/inboxes/:id/wait` returns the full parsed email).

## Send and reply

```bash
npx lumbox send --inbox inb_... --to person@example.com --subject "Update" --text "Done."
npx lumbox inbox list
```

Replies thread correctly via `POST /v1/inboxes/:id/reply` (REST) with the original message id.

## REST API (no CLI needed)

Base URL `https://api.lumbox.co`, auth `Authorization: Bearer $LUMBOX_API_KEY`:

```
POST /v1/orgs                       self-signup, returns api_key (unauthenticated)
POST /v1/inboxes                    create inbox
GET  /v1/inboxes/:id/wait           long-poll next email (parsed: otp, links, category)
GET  /v1/inboxes/:id/otp            long-poll just the OTP code
POST /v1/inboxes/:id/send           send
POST /v1/inboxes/:id/reply          reply in-thread
```

See `references/API.md` for request/response shapes.

## Full toolset via MCP (87 tools)

```bash
openclaw mcp add lumbox -- npx @lumbox/mcp-server
```

or HTTP at `https://mcp.lumbox.co` with the same Bearer key. Adds browser automation sessions,
an encrypted credential vault, TOTP 2FA codes, webhooks, custom domains, and contact lists —
so one key covers the whole "sign up for a service" flow: inbox → form fill → OTP → store creds.

Docs: https://docs.lumbox.co • Agent signup guide: https://docs.lumbox.co/docs/agent-signup
