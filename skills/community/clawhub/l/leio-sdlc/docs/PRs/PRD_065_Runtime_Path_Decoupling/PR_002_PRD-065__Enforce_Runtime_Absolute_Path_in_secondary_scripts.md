status: completed

status: completed
---
# Description
This PR addresses the remaining instances of relative path resolution in secondary orchestrator tools, specifically `spawn_planner.py` and `spawn_manager.py`.

# Implementation Plan
1. In `tests/test_065_path_hijack_secondary.sh`, create a scenario mirroring the primary hijack test, but target `spawn_planner.py` (which might call `create_pr_contract.py` via relative path) and `spawn_manager.py` (which polling queue tests).
2. Refactor `spawn_planner.py` to use `RUNTIME_DIR` (or `SDLC_DIR`) calculated via `os.path.abspath(__file__)` to invoke `create_pr_contract.py`.
3. Refactor `spawn_manager.py` to similarly enforce absolute paths for its sub-scripts.
4. Verify that the secondary hijack tests pass successfully.

# Acceptance Criteria
- Secondary tools (`spawn_planner.py`, `spawn_manager.py`) no longer use relative paths for runtime scripts.
- TDD integration test `tests/test_065_path_hijack_secondary.sh` passes successfully.
