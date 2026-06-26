# refresh_token acquisition and storage

## Acquisition

Prefer getting the iFinD `refresh_token` directly by agent-operated browser flow:

1. Open `https://quantapi.51ifind.com`
2. Use the existing browser login session if available
3. If login is required, let the user complete or approve the login interactively
4. Go to the account information page
5. Read the `refresh_token`
6. Store it immediately through the token store script

Secondary source:

- iFinD 超级命令客户端 → 工具 → `refresh_token` 查询

Fallback only when needed:

- Ask the user to provide the token directly

## Storage

This skill stores the token at:

- `~/.openclaw/skills/ifind/credentials.json`

Example structure:

```json
{
  "refresh_token": "...",
  "updated_at": "2026-03-15T10:00:00+08:00"
}
```

## Rules

- Write only through `scripts/ifind_token_store.py`
- Do not log the token
- Do not print the token after reading it from the browser
- Do not paste the token into shell history if avoidable
- Tighten file permissions after writing
- Prefer environment override only for temporary one-off runs
- Before running API scripts, make sure Python dependency `requests` is available; if not, install it with `python3 -m pip install -r scripts/requirements.txt`

## Commands

```bash
python3 scripts/ifind_token_store.py status
python3 scripts/ifind_token_store.py set --token '<TOKEN>'
python3 scripts/ifind_token_store.py remove
```

`status` reports only whether the token exists and where it is stored. It must never print the token value.
