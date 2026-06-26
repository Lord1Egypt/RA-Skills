status: closed

---
status: closed
dependencies: []
---
# PR 1: Add --slice-failed-pr argument and validation

## Tasks
1. Update `scripts/spawn_planner.py` to include `--slice-failed-pr` in `argparse` (optional, default: `None`).
2. Add pre-flight validation:
   - If `--slice-failed-pr` is provided, check if the file exists and its size is `> 0`.
   - If not, print `[Pre-flight Failed] Planner cannot start. Failed PR file not found or empty at '<PATH>'.` and `sys.exit(1)`.
   - Read the contents of the failed PR into a variable (e.g., `failed_pr_content`).
