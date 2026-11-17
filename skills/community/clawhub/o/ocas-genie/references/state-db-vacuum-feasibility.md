# SQLite VACUUM Feasibility — PRAGMA Recipe & Disk Math

## The question
A large `state.db` looks like reclaimable space. Is it? File size alone does NOT
tell you — SQLite never shrinks on delete; it marks pages free and reuses them.
The dead space is the **free-list**.

## Read-only measurement (instant, no lock — safe to run anytime)
```
sqlite3 <db> "PRAGMA page_size; PRAGMA page_count; PRAGMA freelist_count;"
```
- `freelist_count` = dead pages VACUUM would reclaim
- `live_bytes  = (page_count - freelist_count) * page_size`
- `bloat_bytes = freelist_count * page_size`
- `bloat_pct   = 100 * freelist_count / page_count`

Most live agent DBs show `bloat_pct` < 5% — the file is mostly REAL data, not waste.

## Why VACUUM is expensive
- Classic `VACUUM` rebuilds the DB into a temp file, then swaps.
- During the copy BOTH the original (full size) AND the compacted temp (~live_bytes)
  exist at once → peak free disk needed ≈ `live_bytes` on top of the still-present original.
- Takes an EXCLUSIVE lock for the whole run → gateway / cron / sessions stall or error.
- Slow on multi-GB files (minutes to tens of minutes).
- Atomic on failure: if it runs out of space mid-copy, the original survives but no space is gained.

## Decision rule
- `bloat_pct` low (<5%) → **do NOT VACUUM**. Reclaim via caches / tmp / repos instead.
- VACUUM desired AND `live_bytes < free_disk` → safe to run, prefer off-peak.
- `live_bytes >= free_disk` → will fail; free space first, OR
  `VACUUM INTO '/other/volume/state.db'` to write the compacted copy elsewhere, then swap.
  `PRAGMA incremental_vacuum` only helps if `auto_vacuum` is set and free pages sit at EOF.

## Reproduction (2026-07-26)
- state.db 14.62 GB: freelist 20946 / 3833578 pages → bloat 0.08 GB (0.5%).
  VACUUM would reclaim ~80 MB for ~14.5 GB peak need. Verdict: NOT worth it.
- WAL swung 531 KB → 2.5 GB → 563 KB across runs. The auto analysis caught the drift
  and flipped the SAFE/UNSAFE verdict between runs. A 2.5 GB uncheckpointed WAL is
  itself abnormal — flag the missing checkpoint separately; do not blame it on bloat.
