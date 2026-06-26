# Oura API Complete Export (Claude Skill)

This is a Claude skill folder you can drop into your Claude skills directory.

## Install layout

Place this folder as:

`~/.claude/skills/oura-api-complete-export/`

with files:

- `SKILL.md`
- `README.md`
- `scripts/auth_oura_oauth.py`
- `scripts/export_oura_data.py`
- `scripts/run_full_export.sh`
- `references/endpoints.md`

## 1) Create an Oura OAuth app

1. Open Oura developer portal and create an app.
2. Copy:
   - Client ID
   - Client Secret
3. Add redirect URI (example):
   - `http://localhost:8765/callback`

## 2) Authenticate (OAuth Authorization Code)

Run:

```bash
python3 scripts/auth_oura_oauth.py \
  --client-id "<CLIENT_ID>" \
  --client-secret "<CLIENT_SECRET>" \
  --redirect-uri "http://localhost:8765/callback"
```

The script opens browser auth, captures the callback, exchanges auth code for tokens, and saves config at:

`~/.config/oura-oauth/config.json`

## 3) Export all available data

```bash
python3 scripts/export_oura_data.py --start 2020-01-01 --end $(date +%F) --out ./oura_export
```

Or use wrapper:

```bash
./scripts/run_full_export.sh 2020-01-01 $(date +%F) ./oura_export
```

## 4) Output

- Endpoint JSON files (`daily_sleep.json`, `sleep.json`, `workout.json`, etc.)
- `summary.json` with endpoint counts and errors

## 5) Notes

- Export continues even when specific endpoints are unavailable for account/scope.
- Tokens auto-refresh during export.
- `python3` + `requests` are required.
