status: completed

status: completed
---
# Description
This PR addresses the "Dogfooding Paradox" vulnerability in the primary orchestrator entrypoint (`orchestrator.py`).
It implements absolute path resolution for all internal scripts called by `orchestrator.py`.

# Implementation Plan
1. In `tests/test_065_path_hijack.sh`, create a TDD scenario where a dummy workspace contains a malicious `scripts/spawn_reviewer.py` script. The orchestrator must be pointed at this workspace. The test should assert that the malicious script is NEVER executed.
2. Refactor `orchestrator.py` to calculate `RUNTIME_DIR = os.path.dirname(os.path.abspath(__file__))` at startup.
3. Update all `subprocess.run` calls in `orchestrator.py` that invoke `spawn_planner.py`, `spawn_coder.py`, `spawn_reviewer.py`, `spawn_arbitrator.py`, `merge_code.py`, and `get_next_pr.py` to use `os.path.join(RUNTIME_DIR, ...)` instead of relative paths.
4. Run the newly added test to ensure it passes (Green).

# Acceptance Criteria
- `tests/test_065_path_hijack.sh` runs and passes successfully.
- `orchestrator.py` exclusively relies on absolute paths for internal tooling.
