---
name: sync-adapter
version: 1.0.0
description: "Sync local .md data files to Google Sheets with dedup hashing. Reusable for expenses, investments, and any key-value data."
allowed-tools: [cron, exec, read, write]
---

# Sync Adapter

Pattern for syncing structured `.md` data to Google Sheets. Uses a service account, JWT auth, and content-hash dedup to avoid duplicates.

## Authentication

- Service account: `/home/hobopi/.openclaw/secrets/google-service-account.json`
- JWT flow: sign with RSA256, exchange for access token
- Sheet API: `https://sheets.googleapis.com/v4/spreadsheets/{id}`
- Spreadsheet ID: `1Ikbydh-Xzc6F3pk1Q5lbCTbdEERSb4Hq8obzbABVZbU`

## Dedup strategy

**Key generation:** `(normalized_date|normalized_amount|notes)`
- `normalize_amount(str)` — strips trailing zeros from decimal: `$18.00` → `$18`, `$18.50` → `$18.50`
- This prevents float vs string mismatches between ledger (`$18.00` as float `18.0`) and sheet (`18` as string)

**Flow:**
1. Read all ledger `*.md` files → parse entries
2. Read all existing sheet rows → build set of dedup keys
3. Filter: only entries whose key not already in set
4. Append new entries only

## Parsing ledger format

```python
m = re.match(r'^- ([^$]+) \$([0-9]+\.?[0-9]*) \| (.+)', line)
```

Parses: `- Category $Amount | Notes`

Investment format:
```python
m = re.match(r'^- ([^$]+) \$([0-9.]+)(?: \| (.+))?', line)
```

## Sync implementations

### Expense sync (daily 9:30am)
- Script: `scripts/sync-ledger-to-sheet.py`
- Tab: `Sheet1`
- Columns: Date, Category, Amount (SGD), Notes
- Pinned to `deepseek/deepseek-v4-flash`, timeout 60s

### Investment sync (Saturday 11am)
- Script: `scripts/sync-investments-to-sheet.py` (or agent reads ledger + writes to sheet directly)
- Tab: `Investments`
- Columns: Date, Type (DEPOSIT/WITHDRAW), Amount (SGD), Notes
- Type field: positive → DEPOSIT, negative → WITHDRAW
- Pinned to `deepseek/deepseek-v4-flash`, timeout 600s

## API notes

- Use `valueInputOption: 'USER_ENTERED'` for date/currency formatting
- Date format: `YYYY-MM-DD` (string) — prevents auto-conversion to different format
- Amount: send as number (float), not string — prevents `'` prefix
- Find last row: read column A, count non-empty cells
- Append: start after last populated row
- Never modify existing rows — append only
