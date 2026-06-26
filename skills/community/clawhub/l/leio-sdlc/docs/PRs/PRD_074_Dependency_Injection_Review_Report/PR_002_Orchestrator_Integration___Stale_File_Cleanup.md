status: completed

# PR-002: Orchestrator Integration & Stale File Cleanup

## 1. Objective
Update the Orchestrator to inject the review report path into the Reviewer and proactively clean up stale state to prevent infinite loops.

## 2. Scope & Implementation Details
- **File**: `scripts/orchestrator.py`
- **Logic**: In State 4, define the artifact path (`Review_Report.md`). Proactively delete this file before spawning the Reviewer, safely catching `FileNotFoundError`. Modify the subprocess call to `spawn_reviewer.py` to include `--out-file Review_Report.md`. Update the verdict reading logic to read from this exact path instead of `review_report.txt`.

## 3. TDD & Acceptance Criteria
- **Test**: Create `tests/test_074_orchestrator_cleanup.sh`.
- **Criteria**: Create a stale report file with a fake verdict. Run the Orchestrator's State 4 logic. Assert that the stale file is deleted before the reviewer runs, that the subprocess is called with `--out-file`, and that the Orchestrator successfully reads the new verdict.
