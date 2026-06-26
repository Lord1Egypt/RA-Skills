status: closed

# PR-001: Implement Git Workspace Cleanup Utilities

## 1. Objective
Create reliable Git utility functions to hard reset and clean a dirty workspace to ensure a clean state before branch checkouts.

## 2. Scope (Functional & Implementation Freedom)
- Implement logic to perform a `git reset --hard` to discard tracked file changes.
- Implement logic to perform a `git clean -fd` to remove untracked files and directories.
- Ensure these operations can be called safely and reliably within the project's Git execution context.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
1. Write a test that initializes a dummy Git repository, modifies a tracked file, and adds an untracked file.
2. The test must call the new cleanup utilities.
3. Assert that after the cleanup, the workspace is completely clean (no modified tracked files, no untracked files).
4. The Coder MUST ensure all tests run GREEN before submitting.