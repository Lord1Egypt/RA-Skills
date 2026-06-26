status: closed

# PR-[ID]: Implement Global Crash-Proof Reaper and Signal Handlers

## 1. Objective
Wrap the main execution loop in a global structure to safely reap active subagent process groups on any exit vector, including signals like SIGTERM and SIGINT.

## 2. Scope (Functional & Implementation Freedom)
- Wrap the main execution loop in a `try...finally` structure.
- Implement a crash-proof reaper in the `finally` block that safely terminates active subagent process groups using `os.killpg` and `signal.SIGTERM`.
- Add defensive checks to ensure the process exists before reaping, and catch `OSError` to prevent masking original errors.
- Implement signal handlers using the `signal` module to intercept `SIGTERM` and `SIGINT` to trigger the `finally` reaper by raising a custom exception or `SystemExit`.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- The `finally` block successfully reaps grandchild processes on normal exits, exceptions, and `sys.exit`.
- `OSError` is caught during reaping to prevent secondary crashes.
- Signal handlers correctly intercept `SIGTERM`/`SIGINT` and trigger the reaper.
- Tests must be written/updated to simulate crashes and verify the reaper logic leaves no orphaned processes.
- All tests must pass (100% GREEN) before submitting.