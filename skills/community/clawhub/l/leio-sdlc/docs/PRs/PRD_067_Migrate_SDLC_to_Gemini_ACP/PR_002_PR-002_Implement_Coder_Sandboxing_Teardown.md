status: closed

# PR-002: Implement Coder Sandboxing and Session Teardown

## 1. Objective
Secure the ACP session by constraining its working directory and ensure proper resource cleanup by tearing down the session upon PR merge.

## 2. Scope & Implementation Details
- Update the `sessions_spawn` call in `spawn_coder.py` to include the `cwd` parameter constrained to the target project directory (sandboxing).
- Implement a teardown/kill function in the orchestrator to terminate the session using the PR's `sessionKey`.
- Integrate the teardown function into the PR merge success lifecycle hook.

## 3. TDD & Acceptance Criteria
- Write unit tests to verify `cwd` is correctly passed to `sessions_spawn`.
- Write unit tests mocking the teardown mechanism to verify it is called exactly once with the correct `sessionKey` when a PR is merged.
- Both tests and implementation must be delivered together and pass cleanly.


> [Escalation] Tier 1 Reset triggered due to Coder failure or Arbitrator rejection.
