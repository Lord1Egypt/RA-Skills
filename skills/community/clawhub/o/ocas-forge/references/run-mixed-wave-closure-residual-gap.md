# run_mixed_wave_closure.py — Residual GENUINE GAP after CLOSURE OK

**Observed live 2026-07-23.** The mixed-wave closure runner
(`skills/ocas-forge/scripts/run_mixed_wave_closure.py`) can print
`=== gates ALL CLOSED ===` + `CLOSURE OK` while
`verify_genuine_gap_profile.py --date <DATE>` still reports
`GENUINE GAP (excluding custodian): 1`.

## Why
The runner's terminal sequence is:
1. `closure_convergence_sweep.py --date <DATE>` — iterates bridging until 0
   additions *at that moment*.
2. `verify_genuine_gap_profile.py --date <DATE>` — prints the current gap
   (may be > 0 if a heartbeat landed between step 1 and this call).
3. `advance_gate_state.py --date <DATE>` — recomputes max mtime and advances
   BOTH monitor copies + praxis `last_ingest_run`, **regardless of the gap
   value from step 2**.
4. `closure_closeout_check.py` — passes because gate [1] (wave journal
   bridged) and gate [2] (state advanced past max mtime) are satisfied.
   Gate [2] does NOT check eval-store gap membership.

So a journal that lands during the run (typically a `mentor-light-*` heartbeat
on the ~5-min timer) gets caught by step 2's verify as `GAP` but is never
bridged, yet the runner still closes.

Observed: sweep bridged
`ocas-mentor/2026-07-23/mentor-light-20260723T173739Z.json`; verify then
reported `ocas-mentor/2026-07-23/mentor-light-20260723T174035Z.json` as the
lone `GENUINE GAP`; runner advanced state and printed `CLOSURE OK` anyway.

## Risk
- The monitor will NOT re-fire on the unbridged file: `advance_gate_state.py`
  moved `latest_mtime`/`last_ingest_run` past its mtime, so the re-detection
  gate is satisfied.
- But the eval store (`journals_evaluated.jsonl`) retains a latent gap. A
  future gap-scanner or any process keyed on eval-store completeness will see
  it. It is inconsistent state, not a live trigger.

## Fix (post-run settle pass — ALWAYS do this after the runner)
After `CLOSURE OK`, run one explicit settle pass:
```bash
python3 skills/ocas-forge/scripts/bridge_eval_inline.py \
  --action cross_skill_mitigation --require-exists \
  ocas-mentor/2026-07-23/mentor-light-20260723T174035Z.json   # the file(s) verify reported
python3 skills/ocas-forge/scripts/verify_genuine_gap_profile.py --date 2026-07-23
# require: GENUINE GAP (excluding custodian): 0
```
This is the same settle pass the manual closure runbooks mandate for timer
churn — the runner simply does not loop it internally. Treat `CLOSURE OK` as
"gate state closed," not "eval store clean." Reaching `GENUINE GAP = 0` is a
separate, recommended final step.

## Do NOT treat this as a runner bug
The runner's contract is gate-state closeout (stop the re-fire loop), which it
fulfills. Holding `GENUINE GAP = 0` forever is impossible while
`mentor-light`/`ocas-rally` timers fire. The settle pass is the correct,
bounded way to clear the specific file that landed mid-run.
