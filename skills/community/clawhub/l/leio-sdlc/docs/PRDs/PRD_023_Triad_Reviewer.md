# PRD_023: E2E Testing of Triad Consistency (Sub-Agent Integration Tests)

## 1. Problem Statement
The "Limb Stubbing" tests (ISSUE-020) verify that the Manager attempts to call the correct scripts. However, they do not verify that the sub-agents (Planner, Coder, Reviewer) behave correctly when executed with real prompts and playbooks. We need a "Triad Consistency Test" (testing the integration of Script + Playbook + Injection Prompt) to prevent issues like the Reviewer's format breakdown (ISSUE-022).

## 2. Goals
- Create independent sandboxed tests for the Planner, Coder, and Reviewer.
- These tests must execute the *real* python spawn scripts (without `SDLC_TEST_MODE=true` interception) but operating on *dummy data* so they don't break the main repository.
- Assert the *actual text output/behavior* of the LLM sub-agents.

## 3. Implementation Plan (Iterative)
We will start with the **Reviewer** (the most historically flaky agent).

### 3.1 The Reviewer Triad Test (`scripts/test_triad_reviewer.sh`)
- **Setup Sandbox**:
  - Create a dummy PR contract (`tests/dummy_triad_pr.md`).
  - Create a dummy code diff (`tests/dummy_triad.diff`) containing a harmless `--- a/file +++ b/file` change.
- **Trigger**:
  - We cannot use `SDLC_TEST_MODE=true` because we *want* the script to execute the real `openclaw sessions_spawn`.
  - Wait, if we use the existing `spawn_reviewer.py`, it hardcodes `git diff` execution in production mode!
  - *Architectural Fix*: We need a way to feed a predefined diff file into `spawn_reviewer.py` for testing purposes, bypassing the actual `git diff` shell execution. 
  - Update `spawn_reviewer.py` to accept an optional `--override-diff-file` argument. If provided, it skips running `git diff` and just uses this file.
- **Execution**:
  - Run `python3 scripts/spawn_reviewer.py --pr-file tests/dummy_triad_pr.md --override-diff-file tests/dummy_triad.diff`.
  - Since this prints the agent's output to stdout, we capture the stdout of this script.
- **Assertion**:
  - Assert that the captured stdout contains the exact string `[LGTM]`.
  - Assert that the captured stdout does NOT contain the raw diff strings (e.g., `--- a/`).

## 4. Acceptance Criteria (Reviewer Phase)
- [ ] `spawn_reviewer.py` updated to support `--override-diff-file`.
- [ ] `test_triad_reviewer.sh` correctly provisions dummy files.
- [ ] The test executes the real LLM call and successfully asserts the output format.
- [ ] The test does not leave dirty git state in the main repo.