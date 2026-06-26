status: in_progress

# PR-1009-1: De-duplicate qmt_client.py and Fix Imports

## 1. Objective
Clean up duplicate files and establish a single source of truth for `qmt_client.py` within the `AMS` project, and refactor tests to use the correct import paths.

## 2. Scope & Implementation Details
- Analyze `AMS/qmt_client.py` and `AMS/scripts/qmt_client.py`. Keep the most up-to-date version in `AMS/scripts/` and delete the redundant version at `AMS/qmt_client.py`.
- Modify `AMS/tests/test_qmt_client.py` to import `QMTClient` correctly from `scripts.qmt_client`.
- Update any other scripts (like `pilot_stock_radar.py`) to use the unified import path.
- Add `__init__.py` to `scripts/` if necessary to ensure it's treated as a package.

## 3. TDD & Acceptance Criteria
- Running `pytest AMS/tests/test_qmt_client.py` passes successfully with no `ImportError`.
- `ls AMS/qmt_client.py` returns `No such file or directory`.
- The codebase runs without any broken imports related to `qmt_client`.

> [Escalation] Tier 1 Reset triggered due to Coder failure or Arbitrator rejection.
