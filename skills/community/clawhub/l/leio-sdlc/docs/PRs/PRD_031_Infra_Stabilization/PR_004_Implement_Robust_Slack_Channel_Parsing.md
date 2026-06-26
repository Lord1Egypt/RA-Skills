status: closed

# PR-002: Implement Robust Slack Channel Parsing

## 1. Objective
Fix notification failures by updating the Orchestrator's notification module to properly handle fully-qualified OpenClaw routing keys.

## 2. Scope (Functional & Implementation Freedom)
- Update the notification logic to parse and support routing keys such as `slack:channel:<ID>`, `channel:<ID>`, or `<ID>` without inappropriate splitting or truncation.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- Tests must be written or updated to verify that the notification module correctly parses various formats of routing keys without truncating important identifiers.
- A test should simulate sending a notification to ensure the correct full routing key is utilized.
- All tests must pass (GREEN).
