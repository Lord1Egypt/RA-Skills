---
name: whoop
description: Connect to the WHOOP Developer Platform via official OAuth (authorization code flow), store and refresh tokens, and fetch WHOOP v2 data (recovery, sleep, cycle/strain, workout, profile, body measurements). Use when a user asks to connect/authorize WHOOP, pull WHOOP metrics, summarize today/yesterday, generate daily/weekly WHOOP reports, or send WHOOP updates to any OpenClaw chat channel (TUI/webchat/Slack/Discord/WhatsApp/Telegram/etc.).
---

# WHOOP (official API)

Keep this skill **WHOOP-only** (data source). Do not hardcode any destination channel. Generate a clean text/markdown message and either reply in the current chat or use OpenClaw’s `message` tool to send it to a chosen target.

## Configuration (required)

Provide these via environment variables (preferred) or direct CLI args to scripts:

- `WHOOP_CLIENT_ID`
- `WHOOP_CLIENT_SECRET`
- `WHOOP_REDIRECT_URI` (must exactly match the value in the WHOOP developer dashboard)

Optional:

- `WHOOP_TOKEN_PATH` (default: `~/.config/openclaw/whoop/token.json`)
- `WHOOP_TZ` (default: `Asia/Shanghai`)

## Workflow 1 — Connect WHOOP (OAuth login)

1) Run:

```bash
python3 scripts/whoop_oauth_login.py
```

2) The script prints an authorization URL. Open it, log in, and approve.

3) After redirect, either:
- paste the full redirect URL into the prompt (recommended), or
- paste the `code`.

4) The script stores tokens at `WHOOP_TOKEN_PATH`.

If you need to revoke later, use `delete /v2/user/access` (see `references/whoop_api.md`).

## Workflow 2 — Fetch metrics (today / yesterday)

Fetch raw WHOOP API objects:

```bash
python3 scripts/whoop_fetch.py --date today --out /tmp/whoop_raw_today.json
python3 scripts/whoop_fetch.py --date yesterday --out /tmp/whoop_raw_yday.json

Tip: `whoop_fetch.py` uses WHOOP’s `start`/`end` query params + `nextToken` pagination. Use `--tz` to control which local day is fetched (default from `WHOOP_TZ`).
```

Normalize into a stable schema:

```bash
python3 scripts/whoop_normalize.py /tmp/whoop_raw_today.json --out /tmp/whoop_today.json
```

Render a message for humans:

```bash
python3 scripts/whoop_render.py /tmp/whoop_today.json --format markdown --channel generic

Channel formatting presets:
- `--channel discord` (uses **bold**)
- `--channel slack` / `--channel whatsapp` (uses *bold*, avoids fancy markup)
- `--channel telegram` (plain text)
```

Then either:
- reply with the rendered text in the current chat, or
- send it to another channel via OpenClaw `message(action=send, ...)`.

## Workflow 3 — Daily/weekly push (cron)

If the user wants scheduled push messages, create an OpenClaw cron job that runs an isolated agent turn which:

- calls `scripts/whoop_fetch.py` + `scripts/whoop_normalize.py` + `scripts/whoop_render.py`
- sends the rendered message to the desired destination

Keep the cron job **channel-agnostic**: the destination should be a parameter in the cron payload text.

## Notes on API details

- For scopes, endpoints, and pagination/rate-limits, read: `references/whoop_api.md`.
- For the normalized JSON schema contract, read: `references/output_schemas.md`.
- If OAuth fails (redirect mismatch, invalid_scope, 401/429), read: `references/troubleshooting.md`.
