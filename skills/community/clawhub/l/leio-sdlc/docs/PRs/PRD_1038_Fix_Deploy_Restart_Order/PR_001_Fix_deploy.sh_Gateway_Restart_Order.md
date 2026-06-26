status: closed

# PR-001: Fix deploy.sh Gateway Restart Order

## 1. Objective
Move the `openclaw gateway restart` execution block to the absolute bottom of the deployment function in the main deployment script so that all other steps complete before the process restarts.

## 2. Scope (Functional & Implementation Freedom)
Identify the main deployment script's gateway restart block and move it after cleanup, sync, and hook installation logic.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- The gateway restart command must be the final action within the deployment script.
- All cleanup, sync, and hook installation logic must precede the restart.
- The Coder MUST ensure all tests run GREEN before submitting.