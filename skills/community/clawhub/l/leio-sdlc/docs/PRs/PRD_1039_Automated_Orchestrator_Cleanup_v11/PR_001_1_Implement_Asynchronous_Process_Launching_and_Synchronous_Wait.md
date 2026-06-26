status: closed

# PR-[ID]: Implement Asynchronous Process Launching and Synchronous Wait

## 1. Objective
Refactor the subagent launch mechanism to use asynchronous process creation with isolated process groups, immediately followed by a synchronous wait.

## 2. Scope (Functional & Implementation Freedom)
- Refactor the invocations of long-running subagents from synchronous `subprocess.run` to asynchronous `subprocess.Popen(..., start_new_session=True)`.
- Assign the result to a variable initialized as `proc = None`.
- Explicitly call `proc.wait()` immediately after `Popen` to ensure the state machine remains strictly sequential.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- Subagents are successfully launched via `Popen` with `start_new_session=True`.
- The orchestrator correctly blocks (waits) until the subagent completes.
- Tests must be written/updated to verify the new launching and waiting mechanism works as expected without altering the overall sequential flow.
- All tests must pass (100% GREEN) before submitting.