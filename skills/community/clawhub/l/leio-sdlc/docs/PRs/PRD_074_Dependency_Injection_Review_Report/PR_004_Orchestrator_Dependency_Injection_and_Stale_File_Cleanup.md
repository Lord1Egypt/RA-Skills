status: closed

# PR-002: Orchestrator Dependency Injection and Stale File Cleanup

## 1. Objective
Update the Orchestrator to explicitly inject the review report path into the Reviewer and proactively delete any stale report files before spawning the Reviewer.

## 2. Scope & Implementation Details
- **Target File:** `scripts/orchestrator.py`
- **Implementation:**
  - In State 4 (Review), define a clear variable for the report path (e.g., `report_path = "Review_Report.md"`).
  - Add a step to safely delete `report_path` before calling `spawn_reviewer.py`, handling `FileNotFoundError` gracefully.
  - Update the subprocess call to `spawn_reviewer.py` to append `--out-file {report_path}`.
  - Read the evaluation verdict from `report_path` instead of the legacy `review_report.txt`.

## 3. TDD & Acceptance Criteria
- **Target File:** `tests/test_074_orchestrator_injection.sh` (New)
- **Assertions:**
  - Create a dummy stale report file before the test.
  - Run the relevant Orchestrator state.
  - Assert that the Orchestrator successfully deletes the stale file, passes the `--out-file` argument to the reviewer mock, and reads the final verdict from the correct path.