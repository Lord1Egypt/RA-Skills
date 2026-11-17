# run_mixed_wave_closure.py — dispatched new_files bridge gap (confirmed live 2026-07-25)

## Symptom
`run_mixed_wave_closure.py` returns `=== gates ALL CLOSED ===` / `CLOSURE OK`,
`GENUINE GAP (excluding custodian): 0`, yet a dispatcher-flagged `--new-file`
is missing from the **DISPATCH** eval store (`commons/data/ocas-dispatch/journals_evaluated.jsonl`)
while present in the **PRAXIS** eval store (`commons/data/ocas-praxis/journals_evaluated.jsonl`).

## Root cause
The runner's explicit bridge list is `[MENTOR_REL, FORGE_REL, WAVE_REL, TASTE_REL]`.
The `--new-files` (the journals the dispatcher actually flagged) are NOT in that list —
they depend on `closure_convergence_sweep.py` to bridge. That sweep can leave a
non-custodian dispatched journal one-sided: present in praxis eval, absent from
dispatch eval. `verify_genuine_gap_profile.py` excludes `ocas-custodian` from its
genuine-gap count, so a one-sided non-custodian file still reports `GENUINE GAP=0`
and the closeout verifier still prints `gates ALL CLOSED` (gate `[1]` checks the
named wave journal, not every dispatched file).

Observed 2026-07-25: `ocas-custodian/2026-07-25/custodian-light-20260725T180102Z-lite.json`
was praxis=True dispatch=False after the runner exited CLOSURE OK.

## Fix (post-run, after CLOSURE OK)
For each dispatched `--new-file`, grep BOTH stores with the BARE relpath (no
`commons/journals/` prefix):
```
grep -c '"ocas-custodian/2026-07-25/custodian-light-20260725T180102Z-lite.json"' \
    commons/data/ocas-dispatch/journals_evaluated.jsonl
grep -c '"ocas-custodian/2026-07-25/custodian-light-20260725T180102Z-lite.json"' \
    commons/data/ocas-praxis/journals_evaluated.jsonl
```
If dispatch store count is 0, bridge manually:
```
python3 scripts/bridge_eval_inline.py \
    ocas-custodian/2026-07-25/custodian-light-20260725T180102Z-lite.json \
    --action mixed_wave_20260725 --require-exists
```
Then re-run `verify_genuine_gap_profile.py --date 2026-07-25` (still 0 — custodian excluded).

## Why this matters
A one-sided eval entry is a latent re-fire risk: a later monitor pass can flag
the dispatch-store-absent file as a genuine gap and re-trigger the wave. The
manual bridge makes both stores consistent and removes the latent gap.

## Distinction from other closure gaps
- **cross-date new_file** (`references/run-mixed-wave-closure-crossdate-newfile-pitfall.md`):
  file lives in a FORWARD-dated dir, never touched by the `--date` runner → bridge the stray.
- **mid-run mentor heartbeat** (residual-gap note): file lands after the single sweep →
  `bridge_eval_inline.py --action cross_skill_mitigation --require-exists`.
- **this gap**: file is in the `--date` dir and in praxis eval, but the runner's bridge
  list omits `--new-files` so the dispatch side was never written → manual dispatch-store bridge.
