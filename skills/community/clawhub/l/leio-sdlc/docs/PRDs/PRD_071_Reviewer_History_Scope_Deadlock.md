# PRD-071: Reviewer History Scope Deadlock Fix

## 1. Objective
Fix a critical deadlock where the Reviewer audits intra-branch commit history instead of the base branch. This causes false-positive "Reward Hacking" rejections when a Coder iterates and modifies its own tests within a feature branch. The history extraction must be rigidly locked to the target merge branch (e.g., `master`).

## 2. Scope & Implementation Details
**Target File:** `scripts/spawn_reviewer.py`
- Locate the section where `recent_history.diff` is generated during the Graceful Bypass or standard diff logic.
- The current command is: `history_cmd = f"git log -n {history_depth} -p > recent_history.diff"`
- **Change required:** Append `{args.diff_target}` to the `git log` command so it exclusively pulls history from the base branch, ignoring the current `HEAD`'s local commits.
- **New command format:** `history_cmd = f"git log -n {history_depth} -p {args.diff_target} > recent_history.diff"`

## 3. TDD & Acceptance Criteria

**Self-Explanatory Error Messages:**
- The two error messages added in this issue must be self-explanatory, clearly indicating the context and the reason for the failure.

**E2E Test Mocks:**
- The e2e test for this feature must use mock objects (e.g., mocking `subprocess.run` or `git` calls) instead of relying on a real git workspace to isolate the test environment and ensure reliability.

**Test Script:** Create `tests/test_071_reviewer_history_scope.py` (or modify existing e2e test) using `unittest.mock`.
The test must prove that the generated `recent_history.diff` strictly ignores intra-branch commits by asserting the mocked git command includes `{args.diff_target}`.