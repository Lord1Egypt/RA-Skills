status: superseded

# PR-001: Fix ACP Session Initialization CLI Command Mismatch

## 1. Objective
Refactor the Coder spawning initialization in `scripts/spawn_coder.py` to use valid `openclaw agent --session-id <session_key> --message <task_string>` CLI commands instead of the internal Tool API endpoints like `sessions_spawn`. Ensure session key naming strictly matches the `sdlc_coder_PR_ID` format.

## 2. Scope & Implementation Details
- **`scripts/spawn_coder.py`**: Modify the core session spawn function to execute the `openclaw agent --session-id <session_key> --message <task_string>` CLI command rather than `openclaw sessions_spawn`. Ensure the `<session_key>` format dynamically interpolates to `sdlc_coder_<PR_ID>`.
- **`tests/test_spawn_coder.py`**: Update test mocks handling the subprocess call during initialization to assert that the constructed command list correctly starts with `["openclaw", "agent", "--session-id", "sdlc_coder_<PR_ID>", "--message"]` and strictly forbids `sessions_spawn`.

## 3. TDD & Acceptance Criteria
- A failing test MUST be written (or updated) to verify that the spawned command string does not contain `sessions_spawn` and strictly contains the expected `openclaw agent --session-id` arguments.
- The unit test suite (`pytest tests/test_spawn_coder.py`) MUST pass entirely after the script implementation.


> [Escalation] Tier 1 Reset triggered due to Coder failure or Arbitrator rejection.
