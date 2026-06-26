status: in_progress

# PR-002: SDLC Templates & Native Backgrounding Refactor

## 1. Objective
Refactor SDLC skill templates and the Orchestrator to eliminate legacy shell backgrounding (`nohup` and `&`), substituting them with the OpenClaw native `exec(background: true)` to ensure accurate completion events.

## 2. Scope & Implementation Details
- Audit and update `leio-sdlc/SKILL.md`, `pm-skill/SKILL.md`, and `issue_tracker/SKILL.md` to remove all instances of `nohup` and `&`.
- Refactor the global `AgentSkill_Archetype/SKILL.md.template` in `projects/docs/TEMPLATES/` to propagate native backgrounding best practices.
- Ensure any command strings constructed by the Orchestrator for agent loop execution utilize the `background: true` parameter instead of shell backgrounding operators.

## 3. TDD & Acceptance Criteria
- [ ] All `SKILL.md` templates in the specified locations contain zero instances of `nohup` and `&` for backgrounding.
- [ ] `AgentSkill_Archetype/SKILL.md.template` is successfully updated.
- [ ] A simulated SDLC run correctly uses `exec(background: true)` without hanging the Main Agent.
- [ ] All tests pass locally and in CI.