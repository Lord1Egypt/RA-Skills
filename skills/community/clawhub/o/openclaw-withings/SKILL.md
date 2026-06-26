---
name: openclaw-withings
description: Official Withings OAuth integration for OpenClaw. Use to connect/authorize a personal Withings account, store+refresh tokens locally, and fetch health measurements (weight, body fat, blood pressure, heart rate) plus sleep summaries where available. Supports today/yesterday by timezone and produces normalized daily JSON for the Wellness hub.
---

# Withings (Official API)

This is a **source** skill. It connects to Withings, fetches data, normalizes it, and renders a short message. Delivery is channel-agnostic.

## Configuration

Required env vars:

- `WITHINGS_CLIENT_ID`
- `WITHINGS_CLIENT_SECRET`
- `WITHINGS_REDIRECT_URI`

Optional:

- `WITHINGS_TOKEN_PATH` (default: `~/.config/openclaw/withings/token.json`)
- `WITHINGS_TZ` (default: `Asia/Shanghai`)
- `WITHINGS_SCOPES` (default: `user.metrics user.activity`)

## Connect (OAuth)

Choose one mode:

- **Phone/remote mode (recommended):**

```bash
python3 scripts/withings_oauth_login.py
```

- **Desktop loopback mode (optional):** if you are authorizing in a browser on the same machine that runs OpenClaw and `WITHINGS_REDIRECT_URI` is a loopback URL like `http://127.0.0.1:58539/callback`:

```bash
python3 scripts/withings_oauth_login.py --loopback
```

## Fetch + normalize for a day

```bash
python3 scripts/withings_fetch_daily.py --date today --out /tmp/withings_raw_today.json
python3 scripts/withings_normalize_daily.py /tmp/withings_raw_today.json --out /tmp/withings_today.json
python3 scripts/withings_render.py /tmp/withings_today.json --format markdown --channel generic
```

## References

- API/OAuth notes: `references/withings_api.md`
- Output schema (for Wellness hub): `references/output_schema.md`
