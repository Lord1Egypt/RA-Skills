---
name: openclaw-oura
description: Oura Ring data source for OpenClaw (Tier 1). Use to connect an Oura account using an Oura Personal Access Token, fetch Oura v2 usercollection data (sleep, readiness, activity), normalize it into a stable daily JSON shape for the Wellness hub, and render a short summary message for any chat channel.
---

# Oura (Personal Access Token)

This is a **source** skill. It fetches Oura data and outputs normalized daily JSON + a human-readable digest. It does not hardcode the destination channel.

## Configuration

Required env var:
- `OURA_ACCESS_TOKEN`

Optional:
- `OURA_TZ` (default: `Asia/Shanghai`)

## Fetch + normalize for a day

```bash
python3 scripts/oura_fetch_daily.py --date today --out /tmp/oura_raw_today.json
python3 scripts/oura_normalize_daily.py /tmp/oura_raw_today.json --out /tmp/oura_today.json
python3 scripts/oura_render.py /tmp/oura_today.json --format markdown --channel generic
```

## Notes

- API reference: `references/oura_api.md`
- Output schema: `references/output_schema.md`
