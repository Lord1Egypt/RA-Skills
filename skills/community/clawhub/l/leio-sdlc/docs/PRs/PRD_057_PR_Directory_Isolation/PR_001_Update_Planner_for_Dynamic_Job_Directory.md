status: completed

---
status: completed
dependencies: []
---
# PR 1: Update Planner for Dynamic Job Directory

## Description
Modify `scripts/spawn_planner.py` to support dynamic job directory computation based on the PRD file.

## Requirements
- If `--out-dir` is not explicitly provided, compute the Job Directory from the `--prd-file` argument (e.g., `docs/PRDs/PRD_057_Isolation.md` -> `docs/PRs/PRD_057_Isolation/`).
- The Planner must automatically create this directory (`os.makedirs(..., exist_ok=True)`) before writing the generated `PR_*.md` files.


> [Escalation] Tier 1 Reset triggered due to Coder failure or Arbitrator rejection.
