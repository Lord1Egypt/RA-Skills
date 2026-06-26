status: completed

# PR-001: Scaffolding and Core Playbook for PM AgentSkill

## 1. Objective
Establish the foundational directory structure and core rules for the PM AgentSkill, focusing on Role Definition, Scope Locking, and Artifact Delivery.

## 2. Scope & Implementation Details
- Create `skills/pm-skill/` directory.
- Create `skills/pm-skill/deploy.sh` to symlink the skill to `~/.openclaw/skills/pm-skill`.
- Create `skills/pm-skill/SKILL.md` containing:
  - Role Definition: Summarizer, NOT an Inventor.
  - Scope Locking: Explicitly identify the target project's absolute directory.
  - Artifact Delivery: Use the `write` tool to physically save the PRD into the target project's `docs/PRDs/` directory.

## 3. TDD & Acceptance Criteria
- Create `tests/test_032_pm_skill.sh`.
- Write assertions to read `skills/pm-skill/SKILL.md` and verify it contains the mandatory rules: "Summarizer, NOT an Inventor", "Scope Locking", and "Artifact Delivery".
- Test must pass and exit 0.