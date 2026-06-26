status: in_progress

# PR-002: Native Backgrounding Refactor for Skill Templates

## 1. Objective
Eliminate deadlocks in the Agent Loop by migrating all skill execution commands from legacy shell backgrounding to OpenClaw's native event-driven backgrounding.

## 2. Scope (Functional & Implementation Freedom)
- Refactor the SDLC orchestrator skill templates, related skills (like pm-skill, issue_tracker), and the global AgentSkill archetype to remove `nohup` and `&`.
- Replace the legacy backgrounding mechanisms with the native OpenClaw `exec(background: true)` parameter for all long-running execution commands.
- *The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- A smoke test or mock SDLC run must verify that the Main Agent receives the `Exec completed` notification without blocking the Agent Loop.
- A codebase scan or test must confirm that all relevant `SKILL.md` files (and the AgentSkill archetype template) are free of `nohup` and `&`.
- All tests must run GREEN before submitting.