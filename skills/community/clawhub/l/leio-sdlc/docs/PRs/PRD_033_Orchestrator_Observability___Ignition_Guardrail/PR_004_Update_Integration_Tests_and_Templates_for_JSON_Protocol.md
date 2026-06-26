status: closed

# PR-002b: Update Integration Tests and Templates for JSON Protocol

## 1. Objective
Migrate all remaining peripheral scripts, templates, and integration tests to exclusively use the new JSON review protocol, completing the deprecation of `[LGTM]`.

## 2. Scope & Implementation Details
- Update `scripts/test_preflight_guardrails.sh` to use JSON-formatted mock review reports.
- Identify and clean up any other scripts or templates (e.g., notification formatters or test mocks) still relying on the legacy `[LGTM]` protocol.
- Ensure all end-to-end and preflight tests run successfully with the new JSON schema.

## 3. TDD & Acceptance Criteria
- `scripts/test_preflight_guardrails.sh` passes 100% using JSON mocks.
- No references to `[LGTM]` remain in any test scripts or templates.
- The entire CI pipeline and integration tests pass cleanly with the new protocol.