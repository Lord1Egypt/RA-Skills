# Dispatch re-fire closure (2026-07-24)

**Classification:** re-detection of an already-closed mixed wave (`dispatch-wave-20260724T072118Z`).

**Detection:** dispatcher fired at 07:20:40Z carrying `new_emails` (<operator>, 2 threads) + `new_journals` (`ocas-finch/2026-07-24/scan-0716.json`, `ocas-mentor/2026-07-24/mentor-light-20260724T070458Z.json`).

**Triage:**
- Both `new_files` journals already present in BOTH eval stores (`commons/data/ocas-praxis/journals_evaluated.jsonl` + `commons/data/ocas-dispatch/journals_evaluated.jsonl`) → no pipeline re-run. This is the expected steady-state re-detection pattern (confirmed 50+ times).
- Email: both threads already in evidence via `verify_evidence_threads.py`:
  - `<thread-id>` (Docusign <employer> Separation Agreement) → `action=escalate` PRESERVED from prior genuine wave (requires <operator>'s personal legal sign-off; not re-fired).
  - `<thread-id>` (Roller shade, Daniel Ringkamp Apr 2026) → `action=action:none`.
  - Email-evidence gate: PASS. No drafts, no inbox mutation.

**Genuine gap found:** ONE journal with mtime AFTER the 07:20:40Z detection and absent from both stores:
- `ocas-mentor/2026-07-24/mentor-light-20260724T072518Z.json` (mtime 1784877920.04 ≈ 07:25:20Z). It is a pure heartbeat (`gap_detected: false`, no gap-eval fields) → safe noop-bridge with tag `cross_skill_noop_mentor_heartbeat` (per `references/dispatch-recovery-stale-state-postgap-closure.md`).

**Closure sequence executed (verified working):**
1. Bridge the post-dispatch noop heartbeat:
   `python3 skills/ocas-forge/scripts/bridge_eval_inline.py ocas-mentor/2026-07-24/mentor-light-20260724T072518Z.json --action cross_skill_noop_mentor_heartbeat --require-exists`
   → printed `bridged (praxis=True dispatch=True)`, `total bridged: 1`.
2. Advance gate state past max journal mtime (`NEW = max_mtime + 5.0` pad, NEVER hand-typed literal) into BOTH monitor copies + praxis `ingest_state.last_ingest_run`:
   - `$HERMES_HOME/../indigo/commons/data/monitor_state/journal_ingest_state.json`
   - `~/.hermes/commons/data/monitor_state/journal_ingest_state.json`
   - `$HERMES_HOME/../indigo/commons/data/ocas-praxis/ingest_state.json` (`last_ingest_run`, `last_ingest_run_ts`)
3. Verify: `python3 skills/ocas-forge/scripts/closure_closeout_check.py --named ocas-dispatch/2026-07-24/dispatch-wave-20260724T072118Z.json --date 2026-07-24` → **gates ALL CLOSED**.
4. Verify: `python3 skills/ocas-forge/scripts/verify_genuine_gap_profile.py --date 2026-07-24` → **GENUINE GAP (excluding custodian): 0**.

**MAX journal mtime (excl custodian):** 1784877920.04. Monitor + praxis advanced to 1784877925.04 (07:25:25Z).

**Note for future runs — path-shape trap:** the journals tree is `commons/journals/<skill>/<DATE>/*.json`, NOT `commons/journals/<DATE>/<skill>/`. A diagnostic `os.walk`/`glob` over the wrong shape returns 0 files and falsely implies "no journals / all closed." Use the correct shape (this bit the live run once; corrected by re-globbing `roots/<skill>/<DATE>/`).

**Status:** This is the Nth re-detection closure (2026-06 → 2026-07-24). The monitor re-fire bug (wave writer does not advance gates atomically) remains live; manual closure via bridge + gate-state advance is still the working stopgap. No new skill defect found. Procedure is stable and reproducible.
