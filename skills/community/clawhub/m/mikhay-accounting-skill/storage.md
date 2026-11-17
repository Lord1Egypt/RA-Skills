# Storage Layout

Use year/month shards for real ledgers. Agents should open only the shard needed for the user request.

## Recommended Tree

```text
data/
  ledger/
    2026/
      2026-06.json
      2026-07.json
  assets/
    2026/
      2026-06.assets.json
  wishlist/
    2026/
      wishlist.json
  accounts.json
  categories.json
  settings.json
  import_rules.json
  recurring.json
  items/
    items.json
raw/
  2026/
    2026-06/
exports/
  2026/
reports/
  2026/
```

## Rules

- Store transaction records by month: `data/ledger/YYYY/YYYY-MM.json`.
- Or by day: `data/ledger/YYYY/YYYY-MM/YYYY-MM-DD.json`.
- Shard keys come from `os.path.basename`. Do not slice the full path. `data/ledger/2026/2026-06.json` is month `2026-06`; a bad slice of that path produces `r/202`.
- Store asset snapshots separately when they are not part of the monthly ledger: `data/assets/YYYY/YYYY-MM.assets.json`.
- Store planned purchases separately: `data/wishlist/YYYY/wishlist.json`.
- Store the user's accounts, account aliases (including history windows), and investment-account flags in `data/accounts.json`; custom categories in `data/categories.json`; base currency and investment redemption marker in `data/settings.json`; import keyword rules in `data/import_rules.json`. All scripts read them when present, and every command accepts the matching `--accounts` / `--categories` / `--settings` / `--import-rules` argument.
- Store fixed expenses in `data/recurring.json`. Side files are discovered next to the ledger as well as in `data/`. `scripts/lint_ledger.py` reads them and does not modify the ledger.
- Store subscriptions and holdings in `data/items/items.json`. Active subscriptions are also fixed expenses for lint.
- Keep raw third-party bills under `raw/YYYY/YYYY-MM/`.
- Keep generated CSV/JSON exports under `exports/YYYY/`.
- Keep generated reports under `reports/YYYY/`.
- Do not load all shards for normal tasks. Pick months first, then run scripts on those files.
- For cross-year statistics, summarize each month first and merge totals instead of asking the model to read all records.

## Import Command

```bash
python scripts/import_ledger.py raw/bill.csv --split-by-month --year-dirs --output data/ledger
python scripts/import_ledger.py raw/bill.csv --shard day --year-dirs --output data/ledger
python scripts/import_ledger.py raw/bill.csv --shard month --year-dirs --output data/ledger
```
