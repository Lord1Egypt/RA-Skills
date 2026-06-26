status: closed

# PR-001: Master Branch Guardrail Preflight

## 1. Objective
Prevent the orchestrator from running on non-master branches to avoid nested branch creation and state corruption.

## 2. Scope (Functional & Implementation Freedom)
Add a preflight check before the main orchestration logic begins. This check must verify that the currently active Git branch is exactly `master`. If it is any other branch, the application must IMMEDIATELY print `[FATAL] Orchestrator must be started from the master branch to prevent nested branch creation.` and terminate via `exit(1)`.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
1. The Coder MUST write an automated test verifying that when the active branch is NOT `master`, the process exits with status code `1` and outputs the exact `[FATAL]` message.
2. The Coder MUST write an automated test verifying that when the active branch IS `master`, this specific preflight check passes without exiting.
3. All tests MUST pass (GREEN) before submitting.