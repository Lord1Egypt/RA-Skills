status: closed

# PR-002: Fix AgentSkill Archetype deploy.sh Gateway Restart Order

## 1. Objective
Move the `openclaw gateway restart` execution block to the absolute bottom of the deployment function in the AgentSkill Archetype template to ensure future generated skills inherit the correct logic.

## 2. Scope (Functional & Implementation Freedom)
Identify the archetype template's deployment script and move the gateway restart block after all other trailing steps.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- The gateway restart command must be the final action within the archetype template deployment script.
- All cleanup, sync, and hook installation logic must precede the restart.
- The Coder MUST ensure all tests run GREEN before submitting.