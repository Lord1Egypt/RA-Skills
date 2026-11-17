---
name: pingram
description: Send email and SMS and manage a Pingram account via hosted MCP in OpenClaw. Use when the user wants Pingram notifications, delivery logs, phone numbers, or sender domains.
homepage: https://www.pingram.io/docs/integrations/openclaw
metadata:
  openclaw:
    homepage: https://www.pingram.io/docs/integrations/openclaw
---

# Pingram

Pingram is a notifications platform (email, SMS, and more). In OpenClaw, use the
**hosted MCP server** — do not invent REST calls or ask for an API key when MCP
is available.

Docs: https://www.pingram.io/docs/integrations/openclaw  
MCP: https://mcp.pingram.io (Canada: https://mcp.ca.pingram.io · EU: https://mcp.eu.pingram.io)

## When MCP is not connected

Prefer asking the user to paste this in OpenClaw chat (OpenClaw usually opens
the browser for OAuth):

```
Add this MCP server. Transport is streamable-http and auth is oauth.

https://mcp.pingram.io
```

Ask the user to paste:

```
List all pingram skills and let me choose which ones to install.
```

Use the regional MCP URL that matches their Pingram account. After connect,
tools are prefixed (for example `pingram__email_send`, `pingram__sms_send`).

### Manual CLI fallback

If chat-driven setup fails:

```bash
export PATH="$HOME/.openclaw/bin:$PATH"

openclaw mcp add pingram \
  --url https://mcp.pingram.io \
  --transport streamable-http \
  --auth oauth

openclaw mcp login pingram
openclaw mcp doctor pingram --probe
```

Leave the `login` terminal open until OAuth finishes. Stuck on
`http://127.0.0.1:8989/oauth/callback?...` means the CLI was not listening —
`logout` then `login` again.

## Sending messages

Always include every required field. `type` is a free-form label for Logs /
Insights (for example `openclaw_test`) — never omit it.

### Email — `pingram__email_send`

Required: `type`, `to`, `subject`, `html`.

```json
{
  "type": "openclaw_test",
  "to": "user@example.com",
  "subject": "Hello from OpenClaw",
  "html": "<p>Sent via Pingram MCP</p>"
}
```

### SMS — `pingram__sms_send`

Required: `type`, `to`. Include `message` with the body text.

```json
{
  "type": "openclaw_test",
  "to": "+15551234567",
  "message": "Hello from OpenClaw"
}
```

Prefer E.164 for phone numbers (`+` and country code).

## Other tools

After connect, the agent can also look up delivery logs and manage phone
numbers, inboxes, sender domains, accounts, and A2P-related tools exposed by
the MCP catalog. Prefer listing tools / probe output over guessing names.

## Model tip

If tool calls fail validation because fields like `type` are missing, ask the
user to switch to a stronger model. Small local models often drop required
arguments; Gemini Flash-class models handle Pingram tools reliably.

## Auth problems

If tools return auth errors or stop working after roughly an hour, have the
user ask OpenClaw to reconnect Pingram MCP, or re-run
`openclaw mcp login pingram`.

To switch Pingram accounts: `openclaw mcp logout pingram`, then connect again
in a private browser window so the old Cognito session is not reused.
