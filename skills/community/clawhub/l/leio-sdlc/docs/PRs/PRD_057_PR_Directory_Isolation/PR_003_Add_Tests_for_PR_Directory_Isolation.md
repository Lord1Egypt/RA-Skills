status: closed

---
status: closed
dependencies: []
---
# PR 3: Add Tests for PR Directory Isolation

## Description
Modify `scripts/test_orchestrator_fsm.sh` to ensure the directory isolation is implemented correctly.

## Requirements
- **Scenario 1**: Verify `spawn_planner.py` with `--prd-file` outputs files exclusively to the isolated directory.
- **Scenario 2**: Orchestrator polling with noise injection. Create a fake open PR in the root `docs/PRs/` and a valid one in the isolated dir. Ensure only the isolated PR is picked up and transitioned to closed.
- **Scenario 3**: Missing directory graceful sleep. Run orchestrator against a non-existent isolated directory and ensure it exits 0 without crashing.
