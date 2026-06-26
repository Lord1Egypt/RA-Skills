status: open

# PR-001: Restore True Diff Visibility

## 1. Objective
Ensure that the reviewer system correctly captures and outputs the accumulative diff against the target branch, removing the illusion of an empty diff when changes are already committed locally.

## 2. Scope (Functional & Implementation Freedom)
- Remove any logic that bypasses diff generation if the working tree is clean (e.g., checking for uncommitted changes to skip diff generation).
- Implement an unconditional diff extraction against the target branch to extract the true accumulative diff.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- Implement a test verifying that when a Coder commits changes locally, the reviewer system correctly captures these committed changes and does NOT output an empty diff.
- The Coder MUST ensure all tests run GREEN before submitting.