# Recover a Prior-Wave-Misclassified Dispatch (verbatim command sequence)

Companion to the recovery bullet in the SKILL.md "Dispatch / Cron Integration" section.
Use when a prior sibling wave already wrote `dispatch-wave-<EXISTINGTS>.json`
(registered in BOTH eval stores) but misclassified itself as `all_second_wave` /
`mixed_genuine_no_op` and skipped the explicit-run pipelines (no `forge-scan-*` for the
window, `last_ingest_run` stale).

All paths profile-scoped under `<hermes-home>/profiles/indigo`. Run from that dir.

## 1. Confirm the recovery trigger
```
ls commons/journals/ocas-dispatch/2026-MM-DD/dispatch-wave-*.json
# find the prior wave matching this dispatch's new_files; confirm it's in BOTH eval stores:
grep -c "dispatch-wave-<EXISTINGTS>" commons/data/ocas-praxis/journals_evaluated.jsonl
grep -c "dispatch-wave-<EXISTINGTS>" commons/data/ocas-dispatch/journals_evaluated.jsonl
find commons/journals/ocas-forge/2026-MM-DD/ -name 'forge-scan-*'   # expect EMPTY for the window
python3 -c "import json;print(json.load(open('commons/data/ocas-praxis/ingest_state.json'))['last_ingest_run'])"  # expect stale
```

## 2. Run the genuine pipeline (caller-side bridge)
Write a single Python script to `/tmp/` and run it (so all timestamps compose once).
Key steps inside the script:
- **Forge scan**: count `vp_*/vd_*` in `commons/data/ocas-forge/intake/` NOT in
  `intake/processed/` + data root (EXCLUDE `proposals/`). 0 unprocessed -> no-op.
  Write `commons/journals/ocas-forge/2026-MM-DD/forge-scan-<TS>.json` (all timestamps
  composed ONCE in the script). Assert `os.path.exists(forge_path) and forge_path.endswith(".json")`.
- **Mentor heartbeat**: build feed via `find ... -mtime -3`, run
  `python3 skills/ocas-mentor/scripts/cron-heartbeat-light.py < /tmp/feed.txt`
  (subprocess stdin, NEVER a shell pipe). Capture the ACTUAL journal via a
  content-timestamp scan (max `timestamp` field), NOT `ls -t`. Then run
  `python3 skills/ocas-mentor/scripts/correct_active_skills_30d.py`.
- **Praxis ingest**: `python3 skills/ocas-praxis/scripts/praxis_ingest_run.py`
  (auto-registers into praxis eval only).
- **Bridge**: idempotent append (full-relative-path substring check) of
  [heartbeat journal, forge-scan, every detected new_file, EXISTING dispatch-wave]
  into BOTH eval files (praxis key `journal_id`, dispatch key `filename`).
- **State**: advance `last_ingest_run` to the MAX mtime of all bridged journals;
  resync `journals_evaluated_count` / `last_eval_file_line` to actual line counts.

## 3. Rewrite the EXISTING wave journal (same run_id — do NOT mint a new one)
Use `write_file` on the prior path
`commons/journals/ocas-dispatch/2026-MM-DD/dispatch-wave-<EXISTINGTS>.json`
with `classification: routine_no_op`, `state_updated: true`, full
`journal_pipeline` + `email_triage` notes reflecting the genuine pipeline.

## 4. MANDATORY closeout — reconcile + assert zero gap
The pipeline bridge only covers detected `new_files` + the genuine outputs. Sibling
output journals written after the dispatcher's snapshot (e.g. a later `mentor-light`
from a concurrent heartbeat cron) will still surface as genuine gaps.
```
python3 skills/ocas-dispatch/scripts/reconcile_dispatch_eval_today.py --apply
python3 skills/ocas-dispatch/scripts/verify_genuine_gap_profile.py --date 2026-MM-DD
# assert: GENUINE GAP (excluding custodian): 0
```
If the probe still reports >0, re-run reconcile and re-sweep. Do NOT exit with a
non-zero gap — the dispatcher re-fires on the next scan. (In the 2026-07-14T13:41Z
wave, a sibling `mentor-light-20260714T134544Z.json` was the sole residual gap and was
closed by `--apply`.)

## 5. Guardrails
- Never run `bridge_explicit_run.py` in recovery — it mints a SECOND wave journal.
- Never trust `os.listdir` for the rewrite target — verify via eval-store membership + `ls`.
- Append to eval files with idempotent substring check; verify 0 duplicates after.
- Phantom-entry guard: every `journal_id` bridged must correspond to a real on-disk file.