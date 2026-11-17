# Automation

## Daily cron jobs

| Job | Time | What |
|-----|------|------|
| `plaid-transaction-sync` | 07:00 | Pulls new bank transactions into styx.db |
| `styx:enrich-new-transactions` | 07:30 | Enriches new styx merchants via Google Places |
| `taste:daily-styx-enrichment` | 08:00 | Full pipeline: styx_places_enrich → taste_full_enrich → taste_signals_dedup |
| `taste:historical-email` | 09:02 | Scans email for restaurant reservations/deliveries |
| `taste:historical-calendar` | 10:10 | Scans calendar for restaurant/hotel events |
| `taste:scan` | 13:12 | Daily email/calendar scan + Styx→Taste delta ingestion |
| `Backup Hermes Sessions to GitHub` | 03:00 | Backs up all DBs + taste flatfiles to GitHub LFS |

## Backup

All taste and styx data is backed up to GitHub LFS (`indigo-repo`): `data/styx.db`, `data/ocas-taste-*.jsonl`, `data/chronicle.lbug`, `data/weave.lbug`, `data/transactions.db`, `data/chroma.sqlite3`. LFS tracks: `*.jsonl`, `*.db`, `*.lbug`, `*.sqlite3`, `*.tar.gz`.

⚠️ `state.db` is SKIPPed in backup — too large for GitHub.