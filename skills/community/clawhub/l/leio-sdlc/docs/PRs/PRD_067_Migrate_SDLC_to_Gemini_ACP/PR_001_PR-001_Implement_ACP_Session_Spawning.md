status: closed

# PR-001: Implement ACP Session Spawning and Messaging Abstraction

## 1. Objective
Migrate the base Coder initialization from stateless CLI commands to stateful ACP sessions using `sessions_spawn` and `sessions_send`.

## 2. Scope & Implementation Details
- Modify `spawn_coder.py` to replace `openclaw agent` CLI subprocess calls with `sessions_spawn(runtime="acp", agentId="gemini", mode="session")`.
- Implement a mechanism to store and retrieve the `sessionKey` for the spawned Coder.
- Implement a `send_feedback` function using `sessions_send(sessionKey, message)` to append reviewer feedback to the existing session.

## 3. TDD & Acceptance Criteria
- Write unit tests mocking `sessions_spawn` to verify correct arguments are passed.
- Write unit tests mocking `sessions_send` to verify that feedback is correctly routed to the stored `sessionKey`.
- Both tests and implementation must be delivered together and pass cleanly.


> [Escalation] Tier 1 Reset triggered due to Coder failure or Arbitrator rejection.
