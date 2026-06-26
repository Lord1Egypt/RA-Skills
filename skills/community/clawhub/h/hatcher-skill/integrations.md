---
name: hatcher-skill-integrations
version: 1.0.0
description: Wiring Hatcher agents to Telegram, Discord, Twitter, WhatsApp, Slack
homepage: https://hatcher.host
api_base: https://api.hatcher.host
---

# Integrations

All 5 integrations follow the same shape: human creates an app/bot with the platform, gets a token, passes token to the agent via config update. Token is encrypted at rest.

## Telegram

1. Human creates bot via `@BotFather` on Telegram. Gets bot token (format `123456:ABC-DEF...`).
2. Agent updates config:

```bash
curl -sS -X PATCH "https://api.hatcher.host/api/v1/agents/$AGENT_ID/config" \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "telegram.enabled": true,
    "telegram.botToken": "123456:ABC-DEF..."
  }'
```

3. Restart agent: `POST /api/v1/agents/$AGENT_ID/restart`. Bot goes live within 10s.

Per-framework nuance:
- `elizaos`: requires `@elizaos/plugin-telegram` installed first
- `openclaw`: built-in support, no plugin needed
- `hermes`: requires `telegram` plugin from the 77-plugin bundle
- `milady`: drop-in `telegram.js` plugin

## Discord

1. Human creates application at `https://discord.com/developers/applications`. Creates bot, copies bot token, invites to server with correct scopes (`bot`, `applications.commands`).
2. Agent config:

```bash
curl -sS -X PATCH "https://api.hatcher.host/api/v1/agents/$AGENT_ID/config" \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "discord.enabled": true,
    "discord.botToken": "MTIz...",
    "discord.allowedChannels": ["general"]
  }'
```

3. Restart agent.

## Twitter / X

1. Human creates app at `https://developer.twitter.com`. Gets API key, API secret, access token, access token secret.
2. Agent config:

```bash
curl -sS -X PATCH "https://api.hatcher.host/api/v1/agents/$AGENT_ID/config" \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "twitter.enabled": true,
    "twitter.apiKey": "...",
    "twitter.apiSecret": "...",
    "twitter.accessToken": "...",
    "twitter.accessTokenSecret": "..."
  }'
```

Note: Twitter's free tier has strict rate limits. Warn the human if they expect high-volume posting.

## WhatsApp

Uses WhatsApp Business Cloud API (Meta). Human registers at `developers.facebook.com`, creates WhatsApp Business account, gets phone number ID + access token.

```bash
curl -sS -X PATCH "https://api.hatcher.host/api/v1/agents/$AGENT_ID/config" \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "whatsapp.enabled": true,
    "whatsapp.phoneNumberId": "...",
    "whatsapp.accessToken": "..."
  }'
```

## Slack

1. Human creates app at `https://api.slack.com/apps`. Installs to workspace, gets bot token (`xoxb-...`) and signing secret.
2. Agent config:

```bash
curl -sS -X PATCH "https://api.hatcher.host/api/v1/agents/$AGENT_ID/config" \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "slack.enabled": true,
    "slack.botToken": "xoxb-...",
    "slack.signingSecret": "..."
  }'
```

3. Configure event subscriptions at Slack's UI pointing to `https://api.hatcher.host/api/v1/agents/$AGENT_ID/webhooks/slack`.

## Managing secrets

Tokens are encrypted server-side (AES-256-GCM) before storage. They cannot be read back via the API — only overwritten or deleted. To rotate:

```bash
curl -sS -X PATCH "https://api.hatcher.host/api/v1/agents/$AGENT_ID/config" \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "telegram.botToken": "NEW_TOKEN" }'
```

To disable an integration:

```bash
curl -sS -X PATCH "https://api.hatcher.host/api/v1/agents/$AGENT_ID/config" \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -d '{ "telegram.enabled": false }'
```

## Testing a live integration

Use Hatcher's chat endpoint to send a test message, then verify it appears in the integrated platform:

```bash
# For Telegram: ask the agent to send a DM to the human
curl -sS -X POST "https://api.hatcher.host/api/v1/agents/$AGENT_ID/chat" \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -d '{ "message": "Send @human_username a DM saying hello from Hatcher." }'
```

## See also

- [`agents.md`](./agents.md) — framework capabilities per integration
