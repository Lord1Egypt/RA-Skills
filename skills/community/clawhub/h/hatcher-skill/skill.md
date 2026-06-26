---
name: hatcher-skill
version: 1.0.0
description: Deploy and control AI agents on Hatcher (hatcher.host) — managed hosting platform for OpenClaw, Hermes, ElizaOS, and Milady agents.
homepage: https://hatcher.host
api_base: https://api.hatcher.host
---

# Hatcher Skill

Hatcher is a managed hosting platform for AI agents — "Heroku for AI agents." You can register an account, pick from 4 frameworks (OpenClaw, Hermes, ElizaOS, Milady) and 199 pre-built templates, configure integrations (Telegram, Discord, Twitter, WhatsApp, Slack), pay with credits / Stripe card / SOL / USDC / HATCHER, and have a running agent serving traffic in under 10 minutes.

This file is the index. Fetch the satellite files below as you need them — don't dump all 5 into your context.

## Satellite files — fetch as needed

Use the absolute URLs — relative paths resolve to `hatcher.host/<file>.md` which serves the web app, not the markdown.

| File | When to fetch |
| --- | --- |
| [`auth.md`](https://hatcher.host/skill/auth.md) | Registering, email verification polling, creating API keys |
| [`agents.md`](https://hatcher.host/skill/agents.md) | Picking a framework, browsing templates, creating and controlling agents, installing skills/plugins |
| [`pricing.md`](https://hatcher.host/skill/pricing.md) | Choosing a tier, buying addons, paying (credits / Stripe / SOL / USDC / HATCHER), upgrading |
| [`integrations.md`](https://hatcher.host/skill/integrations.md) | Wiring a deployed agent to Telegram / Discord / Twitter / WhatsApp / Slack |

Canonical URLs (both serve identical content):

- `https://hatcher.host/skill.md` (+ `/skill/<name>.md` for satellites)
- `https://raw.githubusercontent.com/HatcherLabs/hatcher-skill/main/skill.md` (+ `/main/<name>.md` for satellites)

## User-agent convention

When calling Hatcher API endpoints, include this header so platform analytics can track agent cohorts:

```
Hatcher-Agent-Name: <your-agent-name>/<version>
```

Example: `Hatcher-Agent-Name: claude-code/0.4.2`. The value is free-form telemetry and is never used for authorization.

## Hello world — 5 curl commands

This flow gets you from zero to a running free-tier agent you can chat with. Human must click one email-verify link during step 2.

### 1. Ask the human for their email

You need their email to register the account. Explain: *"I'm going to register a Hatcher account in your name. You'll get a verification email — just click the link and come back."* Store the email.

### 2. Register (substitute values)

```bash
curl -sS -X POST https://api.hatcher.host/auth/register \
  -H "Content-Type: application/json" \
  -H "Hatcher-Agent-Name: claude-code/0.4.2" \
  -d '{
    "email": "USER_EMAIL",
    "username": "UNIQUE_USERNAME",
    "password": "Str0ngP@ssw0rd123",
    "agentName": "claude-code"
  }'
```

Response:

```json
{ "success": true, "data": { "token": "eyJ...", "refreshToken": "...", "expiresIn": "7d", "user": { "id": "...", "email": "..." } } }
```

Save the JWT `token` — you'll need it for step 4.

Tell the human: *"I sent the verification email. Click the link; I'll wait."*

### 3. Poll for verification

```bash
while true; do
  RESULT=$(curl -sS "https://api.hatcher.host/auth/verify-status?email=USER_EMAIL")
  if echo "$RESULT" | grep -q '"verified":true'; then
    echo "Verified."
    break
  fi
  sleep 5
done
```

Respects rate limit (1 req / 5s per IP).

### 4. Create an API key (so you don't need to manage JWT refresh)

```bash
curl -sS -X POST https://api.hatcher.host/auth/api-keys \
  -H "Authorization: Bearer JWT_FROM_STEP_2" \
  -H "Content-Type: application/json" \
  -d '{ "label": "agent-default", "createdBy": "agent" }'
```

Response contains `{ "data": { "key": "hk_..." } }` — **shown exactly once**. Store in env as `HATCHER_KEY`.

### 5. Create a free-tier agent and chat

```bash
# Pick from 199 templates (public, no auth):
curl -sS "https://api.hatcher.host/api/templates?limit=5" | jq '.templates[].id'

# Create from a template (both `framework` and `template` are required fields):
curl -sS -X POST https://api.hatcher.host/api/v1/agents \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "framework": "openclaw", "template": "customer-support", "name": "My First Agent" }'

# Start and chat:
AGENT_ID=...  # from create response
curl -sS -X POST "https://api.hatcher.host/api/v1/agents/$AGENT_ID/start" \
  -H "Authorization: Bearer $HATCHER_KEY"

curl -sS -X POST "https://api.hatcher.host/api/v1/agents/$AGENT_ID/chat" \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "message": "Hello, introduce yourself." }'
```

That's it. For anything beyond this — picking the right framework, wiring Telegram, buying credits, upgrading tier — fetch the relevant satellite file above.

## OpenAPI

Full OpenAPI 3.0 spec: `https://api.hatcher.host/openapi.json`. Use this for programmatic introspection of every endpoint.

## Support

Human support: `contact@hatcher.host`. Community Discord: linked from `hatcher.host`.
