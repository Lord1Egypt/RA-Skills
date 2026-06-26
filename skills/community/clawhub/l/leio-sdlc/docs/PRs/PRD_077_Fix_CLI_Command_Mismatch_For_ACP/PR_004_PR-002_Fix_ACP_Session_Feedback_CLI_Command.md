status: completed

# PR-002: Fix ACP Session Feedback CLI Command

## 1. Objective
Refactor the Coder feedback mechanism in `scripts/spawn_coder.py` to use the valid `openclaw agent --session-id <session_key> --message <feedback_message>` CLI command instead of the internal `sessions_send` API endpoint.

## 2. Scope & Implementation Details
- **`scripts/spawn_coder.py`**: Modify the feedback sending function to execute the `openclaw agent --session-id <session_key> --message <feedback_message>` CLI command rather than `openclaw sessions_send`. Reuse the `<session_key>` format `sdlc_coder_<PR_ID>`.
- **`tests/test_spawn_coder.py`**: Update test mocks handling the subprocess call during feedback routing to assert that the constructed command list correctly starts with `["openclaw", "agent", "--session-id", "sdlc_coder_<PR_ID>", "--message"]` and strictly forbids `sessions_send`.

## 3. TDD & Acceptance Criteria
- A failing test MUST be written (or updated) to verify that the feedback command string does not contain `sessions_send` and strictly contains the expected `openclaw agent --session-id` arguments.
- The unit test suite (`pytest tests/test_spawn_coder.py`) MUST pass entirely after the script implementation.