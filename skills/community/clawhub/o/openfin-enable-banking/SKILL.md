---
name: openfin-enable-banking
description: "PSD2 Open Banking integration via Enable Banking API. Connect DACH bank accounts (Sparkasse, Volksbank, Deutsche Bank, Commerzbank, DKB, ING, Postbank + Austrian banks) to fetch balances and transactions. Multi-mandant architecture with 3 modes: onboard, fetch, renew. Designed for tax advisory automation."
license: MIT
---

# Enable Banking Skill

**PSD2 Open Banking integration via Enable Banking API.**
Multi-mandant architecture for onboarding bank connections, fetching balances/transactions, and session renewal.

## Quick Start

```
# 1. Onboard a new mandant
python scripts/onboard.py --bank "Sparkasse Karlsruhe" --country DE --mandant-id mueller

# 2. Fetch balances + transactions
python scripts/fetch.py --mandant-id mueller

# 3. Renew an expired session
python scripts/renew.py --mandant-id mueller
```

## Architecture

```
┌─────────────┐     POST /auth      ┌──────────────────────┐
│  onboard.py │ ──────────────────→  │  Enable Banking API  │
│  renew.py   │ ←── redirect_url ──  │  api.enablebanking.com│
└──────┬──────┘                      └──────────┬───────────┘
       │                                        │
       │ poll pending_callbacks/                 │ User authorizes
       │                                        │ at bank portal
       ▼                                        ▼
┌──────────────────┐    GET /callback    ┌─────────────┐
│ callback_server  │ ←───────────────── │  Bank OAuth  │
│ (port 8443 HTTPS)│                    │  Redirect    │
└──────────────────┘                    └─────────────┘
       │
       │ saves code → pending_callbacks/{state}.json
       │
       ▼
┌─────────────┐     POST /sessions    ┌──────────────────────┐
│  onboard.py │ ──────────────────→   │  Enable Banking API  │
│  renew.py   │ ←── session + accs ── │                      │
└──────┬──────┘                       └──────────────────────┘
       │
       │ saves mandanten/{id}.json
       ▼
┌─────────────┐  GET /accounts/{uid}/ ┌──────────────────────┐
│  fetch.py   │ ──────────────────→   │  Enable Banking API  │
│             │ ←── balances + txns ──│                      │
└──────┬──────┘                       └──────────────────────┘
       │
       │ saves data/{id}/{date}.json
       ▼
   stdout: JSON
```

## Directory Structure

```
enable-banking/
├── SKILL.md              # This file
├── config.json           # App credentials (DO NOT COMMIT)
├── .keys/                # Private key + callback certs (DO NOT COMMIT)
├── .gitignore
├── scripts/
│   ├── lib/
│   │   ├── __init__.py
│   │   └── auth.py       # Shared JWT + API helpers + mandant I/O
│   ├── callback_server.py   # HTTPS callback daemon
│   ├── onboard.py           # New mandant connection
│   ├── fetch.py             # Autonomous data fetch
│   └── renew.py             # Session renewal
├── references/
│   └── api-reference.md
├── mandanten/            # Per-mandant JSON files (DO NOT COMMIT)
├── data/                 # Fetched data (DO NOT COMMIT)
└── pending_callbacks/    # Temporary callback codes (DO NOT COMMIT)
```

## Scripts Reference

### `scripts/lib/auth.py` — Shared Module

| Function | Description |
|---|---|
| `load_config()` | Load `config.json` |
| `generate_jwt(config)` | RS256 JWT for API auth |
| `api_request(method, endpoint, token, **kwargs)` | Authenticated API call with retry (429, timeout) |
| `load_mandant(mandant_id)` | Load `mandanten/{id}.json` |
| `save_mandant(mandant_id, data)` | Save mandant file (chmod 600) |
| `list_mandanten()` | List all mandant IDs |

### `scripts/callback_server.py` — HTTPS Callback Server

```bash
python scripts/callback_server.py              # Port 8443 (HTTPS)
python scripts/callback_server.py --port 9443  # Custom port
python scripts/callback_server.py --no-ssl     # HTTP only (dev)
```

- Auto-generates self-signed cert in `.keys/` on first run
- `GET /callback?code=...&state=...` → saves to `pending_callbacks/{state}.json`
- `GET /health` → 200 OK
- Run as background process: `exec background:true command:"python scripts/callback_server.py"`

### `scripts/onboard.py` — Mandant Onboarding

```bash
# Connect a new mandant
python scripts/onboard.py --bank "Sparkasse Karlsruhe" --mandant-id mueller

# With manual auth code (no callback server needed)
python scripts/onboard.py --bank "Sparkasse Karlsruhe" --mandant-id mueller --code ABC123

# List available banks
python scripts/onboard.py --list-banks --country DE

# Business account
python scripts/onboard.py --bank "DKB" --mandant-id firma --psu-type business
```

**Flow (without `--code`):**
1. POST /auth → generates redirect URL
2. Prints URL to stdout (agent sends via WhatsApp/email)
3. Polls `pending_callbacks/{state}.json` (needs callback_server running)
4. POST /sessions with code
5. Saves `mandanten/{id}.json`

### `scripts/fetch.py` — Autonomous Data Fetch

```bash
# Single mandant
python scripts/fetch.py --mandant-id mandant-1

# All mandanten
python scripts/fetch.py --all

# Date range
python scripts/fetch.py --mandant-id mandant-1 --date-from 2026-03-01 --date-to 2026-03-10

# Only balances or transactions
python scripts/fetch.py --mandant-id mandant-1 --balances-only
python scripts/fetch.py --mandant-id mandant-1 --transactions-only
```

- Default date range: last 30 days
- Saves to `data/{mandant-id}/{YYYY-MM-DD}.json`
- Updates `lastFetch` in mandant file
- Exit code 2: session expired (needs renewal)

### `scripts/renew.py` — Session Renewal

```bash
python scripts/renew.py --mandant-id mueller
python scripts/renew.py --mandant-id mueller --code ABC123
```

- Uses bank + country from existing mandant file
- Same auth flow as onboard
- Keeps backup of previous session in mandant file

## Mandant Data Format

`mandanten/{id}.json`:
```json
{
  "mandantId": "mueller",
  "bank": "Sparkasse Karlsruhe",
  "country": "DE",
  "psuType": "personal",
  "sessionId": "cbe3cd33-...",
  "accounts": [
    {
      "uid": "2818be38-...",
      "iban": "DE17...",
      "name": "Max Mueller",
      "currency": "EUR",
      "product": "Sichteinlagen"
    }
  ],
  "validUntil": "2026-09-06T07:18:35Z",
  "createdAt": "2026-03-10T08:18:00Z",
  "lastFetch": null
}
```

## Fetch Output Format

`data/{id}/{date}.json` and stdout:
```json
{
  "mandantId": "mueller",
  "fetchedAt": "2026-03-10T08:00:00Z",
  "accounts": [
    {
      "uid": "...",
      "iban": "DE17...",
      "name": "Max Mueller",
      "balances": [
        {"type": "CLBD", "amount": "-993.13", "currency": "EUR", "date": "2026-03-10"}
      ],
      "transactions": [
        {
          "date": "2026-03-02",
          "amount": "-171.00",
          "currency": "EUR",
          "creditDebit": "DBIT",
          "counterparty": "...",
          "description": "...",
          "bookingDate": "2026-03-02",
          "valueDate": "2026-03-02"
        }
      ]
    }
  ]
}
```

## Dependencies

- Python 3.10+
- PyJWT (`pip install PyJWT`)
- cryptography (`pip install cryptography`)
- requests (`pip install requests`)

## Deployment

**Local (dev/test):**
- Callback server uses self-signed cert
- Works with `--code` flag (manual code entry, no server needed)

**VPS (production):**
- Run callback_server.py behind nginx/caddy with real SSL
- Point `redirectUrl` in config.json to your domain
- Use cron for scheduled `fetch.py --all` runs

## Troubleshooting

| Issue | Solution |
|---|---|
| `401 Unauthorized` | Check applicationId + key match in Enable Banking portal |
| `403 Forbidden` | Session expired → `python renew.py --mandant-id <id>` |
| Exit code 2 | Session expired → renew |
| `Port already in use` | Kill existing: `lsof -i :8443 \| grep LISTEN \| awk '{print $2}' \| xargs kill` |
| No callback received | Check callback_server is running, firewall allows port |
| Rate limited (429) | Auto-retried; if persistent, wait and retry later |
