status: closed

# PR-001: Implement Structured Notification Formatters

## 1. Objective
Create a dedicated utility or module to generate the structured, emoji-prefixed Chinese notification messages for different SDLC stages.

## 2. Scope (Functional & Implementation Freedom)
- Build a formatter component that takes SDLC state context (e.g., PRD ID, PR ID, slice count, review results) and returns the formatted string as requested in the PRD (e.g., "🚀 1. [prd-xxx] SDLC 启动").
- *The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- Create unit tests for the new formatter component.
- The tests MUST assert that each SDLC stage produces the exact expected string format (including emojis, step numbers, and injected variables).
- All tests MUST pass (GREEN) before submitting.

---
status: closed

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