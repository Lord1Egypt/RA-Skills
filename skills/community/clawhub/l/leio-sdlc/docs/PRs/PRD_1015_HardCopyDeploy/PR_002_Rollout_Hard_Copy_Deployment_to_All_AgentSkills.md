status: superseded

# PR-002: Rollout Hard Copy Deployment to All AgentSkills

## 1. Objective
Apply the newly verified hard-copy deployment and rollback logic to all concrete AgentSkill implementations within the repository.

## 2. Scope (Functional & Implementation Freedom)
Update the deployment scripts of all existing AgentSkills (e.g., pm-skill, issue_tracker, and the main leio-sdlc deploy) to mirror the new hard-copy strategy defined in the archetype.
Ensure that each deployed skill also has access to the rollback mechanism.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
1. All AgentSkill deployment scripts MUST be completely free of symlink (`ln -s`) logic for releases.
2. All AgentSkill deployment scripts MUST implement atomic directory swapping and tarball backups.
3. The global preflight test suite MUST continue to run 100% GREEN, proving that the updates do not break existing CI/CD pipelines.