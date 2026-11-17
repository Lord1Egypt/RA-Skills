# Agent Handoff

Use this folder as a self-contained accounting skill. Skill version `0.4.2` lives in `SKILL.md` frontmatter. Ledger `schema_version` stays `0.3.0`; unedited `0.2.0` books still validate. Homepage: https://github.com/MikhayEeer/mikhay-accounting-skill. The ledger stays on the local machine and is not uploaded. This skill is for Chinese personal ledgers. `slug` stays `mikhay-accounting-skill`.

## Start

1. Read `SKILL.md`. When a record looks wrong, read `references/faq.md`. When a command fails, read `references/troubleshooting.md`.
2. Read `schema.md` before editing ledger data.
3. Read `categories.md` and `accounts.md` before classifying records. Define the user's real accounts in `data/accounts.json` (with `别名`) and categories in `data/categories.json`.
4. Read `storage.md` before locating or writing real ledger files.
5. Import third-party bills when needed:

```bash
python scripts/import_ledger.py <bill.csv-or-xlsx> --shard month --year-dirs --output data/ledger
```

If any target shard already exists, the script aborts the whole batch and writes nothing. Back up `data/` before re-running with `--overwrite`. That flag replaces each target file and can drop records missing from the new bill.

6. Run validation before statistics. Totals must come from these scripts, never hand math:

```bash
python scripts/validate_ledger.py <ledger.csv-or-json-or-directory>
python scripts/summarize_ledger.py <ledger-or-directory>
python scripts/summarize_tags.py <ledger-directory>
```

7. Query assets, debt, net assets, installments, and reminders when needed:

```bash
python scripts/summarize_assets.py <ledger-or-assets.json> --cc-method A
python scripts/summarize_assets.py <ledger-or-assets.json> --forecast
python scripts/project_assets.py <assets.json> <ledger.json>
```

8. Analyze planned purchases when needed:

```bash
python scripts/analyze_wishlist.py <wishlist.json> --ledger <month-ledger.json> --assets <assets.json>
```

9. Export standard JSON when needed:

```bash
python scripts/export_ledger.py <ledger.json> --output exports/ledger.csv
```

Validation warns instead of failing on unknown accounts and categories; `--strict` turns those warnings into errors. There is no payday guess: `--forecast` reports card statements, repayments, due dates, and the current-month cash flow only. Tag namespaces are free-form. Refunds, reimbursements, and AA are normally netted in place on the original row: a fully settled item becomes `金额=0`, a partial one keeps the remainder, and an over-settlement becomes an `收入` row for the difference.

Direct asset edits should report the ledger-derived difference and ask before creating adjustment records.

## Data Safety

Do not print full real ledgers unless the user asks.

Private data should stay in ignored folders:

- `data/`
- `raw/`
- `exports/`
- `private/`
- `real/`

Preferred ledger shards:

- `data/ledger/YYYY/YYYY-MM.json`
- `data/ledger/YYYY/YYYY-MM/YYYY-MM-DD.json`
- `data/assets/YYYY/YYYY-MM.assets.json`
- `data/wishlist/YYYY/wishlist.json`
- `data/accounts.json`
- `data/categories.json`
- `data/settings.json`
- `data/import_rules.json`

## Package

Maintainer-only. `tools/package_skill.py` is not part of the end-user skill. ClawHub publish ignores `tools/` (`.clawhubignore`), and the archive omits `tools/` and `package_skill.py`.

```bash
python tools/package_skill.py
```

Share files from `dist/`.
