# PRD_077: Fix CLI Command Mismatch For ACP in spawn_coder.py

## 1. Problem Statement
During the implementation of PRD-067, the Coder incorrectly refactored `scripts/spawn_coder.py` to use non-existent OpenClaw CLI commands (`openclaw sessions_spawn` and `openclaw sessions_send`). These are actually internal Tool API endpoints and not valid terminal CLI commands. 
As a result, when the Orchestrator invokes `spawn_coder.py`, `subprocess.run` fails with `unknown command 'sessions_spawn'` and exits with code 1. This causes the Orchestrator pipeline to instantly crash and enter an infinite retry/micro-slicing loop, fully blocking the SDLC process.
The unit tests failed to catch this because they naively asserted on the expected argument strings instead of verifying the validity of the CLI signatures.

## 2. Solution (Use Proper ACP Client CLI)
The `spawn_coder.py` script must be refactored to use the actual, valid OpenClaw CLI commands to interact with the ACP session and send feedback.
1. **Replace `sessions_spawn`**: Instead of `sessions_spawn`, the script should initialize the session using `openclaw acp client --cwd <workdir> --session <id> --server gemini`. 
   Wait, if we just need to send a task, we can use:
   `openclaw agent --session-id <id> --message <task>`
   For the sake of simplicity and background execution, `openclaw agent --session-id <session_key> --message <task_string>` is the correct standard CLI entrypoint.
2. **Replace `sessions_send`**: Review feedback should also be routed through `openclaw agent --session-id <session_key> --message <feedback_message>`.
3. **Session Key Naming**: Ensure the session key string format strictly matches standard naming conventions (e.g., `sdlc_coder_PR_ID`).
4. **Harden Mock Tests**: Update `tests/test_spawn_coder.py` to assert that the constructed command lists start with `["openclaw", "agent", "--session-id", ...]` and `["openclaw", "agent", "--session-id", ...]`, explicitly forbidding any `sessions_spawn` or `sessions_send` in the subprocess calls.

## 3. Scope
- **Target Project:** `/root/.openclaw/workspace/projects/leio-sdlc`
- **Files to Modify:**
  - `scripts/spawn_coder.py`
  - `tests/test_spawn_coder.py`

## 4. Testing Strategy
- **Autonomous Test Strategy:** Modify `tests/test_spawn_coder.py` to test that the command arguments explicitly contain `agent`, `--session-id`, and `--message`. 
- **TDD Guardrail:** The implementation and its failing test MUST be delivered in the same PR contract.
