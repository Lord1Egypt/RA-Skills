status: superseded

# PR-001: Implement Process Group Isolation and Crash-Proof Reaper

## 1. Objective
Refactor orchestrator subagent launching to use isolated process groups and guarantee safe, crash-proof reaping of all child processes upon any exit vector.

## 2. Scope (Functional & Implementation Freedom)
- Refactor the synchronous execution of long-running subagents to use asynchronous process creation with new session/process group allocation (`start_new_session=True`), followed immediately by a synchronous wait.
- Wrap the main execution loop in a `try...finally` structure.
- Implement a crash-proof reaper in the `finally` block that safely terminates active subagent process groups (using `os.killpg` and `SIGTERM`) without raising secondary exceptions (e.g., catching `OSError`).
- Ensure signal handlers intercept `SIGTERM`/`SIGINT` to trigger the `finally` reaper.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- Subagents are launched asynchronously with a new process group and immediately waited upon.
- The `finally` block successfully reaps grandchild processes on normal exits, exceptions, and `sys.exit`.
- `OSError` is caught during reaping to prevent masking original errors.
- Tests must be written/updated to simulate crashes and verify the reaper logic leaves no orphaned processes.
- All tests must pass (100% GREEN) before submitting.