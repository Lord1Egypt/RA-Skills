status: closed

# PR-002: Orchestrator Integration of Handoff Matrix

## 1. Objective
Integrate the `HandoffPrompter` utility into the Orchestrator's exit paths so that it successfully outputs actionable prompts to the Manager Agent upon termination.

## 2. Scope (Functional & Implementation Freedom)
- Wire the formatting utility into the 5 core exit points: queue empty (success), dirty workspace, planner failure, git checkout error, and dead end.
- Ensure the orchestrator prints or logs the standardized blocks at these exact exit points.
- *The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- Write or update tests mocking the 5 exit conditions in the orchestrator and assert that the standard output contains the exact `[ACTION REQUIRED FOR MANAGER]` strings.
- Integration tests should verify the output is parsable.
- The Coder MUST ensure all tests run GREEN before submitting.