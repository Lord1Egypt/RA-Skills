# Session 2026-07-14 — Prior-Wave-Misclassification Recovery (explicit-run new_journals)

Confirmed the self-consistency recovery path end-to-end on a live cron dispatch.

## Trigger detected
Dispatcher fired `new_journals` (explicit-run override) + `new_emails` at 2026-07-14T04:25Z. Both `new_files`:
- `ocas-dispatch/2026-07-14/dispatch-wave-20260714T042154Z.json`
- `ocas-mentor/2026-07-14/mentor-light-20260714T042230Z.json`

...were ALREADY present in BOTH eval stores. BUT:
- No `forge-scan-*.json` existed for the 04:2x window.
- `ingest_state.last_ingest_run` was stale at `2026-07-14T02:54:46Z`.

This is the exact failure mode the 07-13 self-consistency rule predicts: a prior wave
(`dispatch-wave-20260714T042154Z.json`) had misclassified itself as `mixed_genuine_no_op`,
written no `forge-scan`, and exited with `state_updated:false`. Pre-flight for the EXCEPTION
re-detection shortcut failed: conditions (b) `forge-scan`-for-window-exists and (c)
`last_ingest_run`-past-timestamps were both FALSE, so the full 3-pipeline had to run again.

## CRITICAL PITFALL — do NOT use bridge_explicit_run.py here
`scripts/bridge_explicit_run.py` composes a fresh timestamp each run and mints a NEW
`dispatch-wave-<TS>.json`. Running it in a recovery would create a SECOND wave journal,
orphan the existing `dispatch-wave-20260714T042154Z.json`, and re-fire the dispatcher.
The script is correct ONLY for a genuine first-time explicit-run wave. For recovery, hand-run
(see procedure below).

## Recovery procedure (hand-run, verified)
1. **Forge scan**: count `vp_*/vd_*` in `intake/` + data root, cross-ref `intake/processed/`;
   EXCLUDE `proposals/` (source mirror). 0 unprocessed → no-op. Write
   `commons/journals/ocas-forge/YYYY-MM-DD/forge-scan-<TS>.json` (single Python block,
   `json.dump`, all timestamps composed ONCE).
2. **Mentor heartbeat**: build feed
   `find commons/journals -name '*.json' \( -path *DATE* -o -path *YEST* \) | grep -v dispatch-wave | sort -u`;
   run `python3 skills/ocas-mentor/scripts/cron-heartbeat-light.py < /tmp/feed.txt`
   (subprocess stdin — never shell pipe). Capture actual journal via content-timestamp scan
   (max `timestamp` field), NOT `ls -t` (mtimes lag ~7h12m). THEN run
   `python3 skills/ocas-mentor/scripts/correct_active_skills_30d.py` (the genuine bridge and the
   cron heartbeat both run it; omitting it during recovery leaves the 30d active-skill correction
   unapplied for the wave).
3. **Praxis ingest**: `cd skills/ocas-praxis/scripts && python3 praxis_ingest_run.py`.
   Auto-registers into praxis eval only.
4. **Bridge**: idempotent append (grep-by-basename) of [heartbeat journal, forge-scan, every
   new_file, existing dispatch-wave] into BOTH eval files (praxis: `journal_id`, dispatch:
   `filename`).
5. **REWRITE EXISTING** `dispatch-wave-<EXISTINGTS>.json` (same run_id) via `write_file` with
   `classification: routine_no_op`, `state_updated: true`, genuine pipeline notes. Do NOT mint a new one.
6. **Advance `last_ingest_run`** to the MAX mtime of ALL journals under `commons/journals/<skill>/DATE/`
   for the wave's date — NOT only the bridged set (using just bridged mtimes can leave a same-day
   cross-skill journal's mtime above the cutoff and re-fire the dispatcher); resync
   `journals_evaluated_count` / `last_eval_file_line` to actual line counts.
7. **Verify**: every bridged journal exists on disk (phantom guard); re-grep each in both eval
   stores (1:1). Post-dispatch cleanup `os.walk` for any `.json` mtime >= `last_ingest_run` not
   in praxis eval (exclude `dispatch-wave-*` + bare `.json`).

## Rewrite-target selection (added 2026-07-14T08:40Z second recovery pass)
When the pre-flight proves a prior wave misclassified itself, you must choose WHICH existing
`dispatch-wave-*.json` to `write_file`-rewrite. There can be 20+ candidates in the date dir.
Deterministic filter (verified live):
1. Among `dispatch-wave-*.json` for the date that are registered in BOTH eval stores
   (praxis `journal_id` + dispatch `filename`), keep those whose content `timestamp` field is
   `>=` the MAX mtime of the detected `new_files`.
2. From those, pick the MINIMUM such `timestamp`.
Rationale: a wave with `timestamp` BEFORE a new_file's mtime could not have processed that file,
so exclude it. The earliest wave that ran AFTER the files appeared is the one that handled them
but skipped its forge-scan + state advance — the misclassified wave. Rewrite THAT file (same
run_id). Never mint a new `dispatch-wave-*.json` (re-fires the dispatcher).

## Result (this session)
- Forge: 0 unprocessed → no-op. `forge-scan-20260714T044921Z.json` written.
- Mentor: real heartbeat → `mentor-light-20260714T044801Z.json` (2 ingested, 0 errors).
- Praxis: 3 routine `no_signal`, 0 lessons/events.
- Bridge: praxis +1, dispatch +2 (rest idempotent skips).
- `dispatch-wave-20260714T042154Z.json` rewritten (`state_updated:true`).
- `last_ingest_run` → `2026-07-14T04:49:21Z`.
- Verification: 0 phantoms; all bridged 1:1 in both eval stores; post-cleanup 0 gaps.
- Email: 4 <operator> threads all `is_new:false`/informational, already `action:none` in
  evidence.jsonl → second-wave, no triage/sends.

## Email side note
All 4 <operator> threads were second-wave (`is_new:false`). Per hard rule, no triage/drafts/inbox
modification even under explicit-run. `verify_evidence_threads.py` confirmed structured
`action:none` in evidence.jsonl. No Chronicle-worthy signals (expert-network solicitations +
stale vendor thread + routine pharmacy notification).

## Second recovery pass — 12:21Z plain re-detection (no explicit-run override)

Dispatcher re-fired `new_emails` + `new_journals` at 2026-07-14T12:21Z. Detected files:
- `ocas-dispatch/2026-07-14/dispatch-wave-20260714T121923Z.json` (already on disk, timestamp 12:19:23)
- `ocas-mentor/2026-07-14/mentor-light-20260714T121535Z.json` (already in both eval stores)

Both were ALREADY present in BOTH eval stores. A prior wave (`dispatch-wave-20260714T121923Z.json`,
outcome `fifth_wave_redetection_no_op`) had ALREADY run the real pipelines (Path A email verify,
`forge-20260714T121430Z.json` + `praxis-20260714T121430Z.json` outputs bridged). It left two defects:
1. `ingest_state.last_ingest_run` stale at `12:14:30` (BEFORE its own wave work at 12:19:23) →
   dispatcher re-detected on the next scan.
2. Its gap enumeration missed a post-dispatch cron heartbeat — `mentor-light-20260714T122113Z.json`
   (12:21:13) landed after it closed.

EXCEPTION pre-flight: (a) both new_files in both eval stores = TRUE; (b) `forge-scan-*.json` for the
12:19 window = FALSE (wave emitted `forge-20260714T121430Z.json`, no `-scan` suffix); (c)
`last_ingest_run` past new_file mtimes = FALSE. Literal EXCEPTION would NOT fire and would force a full
re-run. Correct call: inspect the wave journal `notes` ("GENUINE GAP=0", "bridged … as
cross_skill_mitigation", forge/praxis outputs on disk) → pipelines already ran → completed
re-detection, DO NOT re-run Forge/Mentor/Praxis.

Recovery (hand-run, verified):
1. Bounded per-skill `os.listdir` gap walk (NO recursive glob) → 1 genuine gap:
   `mentor-light-20260714T122113Z.json` (missing from both stores). Bridged both stores as
   `cross_skill_mitigation`.
2. Advanced `last_ingest_run` to `12:21:14` (past wave mtime 12:19:23 + bridged gap 12:21:13).
3. Rewrote existing `dispatch-wave-20260714T121923Z.json` (same run_id) via `write_file`:
   `state_updated:true`, `outcome: fifth_wave_redetection_no_op_recovery_closed`, corrected
   `email_triage` block (account `owner`, `actionable:0`, classification `second-wave`). Do NOT mint new.
4. Stamped email state: BOTH `last_email_check_<account-identity>_gmail_com.json` (sanitized canonical the
   dispatcher reads — had stale `actionable:5`) AND `last_email_check_owner.json` (friendly — had
   `actionable:0`) set to `actionable:0`, `last_dispatch` set, stale-false-positive note. The dispatcher
   reads the sanitized-named file, so it MUST be stamped or the false `actionable:5` re-fires.
5. CONVERGENCE RE-SWEEP: a second cron heartbeat `mentor-light-20260714T122538Z.json` (12:25:38) landed
   during recovery. Bridged it (`post-dispatch-cleanup`), advanced `last_ingest_run` to `12:25:39`,
   re-swept → 0 gaps.

Result: GENUINE GAP=0 in both eval stores; no phantoms; wave `state_updated:true`; email `actionable:0`.
Re-fire loop closed. No drafts, no sends (hard rule 2026-06-24).

Lessons patched into SKILL.md:
- EXCEPTION pre-flight must accept `forge-<TS>.json` (no `-scan`) and/or confirm completion via the
  prior wave journal's `notes`/`outcome`, not solely a `forge-scan-*.json` file.
- Mentor-cron heartbeat ~every 5 min → iterate gap-sweep to convergence after advancing state.
- Stamp BOTH email state filenames (sanitized canonical + friendly) to 0 on email second-wave.