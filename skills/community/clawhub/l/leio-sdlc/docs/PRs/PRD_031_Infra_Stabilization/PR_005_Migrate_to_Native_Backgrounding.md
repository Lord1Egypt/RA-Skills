status: superseded

# PR-003: Migrate to Native Backgrounding

## 1. Objective
Prevent agent deadlocks by replacing legacy shell backgrounding (`nohup` and `&`) with native OpenClaw `exec(background: true)` parameters across all relevant skill templates.

## 2. Scope (Functional & Implementation Freedom)
- Refactor skill definitions and templates to remove legacy backgrounding commands.
- Apply the OpenClaw native `exec` backgrounding pattern to ensure completion events are properly routed back to the Agent Loop.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- Verify via static analysis or testing that `nohup` and `&` are completely removed from the targeted skill templates.
- Ensure the modified templates correctly specify the `background: true` parameter for long-running execution commands.
- All tests must pass (GREEN).
