status: closed

# PR-002a: Update AgentSkill Archetype and Integration Tests

## 1. Objective
Refactor the base AgentSkill deployment and rollback archetype to use hard-copy atomic swapping instead of symlinks, and implement a mock integration test to verify the new logic.

## 2. Scope (Functional & Implementation Freedom)
Update the archetype deployment and rollback scripts to use hard copies and tarball backups. Create an integration test script that simulates a mock environment to verify the atomic swap and rollback mechanisms.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
1. The archetype deployment script MUST NOT use symlink logic and MUST implement atomic directory swapping.
2. The rollback script MUST be able to restore a backup from a tarball.
3. The mock integration test MUST verify the absence of symlinks, the presence of the correct directories, and the existence of the backup tarball. All tests MUST run 100% GREEN.