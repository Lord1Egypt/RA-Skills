# PRD_075_Robust_Git_State_Management

## 1. Issue Definition
Fix the Orchestrator's robust Git State Management and error handling.
- Ensure no missing git add & commit when PR states or files change.
- Ensure safe error handling by wrapping checkout operations in try/except and gracefully exiting without deleting data on failure.

## 2. Playbook Rules
- **Scope Locking**: Restricted to `/root/.openclaw/workspace/projects/leio-sdlc`.
- **TDD Guardrail**: All features must have failing tests written first.
- **Autonomous Test Strategy**: Tests must run autonomously in CI without human intervention.

## 3. Requirements
- Add `try...except` blocks around all `git checkout` commands in Orchestrator.
- Explicitly call `git add .` and `git commit` when modifying PR state trackers or source files.
- Fail gracefully without destructive actions (e.g., `rm -rf`) on git errors.
