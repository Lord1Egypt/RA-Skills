# persona-consent-telegram-hub

Telegram-approved persona access gate for OpenClaw, with optional **persona-service** integration so external chatbots can request your Clawbot’s persona; you approve via Telegram and the result is returned to the hub.

## What this skill does

- Requires explicit owner approval via Telegram for each persona request.
- Returns persona content only when approved; returns `author did not authorize` on deny, timeout, or errors.
- **Persona-service mode**: When configured, a local **persona-client** polls a hosted persona-service for pending requests, runs the same Telegram consent flow, and posts the result back—so you only run your Clawbot; no need to expose it as an API.

## Install from ClawHub

```bash
openclaw skills add persona-consent-telegram-hub
```

After install, **edit `~/.openclaw/openclaw.json` by hand** and add a `skills.entries["persona-consent-telegram-hub"]` block for this skill.
See the exact JSON snippet in the **Configuration** section below.

## Configuration

In `~/.openclaw/openclaw.json`, under `skills.entries["persona-consent-telegram-hub"].env`, set:

**Required for Telegram consent (and for persona-client when using persona-service):**

- `TELEGRAM_BOT_TOKEN` – Bot token for approval (use a **separate** bot from your main OpenClaw bot to avoid `409 Conflict` on getUpdates).
- `TELEGRAM_OWNER_CHAT_ID` – Your Telegram chat ID.
- `PERSONA_PATH` – Path to your persona file (e.g. `~/.openclaw/persona.md`).
- `ALLOWED_PERSONA_PATH` – Same as `PERSONA_PATH` (allowed read path).

**Required only for persona-service (auto-run persona-client):**

- `PERSONA_SERVICE_URL` – Base URL of persona-service (e.g. `https://persona.example.com`).
- `PERSONA_CLIENT_ID` – Unique identifier for this Clawbot (issued by persona-service).

**Optional:**

- `PERSONA_CLIENT_SHARED_SECRET` – Shared secret; must match persona-service if it enforces one.
- `PERSONA_CLIENT_POLL_INTERVAL_SECONDS` – Poll interval (default `10`).
- `PERSONA_CLIENT_MAX_BACKOFF_SECONDS` – Max backoff on errors (default `60`).
- `REQUEST_TIMEOUT_SECONDS` – Telegram approval timeout (default `90`).
- `POLL_INTERVAL_SECONDS` – Telegram polling interval (default `2`).

Example snippet:

```json
{
  "skills": {
    "entries": {
      "persona-consent-telegram-hub": {
        "env": {
          "TELEGRAM_BOT_TOKEN": "…",
          "TELEGRAM_OWNER_CHAT_ID": "…",
          "PERSONA_PATH": "/home/you/.openclaw/persona.md",
          "ALLOWED_PERSONA_PATH": "/home/you/.openclaw/persona.md",
          "PERSONA_SERVICE_URL": "https://persona.example.com",
          "PERSONA_CLIENT_ID": "your-client-id",
          "PERSONA_CLIENT_SHARED_SECRET": "optional-secret"
        }
      }
    }
  }
}
```

## One command: gateway + persona-client

OpenClaw does not yet support “run this when gateway starts” hooks from skills. To get **install skill and it auto-runs**, use the provided wrapper so that one command starts both the gateway and the persona-client:

```bash
cd ~/.openclaw/skills/persona-consent-telegram-hub
node scripts/run-gateway-with-persona-client.js -- --port 18789
```

This script:

1. Reads `~/.openclaw/openclaw.json` and the skill’s env.
2. If `PERSONA_SERVICE_URL` and `PERSONA_CLIENT_ID` are set, starts `scripts/persona_client.sh` in the background.
3. Runs `openclaw gateway` with the rest of the arguments (e.g. `--port 18789`).

You can alias it, e.g.:

```bash
alias openclaw-gateway-persona='node ~/.openclaw/skills/persona-consent-telegram-hub/scripts/run-gateway-with-persona-client.js --'
openclaw-gateway-persona --port 18789
```

If you prefer not to use the wrapper, run the persona-client manually in a second terminal:

```bash
cd ~/.openclaw/skills/persona-consent-telegram-hub
# Export env from openclaw.json or set PERSONA_SERVICE_URL, PERSONA_CLIENT_ID, etc.
bash scripts/persona_client.sh
```

## Files

- `SKILL.md` – Skill metadata and instructions for the agent.
- `scripts/request_persona.sh` – Telegram Approve/Deny; reads persona file if approved.
- `scripts/persona_client.sh` – Polls persona-service, runs consent, POSTs result.
- `scripts/run-gateway-with-persona-client.js` – Wrapper: start persona-client + `openclaw gateway`.
- `src/index.ts` – Plugin entry; when OpenClaw supports gateway lifecycle hooks, `onGatewayStart` will be used to start the persona-client automatically.

## Local script test

```bash
bash scripts/request_persona.sh "<requester_id>" "persona requested for <reason>"
```

Expected JSON:  
- Approved: `{"allowed":true,"persona_md":"..."}`  
- Denied/timeout/error: `{"allowed":false,"message":"author did not authorize"}`

## ClawHub packaging

- Skill is self-contained in this folder.
- Keep secrets out of `SKILL.md` and docs.
- Rotate bot tokens before publishing screenshots or logs.
