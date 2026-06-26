status: closed

---
status: closed
---
# PR 1: Runtime Path Isolation (Orchestrator Absolute Paths)

## 1. Description
This PR refactors `scripts/orchestrator.py` to use absolute paths based on `__file__`, resolving the execution context securely from the installed Runtime instead of the user workspace. It also introduces the TDD infrastructure `scripts/test_anti_reward_hacking.sh` testing physical path independence.

## 2. Tasks
- Modify `scripts/orchestrator.py`: Define `RUNTIME_DIR = os.path.dirname(os.path.abspath(__file__))`.
- Replace all relative invocations in `subprocess.run` (e.g., `["scripts/spawn_coder.py", ...]`) with `os.path.join(RUNTIME_DIR, "spawn_coder.py")`. Do this for coder, reviewer, planner, arbitrator, merge_code, and get_next_pr.
- Create `scripts/test_anti_reward_hacking.sh`. Include Test Scenario 1 (Path Independence - Physical Execution Test): Create an empty `dummy_workspace`, call orchestrator on it, and ensure it uses absolute paths without erroring on missing `scripts/` folder.
- Add `test_anti_reward_hacking.sh` to CI (`scripts/run_sdlc_tests.sh` or `preflight.sh`).

## 3. Acceptance Criteria
- `orchestrator.py` uses absolutely no `"scripts/..."` relative paths in its subprocess calls.
- `scripts/test_anti_reward_hacking.sh` validates the lack of relative paths by running in a scriptless directory successfully.
