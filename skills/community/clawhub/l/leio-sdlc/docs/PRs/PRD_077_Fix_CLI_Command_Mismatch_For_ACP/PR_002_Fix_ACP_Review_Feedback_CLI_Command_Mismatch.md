status: completed

# PR-002: Fix ACP Review Feedback CLI Command Mismatch

## 1. Objective
Refactor the Coder feedback loop in `scripts/spawn_coder.py` to route subsequent task or review messages using valid `openclaw agent --session-id <session_key> --message <feedback_message>` CLI commands rather than the internal `sessions_send` Tool API endpoint.

## 2. Scope & Implementation Details
- **`scripts/spawn_coder.py`**: Modify the review/feedback transmission function to construct and execute the `openclaw agent --session-id <session_key> --message <feedback_message>` CLI command. Eliminate all instances of `openclaw sessions_send`.
- **`tests/test_spawn_coder.py`**: Update test mocks handling the subprocess call during feedback transmission to assert that the constructed command list correctly starts with `["openclaw", "agent", "--session-id", "sdlc_coder_<PR_ID>", "--message"]` and strictly forbids `sessions_send`. Ensure the `session_key` is correctly re-used from initialization.

## 3. TDD & Acceptance Criteria
- A failing test MUST be written (or updated) to verify that the feedback transmission command string does not contain `sessions_send` and strictly contains the expected `openclaw agent --session-id` arguments.
- The unit test suite (`pytest tests/test_spawn_coder.py`) MUST pass entirely after the script implementation.
