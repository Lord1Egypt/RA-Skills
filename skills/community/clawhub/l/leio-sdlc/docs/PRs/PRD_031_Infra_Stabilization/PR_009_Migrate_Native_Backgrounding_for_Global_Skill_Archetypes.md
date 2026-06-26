status: closed

# PR-003-2: Migrate Native Backgrounding for Global Skill Archetypes

## 1. Objective
Ensure future skills do not suffer from agent deadlocks by replacing legacy shell backgrounding with native OpenClaw `exec(background: true)` in the global AgentSkill Archetype templates.

## 2. Scope & Implementation Details
- Refactor the global skill template: `projects/docs/TEMPLATES/AgentSkill_Archetype/SKILL.md.template`
- Remove any instances of `nohup` and `&` and replace them with instructions or examples using the native `exec(background: true)` pattern.

## 3. TDD & Acceptance Criteria
- Verify via static analysis or testing that `nohup` and `&` are completely removed from the archetype template.
- Ensure the modified template correctly specifies the `background: true` pattern.
- All tests must pass (GREEN).