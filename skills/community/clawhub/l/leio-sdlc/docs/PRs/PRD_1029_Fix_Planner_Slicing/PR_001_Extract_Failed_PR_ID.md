status: closed

# PR-001: Extract Failed PR ID

## 1. Objective
Implement logic to correctly extract the index prefix of a failed PR when slicing is requested.

## 2. Scope (Functional & Implementation Freedom)
- Add regex-based extraction logic to identify the parent PR ID (e.g., `001` from `PR_001_xxx.md`) when a failed PR is passed for slicing.
- Use Python's `re` module with the pattern `r"^PR_(\d+(?:_\d+)*)_"`.
- *The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- When a filename like `PR_001_xxx.md` is provided, the extracted ID is `001`.
- When a filename like `PR_002_1_xxx.md` is provided, the extracted ID is `002_1`.
- The Coder MUST ensure all tests run GREEN before submitting, including unit tests for the extraction logic.