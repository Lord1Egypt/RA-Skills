status: completed

---
status: completed
title: Fix Orchestrator Merge Arguments and Update Tests
dependencies: ["PR-060-1"]
---
# PR-060-2: Fix Orchestrator Merge Arguments and Update Tests

## Objective
Fix the `merge_code.py` invocation signature in `orchestrator.py` and update TDD stubs to match the new template format.

## Tasks
1. In `scripts/orchestrator.py`, update `subprocess.run` calls for `scripts/merge_code.py`:
   - Replace `--pr-file current_pr` with `--branch branch_name`.
   - Replace `--repo-dir workdir` with `--review-file review_report_path`.
2. In `scripts/test_orchestrator_fsm.sh`:
   - Modify the `spawn_reviewer.py` stub for the Green Path test to output `[LGTM]`.
   - Modify the `spawn_reviewer.py` stub for the Red Path test to output `[ACTION_REQUIRED]`.
