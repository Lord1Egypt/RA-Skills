# Stale-state re-detection with post-dispatch gap journal closure

**Pattern date:** 2026-07-22

## Summary

When a stale-state re-detection finds its named journal already registered in BOTH eval stores, the post-dispatch verifier can still report GENUINE_GAP = 1 because an additional mentor-light journal landed AFTER the dispatcher's detected_at. If that gap journal is a self-referencing ocas-mentor light heartbeat with no actionable signals, do NOT rerun the full Forge/Mentor/Praxis pipelines. Close as a genuine no-op by bridging the gap relpath only, re-sweeping the verifier, and advancing state past the true max non-custodian/dispatch-wave journal mtime.

## Discrimination test

Read the gap journal. A post-dispatch Mentor self-reference shows:

- schema: mentor-journal-v2
- run_id: mentor-light-<TS>
- heartbeat_type: light
- entities_observed: ["ocas-mentor"] OR ["ocas-mentor", "ocas-dispatch"] OR any list dominated by ocas-mentor. A heartbeat that ALSO observed dispatch state (ocas-dispatch in the list) is STILL a self-reference, NOT a genuine gap — do not rerun the full pipeline on it.
- metrics.new_files_ingested: 1 (or 2 — a 2026-07-22T154530Z instance ingested the current wave's dispatch-wave journal + one sibling and was STILL a no-op self-reference; count=2 is NOT a genuine gap)
- metrics.new_entries: 1 (or 2, matching the ingest count)
- metrics.gap_detected: false OR absent/None (transient heartbeats may omit or null this key)
- outcome: success OR absent/None
- top-level type: may be null/None
- 0 events / 0 proposals / 0 decisions

If it matches, treat as mixed_genuine_no_op.

### Concrete observed instance (2026-07-22T075555Z)

A real post-dispatch mentor-light gap journal landed AFTER the dispatcher's detected_at with exactly: `entities_observed: ["ocas-dispatch", "ocas-mentor"]`, `gap_detected: None`, `type: None` (top level), `run_id: mentor-light-20260722T075555Z`, and 0 events/proposals/decisions. It was absent from dispatch-eval but present in praxis-eval. Bridged with `--action cross_skill_noop_mentor_self_reference` and re-swept: GENUINE GAP 1 -> 0. The presence of `ocas-dispatch` in `entities_observed` and `None` for `gap_detected`/`type` did NOT make it a genuine gap — it was a routine exogenous heartbeat. Lesson: key on the POSITIVE self-reference signals (mentor-light run_id prefix, 0 events, small ingest counts), and accept absent/None for the negative fields rather than requiring literal `false`/`success`. A heartbeat that observed dispatch state is still a no-op self-reference.

### Second confirmed instance (2026-07-22T154530Z)
A post-dispatch mentor-light gap journal landed at 15:45:30Z (after the 15:40:36Z dispatcher detected_at) with `entities_observed: ["ocas-dispatch", "ocas-mentor"]`, `new_files_ingested: 2`, `new_entries: 2`, `gap_detected: false`, `outcome: success`, 0 events/proposals/decisions. Despite the ingest count of 2 (it consumed the current wave's dispatch-wave journal + one sibling), it was a routine exogenous heartbeat — NOT a genuine gap. Bridged with `--action cross_skill_noop_mentor_self_reference`; verifier moved GENUINE GAP 1 -> 0. Confirms the discriminator is the POSITIVE self-reference signals (mentor-light run_id, 0 events, ocas-mentor-dominated entities), and the exact `new_files_ingested` value of 1 vs 2 is immaterial. This was the 15:40Z re-detection fire's only genuine gap; all other named journals were already in both eval stores and all 10 email threads were `action=none`, so the wave closed as a full MODE C no-op.

## Closure sequence

### 1. Bridge the gap in both eval stores
python3 scripts/bridge_eval_inline.py ocas-mentor/<DATE>/mentor-light-<TS>.json --action cross_skill_noop_mentor_self_reference

### 2. Re-sweep for additional genuine gaps
python3 scripts/verify_genuine_gap_profile.py --date <DATE>
Iterate until exit code 0 (GENUINE GAP = 0). If another post-dispatch journal surfaced, classify and bridge it before advancing state.

### 3. Advance praxis last_ingest_run
Recompute the max mtime across today's journals EXCLUDING ocas-custodian and dispatch-wave-*:
max_ts = max(os.path.getmtime(p) for p in today_journal_paths)
advance_ts = max_ts + 5.0
Write last_ingest_run as an ISO string derived from advance_ts, plus the raw float fields last_ingest_run_ts / last_ingest_ts. Use json.load + full overwrite; do not hand-type the literal.

### 4. Advance BOTH monitor copies
Overwrite both:
- ~/.hermes/commons/data/monitor_state/journal_ingest_state.json
- $HERMES_HOME/../indigo/commons/data/monitor_state/journal_ingest_state.json

Set latest_mtime = advance_ts and checked_at to the same ISO timestamp.

### 5. Re-affirm email second-wave state
For mixed waves on <operator>'s account, ensure dispatch-owned copies carry verified_second_wave: true:
- commons/data/ocas-dispatch/owner/last_email_check.json
- commons/data/ocas-dispatch/last_email_check_owner.json

Top-level GWS snapshot files (last_email_check.json, last_email_check_<account-identity>_gmail_com.json) may remain null under the monitor re-fire bug and are expected warnings from closure_closeout_check.py.

## Why full pipeline rerun is wrong

The dispatcher's new_files snapshot only covers journals present at detected_at. A later landing mentor-light heartbeat is an exogenous event, not a misclassified original. Rerunning Forge/Mentor/Praxis for a self-referencing light heartbeat wastes cycles and can mint spurious pipeline journals that re-trigger detection in the next wave. The correct response is no-op closure by bridging the residual gap only.

## Supported by session
## Supported by session
- Pre-bridge: both named dispatcher journals present in praxis + dispatch eval stores.
- Post-bridge: only the post-dispatch mentor-light journal was missing.
- Gap verifier moved from 1 -> 0 after single bridge + state advances.

## Closure-phase scan authority (CRITICAL — 2026-07-23 confirmation)
The dispatcher's `new_files` list is NOT the complete gap set during closure.
The genuine-gap SCAN (`verify_genuine_gap_profile.py --date <DATE>`) is
authoritative. In the 2026-07-23T0245Z re-detection, the dispatcher named
exactly ONE journal (`mentor-light-20260723T024049Z.json`) as `new_files`,
but the gap scan found SIX post-dispatch mentor-light heartbeats all missing
from eval stores (T023507Z, T023925Z, T024049Z, T024547Z, T025307Z,
T025548Z). Five of them were never in the dispatcher's `new_files`.
**Lesson:** When closing a Mode-C no-op wave, run the gap scan and bridge
EVERY `GAP <relpath>` line it reports — do NOT limit bridging to the
dispatcher's named `new_files`. Bridging 1 of 6 leaves 5 gaps, and the
wave re-fires forever.

### Third confirmed instance (2026-07-23T0245Z, 6-gap)
A Mode-C re-detection fire named 1 journal but the gap scan exposed 6
post-dispatch mentor-light no-op self-reference heartbeats:
- T023507Z: ent=['ocas-custodian','ocas-mentor'], new_files=2, gap=false, success
- T023925Z: ent=['journals','ocas-custodian','ocas-dispatch','ocas-forge','ocas-mentor'], new_files=282, gap=false, success  (proves ingest COUNT is immaterial — a 282-ingest heartbeat is still a noop self-reference)
- T024049Z: ent=['ocas-dispatch','ocas-mentor'], new_files=2, gap=false, success  (the dispatcher-named journal)
- T024547Z / T025307Z / T025548Z: ent=['ocas-mentor'], new_files=1, gap=false, success
All six matched the noop-self-reference discriminator (mentor-light prefix,
ocas-mentor in entities, gap_detected false/None, outcome success/None, 0
events/proposals/decisions). Bridged all six with `--action
cross_skill_noop_mentor_self_reference` in one `bridge_eval_inline.py`
call, re-swept (GAPS BRIDGED: 0), advanced praxis + both monitor gate
state via `advance_gate_state.py --date 2026-07-23`, re-affirmed email
second-wave, and asserted `=== gates ALL CLOSED ===`. GENUINE GAP 6 -> 0.
Companion `scripts/classify_gap_journals.py` now automates the
discriminator print for all gaps in one command.