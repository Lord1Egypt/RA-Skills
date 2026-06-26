status: completed

# PR 2: Complete Refactoring of All Subprocess Invocations

## 1. Goal
Complete the refactoring of all `subprocess.run` or `Popen` calls in the entire `leio-sdlc` engine to use absolute path resolution relative to `RUNTIME_DIR`.

## 2. Changes
- **orchestrator.py**:
  - Scan and refactor ALL remaining `subprocess` calls (e.g., `spawn_coder.py`, `spawn_reviewer.py`, `merge_code.py`, `update_pr_status.py`).
- **scripts/merge_code.py** (if applicable):
  - Ensure any internal SDLC script calls here also follow the absolute path rule.
- **scripts/spawn_reviewer.py** (if applicable):
  - Ensure any internal SDLC script calls here also follow the absolute path rule.
- **Integration Test Expansion**:
  - Update `tests/test_065_path_hijack.py` to verify that not only `spawn_planner.py` but also other scripts like `spawn_reviewer.py` are protected from hijacking.

## 3. Acceptance Criteria
- [ ] No internal SDLC script calls in the engine use relative paths.
- [ ] ALL `subprocess` calls resolve relative to the engine's absolute base path.
- [ ] Expanded integration test passes across multiple hijacked script scenarios.
- [ ] status: open