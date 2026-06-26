---
name: whoop
description: Official WHOOP Developer Platform integration for OpenClaw: OAuth connect/authorize, local token storage + refresh, and WHOOP v2 metric fetch (recovery, sleep, strain/cycle, workouts, profile, body measurements). Use when users say: connect WHOOP, authorize WHOOP, pull WHOOP data, get today/yesterday recovery/sleep/strain, generate daily/weekly WHOOP summaries, or push WHOOP updates to any chat channel (TUI/webchat/Slack/Discord/WhatsApp/Telegram/etc.).
---

# WHOOP (Official API)

Use this skill to **connect WHOOP → fetch metrics → produce a message**.

Scope: WHOOP is the data source only. Keep delivery channel-agnostic: generate text/markdown and either reply in the current chat or send via OpenClaw’s `message` tool.

## Quick start (minimal)

1) Set env vars:

- `WHOOP_CLIENT_ID`
- `WHOOP_CLIENT_SECRET`
- `WHOOP_REDIRECT_URI`

2) Connect once (choose one):

**Phone/remote mode (recommended):** run, then copy/paste the redirect URL or code back into chat.

```bash
python3 scripts/whoop_oauth_login.py
```

**Desktop fast path (optional):** if you are authorizing in a browser on the same machine that runs OpenClaw, set `WHOOP_REDIRECT_URI` to a loopback URL (e.g. `http://127.0.0.1:58539/callback`) and run:

```bash
python3 scripts/whoop_oauth_login.py --loopback
```

3) Fetch + render today:

```bash
python3 scripts/whoop_fetch.py --date today --out /tmp/whoop_raw_today.json
python3 scripts/whoop_normalize.py /tmp/whoop_raw_today.json --out /tmp/whoop_today.json
python3 scripts/whoop_render.py /tmp/whoop_today.json --format markdown --channel generic
```

## Configuration (required)

Provide these via environment variables (preferred) or direct CLI args to scripts:

- `WHOOP_CLIENT_ID`
- `WHOOP_CLIENT_SECRET`
- `WHOOP_REDIRECT_URI` (must exactly match the value in the WHOOP developer dashboard)

Optional:

- `WHOOP_TOKEN_PATH` (default: `~/.config/openclaw/whoop/token.json`)
- `WHOOP_TZ` (default: `Asia/Shanghai`)

## Workflow 1 — Connect WHOOP (OAuth login)

1) Run one of these modes:

- **Phone/remote mode (recommended):**

```bash
python3 scripts/whoop_oauth_login.py
```

Then open the printed URL on any device, approve access, and paste the redirect URL (or code) back into the prompt.

- **Desktop loopback mode (optional):**

```bash
python3 scripts/whoop_oauth_login.py --loopback
```

Use this only if your browser authorization happens on the same machine that runs OpenClaw, and `WHOOP_REDIRECT_URI` is a loopback URL like `http://127.0.0.1:<port>/callback`.

2) The script stores tokens at `WHOOP_TOKEN_PATH`. 

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
