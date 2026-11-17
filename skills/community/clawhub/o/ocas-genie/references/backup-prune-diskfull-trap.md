# Backup Prune-Order / Disk-Full Trap (CONFIRMED root cause of <fs-root>/backup bloat)

## STATUS: FIX APPLIED (2026-07-14)
The three root-cause guards are now present in the canonical live writer `<repo-root>/scripts/backup_all_hermes_data.sh` (applied by finch:work, verified 2026-07-14T12:33). The bug is dormant and should not refire.
- Prune (`find <fs-root>/backup -mtime +3`) moved to ~line 18, **before** the 14G `cp <hermes-home>/state.db` at ~line 67.
- Free-space guard: `readlink -f` resolves the symlink to the real ~14G target, `stat -L` sizes it, copy skipped (with WARN) if `avail < size*1.1`.
- `trap cleanup_partial ERR` removes the partial `$BACKUP_DIR` on any failure.
The one-time destructive prune (4 of 5 `<fs-root>/backup` dirs) was also completed in an earlier run; `<fs-root>/backup` now holds 1 dir (3.2G). The separate TASK-015 (state.db FTS-trigram bloat, VACUUM/retention) remains open and is NOT addressed by this fix.

## Verification recipe (confirm guards are present — do NOT re-patch blindly)
```bash
SCRIPT=<fs-root>/indigo-repo/scripts/backup_all_hermes_data.sh
bash -n "$SCRIPT" && echo 'SYNTAX OK'
# (1) prune must run BEFORE state.db cp under set -e
awk '/Early prune of stale local backups/{p=NR} /cp \/root\/.hermes\/state.db/{c=NR} END{print "prune~"p" cp~"c; if(p>0&&c>0&&p<c)print "PASS: prune before cp"; else print "FAIL"}' "$SCRIPT"
# (2) free-space guard tokens present
grep -c 'readlink -f\|stat -L\|AVAIL_BYTES' "$SCRIPT"
# (3) partial-dir cleanup trap
grep -c 'trap cleanup_partial ERR' "$SCRIPT"
```
If all three pass, the fix is intact — do not re-apply.

## The bug
The live Hermes backup writer is:

- Canonical: `<repo-root>/scripts/backup_all_hermes_data.sh`
- Wrappers that exec it:
  - `<hermes-home>/profiles/indigo/skills/ocas-custodian/scripts/backup_all_hermes_data.sh`
  - `<hermes-home>/profiles/indigo/scripts/backup_all_hermes_data.sh` (3-line)

Cron job: **"Backup Hermes Sessions to GitHub"**, schedule `0 */6 * * *` (no retry config).

Key structure (canonical script):
- `set -euo pipefail`
- `BACKUP_DIR="<fs-root>/backup/$TIMESTAMP"` (line 9), `mkdir -p` (line 12)
- Copies small DBs (chronicle.lbug etc.)
- `cp <hermes-home>/state.db "$BACKUP_DIR/state.db"` at **line 51** — `state.db` is a **symlink -> `<hermes-home>/profiles/indigo/state.db`, ~14G**
- GitHub push (lines ~80-112)
- Prune at **line 114**: `find <fs-root>/backup -maxdepth 1 -mindepth 1 -type d -mtime +3 -exec rm -rf {} + 2>/dev/null || true`

**The prune line EXISTS but is unreachable on a near-full disk.** Because line 51 (the 14G `cp state.db`) runs *before* line 114, and the script uses `set -e`, when free space is low the `cp` hits ENOSPC, the script aborts, and the prune at line 114 **never executes**. A partial timestamped dir is left behind every failed run. Failed refires of the 6-hourly cron accumulate dirs faster than any relief.

The prune keeps 3 days (`-mtime +3`), so even when it DOES run it removes nothing younger than 3 days — and on a chronically 80%+ full disk the cp aborts before it ever gets there.

## Signature of the failure (how to confirm)
All `<fs-root>/backup/active-dbs-*` dirs contain only `chronicle.db` and **NO `state.db`**. That missing 14G file is the proof of ENOSPC abort — the small copies succeeded, the large one failed, script died before prune. In the observed case: 5 dirs (~15GB), 3 created within 4 minutes (19:19 / 19:21 / 19:23) = failed cron refires.

## Decoy-script trap (do NOT repeat this mistake)
Earlier scans concluded "backup scripts have ZERO retention logic" — WRONG. They inspected `backup_system.sh` (`<hermes-home>/profiles/indigo/scripts/backup_system.sh` and the ocas-custodian copy), which targets `<fs-root>/backups` (plural) and is **UNUSED**. The live writer is `backup_all_hermes_data.sh` (singular `<fs-root>/backup`).

**Re-investigation rule:** to find the live writer, follow the real chain — read `jobs.json` `command`/`script_path`, grep `<hermes-home>/cron/output/<id>/*.md` logs for the job name, or follow `exec` chains in wrappers. Do NOT conclude root cause from a plausibly-named sibling script. Also confirm which directory actually receives writes (`<fs-root>/backup` here, not `<fs-root>/backups`). And check whether a retention line is *reachable* — a prune after a large/failing `cp` under `set -e` is effectively dead code on a full disk.

## Fix (APPLIED 2026-07-14 — see STATUS above; historical recipe kept for reference)
In `backup_all_hermes_data.sh`:
1. Move/guard the prune **before** the `state.db` copy (or wrap the cp so failure doesn't abort the whole script before pruning).
2. Add a free-space guard: measure real `state.db` size with `readlink -f` + `stat -L` (NOT `stat` on the symlink — it returns 38 bytes), and skip the local `state.db` copy if `avail < size*1.1`.
3. `rm -rf` the partial `$BACKUP_DIR` on any failure before exiting/retrying.
Then a one-time destructive prune of 4 of 5 `<fs-root>/backup` dirs (~12GB) frees the danger zone.

## Symptom -> triage map
- `df -h /` >= 80% AND `<fs-root>/backup` has multiple `active-dbs-*` dirs from the same day -> this trap.
- Dirs missing `state.db` -> ENOSPC abort confirmed (partial-copy signature).
- `du -sh` on each dir: uniform 3.2G (just chronicle.db) or smaller (partial) -> all failed runs.

See `references/root-audit-and-backup-retention.md` for the one-historical-backup policy genie enforces against these dirs.