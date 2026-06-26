status: closed

# PR-001: Implement git force-commit helper function

## 1. Objective
Implement a standalone helper function to forcefully commit any uncommitted changes in the repository, laying the groundwork for defensive commits before the Reviewer state.

## 2. Scope & Implementation Details
- **File:** `scripts/orchestrator.py`
- Add a function `force_commit_untracked_changes(repo_path=".")` that runs `git add .` and `git commit -m "chore(auto): force commit uncommitted changes before review"`. Handle cases where there are no changes gracefully.

## 3. TDD & Acceptance Criteria
- **File:** `tests/test_076_unit_git_commit.sh`
- Write a bash test that initializes a dummy git repo, creates an untracked file, calls the python helper function, and asserts that the git log contains the "chore(auto)" commit.
