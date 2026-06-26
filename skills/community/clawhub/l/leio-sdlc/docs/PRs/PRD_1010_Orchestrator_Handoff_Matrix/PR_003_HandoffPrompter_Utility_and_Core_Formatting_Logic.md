status: closed

# PR-001: HandoffPrompter Utility and Core Formatting Logic

## 1. Objective
Create a centralized, reusable utility (`HandoffPrompter`) responsible for generating the standardized `[ACTION REQUIRED FOR MANAGER]` prompt blocks for the 5 core exit conditions.

## 2. Scope (Functional & Implementation Freedom)
- Implement a utility class or module that formats the specific handoff messages for: Happy Path, Dirty Workspace, Planner Failure, Git Checkout Error, and Dead End.
- *The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- Write unit tests that verify the utility correctly returns the exact prompt strings for each of the 5 exit conditions.
- The Coder MUST ensure all tests run GREEN before submitting.