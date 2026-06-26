# PRD_034: Manager Queue Polling Skill (The Brain)

## 1. Problem Statement
The `leio-sdlc` Manager agent currently assumes a one-to-one relationship between a project and a single PR contract. When it is invoked, it runs the `Coder -> Reviewer -> Merge` pipeline exactly once and then stops. To support "Micro-Slicing" (where a complex PRD is broken down into multiple smaller PR contracts), the Manager must be upgraded into a continuous "Queue Polling Engine" using the deterministic tools developed in ISSUE-028.

Furthermore, we must strictly enforce the **Token-Optimized CI Rule**: The Manager should never run tests directly. It must delegate test execution to the Coder.

## 2. Solution: The State Machine Loop
We will update the Manager's prompt/runbook (`SKILL.md`) to teach it the following deterministic `while` loop:

1. **Poll Queue**: Use `python3 scripts/get_next_pr.py --job-dir .sdlc/jobs/<Feature_Name>`.
   - If output contains `[QUEUE_EMPTY]`, the Manager announces project completion and exits cleanly.
   - If output is a file path (e.g., `PR_001.md`), proceed to step 2.
2. **Delegate Coding**: Call the Coder (via `spawn_coder.py` or equivalent). 
   - **Strict Delegation Rule**: The Manager MUST append the following instruction to the Coder: *"You must execute `./preflight.sh` yourself in your sandbox. If it fails, you must fix it. Do NOT return to me until you see `✅ PREFLIGHT SUCCESS`."*
3. **Delegate Review**: Call the Reviewer. If `[ACTION_REQUIRED]`, loop back to the Coder with the feedback (Correction Loop).
4. **Merge**: If `[LGTM]`, call `merge_code.py`.
5. **Close PR**: Use `python3 scripts/update_pr_status.py --pr-file <file> --status closed` to mark the current PR as done.
6. **Repeat**: Go back to Step 1.

## 3. Testing Strategy (E2E)
We will create a new E2E test: `scripts/test_manager_queue_polling.sh`.
- **Sandbox Setup**: Create an isolated git repository. Create a `.sdlc/jobs/Feature_X/` directory.
- **Mock PRs**: Create `PR_001_DB.md` (status: open), `PR_002_API.md` (status: open), and `PR_003_UI.md` (status: open).
- **Mock Tooling**: To save tokens and avoid nested LLM calls during the test, the test script should replace `spawn_coder.py`, `spawn_reviewer.py`, and `merge_code.py` with dummy bash scripts that simply return success (exit 0) and output `[LGTM]` when called.
- **Execution**: Run the Manager agent against this sandbox.
- **Assertions**: 
  - Assert that `get_next_pr.py` was called successfully until empty.
  - Assert that all three PR files now contain `status: closed`.
  - Assert that the Manager exits successfully.

## 4. Acceptance Criteria
- [ ] `scripts/test_manager_queue_polling.sh` is written and accurately tests the loop logic using mocked sub-agents.
- [ ] `SKILL.md` is updated to include the Queue Polling state machine and the strict Coder delegation rule.
- [ ] The E2E test passes when the updated Manager Skill is executed.