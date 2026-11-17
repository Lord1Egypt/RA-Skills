# Stale Proposal Backlog Handling

**Confirmed 2026-06-25 dispatch ~#80:** 11 unprocessed proposals from April 17-25, 2026 sitting in `proposals/` directory. These are NOT part of any dispatch's `new_files` and have no corresponding journal entries.

## Problem

Forge's dispatch integration says "scan for unprocessed proposals/decisions" but provides no guidance on what to do with stale proposals that:
1. Predate any recent dispatch by weeks/months
2. Reference older versions of skills that have since evolved
3. Were never processed because they were missed by prior scans

## Detection

```bash
# Find proposals older than 30 days in proposals/
find <hermes-home>/profiles/indigo/commons/data/ocas-forge/proposals/ -name "vp_*.json" -mtime +30

# Cross-reference against processed/ and intake/processed/
FORGE_DATA="<hermes-home>/profiles/indigo/commons/data/ocas-forge"
for f in "$FORGE_DATA/proposals"/vp_*.json; do
    base=$(basename "$f")
    if ! grep -q "$base" "$FORGE_DATA/intake/processed/"*.json "$FORGE_DATA/processed/"*.json 2>/dev/null; then
        echo "UNPROCESSED: $base"
    fi
done
```

## Handling Rules

1. **Proposals older than 30 days with no corresponding dispatch:** These are stale backlog. Do NOT process them as new work — they reference old skill states and the evidence they contain is no longer actionable.

2. **Action:** Write a no-op journal noting the stale count. Move on. The proposals remain in `proposals/` but are not re-processed on subsequent scans.

3. **Why not delete them?** They may have audit value (tracking what was proposed and why). Deletion loses history. Leaving them unprocessed is harmless — the cross-reference technique skips them once they're in `processed/`.

4. **When to clean up:** If stale proposals exceed 20+ files, move them to an archive subdirectory (`proposals/archive/2026-04/`) to keep the active proposals directory clean. This is optional housekeeping.

5. **Stale decisions (`vd_*.json`):** Same handling. If older than 30 days and unprocessed, skip silently.

## Example No-Op Journal for Stale Backlog

```json
{
  "run_id": "forge-scan-YYYYMMDDTHHMMSSZ",
  "timestamp": "ISO UTC",
  "action": {"result": "no_op", "unprocessed_proposals": 0, "unprocessed_decisions": 0},
  "findings": {
    "unprocessed_proposals": 0,
    "unprocessed_decisions": 0,
    "stale_proposals_skipped": 11,
    "stale_note": "11 proposals from April 17-25 remain unprocessed (stale backlog, not part of this dispatch)"
  }
}
```

## Pitfall: Don't Block on Stale Backlog

When the dispatcher triggers a `new_journals` dispatch, the Forge pipeline's job is to check for NEW proposals/decisions from Mentor. If none exist, write no-op journal and exit. Do NOT attempt to process stale April proposals — they are not the dispatch's work item. The dispatcher's `new_files` list (if it contains Forge files) is the authoritative source of new work.

## Surfacing to User (explicit-run dispatch)

When the stale backlog is detected during an **explicit-run override** dispatch (the dispatcher prompt says "run Forge journal scan" or similar), do NOT silently skip it. The backlog is a genuine signal worth the user's attention:

- Write the no-op forge-scan journal with `stale_proposals_skipped: N` (per the format above).
- Add a `notes` entry to the dispatch-wave journal summarizing the count and age range.
- **Surface it in the delivered dispatch report** under an "Items needing your attention" section. The user (<operator>) should decide whether to process, archive, or retire the backlog — Forge must not auto-build variant packages autonomously in a cron run (that could create GitHub repos/PRs without human review).

**Threshold:** 12 files (2026-07-13 session) is below the 20+ archive threshold but still worth flagging. Use judgment: any stale backlog ≥ ~10 files that recurs across dispatches is worth a one-line flag.

## Field-naming pitfall (confirmed 2026-07-13)

Do NOT conflate the backlog count with `unprocessed_proposals`. `unprocessed_proposals` means proposals NEW to THIS dispatch (Mentor just queued them) — in a stale-backlog-only scan this is `0`. The stale count goes in `stale_proposals_skipped`. The 2026-07-13 session incorrectly set `unprocessed_proposals: 12` for a stale backlog; correct form is `unprocessed_proposals: 0, stale_proposals_skipped: 12`. A future dispatcher reading `unprocessed_proposals: 12` would misclassify the dispatch as carrying 12 new Forge work items.

**Confirmed 2026-06-25:** Dispatch listed only `ocas-mentor/` journals in `new_files`. No Forge proposals were queued. The 11 stale proposals in `proposals/` are a pre-existing backlog, not new work.