# PRD: Enforce Global Singleton Lock for Orchestrator Process

## Metadata
- **ID**: ISSUE-1011
- **Title**: Enforce Global Singleton Lock and Master Branch Preflight for Orchestrator Process
- **Project**: leio-sdlc
- **Target Path**: `/root/.openclaw/workspace/projects/leio-sdlc`
- **Status**: Open
- **Type**: Bugfix
- **Priority**: Critical
- **Date**: 2026-03-22

## Problem Statement
Currently, it is possible to accidentally spawn multiple `orchestrator.py` processes in the same workspace. Since they share the same Git index and state files, this leads to catastrophic race conditions, state corruption, and infinite loops.

## Solution (Approved Approach)
Implement a physical prevention mechanism for concurrent SDLC runs using OS-level file locking (`fcntl`). This serves as a critical stopgap before Git Worktree Isolation (ISSUE-1000) is fully implemented.

### Action Items
0. **Master Branch Guardrail (Preflight Check)**: Before even attempting to acquire the lock, `orchestrator.py` MUST verify that the current active Git branch is exactly `master`. If it is any other branch (e.g., a feature branch), the script must IMMEDIATELY print `[FATAL] Orchestrator must be started from the master branch to prevent nested branch creation.` and terminate via `exit(1)`.
1. **Implement Global Lock**: Introduce an OS-level file lock using `fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)` at the very beginning of `orchestrator.py` to ensure only one instance can run per workspace. Use a lock file named `.sdlc_run.lock` in the project root.
2. **Fail-Fast Exit & Self-Explanatory Handoff**: If the lock cannot be acquired (a `BlockingIOError` is raised), the script must IMMEDIATELY print the following self-explanatory action block (Tool-as-Prompt) and terminate via `exit(1)`:
   ```
   [FATAL] Another SDLC pipeline is currently running. Concurrent execution is blocked.
   [ACTION REQUIRED FOR MANAGER]: Another SDLC pipeline is currently running in this workspace. Concurrent execution is physically blocked by the OS lock. Do NOT retry immediately. Wait for the existing Orchestrator process to finish.
   ```
3. **No Zombie Locks**: Leverage OS behavior that automatically releases `fcntl` locks upon process termination (graceful or ungraceful, e.g., `kill -9`). This eliminates the risk of stale lock files paralyzing the system.

## Scope
- Target File: `orchestrator.py` within `/root/.openclaw/workspace/projects/leio-sdlc`
- Mechanism: `fcntl.flock` implementation
- Error Output: Specific console message including the `[ACTION REQUIRED FOR MANAGER]` block.

## Autonomous Test Strategy
Since this project involves a Python script/CLI execution (`orchestrator.py`), the optimal testing strategy is Integration testing with process mocking/spawning:
- A test script should start a background `orchestrator.py` process, then immediately attempt to start a second `orchestrator.py` process in the same workspace.
- The test must verify that the second process exits with status code `1`.
- The test must verify that the second process's standard output contains the exact `[ACTION REQUIRED FOR MANAGER]` string required.
- The background process should then be killed to release the lock.

## TDD Guardrails
**MANDATORY**: The implementation and its failing test MUST be delivered in the same PR contract. No implementation will be accepted without a concurrent failing/passing test demonstrating the concurrency prevention works as designed.
