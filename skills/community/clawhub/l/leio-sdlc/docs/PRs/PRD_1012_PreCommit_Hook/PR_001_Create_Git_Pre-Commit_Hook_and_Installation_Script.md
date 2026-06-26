status: in_progress

# PR-001: Create Git Pre-Commit Hook and Installation Script

## 1. Objective
Implement the core Git pre-commit hook logic and a script to install it, ensuring that direct commits are rejected unless explicitly authorized by the SDLC orchestrator.

## 2. Scope (Functional & Implementation Freedom)
- Create the git pre-commit hook script payload that checks for a specific environment variable (e.g., `SDLC_ORCHESTRATOR_RUNNING=1`).
- If the variable is not present, the hook MUST reject the commit and echo: `"ERROR: SDLC Violation! Direct commits are forbidden. You must use orchestrator.py."`
- Create an installation script that can automatically bind this hook into a repository's `.git/hooks/pre-commit` directory.
- *The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- A standalone test must verify that the hook script rejects execution when the environment variable is missing and outputs the exact error message.
- A test must verify that the hook script allows execution when the environment variable is present.
- The installation script successfully copies the hook to a target directory and makes it executable.
- The Coder MUST ensure all tests run GREEN before submitting.