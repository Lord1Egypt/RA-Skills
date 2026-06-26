status: closed

# PR-001: Implement Base HandoffPrompter Utility

## 1. Objective
Create the centralized utility class that generates the exact `[ACTION REQUIRED FOR MANAGER]` strings for the 5 core exit conditions.

## 2. Scope (Functional & Implementation Freedom)
- Implement a standalone utility class (e.g., `HandoffPrompter`) to generate the formatted handoff prompts.
- Implement the pure string generation logic for: Happy Path, Dirty Workspace, Planner Failure, Git Checkout Error, and Dead End.
- Do not integrate into the orchestrator yet.
- *The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- Write pure unit tests for the utility class that verify the exact strings are generated for all 5 exit conditions as defined in the PRD.
- The Coder MUST ensure all tests run GREEN before submitting.