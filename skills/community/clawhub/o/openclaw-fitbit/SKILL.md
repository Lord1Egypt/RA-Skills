---
name: openclaw-fitbit
description: Official Fitbit OAuth integration for OpenClaw (Tier 1). Use to connect/authorize Fitbit, store+refresh tokens locally, fetch daily activity + sleep summaries, normalize into a stable daily JSON shape for the Wellness hub, and render a short digest for any chat channel.
---

# Fitbit (Official API)

This is a **source** skill. It connects to Fitbit, fetches data, normalizes it, and renders a short message.

## Configuration

Required env vars:
- `FITBIT_CLIENT_ID`
- `FITBIT_CLIENT_SECRET`
- `FITBIT_REDIRECT_URI`

Optional:
- `FITBIT_TOKEN_PATH` (default: `~/.config/openclaw/fitbit/token.json`)
- `FITBIT_TZ` (default: `Asia/Shanghai`)
- `FITBIT_SCOPES` (default: `activity sleep heartrate profile weight`)

## Connect (OAuth)

- **Phone/remote mode (recommended):**

```bash
python3 scripts/fitbit_oauth_login.py
```

- **Desktop loopback mode (optional):** if authorizing on the same machine and `FITBIT_REDIRECT_URI` is loopback:

```bash
python3 scripts/fitbit_oauth_login.py --loopback
```

## Fetch + normalize for a day

```bash
python3 scripts/fitbit_fetch_daily.py --date today --out /tmp/fitbit_raw_today.json
python3 scripts/fitbit_normalize_daily.py /tmp/fitbit_raw_today.json --out /tmp/fitbit_today.json
python3 scripts/fitbit_render.py /tmp/fitbit_today.json --format markdown --channel generic
```

## References

- API/OAuth notes: `references/fitbit_api.md`
- Output schema: `references/output_schema.md`
