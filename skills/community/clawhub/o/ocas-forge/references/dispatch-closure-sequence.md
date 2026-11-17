# Dispatch Closure Sequence (explicit-run new_journals)

After running `scripts/bridge_explicit_run.py --new-files <relpath>` for a `new_journals` explicit-run dispatch, the caller MUST close eval gaps to 0 before declaring done. `bridge_explicit_run.py` advances `last_ingest_run` but does NOT run the gap verifier. Cron pipelines (mentor-light, finch, custodian) write new journals in the window between the bridge and closure, so a re-sweep is required.

Verified caller sequence (2026-07-16 live run):

1. `python3 scripts/closure_convergence_sweep.py --date <YYYY-MM-DD>` bridges any journal missing from either eval store (dispatch + praxis). Run iteratively. It exits 0 when it bridges 0 gaps.
2. Re-run step 1 until it prints `GAPS BRIDGED: 0`.
3. `python3 scripts/verify_genuine_gap_profile.py --date <YYYY-MM-DD>` asserts GENUINE GAP = 0 (exit code 0). Custodian self-bridged journals are excluded by design, not genuine gaps.

Both scripts ARE present on disk (`scripts/closure_convergence_sweep.py`, `scripts/verify_genuine_gap_profile.py`). The older SKILL.md note that `reconcile_*`/`verify_*`/`closure_*` helpers "do NOT exist on disk" is obsolete for these two. `scripts/dispatch_redetection_close.py` still exists, but the ungated two-store reconcile is now owned by the two scripts above.