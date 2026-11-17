# run_mixed_wave_closure.py — `--date` is load-bearing (not cosmetic)

`skills/ocas-forge/scripts/run_mixed_wave_closure.py` writes its
`forge-scan-*` + `dispatch-wave-*` journals into `ocas-<skill>/<DATE>/`
and runs `closure_convergence_sweep.py`, `verify_genuine_gap_profile.py`,
`advance_gate_state.py`, and `closure_closeout_check.py` **all against that
same `<DATE>` directory**.

`--date` defaults to `datetime.now(timezone.utc).strftime("%Y-%m-%d")`
= **system UTC today**. `--dispatch-ts` is cosmetic (only echoed into a
`note` field; the journal is self-minted at the script's runtime TS).

## The trap (confirmed live 2026-07-23)
Custodian journal files carry a ~7h12m mtime/clock offset: a file named
`ocas-custodian/.../light-scan-20260723T000857Z.json` can physically
reside in the **`ocas-custodian/2026-07-22/`** directory (date dir = prior
day relative to the filename / detection date). The dispatcher's `new_files`
list mixes both shapes.

If you pass `--date 2026-07-23` (detection date) or accept the default
`today`:
- the wave journal is written into the wrong `2026-07-23/` dir,
- the gap-scan walks `2026-07-23/` and never re-scans the custodian
  journals in `2026-07-22/`,
- `GENUINE GAP` stays > 0 (or the custodian gap is silently missed),
- the wave re-fires forever.

## Rule
Derive `<DATE>` from the **actual directory each dispatcher `new_file`
resides in** — `ls -la` the parent of every relpath — never from
`detected_at`. For custodian files spanning midnight, `<DATE>` is typically
the **prior day** relative to detection. In the 2026-07-23 dispatch the
correct call was:

```
python3 skills/ocas-forge/scripts/run_mixed_wave_closure.py \
  --dispatch-ts 20260723T000929Z \
  --new-files ocas-custodian/light-scan-20260723T000857Z.json \
              ocas-custodian/2026-07-22/escalation-loop-20260723T000920Z.json \
  --date 2026-07-22
```

(`--date 2026-07-22` matched the physical dir both custodian files live in.)

## Also note (same script)
- The wave journal's `emails` block is hardcoded `path_a: 0, path_b: 0,
  mode: "path_a_skip_verify_evidence"`. If this wave closed a genuine
  email Path B gap, `patch` the **entire** `emails` object (not the inner
  fragment — fuzzy match leaves a dangling comma → invalid JSON) to the real
  counts, then re-validate with `python3 -c "import json; json.load(open(...))"`
  and re-run `closure_closeout_check.py --named <wave> --date <DATE>`.
- Newest custodian/mentor journals may carry a `2026-07-23/` *filename*
  but a `2026-07-22/` *dir* with 07-22 mtime — always trust the dir,
  not the name.

## Two-date-dir mixed wave (confirmed live 2026-07-23)

When the dispatcher's `new_files` span MORE THAN ONE date dir — this
session: `ocas-finch/2026-07-23/scan-0107.json` +
`ocas-mentor/2026-07-23/mentor-light-20260723T010034Z.json` (both in
`2026-07-23/`) AND `ocas-custodian/2026-07-22/
light-scan-20260722T1805Z.json` (in `2026-07-22/`) — a SINGLE
`--date` is insufficient. The gap verifier and `advance_gate_state.py` each
walk ONE `<DATE>` dir only. Re-detection closure (do NOT re-run pipelines
or mint a wave journal) must instead:

1. **Verify/bridge for BOTH dates.** Run `verify_genuine_gap_profile.py
   --date 2026-07-22` AND `--date 2026-07-23`. Each covers its own
   dir. A genuine gap reported by the verifier but ABSENT from `new_files`
   is the EXPECTED straggler shape (post-detection mentor heartbeats land
   after `detected_at`) — bridge it (`bridge_eval_inline.py
   --require-exists`), do NOT treat it as a false positive.
2. **`advance_gate_state.py` is GLOBAL, not per-date.** It recomputes
   `max_mt` over the one `--date` dir and writes BOTH monitor copies +
   praxis `last_ingest_run` from that single dir's max. If you advance
   `2026-07-22` LAST, the global `latest_mtime` would be the custodian
   file's ~01:03Z — which is BELOW the finch/mentor files at ~01:10–01:20Z
   in `2026-07-23/`, so gate [2] goes False and the wave re-fires.
   **RULE: run `advance_gate_state.py --date 2026-07-22` FIRST, then
   `--date 2026-07-23` LAST** so the final global `latest_mtime`
   covers the newest file across BOTH dirs.
3. **`closure_closeout_check.py` is safe per-date** (reads global state),
   but the `--named` journal must exist in BOTH eval stores. Pick any
   already-bridged journal in either dir.

Convergence-sweep caveat: `closure_convergence_sweep.py` EXCLUDES custodian
(`EXCLUDED = {"ocas-custodian"}`), so it will NOT bridge a custodian file
missing from dispatch-eval. Bridge custodian manually via
`bridge_eval_inline.py --require-exists` (its `append_unique` skips any
store the rel is already in, so only the missing side is added), then let
the sweep handle finch/mentor for the other date.

This session closed clean: GENUINE GAP=0 for both `2026-07-22` and
`2026-07-23`; `=== gates ALL CLOSED ===` on both closeout checks;
`wave_redetection_no_op` evidence record appended.
