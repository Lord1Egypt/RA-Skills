---
name: oura-api-complete-export
description: Authenticate with an Oura OAuth app (client id/secret + redirect URI), store and refresh tokens, and export all available Oura v2 usercollection datasets to JSON files. Use when the user asks for full Oura backup/raw export, end-to-end Oura auth setup, or repeatable data pulls for analysis/ETL.
---

# Oura API Complete Export

Use this skill to set up OAuth auth for Oura and export all available Oura data into JSON.

## Folder structure

- `SKILL.md`
- `README.md`
- `scripts/auth_oura_oauth.py`
- `scripts/export_oura_data.py`
- `scripts/run_full_export.sh`
- `references/endpoints.md`

## Workflow

1. Run OAuth auth once:
   ```bash
   python3 scripts/auth_oura_oauth.py --client-id <CLIENT_ID> --client-secret <CLIENT_SECRET> --redirect-uri http://localhost:8765/callback
   ```
2. Run export:
   ```bash
   python3 scripts/export_oura_data.py --start 2020-01-01 --end $(date +%F) --out ./oura_export
   ```
3. For convenience:
   ```bash
   ./scripts/run_full_export.sh 2020-01-01 $(date +%F) ./oura_export
   ```

## Behavior

- Refresh token automatically before/when needed.
- Follow paginated endpoints automatically.
- Continue export on per-endpoint failures and log errors.
- Keep raw payloads in endpoint-specific JSON files for downstream tools.
