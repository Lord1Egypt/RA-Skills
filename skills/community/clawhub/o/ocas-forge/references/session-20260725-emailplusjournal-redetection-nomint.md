# Session 2026-07-25 — E-mail + journal COMBINED re-detection, ZERO wave journals minted

**Date:** 2026-07-25 (dispatch detected 16:25:39Z, wave journal dated 16:23:04Z)

## Trigger
A scheduled dispatcher fire carried BOTH dispatch items at once:
- `new_emails` (owner account, 10 actionable threads)
- `new_journals` (`ocas-dispatch/2026-07-25/dispatch-wave-20260725T162304Z.json`)

The wave journal was ALREADY in both eval stores from the 16:23 closure. This is a
re-detection re-fire of a single already-closed wave — NOT a fresh mixed wave and
NOT a prior-wave-misclassification recovery.

## Why this case is distinct (the trap)
The mixed-wave closure runner `run_mixed_wave_closure.py` is the natural instinct
when you see `new_emails` + `new_journals` together. But that runner MINTS a fresh
`dispatch-wave-*.json` journal. For a re-detection that journal is a PHANTOM (already
closed) → the monitor re-fires forever. Confirmed re-detection rule: do NOT re-run
the pipelines, do NOT mint a wave journal.

## Correct closure procedure (executed live, all gates closed)

### Email pass — evidence append only, NO journal
1. `verify_evidence_threads.py --evidence commons/data/ocas-dispatch/evidence.jsonl <10 tids>`
   → all `in_evidence(structured) action=...` (1 escalate preserved, 9 none). Second-wave.
2. `python3 skills/ocas-dispatch/scripts/close_email_only_wave.py \
     <user-google-email> dispatch-email-<TS> <ISO> /tmp/owner_threads.json`
   → appends `email_triage` entry, NO dispatch-wave journal, inbox untouched.
   The script's internal re-verify guard + escalate-preservation rule handled the
   <employer> separation-agreement escalation (action=escalate PRESERVED, not re-fired).

### Journal pass — bridge residual + advance gate, NO journal
3. Determine genuine gap: the named wave journal is already in BOTH eval stores
   (`grep -c` for `ocas-dispatch/2026-07-25/dispatch-wave-20260725T162304Z.json` in
   `commons/data/ocas-praxis/journals_evaluated.jsonl` AND
   `commons/data/ocas-dispatch/journals_evaluated.jsonl` → both 1).
   Only ONE journal missing: a post-dispatch mentor heartbeat
   `mentor-light-20260725T162541Z.json` (`gap_detected:false`, no-op heartbeat).
4. `python3 skills/ocas-forge/scripts/bridge_eval_inline.py \
     ocas-mentor/2026-07-25/mentor-light-20260725T162541Z.json \
     --action cross_skill_noop_mentor_heartbeat --require-exists`
5. `python3 skills/ocas-forge/scripts/closure_convergence_sweep.py --date 2026-07-25`
   → GAPS BRIDGED: 0 (stable)
6. `python3 skills/ocas-forge/scripts/advance_gate_state.py --date 2026-07-25`
   → recomputes max mtime programmatically (no hand-typed literal), writes both
   monitor copies + praxis `ingest_state.last_ingest_run` (ISO format).
7. `python3 skills/ocas-forge/scripts/verify_genuine_gap_profile.py --date 2026-07-25`
   → `GENUINE GAP (excluding custodian): 0`
8. `python3 skills/ocas-forge/scripts/closure_closeout_check.py \
     --named ocas-dispatch/2026-07-25/dispatch-wave-20260725T162304Z.json --date 2026-07-25`
   → `=== gates ALL CLOSED ===`

## Result
- ZERO dispatch-wave journals minted this run (the existing 16:23 journal stays the only one).
- Email evidence durable in `evidence.jsonl` (dispatch-email-20260725T162539Z).
- GENUINE GAP = 0, all three closure gates green.

## Lesson
When a single dispatcher fire combines `new_emails` + `new_journals` for an ALREADY-CLOSED
wave: treat it as re-detection, run the email `close_email_only_wave.py` append (no journal)
plus the journal bridge+advance (no journal). Never invoke `run_mixed_wave_closure.py`
for a re-detection — that is the bug that perpetuates the re-fire loop.
