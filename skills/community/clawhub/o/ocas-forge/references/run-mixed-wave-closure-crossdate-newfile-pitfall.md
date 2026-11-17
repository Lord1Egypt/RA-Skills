# Cross-Date new_file Gap in run_mixed_wave_closure.py (confirmed live 2026-07-25)

A mixed dispatch wave (`dispatch-wave-20260725T103830Z`) carried `new_files` including
`ocas-sands/2026-07-26_evening_brief.json`. The closure runner was invoked with
`--date 2026-07-25`.

## The miss
`run_mixed_wave_closure.py` (steps 7–9: `closure_convergence_sweep.py` +
`verify_genuine_gap_profile.py`) gap-scans and bridges ONLY
`commons/journals/<skill>/<DATE>/` where `DATE == --date`. The Sands evening brief is
physically in `ocas-sands/2026-07-26/` (its `target_date` is the next day; Sands writes
the brief before midnight). Its mtime is on 2026-07-25, so the dispatcher flags it for the
2026-07-25 wave — but the directory is `2026-07-26`, which the `--date 2026-07-25` walker
never visits.

Result: `verify_genuine_gap_profile.py --date 2026-07-25` reported
`GENUINE GAP (excluding custodian): 0` (it only walks 2026-07-25 dirs), yet the file was
`0/0` in both eval stores (`commons/data/ocas-praxis/journals_evaluated.jsonl` and
`commons/data/ocas-dispatch/journals_evaluated.jsonl`) — a silent unbridged gap that
would re-surface on the next wave.

## Distinction from the custodian date pitfall
- **Custodian case** (`references/run-mixed-wave-closure-date-pitfall.md`): file NAMED with
  a future timestamp but living in a PAST dir (e.g. `ocas-custodian/2026-07-22/light-scan-...20260723T00...Z.json`).
  Fix: pass `--date 2026-07-22` (the DIR date) so the walker enters that dir.
- **Sands case (this doc):** file living in a genuinely FORWARD-dated dir with a PAST mtime.
  You CANNOT pass the forward date as `--date` (that would mis-scope the whole wave and drop
  all the real `--date` journals). The runner's own convergence sweep will not bridge it.

## Fix (manual, after the runner returns CLOSURE OK)
For each `new_file` whose parent dir date != `--date`:
```bash
python3 scripts/bridge_eval_inline.py <relpath> --action mixed_wave_<DATE> --require-exists
```
Then re-run `verify_genuine_gap_profile.py --date <DATE>` (still 0 expected for the main
date) and confirm the stray file now appears in BOTH eval stores. No gate-state re-advance
is needed if the stray file's mtime is already below the advanced `max_mt` (the Sands case:
mtime 10:26 < gate 10:38). If its mtime is ABOVE the gate, also re-run
`advance_gate_state.py --date <DATE>` + `closure_closeout_check.py`.

## Prevention note
The runner could be hardened to bridge the explicit `--new-files` list regardless of
directory date. Until that lands, the manual bridge above is REQUIRED for any cross-date
`new_file`, or the wave silently leaves a real eval gap.
