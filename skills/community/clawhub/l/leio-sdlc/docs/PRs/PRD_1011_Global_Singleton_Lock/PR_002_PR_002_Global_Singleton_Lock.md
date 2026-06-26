status: closed

# PR-002: Global Singleton Lock

## 1. Objective
Implement a physical prevention mechanism for concurrent SDLC runs using OS-level file locking (`fcntl`) to eliminate race conditions and state corruption.

## 2. Scope (Functional & Implementation Freedom)
Introduce an OS-level file lock (`fcntl.flock` with `LOCK_EX | LOCK_NB`) on a `.sdlc_run.lock` file at the very beginning of the orchestrator process. If a `BlockingIOError` is raised, the script must IMMEDIATELY print the specified `[FATAL] Another SDLC pipeline is currently running.` message and the subsequent `[ACTION REQUIRED FOR MANAGER]` block, then terminate via `exit(1)`. The lock must be automatically released by the OS when the process terminates.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
1. The Coder MUST write an integration test that spawns a background orchestrator process and immediately attempts to start a second orchestrator process in the same workspace.
2. The test must verify that the second process exits with status code `1`.
3. The test must verify that the second process's standard output contains the exact `[ACTION REQUIRED FOR MANAGER]` string.
4. The test must gracefully kill the background process to release the lock.
5. All tests MUST pass (GREEN) before submitting.