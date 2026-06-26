status: closed

# PR-003-1: Migrate Native Backgrounding for Core LEIO SDLC Skills

## 1. Objective
Prevent agent deadlocks in the core LEIO SDLC skills by replacing legacy shell backgrounding (`nohup` and `&`) with native OpenClaw `exec(background: true)` parameters.

## 2. Scope & Implementation Details
- Refactor the following specific skill definitions to remove legacy backgrounding commands (`nohup`, `&`):
  - `projects/leio-sdlc/SKILL.md`
  - `projects/leio-sdlc/skills/pm-skill/SKILL.md`
  - `projects/leio-sdlc/skills/issue_tracker/SKILL.md`
- Apply the OpenClaw native `exec` backgrounding pattern to ensure completion events are properly routed back to the Agent Loop.

## 3. TDD & Acceptance Criteria
- Verify via static analysis or testing that `nohup` and `&` are completely removed from the targeted skill files.
- Ensure the modified files correctly specify the `background: true` parameter for long-running execution commands.
- All tests must pass (GREEN).