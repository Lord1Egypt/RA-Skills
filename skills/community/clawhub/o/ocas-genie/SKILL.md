---
name: ocas-genie
description: Safely audits and reclaims VPS/Linux disk space, investigates root-filesystem growth, and enforces backup retention when disk usage is high or maintenance is requested; use keywords disk cleanup, disk full, disk usage, snapshots, backups, stale repos, or disk spike. NOT for database maintenance beyond read-only analysis, logrotate configuration, or real-time monitoring.
version: "1.9.0"
author: Indigo Karasu (indigokarasu)
license: MIT
platforms: [linux]
source: https://github.com/indigokarasu/genie
triggers:
  - disk cleanup
  - disk full
  - disk usage
  - disk spike
  - snapshots
  - backup retention
  - stale repos
includes:
  - references/**
  - scripts/**
metadata:
  hermes:
    tags: [cleanup, disk-space, filesystem, maintenance]
    category: infrastructure
    config:
      - key: genie.snapshot_max_age_days
        description: "Delete snapshots older than N days"
        default: "7"
      - key: genie.log_compress_age_days
        description: "Compress logs older than N days"
        default: "7"
      - key: genie.log_delete_age_days
        description: "Delete compressed logs older than N days"
        default: "30"
      - key: genie.cron_output_compress_age_days
        description: "Compress cron output files older than N days"
        default: "7"
      - key: genie.session_compress_age_days
        description: "Compress session JSONs older than N days"
        default: "14"
      - key: genie.tmp_stale_hours
        description: "Delete /tmp files older than N hours (0 to skip)"
        default: "24"
      - key: genie.git_clone_max_age_days
        description: "Delete git clones in <projects-root>/ untouched for N days (must have remote)"
        default: "5"
      - key: genie.dry_run
        description: "If true, only report — don't delete/compress"
        default: "false"
---

# Genie — VPS Disk Cleanup

Safely reclaims disk space on Linux VPS and workstations by deleting or compressing stale state snapshots, logs, cron output, temp files, and package caches. Also owns `/root` disk-spike investigation, duplicate repo detection, and backup-retention audits formerly covered by `util-vps-cleanup`. Does not touch live databases, auth files, or active sessions.

## When to Use

- VPS disk usage is high (above 50%)
- User asks to "clean up disk space" or "check disk usage"
- User asks why disk usage grew or where space went
- `/root` needs a safe audit/classification pass
- Backup directories, snapshots, or `.bak-*` files may violate retention
- Weekly maintenance cron fires
- Before/after large operations (backups, migrations)

## When NOT to Use

- Database maintenance tasks (genie does not manage databases)
- Real-time monitoring or alerting
- Log rotation configuration (genie handles specific files, not system-wide logrotate)

## Prerequisites

No external dependencies — uses only Python 3.11+ stdlib.

Configuration lives in `config.yaml` under `skills.config.genie.*` (see Configuration below). Behavioral settings are never read from environment variables.

## How to Run

```bash
# Assess disk usage and identify cleanup targets
python3 <hermes-home>/profiles/indigo/skills/ocas-genie/scripts/genie.py --assess

# Execute cleanup (Tier 1 + Tier 2)
python3 <hermes-home>/profiles/indigo/skills/ocas-genie/scripts/genie.py --clean

# Dry run — preview without deleting
python3 <hermes-home>/profiles/indigo/skills/ocas-genie/scripts/genie.py --clean --dry-run

# Map filesystem and generate FILESYSTEM.md manifest
python3 <hermes-home>/profiles/indigo/skills/ocas-genie/scripts/genie.py --discover
```

For large file counts (>2,000), run in background: `terminal(background=True, notify_on_complete=True)`.

## Quick Reference

| Flag | Action |
|------|--------|
| `--assess` | Report disk usage and cleanup targets |
| `--clean` | Execute Tier 1 + Tier 2 cleanup |
| `--clean --tier 1` | Only Tier 1 (zero risk) |
| `--dry-run` | Preview without modifying anything |
| `--discover` | Map filesystem, create/update FILESYSTEM.md |
| `--analyze` | Tier 3 analysis only (read-only) |
| `--json` | Output as JSON |

## Backup Retention Rule

The VPS should keep **only one historical backup at a time**, plus current live data. Genie owns detecting and reporting violations.

Historical backup candidates include:
- `<fs-root>/backup/*`
- `<fs-root>/backups/*`
- `<hermes-home>/profiles/<profile>/state-snapshots/*` (profile-scoped — the bare `<hermes-home>/state-snapshots` is a different, usually-empty path)
- `<hermes-home>/migrations/*/backups/*`
- profile DB `.bak-*` files under `<hermes-home>/profiles/*/commons/db/`

Default behavior:
1. local full `state.db` backup copies are invalid unless explicitly requested
2. keep the newest valid historical backup
3. mark older or invalid historical backups as reclaimable
4. do not create an additional local historical backup unless replacing the retained one
5. after a replacement backup is verified, remove the superseded backup
6. report path, size, timestamp, and reclaimed/expected space

For the full audit workflow, see `references/root-audit-and-backup-retention.md`.

## Procedure

Use this checklist so destructive cleanup is preceded by assessment and followed by independent verification:

- [ ] Locate the live script and confirm the intended Hermes home/profile paths.
- [ ] Run `--assess` (or `--clean --dry-run`) and capture the report before changing files.
- [ ] Review retention candidates and confirm the newest snapshot/backup is protected.
- [ ] Run the smallest authorized cleanup tier.
- [ ] Verify `df`, snapshot survival, and relevant database integrity after cleanup.

The sequence matters because an aggregate cleanup total cannot prove which backup survived, and a nearly-full disk can make a later verification command fail.

1. **Locate the script** — check these paths in order:
   - `<hermes-home>/profiles/indigo/skills/ocas-genie/scripts/genie.py` (profile — note `ocas-` prefix)
   - `<hermes-home>/profiles/indigo/scripts/genie.py` (profile scripts dir — alternate location)
   - `<hermes-home>/skills/ocas-genie/scripts/genie.py` (skill-bundled)
   - Use absolute paths only — never `~` in cron context
   - **Gotcha**: the skill folder is `ocas-genie/`, not `genie/`. A literal read of the old path will fail with ENOENT.

2. **Assess** — run `--assess` to identify targets

3. **Execute** — run `--clean` (or `--clean --dry-run` to preview)

4. **Report & verify** — `df -h /` after cleanup, then MANDATORY post-clean checks: confirm the `state-snapshots/` dir still holds the most-recent snapshot (do NOT trust a `0.0 B snapshots` line as proof), and run `PRAGMA integrity_check` on live DBs the user cares about (e.g. `styx.db`, `transactions.db`). See Verification. Note genie logs no per-file manifest, so capture pre-clean dir listings if an audit trail is needed.

## Manual / Investigative Targets

Some large disk consumers require an audit pass before cleanup because they may be live data, backups, or duplicate worktrees. Use `references/root-audit-and-backup-retention.md` for the full procedure.

1. **Manual backups** (`<fs-root>/backup/`, `<fs-root>/backups/`) — enforce one historical backup total on the VPS. Keep newest valid backup; older backups are reclaimable.
2. **Pre-update snapshots** (`<hermes-home>/profiles/<profile>/state-snapshots/`) — count as historical backups. Keep only the newest valid one once the post-update gateway is confirmed healthy. **CAUTION:** `backup_retention` may delete this snapshot despite the preservation rule (see Known Issues) — verify it survived after every `--clean`.
3. **Migration backups** (`<hermes-home>/migrations/*/backups/`) — count as historical backups. Keep only if they are the newest/only valid historical backup.
4. **Pre-migration `.bak-*` files** (`profiles/*/commons/db/*/.bak-*`) — count as historical backups. Reclaim older ones once the live DB has newer writes and integrity checks pass.
5. **Duplicate git repos** — compare remote + HEAD before removing. Same remote and same HEAD = duplicate candidate.
6. **Browser caches** (`~/.cache/camoufox/`) — safe to delete when no creating process is running.
7. **Stale /tmp extracts** (`/tmp/camoufox-*/`, `/tmp/uc_*/`, `/tmp/body_*`) — safe to delete when no creating process is running.
8. **Retention is per class and root, newest-first.** Candidates are grouped by kind/root so two backup roots can never delete each other's only copy, and recency selects the survivor — completeness (`backup_score`) only *adds* a rescue keep, it never outranks mtime, which is how a 19-month-old copy once outranked today's. An entry whose NAME carries no calendar date or backup marker is the live copy the pipeline refreshes in place (`chronicle.db`, `current/`, `mempalace.tar.gz`) and is never a retention candidate; this covers directories as well as files. Symlinks are skipped entirely — following one lets retention "keep" the link while deleting the directory it points at. "Any eight digits" is not a date: account numbers, phone numbers and epoch stamps must not strip that protection.
8. **state.db VACUUM** — Genie does not run `VACUUM` automatically. As of v1.7.x the default `--assess` (and `--clean`/`--discover`) pass reads `PRAGMA page_count`/`page_size`/`freelist_count` and prints `live_bytes`, `bloat_bytes`, `bloat_pct`, and whether a classic `VACUUM` (which duplicates the file inline → needs ~`live_bytes` free on top of the original) would fit. **Decision rule: if `bloat_pct` < ~5%, do NOT VACUUM — the file is mostly real data; reclaim via caches/tmp/repos instead.** Most live agent DBs sit at 0.5–2.4% bloat. See `references/state-db-vacuum-feasibility.md`. A 2.5 GB+ uncheckpointed WAL is itself abnormal — flag the missing checkpoint separately; do not attribute it to bloat.
10. **Orphaned language-runtime trees** — a second interpreter tree (e.g. `/usr/local/lib/python3.13` alongside a system 3.14) can hold GB nothing imports; a CUDA/GPU stack (`torch`, `triton`, `nvidia-*` ≈ 4.5 GB) on a GPU-less VPS is pure dead weight. Prove orphanhood before deleting: no shebang, cron entry, service venv, or script references it.
11. **Duplicate model/asset stores** — a daemon whose systemd unit sets its own `HOME` (e.g. `HOME=/usr/share/ollama`) cannot see assets pulled into another home, so the box carries two stores *and* the service is silently missing its model. Compare both, merge, fix ownership — do not delete blindly.
9. **Git LFS caches** — a fully-pushed repo can hide many GB in `.git/lfs` (local copies of objects the LFS server already holds). Check with `du -sh <repo>/.git/lfs` whenever a repo's `.git` dwarfs its `git count-objects -vH` size-pack. Reclaim with `git lfs prune --verify-remote` (dry-run first; it verifies each object exists on the remote before deleting). Precondition: clean tree, no unpushed commits. 2026-08-16: indigo-repo `.git/lfs` 12 GB → 767 MB.

When disk is critically high, flag these in the report even if `--clean` cannot auto-clean them.

## Safety Rules

- NEVER modify `state.db` directly — Tier 3 analysis only. Note: `<hermes-home>/state.db` is typically a symlink to a profile's DB (e.g., `→ profiles/indigo/state.db`). Resolve symlinks before analyzing or reporting.
- Enforce the one-historical-backup rule: keep current live data plus the newest valid historical backup; older backup copies/snapshots are reclaimable.
- NEVER delete files without compressing first (Tier 2+) unless they are superseded historical backups being removed under the one-backup retention rule.
- ALWAYS report what was done
- If disk usage is below 50%, report "no action needed"
- If any operation fails, report the error and continue
- **Backup-freshness gate (v1.8.0):** when `backup_stamps_path` exists (default `<hermes-home>/logs/stamps`, holding `<name>.ok` files whose mtime marks each backup path's last success), genie **refuses backup-class cleanup while any path is stale** (older than `backup_stamp_max_age_hours`, default 26). The moment the offsite pipeline stops is precisely when the local copy becomes the only copy. `--assess` prints a `Backup freshness:` line; a generic install with no stamp directory is unaffected.
- If a snapshot deletion fails, leave the snapshot in place and report at the end
- The most recent snapshot is always preserved (never auto-deleted) — **NOTE: this is currently undermined by `backup_retention` (see Known Issues); verify the snapshot dir survived after every `--clean`, do not assume it from the summary line.**
- **Do not preserve multiple backups**: The VPS policy is one historical backup plus current live data. Count all historical backup classes together (`<fs-root>/backup`, `<backups-root>`, snapshots, migration backups, `.bak-*`) and report/remove older valid copies.
- **Repo deletion guard — ENFORCED IN CODE as of v1.8.0** (`clone_delete_blockers()`; it was documented-only before, and the gap destroyed a clone on a production box — see `references/clone-deletion-safety.md`). A clone is deletable only when ALL hold: (a) working tree **clean**, (b) **no stashes**, (c) **every local branch fully pushed** to a configured upstream — a branch with no upstream is unverifiable and therefore blocking, (d) has a **remote** (re-clonable), (e) untouched > `git_clone_max_age_days` (default 5), (f) not matched by `git_clones_protected` (config: site-source trees, in-progress projects, the operator's own site repo). The probe **fails closed** — an unreadable repo is never deleted. It also **contacts the remote** (`git ls-remote`, disable with `git_clones_verify_remote: false`): remote-tracking refs are a local cache, so "not ahead of origin/main" says nothing about whether the remote still *has* origin/main — a branch deleted upstream or a deleted repository would otherwise read as fully pushed. Commits held only by a tag or a detached HEAD are caught by `rev-list --all --not --remotes`, and **git-ignored paths block deletion** unless they are rebuildable (`node_modules`, `__pycache__`, ...) — a clone's `.env` or `data/` is routinely the only copy in existence. The probes are also **immune to their environment and to the repository's own config**: `GIT_DIR`/`GIT_WORK_TREE` are scrubbed (they would redirect every check at another repo), and `status.showUntrackedFiles` / `diff.ignoreSubmodules` are forced on the command line so a repo cannot hide its own work. Stash detection reads `refs/stash` rather than the reflog (which fails open after an expiry), and the gate additionally blocks on skip-worktree/assume-unchanged files, submodules holding local-only work, and linked worktrees that share the object store. Blocked clones are counted as `skipped_unsafe` and reported with their reasons. Regression test: `tests/test_clone_delete_gate.py` (7 cases). The manual playbook remains in `references/manual-repo-pruning.md`.

## Known Issues / Pitfalls

### backup_retention can delete the most-recent rollback snapshot (CONFIRMED BUG)
`clean_backup_retention` keeps only the single newest candidate across ALL backup classes combined (`keep = valid[:1]`). The most-recent pre-update `state-snapshot` is itself a candidate in this scan. If a different backup file (e.g. a `transactions.db` copy) has a newer mtime, the snapshot is pushed into `reclaim` and `shutil.rmtree`'d — **violating the Safety Rule "the most recent snapshot is always preserved."** Symptom: after `--clean`, `clean_snapshots` reports `snapshots: freed 0.0 B` (the dir is already empty, so it has nothing to preserve) — do NOT read that 0.0 B as proof the snapshot survived. Verify the snapshot dir directly (see Verification). Fix is pending in `scripts/genie.py`; until then, treat snapshot preservation as UNVERIFIED after any `--clean` run. See `references/genie-snapshot-retention-bug.md` for the full analysis and reproduction recipe.

### genie emits no per-file deletion manifest
`--clean` prints only aggregate totals (e.g. "backup_retention: freed 26.6 GB"). Deleted paths are NOT logged. Once files are removed they are unrecoverable (no git/LFS tracking of `<hermes-home>`). To answer "what was deleted," reconstruct by comparing directory state before/after — you cannot recover a file list from the tool output. Always capture `ls -la` of every backup class BEFORE `--clean` if you need an audit trail.

### Wrong snapshot path in older docs
The pre-update snapshot lives at `<hermes-home>/profiles/<profile>/state-snapshots` (profile-scoped), confirmed by `FILESYSTEM.md` and genie's `snapshots_path` default. The bare path `<hermes-home>/state-snapshots` is a different, usually-empty directory — do not verify against it.

### Decoy-script trap + unreachable prune (CONFIRMED root cause of <fs-root>/backup bloat, 2026-07-13)
When re-investigating disk spikes from backup copies, the **live writer is `backup_all_hermes_data.sh`** (`<repo-root>/scripts/...`, exec'd via the ocas-custodian wrapper), NOT `backup_system.sh`. `backup_system.sh` targets `<fs-root>/backups` (plural) and is **unused** — an earlier scan blamed it for "zero retention logic," which was wrong. The live `backup_all_hermes_data.sh` DOES have a prune line (`find <fs-root>/backup -mtime +3 -exec rm -rf`), but it sits at **line 114**, *after* the `cp <hermes-home>/state.db` (symlink -> 14G profile DB) at **line 51**, under `set -euo pipefail`. On a near-full disk the `cp` hits ENOSPC, the script aborts, and the prune **never runs** -> partial `active-dbs-*` dirs accumulate (all lacking `state.db` = the ENOSPC-abort signature).

**FIX APPLIED 2026-07-14 (verify before re-patching):** the prune was moved to BEFORE the 14G cp, a free-space guard (`readlink -f` + `stat -L`, skip copy if `avail < size*1.1`) was added, and `trap cleanup_partial ERR` removes the partial dir on failure. See `references/backup-prune-diskfull-trap.md` STATUS + Verification recipe — run the recipe first; if all three checks pass, the fix is intact and you must NOT re-apply it (doing so would duplicate the guards). The separate TASK-015 (state.db FTS-trigram bloat, VACUUM) is a distinct open task and is NOT covered by this fix.

**Re-investigation discipline:** to find the live writer, follow the real chain (read `jobs.json` `command`/`script_path`, grep `<hermes-home>/cron/output/*/*.md` for the job name, follow `exec` chains in wrappers). Do NOT conclude root cause from a plausibly-named sibling. And check whether a retention line is *reachable* — a prune after a large/failing `cp` under `set -e` is dead code on a full disk.

### Publishing a genie.py change when the remote was force-updated (2026-07-26)
The live skill dir `/root/.hermes/profiles/indigo/skills/ocas-genie` IS its own git repo (remote `indigokarasu/genie`). The daily `skill-sync-all` cron can clobber unpushed edits, so PUSH FROM THE LOCAL SKILL REPO, never a `/tmp` clone. If `git push` is rejected because the remote advanced (and `fetch` shows `(forced update)`): a plain `rebase origin/main` may hit CONFLICT in `references/*.md` (their PII-sanitize/beautify commits) — these are doc-only and unrelated to `genie.py`. Resolve by `git checkout --theirs -- references/` then `git rebase --skip` for each conflicting doc commit; your `genie.py` commit (separate file) will apply cleanly on top. Then non-force push. Do NOT `--force` push (could clobber remote work). After push, verify `git rev-list --count HEAD..origin/main` = 0. If an unrelated uncommitted edit (e.g. README) is present, stash it before rebasing and do not bundle it into your commit.

### A retention line pointing at a nonexistent path is a silent no-op (2026-08-16)
A nightly prune ran `git -C <fs-root>/indigo lfs prune` for two months — but the repository is `<fs-root>/indigo-repo`. `git -C` on a non-repo fails quietly, and the line was wrapped in `>/dev/null 2>&1`, so the job reported success daily while the LFS cache grew to 12 GB and filled the disk. **Verify every retention target resolves** before trusting the line (`[ -d "$P/.git" ] || echo MISSING`), and prefer loud failure to silent success. Same family as the placeholder-token defect: code that runs, and does nothing.

## Error Handling

| Failure | Handling |
|---|---|
| `--clean` reports an operation error | Record the path/error, continue independent targets, and report every failed target; do not claim cleanup completed. |
| Snapshot deletion fails | Leave the snapshot in place, verify the directory directly, and report the failure. |
| Disk reaches 100% | Run only Tier 1 recovery first; defer backup workflows because copy/verification can require temporary space. |
| `gzip -t` finds corruption | Keep the original, regenerate the archive, and delete nothing until the replacement passes `gzip -t`. |
| Live DB integrity check is not `ok` | Stop database-related follow-up, preserve the DB, and escalate the exact result; Genie never repairs DBs. |

The explicit fallback paths prevent a partial cleanup or a failed verification from being misreported as a successful run.

## What Genie Cleans

### Tier 1 — Zero Risk (auto-executed)
1. **Stale state snapshots** — directories older than 7 days (most recent always preserved)
2. **Old log files** — compress after 7 days, delete compressed after 30 days
3. **Old cron output** — compress after 7 days
4. **Stale `/tmp` files** — delete after 24 hours
5. **Package caches** — pip, uv, npm (all rebuildable)
6. **Browser profile caches** — `~/.cache/camoufox/` (rebuildable, often 1+ GB)
7. **Inactive git clones** — `<projects-root>/` dirs untouched >5 days with confirmed remote (safe to re-clone)

### Tier 2 — Low Risk (requires confirmation)
1. **Session JSON duplicates** — compress after 14 days (data also in `state.db`)

### Tier 3 — Analysis Only (never auto-executes)
1. **state.db bloat analysis** — runs on the **default** `--assess`/`--clean`/`--discover` pass (not just `--analyze`). Reports `live_bytes`, `bloat_bytes`, `bloat_pct`, and a VACUUM-feasibility verdict (see Manual / Investigative Targets #8 and `references/state-db-vacuum-feasibility.md`).
2. **Large directories** — reports git checkpoints, commons/data, commons/db for manual review

## Manual Repo Pruning (user-requested clone deletion)

When the user asks to delete cloned repos beyond Genie's automated inactive-clone Tier 1, do **NOT** blanket `rm -rf` every repo — clones may hold unpushed commits or be live skill source. Full decision gate + blocker playbook in `references/manual-repo-pruning.md`.

- **Eligible (delete now):** clean (`git status --porcelain` empty), has a remote (re-clonable), untouched > `git_clone_max_age_days` (5d), NOT a protected path (live skill dirs, active working repo, `indigokarasu-site-commons/*`).
- **Needs sync first:** dirty or `ahead>0`. Commit → push → re-verify `dirty==0 && ahead==0` → only then `rm -rf`. Never delete before the remote actually has the commit.
- **Exclude:** stale mirrors (local clone older/smaller than the live source, e.g. `indigo-repo` 104 vs live 141 skills) and protected live-skill directories. For a stale mirror where local HEAD == remote HEAD, a local-only delete is safe (GitHub holds the commit; live skills live elsewhere) — but a daily skill-sync may recreate it.

Blockers that prevent a clean sync: dead local `origin` remote → repush to the real GitHub remote; nested git repo / submodule → sync the nested repo then pin the parent gitlink; pull-rebase conflict on a stale mirror → `git reset --hard origin/main` (remote supercedes — ONLY for disposable mirror clones; NEVER in a live skill dir, where divergence must refuse loudly and be reconciled with an explicit rebase); husky pre-push test stalls → do **NOT** bypass the hook, diagnose/fix the suite or drop the clone after user confirms.

## Configuration

Genie reads all behavioral settings from `config.yaml` under
`skills.config.genie.*`. Set them with `hermes config set` or by editing
`config.yaml` directly. CLI flags (e.g. `--dry-run`) override config at runtime.
Any setting not present falls back to the built-in default shown below.

| Config key (`skills.config.genie.*`) | Default | Description |
|---|---|---|
| `snapshot_max_age_days` | 7 | Delete snapshots older than N days |
| `log_compress_age_days` | 7 | Compress logs older than N days |
| `log_delete_age_days` | 30 | Delete compressed logs older than N days |
| `cron_output_compress_age_days` | 7 | Compress cron output files older than N days |
| `session_compress_age_days` | 14 | Compress session JSONs older than N days |
| `tmp_stale_hours` | 24 | Delete /tmp files older than N hours (0 to skip) |
| `git_clone_max_age_days` | 5 | Delete git clones in <projects-root>/ untouched for N days (must have remote) |
| `dry_run` | false | If true, only report — don't delete/compress |
| `filesystem_md` | (empty) | Optional override path for FILESYSTEM.md |
| `allow_local_state_db_backup` | false | If true, local full state.db copies count as valid retained backups |

## Verification

- `df -h /` — check disk usage dropped
- `du -sh <hermes-home>/` — check .hermes size
- **Snapshot survival (MANDATORY):** `ls -la <hermes-home>/profiles/<profile>/state-snapshots/` — the most-recent pre-update snapshot dir MUST still be present. If empty, `backup_retention` deleted it (see Known Issues). A `snapshots: freed 0.0 B` line does NOT prove preservation.
- **Live DB integrity:** for each live DB the user cares about, run `sqlite3 <db> "PRAGMA integrity_check;"` and confirm `ok`. For Styx: `<hermes-home>/data/styx.db` (often a symlink to the repo copy) and the live Plaid source `<hermes-home>/data/transactions.db`. Resolve symlinks first.
- Session search still works (confirms state.db intact)

## Support File Map

| File | When to read |
|---|---|
| `references/root-audit-and-backup-retention.md` | Root disk-spike investigation, duplicate repo checks, and one-historical-backup retention rule |
| `references/backup-prune-diskfull-trap.md` | CONFIRMED root cause of <fs-root>/backup bloat: live writer is backup_all_hermes_data.sh; prune line unreachable (after 14G state.db cp under set -e); decoy-script trap. **FIX APPLIED 2026-07-14 — top of file has STATUS + a Verification recipe; run it before re-patching.** |
| `references/genie-gotchas.md` | Before first production run or when debugging |
| `references/operational-notes.md` | Real-world examples and case studies |
| `references/os-walk-pitfall.md` | Debugging nested directory traversal issues |
| `references/session-2026-05-29-disk-recovery.md` | Disk emergency case study |
| `references/snapshot-backup-redaction.md` | Backing up snapshots to git/LFS |
| `references/snapshot-structures.md` | Snapshot format breakdown |
| `references/state-db-compaction.md` | Tackling state.db bloat |
| `references/state-db-vacuum-feasibility.md` | PRAGMA recipe + disk math for VACUUM feasibility; why `bloat_pct` <5% means DON'T VACUUM |
| `references/state-db-size-breakdown.md` | State DB composition analysis |
| `references/disk-growth-patterns.md` | Recurring disk hogs: pre-update snapshots, <fs-root>/backup/, browser caches |
| `references/state-db-retention.md` | State DB retention policy: audit all instances, keep current + one backup, delete oldest first |
| `references/self-update-genie.md` | Self-update hash comparison procedure |
| `references/repo-path-conventions.md` | Repo path convention — all remote clones under `projects/github*` |
| `references/manual-repo-pruning.md` | User-requested clone deletion: decision gate + blocker playbook (dead remote, nested submodule, husky-stall, stale mirror) |
| `scripts/genie.py` | Main cleanup script |
| `scripts/genie_rebuild_fts.py` | FTS rebuild after restoring no-FTS backup |
| `references/genie-snapshot-retention-bug.md` | CONFIRMED bug: backup_retention deletes the most-recent rollback snapshot; post-clean verification recipe; Plaid-source vs Styx DB distinction |