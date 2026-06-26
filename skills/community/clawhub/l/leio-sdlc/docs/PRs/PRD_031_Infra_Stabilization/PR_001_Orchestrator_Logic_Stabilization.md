status: in_progress

# PR-001: Orchestrator Logic Stabilization (Channel Parsing & PRD Guardrail)

## 1. Objective
Fix notification failures by supporting full-qualified OpenClaw routing keys and enforce requirement discipline by verifying the target PRD is committed to Git before execution.

## 2. Scope (Functional & Implementation Freedom)
- Update the notification logic within the orchestrator to correctly parse and handle raw routing keys (like `slack:channel:<ID>`) without splitting or truncation.
- Add a startup validation check in the orchestrator to verify that the target PRD file is tracked by Git and has no uncommitted changes. If it is modified or untracked, exit with a clear error message.
- *The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- Integration tests must verify that channel parsing handles various routing key formats correctly.
- Integration tests must verify the PRD commit guardrail triggers an error for untracked/modified PRDs and passes for committed ones.
- All tests must run GREEN before submitting.