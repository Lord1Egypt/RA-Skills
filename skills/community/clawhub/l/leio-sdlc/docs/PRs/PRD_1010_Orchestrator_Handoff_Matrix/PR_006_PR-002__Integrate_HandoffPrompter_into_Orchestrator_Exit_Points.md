status: in_progress

# PR-002: Integrate HandoffPrompter into Orchestrator Exit Points

## 1. Objective
Integrate the `HandoffPrompter` utility into the actual exit points of the Orchestrator to ensure the prompts are printed to standard output upon termination.

## 2. Scope (Functional & Implementation Freedom)
- Locate the Orchestrator's exit handling logic.
- Replace or add print/logging statements using the `HandoffPrompter` utility for the 5 exit conditions (Happy Path, Dirty Workspace, Planner Failure, Git Checkout Error, and Dead End).
- *The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- Write integration tests that mock the Orchestrator exit conditions and assert that the standard output contains the correct `[ACTION REQUIRED FOR MANAGER]` strings.
- The Coder MUST ensure all tests run GREEN before submitting.