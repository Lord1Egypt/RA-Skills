status: closed

# PR-001: Context Switching, Git Boundaries, and Per-Repo Locking

## 1. Objective
Establish strict directory contexts for the orchestrator, enforcing Git boundaries and replacing global locks with per-repository locks to ensure concurrency safety.

## 2. Scope (Functional & Implementation Freedom)
Refactor the orchestrator's initialization logic to switch directories immediately after argument parsing. Enforce that the target directory is a valid Git repository unless explicitly bypassed. Update the locking mechanism to be repository-local rather than global. Allow both `main` and `master` as valid starting branches.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
1. Implement an integration test (`test_polyrepo_context.sh`) that creates a mock working directory with `git init` and asserts that the local lock file is created *inside* that mock directory.
2. Implement an integration test (`test_git_boundary.sh`) that passes a working directory without a `.git` folder and asserts a fatal exit occurs (when bypass is off).
3. The Coder MUST ensure all tests run GREEN before submitting. Test scripts and implementation must be delivered in this exact PR.