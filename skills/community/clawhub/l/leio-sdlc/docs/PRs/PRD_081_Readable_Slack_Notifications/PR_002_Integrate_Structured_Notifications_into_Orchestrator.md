status: open

# PR-002: Integrate Structured Notifications into Orchestrator

## 1. Objective
Replace the existing unstructured Slack notification calls in the main orchestrator flow with the new structured formatter.

## 2. Scope (Functional & Implementation Freedom)
- Locate all SDLC state transitions in the orchestrator workflow (e.g., start, slicing, coder start, review start, etc.).
- Update the notification dispatch logic to use the formatters built in PR-001.
- *The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- Update or create integration/unit tests for the orchestrator's notification dispatch.
- Use mocks to intercept the notification channel calls and assert that the correctly formatted strings are being dispatched at each stage.
- All tests MUST pass (GREEN) before submitting.