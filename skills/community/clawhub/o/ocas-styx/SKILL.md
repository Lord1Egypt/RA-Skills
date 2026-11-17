---
license: MIT
name: ocas-styx
description: Transaction data store with merchant enrichment. Provides a clean, queryable
  interface over raw bank transaction data. Enriches garbled/obfuscated transaction
  names into real business entities using SearXNG search plus LLM resolution. Includes
  financial sync (Plaid API) for pulling transactions and balances daily. Other skills
  (Taste, Rally, Vesper, Sands) read from Styx for consumption signals, spending
  analysis, and pattern detection. NOT for creating transactions (use bank), budgeting
  strategy (use Rally), or email-based consumption scanning (use Taste).
source: https://github.com/<agent-handle>/styx
includes:
- references/**
- scripts/**
metadata:
  author: Indigo Karasu (indigokarasu)
  version: "1.5.0"
  hermes:
    category: data-science
    tags:
    - transactions
    - finance
    - merchant-enrichment
    - banking
tags:
- transactions
- finance
- merchant-enrichment
- banking
- data-store
triggers:
- transaction data
- bank transactions
- merchant enrichment
- financial data store
- query transactions
---

# Styx — Transaction Data Store

Styx is the system's transaction intelligence layer. It sits between raw bank
data (from Plaid via financial-sync) and consumer skills that need clean
merchant information (Taste, Rally, Vesper, Sands).

## When to Use

- Enriching garbled/obfuscated transaction names into real business entities
- Merchant lookup and business matching from transaction data
- Answering "what did I spend" or "where did I spend" questions
- Pulling/syncing bank transactions via Plaid API
- Spending analysis, pattern detection, or calendar-based spending context
- Providing clean merchant data to consumer skills (Taste, Rally, Vesper, Sands)
- Parsing email receipts (e.g., Rainbow Grocery eReceipts) and storing line items in `receipt_line_items` table

## When NOT to Use

- Budgeting strategy or financial planning (use Rally)
- Email-based consumption scanning (use Taste)
- Creating or modifying transactions (use your bank directly)
- General web research or non-transaction search (use Sift)
- Account management (adding/removing bank links) — use Plaid Link flow directly

## Workflow

Styx operates a continuous ingest-enrich-serve workflow because raw transaction data requires normalization before it becomes useful to downstream skills.

- [ ] **Ingest** — Pull transactions from Plaid API (daily cron or on-demand)
- [ ] **Enrich** — Resolve garbled merchant names via SearXNG search + LLM resolution
- [ ] **Store** — Write enriched records to SQLite database
- [ ] **Serve** — Expose query API for consumer skills (Taste, Rally, Vesper, Sands)

Example: a transaction from "UNK MERCHANT 1234" is enriched via SearXNG search → identified as "Whole Foods Market" → stored with clean merchant name → Taste queries for spending patterns.

## Core principles

1. **Raw data is sacred** — transaction records from Plaid are never modified.
   Enrichment data lives in separate tables, linked by transaction_id.
2. **Append-only** — Styx only adds new records. It never deletes or updates
   raw transactions. Enrichment records can be superseded (marked stale) but
   not deleted.
3. **Read-only for consumers** — other skills query Styx via the query API
   or read the SQLite DB directly. They do NOT write to Styx tables.
4. **Enrichment is idempotent** — running enrichment on already-enriched
   transactions produces the same result. Safe to re-run.

## Data flow

See `references/data-flow.md` for the data flow diagram.

## Database

Styx maintains its own SQLite database at `<hermes-home>/data/styx.db`.
**IMPORTANT:** Hardcode this path. Do NOT use `{agent_root}` — it resolves to the indigo profile home, not the shared data directory.

The active DBs are:
- `<hermes-home>/data/transactions.db` — raw Plaid transaction data (1,187 transactions, last: 2026-06-24)
- `<hermes-home>/data/styx.db` — enriched merchant data (1,193 transaction_merchants links, 493 merchants)

**Note:** Plaid `/transactions/sync` cursor can get stuck and miss transactions. If `MAX(date)` is stale, use `/transactions/get` backfill pattern (see `references/plaid-sync-cursor-recovery.md`). Sync cursors reset after backfill.

A second copy exists at `<hermes-home>/commons/data/ocas-styx/styx.db` but it is a stale 0-byte stub — ignore it.

### Schema

Three core tables: `merchants`, `transaction_merchants`, `enrichment_runs`.
Receipt parsing table: `receipt_line_items` (23 columns — see below).
Full DDL: [`references/schema.md`](references/schema.md)

### receipt_line_items Table (23 columns)

Used for storing parsed email receipt line items (e.g., Rainbow Grocery eReceipts).

See `references/receipt-line-items-insert.md` for the correct INSERT pattern and gotchas.

## Enrichment pipeline

### Google Places Enrichment (All Categories)

The enrichment pipeline resolves garbled/obfuscated transaction names into real businesses.
The **default script only enriches food merchants**. For full coverage, use the 
**universal enrichment script**:

**Script:** [`styx_universal_enrichment.md`](references/styx_universal_enrichment.md) ← read this reference first

```bash
# Universal enrichment — all non-financial categories
# Created 2026-06-20. Script exists at:
# <hermes-home>/profiles/indigo/skills/ocas-styx/scripts/styx_universal_enrich.py
# references/styx_universal_enrichment.md if needed.
# Last known path (may not exist): <hermes-home>/commons/data/ocas-styx/styx_universal_enrich.py

# Food-only (original script) — confirmed working
python3 <hermes-home>/profiles/indigo/skills/ocas-styx/scripts/styx_places_enrich.py --all
```

**Categories covered by universal script:** retail, service, entertainment, transport,
personal_care, medical, home, government, housing, travel, food/restaurant (all 10 food subcategories).

**Categories skipped (no physical location):** transfer, income, bank_fees, loan_payments,
loan_disbursements. These get `source: 'internal'`.

### Legacy LLM Enrichment Pipeline

For garbled names that Google Places can't resolve: exact match → fuzzy match → SearXNG search → LLM resolution → manual review queue. Full details: [`references/enrichment-pipeline.md`](references/enrichment-pipeline.md)

## Query API

Other skills read from Styx using these patterns:
- **Category transactions**: enriched transactions filtered by merchant category
- **Spending by merchant**: aggregated totals and visit counts
- **Unresolved transactions**: candidates needing enrichment

DB path: `{agent_root}/data/styx.db`

## Receipt Parsing Pipeline

When parsing email receipts (e.g., Rainbow Grocery):
1. **Fetch emails** via `get_gmail_messages_content_batch` — large results persisted to `/tmp/hermes-results/<uuid>.txt`
2. **Parse persisted files** — XML wrapper around JSON requires brace-depth counting to extract first complete JSON object
3. **Extract bodies** — split by `\n\nMessage ID: `, then extract between `--- BODY ---` and `---\n\n`
4. **Parse line items** — handle department headers, PLU/UPC codes, prices, weight/quantity info
5. **Write to Styx** — use the `receipt_line_items` INSERT pattern above (22 values, `id` auto-increments)

## Consumer skill contracts

### Taste
Taste reads from Styx to discover restaurants and food businesses that <operator>
has transacted with but that didn't appear in email/calendar.

Taste queries:
- `m.category IN ('restaurant', 'cafe', 'bar', 'food')` for dining
- `m.category IN ('grocery', 'supermarket', 'food_store')` for food shopping
- Transactions with `personal_finance_category = 'FOOD_AND_DRINK'` as fallback

Taste does NOT write to Styx. It writes to its own `signals.jsonl` and `items.jsonl`.

### Rally
Rally reads from Styx for spending analysis and budget tracking.

### Vesper
Vesper reads from Styx for daily/weekly spending summaries in briefings.

### Sands
Sands reads from Styx for calendar-based spending context.

## Security
- Styx DB is read-only for consumer skills (enforced by skill contract, not filesystem)
- Raw transaction data in transactions.db is never modified by Styx
- Enrichment data is additive only

## Financial Sync
- Sync script: `{skill_root}/scripts/plaid_sync.py` (incremental, daily 7 AM cron)
- History script: `{skill_root}/scripts/plaid_history.py` (full 24-month pull)
- DB: `{agent_root}/data/transactions.db` (raw, read-only)
- Cron job `a418e00ee21e`: daily 7 AM, `no_agent: true`

## Gotchas

Error handling in styx follows a strict never-modify-raw-data policy: if enrichment fails, log the error, mark the record as unresolved, and continue processing.

- **Self-update: untracked files block `git pull`** — `git stash` only stashes tracked files. New (untracked) files in the skill directory will block the merge. Move them aside before pulling, then compare/restore afterward.
- **Self-update: stash pop may conflict** — After pulling, `git stash pop` can produce merge conflicts if both the pulled changes and the stashed changes touch the same lines.
- **`query.py --health-check` does not exist** — Use inline Python to verify DB integrity instead.
- **Raw transaction data is sacred** — Styx never modifies or deletes records in `transactions.db`.
- **Name cleaning is essential** — Plaid transaction names are heavily obfuscated (e.g., `DD *DOORDASH ROYALINDI`, `ABM-350 MISSION GARAGE`). Strip prefixes before matching.
- **Redacted names can't be enriched** — Transactions with fully redacted names (`***************`) are skipped entirely.
- **Consumer skills are read-only** — Taste, Rally, Vesper, and Sands query Styx but must never write to Styx tables.
- **receipt_line_items INSERT requires 22 values** — The table has 23 columns but `id` auto-increments.
- **`google_auth_mcp` import path is profile-dependent** — When running under the `indigo` Hermes profile, `Path.home()` returns `<hermes-home>/profiles/indigo/home` instead of `/root`. Scripts that do `sys.path.insert(0, str(Path.home() / '.hermes' / 'scripts'))` or `sys.path.insert(0, str(AGENT_ROOT / 'scripts'))` will fail to find `google_auth_mcp.py`. **Fix:** Hardcode `sys.path.insert(0, str(Path('<hermes-home>/scripts')))` in any script that imports `google_auth_mcp`. **Affected scripts (all fixed as of 2026-06-04):** dispatch: `triage.py`, `check_unread.py`, `gmail_search.py`, `gmail_scan.py`; taste: `email_scan.py`, `run_historical_scans.py`; scripts: `email_check.py`, `dream_journal_pipeline.py`.
- **the agent's OAuth token file may lack `client_secret`** — The token file at `<gworkspace-creds>/credentials/<third-party-or-user-email>.json` may only have `access_token`, `refresh_token`, `client_id` — but `google_auth_mcp.py` needs `client_secret` for token refresh and a `token` key alias. **Fix:** Add `client_secret` from the cached client secret file. Also add `token` as an alias for `access_token` and `token_uri: 'https://oauth2.googleapis.com/token'`.
- **Database and secrets path mismatch (migration artifact)** — After a profile/data migration, the active databases live at `<hermes-home>.old/data/` (`styx.db`, `transactions.db`) and secrets at `<hermes-home>.old/secrets/plaid.env`, but all scripts hardcode `<hermes-home>/data/` and `<hermes-home>/secrets/`. **Workaround:** Create symlinks before running scripts:
  ```bash
  mkdir -p <hermes-home>/data
  ln -sf <hermes-home>.old/data/styx.db <hermes-home>/data/styx.db
  ln -sf <hermes-home>.old/data/transactions.db <hermes-home>/data/transactions.db
  ln -sf <hermes-home>.old/secrets <hermes-home>/secrets
  ```
  The universal enrichment script at `<hermes-home>.old/commons/data/ocas-styx/styx_universal_enrich.py` (not in the skill's `scripts/` or `commons/data/`) must be run from that location.
- **<operator>'s token refresh adds `access_token` key** — When refreshing <operator>'s token, the Google OAuth response includes `access_token` (not `token`). The original file used `token` as the key. After refresh, both keys exist. `google_auth_mcp.py` reads `token_data.get("token")`, so ensure the `token` key is present.
- **styx.db may exist with no tables** — The DB file can be created empty (0 bytes) by the skill initialization script without the schema being applied. Before any receipt parsing or enrichment, verify tables exist.
- **`llm_resolve.py` does NOT work in cron/background context** — The script calls `hermes ask --no-stream` via subprocess, which returns no output when there is no interactive session.
- **styx_places_enrich.py is food-only** — The original enrichment script only covers food/restaurant categories. Use `styx_universal_enrich.py` for all categories. See `references/styx_universal_enrichment.md`.
- **SearXNG port is 8888** — The `enrich.py` script defaults to `http://localhost:8888` (not 8880). If SearXNG errors with "Connection refused", verify the container port mapping: `docker ps | grep searx`.
- **styx_universal_enrich.py created 2026-06-20** — Now exists at `<hermes-home>/profiles/indigo/skills/ocas-styx/scripts/styx_universal_enrich.py`. Covers retail, service, entertainment, transport, personal_care, medical, home, government, housing, travel. Skips financial categories (transfer, income, bank_fees, loan_payments, loan_disbursements). Run: `python3 styx_universal_enrich.py --limit 0` to enrich all pending non-food merchants. Includes name cleaning (strips FSP*, SP , ABM-, etc.) and international address parsing (UK postcodes, city-only addresses).
- **Correct script path for food-only enrichment** — The food-only script lives at `<hermes-home>/profiles/indigo/skills/ocas-styx/scripts/styx_places_enrich.py`, NOT at `<hermes-home>/skills/ocas-styx/scripts/styx_places_enrich.py` (that path doesn't exist).
- **Taste enrichment fails on LLM items in cron** — `taste_full_enrich.py` reports "Failed: N" for items requiring LLM resolution. This is because `llm_resolve.py` calls `hermes ask --no-stream` which returns no output in non-interactive/cron context. These items are not lost — they remain in the Taste items queue and will be retried on the next interactive or non-cron enrichment run. Do NOT treat these failures as pipeline errors.
- **No new transactions ≠ no work** — When Plaid sync hasn't pulled new data (check `MAX(date)` in transactions.db), `styx_universal_enrich.py` may still find 5–15 merchants to re-enrich. This is normal: the script re-queriers pending/unresolved merchants against Google Places on each run. `no_result` responses are expected for heavily obfuscated names (e.g., `DD *DOORDASH *********`, `SP THANKS ICON`).

## Cron pipeline (daily enrichment)

When invoked as a scheduled cron job, run the full pipeline in sequence:

```bash
# Step 1: Universal merchant enrichment (all categories)
python3 <hermes-home>/profiles/indigo/skills/ocas-styx/scripts/styx_universal_enrich.py

# Step 2: Ingest enriched merchants into Taste
python3 <hermes-home>/commons/data/ocas-taste/scripts/taste_full_enrich.py

# Step 3: Deduplicate same-day Taste signals
python3 <hermes-home>/commons/data/ocas-taste/scripts/taste_signals_dedup.py
```

**Taste signal emission:** Steps 2–3 satisfy the consumption-signal contract — enriched merchant records (with Taste categories) are ingested into Taste and consumption signals are emitted to Taste's intake (deduped same-day). This is the canonical Styx→Taste enrichment path; do not bypass it. See `spec-ocas-suite-cross-skill-updates.md` (Preference & Data layer).

**IMPORTANT script paths:**
- `styx_universal_enrich.py` is at `<hermes-home>/profiles/indigo/skills/ocas-styx/scripts/` (NOT `<hermes-home>/commons/data/ocas-styx/`)
- Taste scripts are at `<hermes-home>/commons/data/ocas-taste/scripts/`

**Expected cron behaviors:**
- If no new transactions since last sync, `styx_universal_enrich.py` may still find a small number (5–15) of merchants to re-enrich. These are already-enriched merchants being re-queried against Google Places. `no_result` is expected for garbled names that Google can't match — the existing enrichment from prior runs (searxng, plaid_merchant_name, internal) is preserved.
- `taste_full_enrich.py` may report "Failed: N" for items that need LLM resolution. This is a known cron limitation (`llm_resolve.py` calls `hermes ask` which returns no output without an interactive session). Items will be retried on the next non-cron enrichment run.

**Report format:** After cron run, report: merchants enriched by category, new Taste items created, signals deduped, and any errors. See `references/cron-gotchas.md` for expected cron behaviors that are NOT errors.

## Post-enrichment verification

After every enrichment run, verify the results before marking the run as complete:
1. Spot-check 5–10 enriched `transaction_merchants` records at random.
2. Confirm the `enrichment_runs` table row for this run shows status `completed`.
3. Verify `review_queue.jsonl` has been updated with any new low-confidence matches.

## Automation

### Self-update
Pull the latest Styx package from GitHub source. Full procedure: `references/self_update.md`.

## Support File Map

| File | When to read |
|---|---|
| `references/styx_universal_enrichment.md` | Before running Google Places enrichment — use this instead of the food-only default |
| `references/financial-sync.md` | Before configuring Plaid sync |
| `references/scripts.md` | Before running enrichment or query scripts |
| `references/schema.md` | Before querying or modifying the database |
| `references/query-api.md` | Before writing consumer queries |
| `references/enrichment-pipeline.md` | Before running or debugging LLM enrichment |
| `references/styx_universal_enrichment.md` | Before running Google Places enrichment (read FIRST) |
| `references/self_update.md` | Before running self-update |
| `references/cron-gotchas.md` | Before debugging cron enrichment failures |
| `references/verify-bank-alert.md` | Before cross-checking a bank/card email alert against local ledger |

## Files

See `references/storage-layout.md` for the full file table.

## OKRs

### schedule_adherence
- **Target**: On-demand enrichment runs complete within 5 minutes of invocation.

### data_integrity
- **Target**: Zero raw transaction records modified or deleted by enrichment pipeline.

## Visibility

public