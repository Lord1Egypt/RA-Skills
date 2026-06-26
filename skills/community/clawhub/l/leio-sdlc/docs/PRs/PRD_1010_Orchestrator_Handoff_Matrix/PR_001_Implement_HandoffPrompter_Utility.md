status: superseded

# PR-001: Implement HandoffPrompter Utility

## 1. Objective
Create a centralized utility class (`HandoffPrompter`) responsible for generating consistent, actionable handoff prompts for the Manager Agent across various exit conditions.

## 2. Scope (Functional & Implementation Freedom)
- Implement a utility to generate explicit `[ACTION REQUIRED FOR MANAGER]` blocks.
- Support the 5 core exit conditions defined in PRD 1010: Happy Path, Dirty Workspace, Planner Failure, Git Checkout Error, and Dead End.
- *The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
1. Write unit tests for the `HandoffPrompter` utility that verify the correct prompt string is generated for each of the 5 exit conditions.
2. The Coder MUST ensure all tests run GREEN before submitting.