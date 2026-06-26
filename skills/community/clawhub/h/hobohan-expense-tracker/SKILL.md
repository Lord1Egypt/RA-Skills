---
name: expense-tracker
version: 1.0.0
description: "Log daily expenses via check-in prompts; dedup, categorize, sync to local ledger and Google Sheets."
allowed-tools: [cron, read, write, edit, exec]
---

# Expense Tracker

Track daily spending via Telegram check-ins. Three prompts per day; cron-driven. All data flows to local `.md` ledger + Google Sheet.

## Ledger format

Each file at `ledger/YYYY-MM-DD.md`:

```markdown
# Ledger — 2026-06-03

- Food & Drinks $1.80 | Coffee
- AI $11.53 | Netlify
```

Format: `- Category $Amount | Notes`

## Categories

**Allowed:** Food & Drinks | Groceries | Transportation | Household/Utilities | Pet | Shopping | Entertainment | Other | AI

- Bakery bread → Food & Drinks (NOT Groceries)
- Groceries = supermarket bulk/household runs
- Unsure → ask Hobo or default to Other with note

## Check-in schedule

| Time | Prompt |
|------|--------|
| 10am | Morning spend (coffee, breakfast, transport) |
| 1:30pm | Afternoon spend (lunch, transport) |
| 10pm | End-of-day recap |

Each check-in runs as an isolated cron agentTurn with `model: deepseek/deepseek-v4-flash` and `timeoutSeconds: 300`.

### Transport check-in (9am, previous day)

Separate cron asks: "Any transport yesterday?" Pinned to `deepseek/deepseek-v4-flash`.

## Dedup rules

Before writing to today's ledger file:

1. **Read** today's ledger file first.
2. **Time qualifiers** (morning/afternoon/evening coffee): always ADD new entry, never replace.
3. **Same category + amount**: assume repeat purchase → ADD new entry.
4. **Only REPLACE** if Hobo explicitly says "change X to Y".
5. **When in doubt** → ask Hobo to confirm.

## Expense sync

Daily at 9:30am via `scripts/sync-ledger-to-sheet.py`:
- Reads all `ledger/*.md` files
- Parses entries per format above
- Generates dedup key: `(normalized_date|normalized_amount|notes)` where `normalize_amount()` strips trailing zeros
- Compares against existing sheet rows → appends only new ones
- Uses Google Sheets API with service account at `/home/hobopi/.openclaw/secrets/google-service-account.json`
- Sheet ID: `1Ikbydh-Xzc6F3pk1Q5lbCTbdEERSb4Hq8obzbABVZbU`, tab: `Sheet1`

## Historical backfill

To backfill missing days (e.g., April 18-26 reconstructed from sheet data):
1. Query sheet for all rows with dates not in ledger
2. Parse each row as `Date, Category, Amount, Notes`
3. Create `ledger/YYYY-MM-DD.md` with entries in correct format
4. Verify count matches between ledger and sheet

## Scripts

- `scripts/sync-ledger-to-sheet.py` — main sync engine
- `scripts/gen-expense-data.py` — dumps all entries to JSON for dashboard

## Cron notes

- All expense crons MUST pin model to `deepseek/deepseek-v4-flash` (time-sensitive)
- Timeout: 300s minimum (600s for 10pm check-in)
- Use absolute paths only in payload messages — no `cd && python3` chains
