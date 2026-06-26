status: closed

# PR-001: CLI Parameter Hardening and Environment Integration

## 1. Objective
Enforce strict CLI arguments to prevent runaway loops and migrate notification configuration to environment variables.

## 2. Scope (Functional & Implementation Freedom)
- Update the CLI argument parser to make working directory, PRD file, max PRs to process, and coder session strategy strictly required.
- Remove deprecated CLI parameters related to job directories and notification channels.
- Implement fallback logic to fetch notification channels from the environment (`OPENCLAW_SESSION_KEY` or `OPENCLAW_CHANNEL_ID`).
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
1. Running the orchestrator without the new required arguments (e.g., max PRs to process) must throw a native missing argument error.
2. The application must successfully read notification configuration from environment variables when the deprecated CLI flags are no longer provided.
3. All existing and new tests MUST run GREEN before submitting.