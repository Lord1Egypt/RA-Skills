status: closed

# PR-001: Core Hard Copy Deploy and Rollback Logic with Integration Tests

## 1. Objective
Implement the base deployment and rollback scripts utilizing physical copying and tarball backups, alongside a comprehensive integration test suite to verify the hard-copy deployment behavior.

## 2. Scope (Functional & Implementation Freedom)
Create or update the foundational archetype deployment script to use atomic directory swapping (`mv -T`) and tarball backups (`.tar.gz`) instead of symlinks.
Create a corresponding rollback script that restores from the tarball backups.
Develop a bash integration test script that mocks the environment (e.g., a mock `HOME` directory) to safely test the deploy and rollback flows.
Integrate this test into the main preflight checks.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
1. The integration test MUST verify that the deployment results in a physical directory, NOT a symlink.
2. The integration test MUST verify that a `.tar.gz` backup is successfully created in the releases directory prior to staging new code.
3. The integration test MUST verify that the rollback script successfully restores the directory state from the backup tarball.
4. The preflight script MUST execute the integration test and pass (100% GREEN) before the PR is considered complete.