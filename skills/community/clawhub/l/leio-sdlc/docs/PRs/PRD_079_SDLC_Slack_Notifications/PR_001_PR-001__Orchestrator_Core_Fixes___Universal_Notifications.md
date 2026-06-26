status: open

# PR-001: Orchestrator Core Fixes & Universal Notifications

## 1. Objective
Introduce fail-fast mechanisms for dirty workspaces, fix the broken session teardown logic, and add universal channel notifications to broadcast Orchestrator progress.

## 2. Scope & Implementation Details
- `scripts/orchestrator.py`:
  - Add an early check in `main()` using `subprocess.run(["git", "status", "--porcelain"])`. If output exists, log `[FATAL] Dirty Git Workspace detected!` and exit.
  - In `teardown_coder_session`, remove the `subprocess.run(["openclaw", "subagents", "kill"...])` block to prevent invalid CLI errors.
  - Add `--notify-channel` and `--notify-target` CLI arguments.
  - Implement `notify_channel(args, msg)` using `subprocess.run(["openclaw", "message", "send", "--channel", args.notify_channel, "--target", args.notify_target, "-m", f"🤖 [SDLC Engine] {msg}"], check=False)`.
  - Integrate `notify_channel` at Ignition (State 0/1), PR Switch (State 2/3), Dead End (State 5 Arbitrator failure), and Success (End of script).

## 3. TDD & Acceptance Criteria
- Ensure unit tests in `tests/test_orchestrator.py` pass and cover:
  1. Early exit when a dirty git workspace is detected.
  2. The absence of the `subagents kill` command during session teardown.
  3. `notify_channel` correctly invokes the `openclaw` subprocess with the right arguments.