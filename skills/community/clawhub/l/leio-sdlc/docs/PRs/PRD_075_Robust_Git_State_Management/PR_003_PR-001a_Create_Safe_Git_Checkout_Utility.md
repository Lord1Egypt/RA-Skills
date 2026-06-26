status: completed

# PR-001a: Create Safe Git Checkout Utility

## 1. Objective
Create a reusable, robust utility function for executing `git checkout` operations safely.

## 2. Scope & Implementation Details
- Add a new function `safe_git_checkout(branch_name)` in the Orchestrator's git utility module (or wherever git operations are centralized).
- Wrap the `subprocess` call for `git checkout` in a `try...except` block.
- On `subprocess.CalledProcessError`, catch the exception, log the error clearly, and raise a custom exception or return a defined failure state without executing any destructive commands.

## 3. TDD & Acceptance Criteria
- Write a unit test that calls `safe_git_checkout` with a non-existent branch or forcing a conflict.
- Assert that the expected exception is caught/returned and the system does not crash ungracefully.
