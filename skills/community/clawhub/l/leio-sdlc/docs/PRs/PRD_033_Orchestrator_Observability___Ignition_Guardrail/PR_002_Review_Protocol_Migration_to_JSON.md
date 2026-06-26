status: superseded

# PR-002: Review Protocol Migration to JSON

## 1. Objective
Deprecate the legacy `[LGTM]` string-based review protocol and enforce structured JSON parsing for review reports across the SDLC framework.

## 2. Scope & Implementation Details
- Refactor `merge_code.py` to natively parse JSON output from the Reviewer and check for `"status": "APPROVED"` instead of relying on `[LGTM]`.
- Completely remove any legacy `[LGTM]` checking logic.
- Identify and clean up any other scripts or templates relying on the legacy protocol.
- Update preflight and integration tests (e.g., `scripts/test_preflight_guardrails.sh`) to use JSON-formatted mock review reports aligned with the new schema.

## 3. TDD & Acceptance Criteria
- `merge_code.py` successfully parses and merges PRs based solely on the JSON `"status": "APPROVED"`.
- All `[LGTM]` string dependencies are removed.
- All preflight and integration tests pass 100% using the new JSON review protocol.
