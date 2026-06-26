status: in_progress

# PR-001: Core Orchestrator Infrastructure Updates

## 1. Objective
Stabilize the Orchestrator's execution pipeline by implementing a strict PRD tracking guardrail, robust Slack channel parsing, and atomic branch isolation to prevent branch collisions.

## 2. Scope & Implementation Details
- Update `notify_channel` logic in the Orchestrator (e.g., `scripts/orchestrator.py`) to correctly handle fully qualified routing keys (like `slack:channel:CXXX`) without improper truncation or splitting.
- Implement a `validate_prd_is_committed()` function in the Orchestrator startup sequence. This must verify that the target PRD file is tracked by Git and contains no uncommitted changes, halting execution if violated.
- Update the branch generation logic to ensure atomic branch isolation for every PR execution run (e.g., appending a timestamp or UUID to the branch name) to avoid reusing stale branches from failed attempts.

## 3. TDD & Acceptance Criteria
- [ ] Integration test verifies `notify_channel` correctly parses routing keys.
- [ ] Orchestrator exits with an error when run against an uncommitted or untracked PRD.
- [ ] Orchestrator successfully generates unique, timestamped/UUID branch names during test SDLC runs.
- [ ] All tests pass locally and in CI.