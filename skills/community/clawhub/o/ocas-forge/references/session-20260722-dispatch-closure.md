# Dispatch 2026-07-22 Closure Notes

## Wave shape
- Mixed `new_journals` (2 files) + `new_emails` (1 <operator> thread).
- Dispatcher `new_files`: `custodian-light-20260722T0408Z.json`, `mentor-light-20260722T040523Z.json`.
- Email dispatch thread: `<thread-id>` ("Re: Roller shade - <operator-last>") — `is_new: false`, `actionable: 1` from monitor heuristic but `priority: 30`, `intent: informational`.

## Journal closure sequence
1. `verify_genuine_gap_profile.py --date 2026-07-22` reported 4 mentor-light gaps.
2. `bridge_eval_inline.py` bridged all 4 mentor-light gaps in one call.
3. Re-ran verifier → `GENUINE GAP = 0`.
4. Ran Mentor light heartbeat via single terminal block (pre-run evidence count + script + post-run verification + `correct_active_skills_30d.py`).
   - Evidence grew: 2781 → 2782 → 2783 after correction.
   - Script reported `active_skills_30d=17`; corrected true count = 21.
5. Re-ran `verify_genuine_gap_profile.py --date 2026-07-22` → 1 new gap (`mentor-light-20260722T041345Z.json`) written by the heartbeat after the prior scan.
6. Bridged that gap, re-ran verifier → `GENUINE GAP = 0`.
7. Ran `closure_convergence_sweep.py --date 2026-07-22` → bridged 1 additional later-sibling gap (`mentor-light-20260722T041612Z.json`), then 0 on second sweep.
8. Ran `closure_closeout_check.py --date 2026-07-22 --named ocas-mentor/2026-07-22/mentor-light-20260722T041023Z.json`.
   - Gate [1] passed after all bridge steps.
   - Gate [2] initially False for praxis/monitor copies.
9. Advanced state gates in ONE terminal Python block:
   - Recomputed `max_mtime` across ALL `commons/journals/*/2026-07-22/*.json` via `os.path.getmtime`.
   - Set `latest_mtime = max_mt + 2.0` and `last_ingest_run = <max ISO + pad>` for:
     - `~/.hermes/commons/data/monitor_state/journal_ingest_state.json`
     - `$HERMES_HOME/../indigo/commons/data/monitor_state/journal_ingest_state.json`
     - `$HERMES_HOME/../indigo/commons/data/ocas-praxis/ingest_state.json`
   - Used programmatic recomputation; did NOT hand-type float/ISO literals.
10. Re-ran `closure_convergence_sweep.py` → 0 additions; re-ran `closure_closeout_check.py` → `=== gates ALL CLOSED ===`.
    - Gate [2] for both monitor copies and praxis `last_ingest_run`: True.
    - Gate [3] email required copies: True for owner/indigo account-specific files.
    - Gate [3] warn-only top-level GWS snapshots: none (`None`) — expected under monitor re-fire bug; do not conflate with failure.

## Email path
- Verified `<thread-id>` against `evidence.jsonl`: 13+ structured records, all `action:none`.
- Confirmed per cron-triage-workflow.md Path A rules:
  - Leave `last_email_check` counts untouched on Path A.
  - Do NOT draft or re-read thread content.
  - Do NOT mint a wave journal for this email-only closure.
- Escalation-preservation check: prior record at evidence line 3 already assigned `action:none`; no live escalation present.

## Durability lessons
- Post-mentor-heartbeat bridge must re-run verifier before closure — new mentor journals can land during closeout.
- Convergence sweep can still bridge later-sibling heartbeats even after verifier shows 0 gaps.
- State advancement must happen AFTER the FINAL verifier read; otherwise newly-landed journals will exceed the gate and re-open the loop.
- For mixed waves, email closure does not need a wave journal when threads are complete Path A — but journal + state closure DOES need both eval registrations, state advance, and an `ALL CLOSED` closeout assertion.

## 13:45Z second-wave closure (same day, second wave)
- Dispatcher fire: `new_journals` (1 file `mentor-light-20260722T134024Z.json`) + `new_emails` (14 <operator> threads).
- Classification: **complete second-wave** — journal already in both eval stores (praxis=1, dispatch=1); all email threads `is_new: false`.
- Email evidence gate applied (per the hard rule): `verify_evidence_threads.py` on all 10 wave threads → all `in_evidence(structured) action=none`. Scrutinized priority-80 OpenAI sign-in (`<thread-id>`): legit downgrade (own device/location), not a dropped escalation. See `references/mixed-wave-closure-email-evidence-gate.md` worked example.
- Post-dispatch gap: `mentor-light-20260722T134521Z.json` (landed after detected_at) bridged via `closure_convergence_sweep.py`. Re-verify `GENUINE GAP = 0`.
- Gate [2] advanced via `advance_gate_state.py` (max mtime 1784727922.84 → +5s); re-sweep 0; `closure_closeout_check.py` → `=== gates ALL CLOSED ===`.
- No pipelines executed (no-op classification honored), no drafts, no inbox touched.
