status: closed

---
status: closed
dependencies: ["PR 1: Add --slice-failed-pr argument and validation"]
---
# PR 2: Logic Routing and TDD Implementation

## Tasks
1. Update `scripts/spawn_planner.py` Prompt & Logic Routing:
   - **Test Mode (`SDLC_TEST_MODE=true`)**: If `--slice-failed-pr` is present, log the call, generate two mock files (`PR_Slice_1.md`, `PR_Slice_2.md`) containing `status: closed and exit `0`.
   - **Real Mode**: Override `task_string` if `--slice-failed-pr` is provided with the specific prompt mentioned in PRD-063.
2. Create `scripts/test_planner_slice_failed_pr.sh` (hermetic test script):
   - Use `setup_sandbox` and set `export SDLC_TEST_MODE=true`.
   - Implement Test Scenario 1 (Regression), 2 (File Missing), and 3 (Successful Slice).
3. Update `scripts/run_sdlc_tests.sh` (or `preflight.sh`) to include `./scripts/test_planner_slice_failed_pr.sh`.
