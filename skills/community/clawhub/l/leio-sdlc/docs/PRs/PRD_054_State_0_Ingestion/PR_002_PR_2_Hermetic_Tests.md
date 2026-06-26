status: completed

---
status: completed
dependencies: ["PR_1_State_0_Logic"]
---
# PR 2: Implement Hermetic Tests for Orchestrator State 0

## Description
Implement 4 deterministic TDD test scenarios in `scripts/test_orchestrator_fsm.sh` to validate Orchestrator State 0 logic without network flakiness.

## Tasks
1. In `scripts/test_orchestrator_fsm.sh`, append the following 4 tests using `setup_sandbox`:
   a. **Test 1: Pure State 0 Start**: Stub Planner to create `PR_001_Mock.md` in `job_dir`. Run Orchestrator without `--force-replan`. Assert it logs "State 0: Auto-slicing PRD", successfully calls Planner, and processes `PR_001_Mock.md`.
   b. **Test 2: Idempotency (Resume)**: Pre-create `PR_001_Existing.md` in `job_dir`. Stub Planner to throw an exception if called. Run Orchestrator. Assert it logs "Resuming queue", does NOT call Planner, and processes existing PR.
   c. **Test 3: Force Replan**: Pre-create `PR_Old.md`. Stub Planner to create `PR_New.md`. Run Orchestrator with `--force-replan`. Assert `PR_Old.md` is deleted, Planner is called, and `PR_New.md` is processed.
   d. **Test 4: Planner Failure**: Stub Planner to do absolutely nothing. Run Orchestrator. Assert Orchestrator exits with code 1 and logs "[FATAL] Planner failed".
2. Ensure `./preflight.sh` executes successfully.
