# Micro-PR-001.1: Git Validation Utility and Unit Tests

## 1. Objective
Create a standalone Git validation utility function to check if a specific file (like a PRD) is fully tracked by Git and has no uncommitted changes.

## 2. Scope & Implementation Details
- Create a new utility function (e.g., in `scripts/git_utils.py` or similar appropriate location based on existing codebase) that takes a file path.
- The function should use the `subprocess` module to run `git` commands (e.g., `git status --porcelain <file>`) to determine if the file is tracked and unmodified.
- The function should return a status indicating success or the specific validation failure (untracked vs. modified).

## 3. TDD & Acceptance Criteria
- Unit tests must be written for the new utility function.
- Tests must mock or setup actual git repositories to verify behavior for: a completely untracked file, a tracked but modified file, and a committed, clean file.
- All tests must pass (GREEN).