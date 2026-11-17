# Session 2026-07-14 — 21:50Z Mixed Wave (dispatch-eval gap + email second-wave)

A single dispatcher fire carried TWO items that look unrelated but must be resolved together:

- `new_journals` → 1 file `ocas-mentor/2026-07-14/mentor-light-20260714T213605Z.json`
- `new_emails` → owner account, 7 threads (1 high-priority), all `is_new:false`

## Pre-flight diagnosis

Grep each genuine `new_file` against BOTH eval stores:
- `mentor-light-20260714T213605Z.json` → PRESENT in `ocas-praxis/journals_evaluated.jsonl`, **ABSENT** from `ocas-dispatch/journals_evaluated.jsonl`.
- This is a **one-sided dispatch-eval gap** — the genuine re-fire cause. The dispatcher's `new_files` always includes its own newly-written journals; if one landed only in praxis-eval, the dispatch-eval store is behind and re-fires.

Email state file (`commons/data/ocas-dispatch/owner/last_email_check.json`) already showed:
- `verified_second_wave: true`
- `last_dispatch_wave: dispatch-wave-20260714T213604Z`
- Zillow (`<thread-id>`) + Carta Path-B gaps already CLOSED by that prior wave.

So the email item is a **redundant re-detection** of an already-closed second-wave.

Check for a newer concurrent wave that already closed it: the newest prior `dispatch-wave-*` (`212036Z`) predates `detected_at` (21:40:35), so NO later wave has closed this. Must run the full pipeline.

## Resolution (what actually worked)

### 1. Forge no-op scan
- `intake/` had 0 `vp_/vd_*` unprocessed (11 already in `intake/processed/`; `proposals/` is a source mirror — excluded).
- Wrote `forge-scan-20260714T214847Z.json` via `write_file` (atomic; avoids heredoc/pipe pitfalls).

### 2. Mentor real heartbeat
- Built feed: `find commons/journals -name "*.json" \( -path "*TODAY*" -o -path "*YESTERDAY*" \) | grep -v dispatch-wave | sort -u > /tmp/mentor_feed.txt`
- Ran `python3 skills/ocas-mentor/scripts/cron-heartbeat-light.py < /tmp/mentor_feed.txt` (stdin redirect — NEVER `cat file | python3`).
- 25 new files ingested, 0 errors. Heartbeat journal: `mentor-light-20260714T214853Z.json` (captured via content-timestamp scan, NOT `ls -t` — mtimes lag content ~7h12m).
- ANTI-JOURNALIZATION: did NOT write a second mentor-light journal.
- Mandatory `active_skills_30d` correction: `python3 skills/ocas-mentor/scripts/correct_active_skills_30d.py` → true 30d = 23 (script undercount 1).
- Sync profile→commons: `python3 skills/ocas-mentor/scripts/mentor_sync_commons.py`.

### 3. Praxis real ingest
- `cd skills/ocas-praxis/scripts && python3 praxis_ingest_run.py` (must run from script dir so `from praxis_common import ...` resolves).
- 3 new journals processed (the 3 post-dispatch mentor-light cron journals 214036/214306/214538), 2 `no_signal` events, 0 lessons.
- Cron checklist:
  - Gap backfill FIRST (before state update): `python3 gap_backfill.py` → 0 in praxis-eval (the genuine gap was in dispatch-eval — handled by bridge).
  - Noise cleanup: `python3 cleanup_noise_lessons.py --new-genuine-events 0` → archived 14 Bug-2 full-history noise lessons; `lessons.jsonl` empty.
  - Wrote `praxis-cron-20260714T214950Z.json`.
  - Re-read `ingest_state.json` AFTER gap_backfill (it writes counters), then `last_ingest_run` advanced to `2026-07-14T21:49:50Z` via load→modify→dump (preserves all 58 fields; never hand-type).

### 4. Bridge to BOTH eval stores (idempotent, phantom-guarded)
Bridged set (skill-first relative paths):
- `ocas-forge/2026-07-14/forge-scan-20260714T214847Z.json`
- `ocas-mentor/2026-07-14/mentor-light-20260714T214853Z.json`
- `ocas-praxis/2026-07-14/praxis-cron-20260714T214950Z.json`
- `ocas-mentor/2026-07-14/mentor-light-20260714T213605Z.json` ← the genuine gap
- `ocas-mentor/2026-07-14/mentor-light-20260714T214036Z.json` (sibling post-dispatch cron)
- `ocas-mentor/2026-07-14/mentor-light-20260714T214306Z.json`
- `ocas-mentor/2026-07-14/mentor-light-20260714T214538Z.json`

For each: append to praxis-eval (`journal_id`) if absent, to dispatch-eval (`filename`) if absent. **Phantom guard:** skip any entry whose file is not on disk (`os.path.exists(commons/journals/<rel>)`). Result: 0 phantoms.

ALSO discovered `ocas-dispatch/2026-07-14/triage-20260714T2142Z.json` (the prior wave's email-triage evidence journal) was in praxis-eval but absent from dispatch-eval → bridged it too. This is the KEY step for the email second-wave: the triage journal that records the Zillow/Carta Path-B closures must be registered in dispatch-eval or it re-fires.

### 5. Dispatch-wave meta-journal
Wrote `dispatch-wave-20260714T215057Z.json` with `classification: genuine_dispatch_eval_gap_plus_email_second_wave`, full `journal_pipeline` + `email_triage` (account: owner, actionable: 0, classification: second_wave) blocks. Bridged into both eval stores (`dispatch_output_skip`).

### 6. Closure verification
Bounded per-skill `os.listdir` walk of `commons/journals/ocas-*/2026-07-14/` (NOT recursive `glob`/`os.walk` — self-nested `journals/journals/...` symlinks produce false "gap" hits). Result:
- 16 gaps total, all `ocas-custodian/*` (self-bridged by their own cron — excluded by design).
- **NON-CUSTODIAN genuine gaps: 0.** → wave closed.

### 7. Email state re-affirmation
Re-affirmed `owner/last_email_check.json` via FULL-FILE `write_file` rewrite (re-read immediately before writing):
- `verified_second_wave: true`
- `last_dispatch: 2026-07-14T21:50:57+00:00`
- `last_dispatch_wave: dispatch-wave-20260714T215057Z`
- `email_second_wave_handled_20260714T215057Z: true`
- Note: redundant re-detection, no inbox changes/sends (hard rule 2026-06-24).

Do NOT use `patch` on this file — fuzzy matcher drops the lines between first/last match and can insert a DUPLICATE KEY (confirmed 2026-07-14T17:04Z corruption: dropped `last_check_ts`, inserted second `"timestamp"`).

## Key takeaways
1. When a wave has BOTH a journals gap AND an emails item, the EMAIL re-detection is noise; the JOURNALS dispatch-eval gap is what re-fires. Close the dispatch-eval gaps.
2. The email-triage evidence journal (`triage-*.json`) is itself a dispatch-eval gap when present in praxis-eval only — bridge it.
3. The stale `last_ingest_run` (not the journals) is the usual re-fire driver; advance it past max mtime of all bridged journals.
4. Use bounded per-skill `os.listdir` for closure, never recursive `glob`/`os.walk`.