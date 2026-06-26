status: closed

# PR-002a: Refactor Merge Script to Parse JSON Review Protocol

## 1. Objective
Update the core merge logic to natively parse JSON output from the Reviewer instead of relying on the legacy `[LGTM]` string, ensuring the core merge component is migrated.

## 2. Scope & Implementation Details
- Refactor `scripts/merge_code.py` to parse JSON and check for `"status": "APPROVED"`.
- Remove legacy `[LGTM]` checking logic exclusively from `merge_code.py`.
- Ensure basic unit tests for `merge_code.py` pass with JSON mock inputs.

## 3. TDD & Acceptance Criteria
- `merge_code.py` correctly parses JSON and triggers merge only on `"status": "APPROVED"`.
- `merge_code.py` no longer contains or relies on `[LGTM]` string checks.
- Related unit tests for `merge_code.py` pass cleanly.