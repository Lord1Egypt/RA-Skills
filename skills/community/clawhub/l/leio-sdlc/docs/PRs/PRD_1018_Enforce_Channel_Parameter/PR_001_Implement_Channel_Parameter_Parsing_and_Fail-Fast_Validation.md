status: closed

# PR-001: Implement Channel Parameter Parsing and Fail-Fast Validation

## 1. Objective
Introduce explicit channel parameter parsing with environment variable fallbacks and implement a fail-fast mechanism when the channel is missing.

## 2. Scope (Functional & Implementation Freedom)
- Add `--channel` as an optional CLI argument to the orchestrator.
- Implement resolution logic: `effective_channel = args.channel or os.environ.get("OPENCLAW_SESSION_KEY") or os.environ.get("OPENCLAW_CHANNEL_ID")`.
- Implement fail-fast validation: If `effective_channel` is missing, abort execution immediately and output a self-explaining error using the designated prompter (e.g., `[FATAL_STARTUP]`).
- Create a test script to explicitly run the orchestrator without the parameter and environment variables to verify the non-zero exit code and `[FATAL_STARTUP]` output.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- The orchestrator successfully identifies when no channel parameter or fallback environment variable is provided.
- On failure, it exits with a non-zero code and prints the required `[FATAL_STARTUP]` message.
- The newly created test script runs GREEN, successfully asserting the failure condition.