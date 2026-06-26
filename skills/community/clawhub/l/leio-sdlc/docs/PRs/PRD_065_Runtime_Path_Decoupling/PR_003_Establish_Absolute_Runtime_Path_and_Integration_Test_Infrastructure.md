status: completed

# PR 1: Establish Absolute Runtime Path and Integration Test Infrastructure

## 1. Goal
Introduce a robust mechanism for calculating the absolute runtime directory in `orchestrator.py` and implement a TDD integration test that detects path hijacking attempts.

## 2. Changes
- **orchestrator.py**:
  - Ensure `RUNTIME_DIR` is correctly established at the start of `main()`.
  - Refactor at least one internal `subprocess.run` call (e.g., the `spawn_planner.py` or `get_next_pr.py` call) to use `os.path.join(RUNTIME_DIR, ...)` if not already done, ensuring it works even after `os.chdir(workdir)`.
- **tests/test_065_path_hijack.py** (or `.sh`):
  - Implement the TDD strategy:
    1. Create a temporary `workdir`.
    2. Create a fake `scripts/spawn_planner.py` (or similar) inside the `workdir` that writes a "HIJACKED" sentinel.
    3. Run the real `orchestrator.py` with `--workdir` pointing to the temp dir.
    4. Assert that the "HIJACKED" sentinel is NOT found and the real script was executed.

## 3. Acceptance Criteria
- [ ] `orchestrator.py` calculates `RUNTIME_DIR` using `os.path.dirname(os.path.abspath(__file__))`.
- [ ] Integration test `tests/test_065_path_hijack.py` exists and passes.
- [ ] The orchestrator does not execute scripts from the target `workdir`.
- [ ] status: open