# PRD: Migrate SDLC Execution to Gemini CLI via ACP Protocol

## Problem Statement
The current SDLC flow relies entirely on the OpenClaw native agent running locally, which suffers from Stateless Amnesia (every time a Coder is rejected, a new amnesiac Coder process is spawned) and Overprivileged Sandboxing (Coders run with full read/write access to the entire workspace, allowing for potential Reward Hacking/UAT Forgery).

## Solution
Migrate the Coder execution in `spawn_coder.py` from the stateless 'openclaw agent' CLI command to persistent, PR-scoped Gemini ACP sessions using the 'sessions_spawn', 'sessions_send', and teardown mechanisms. 
1. Stateful Session Spawning: Use `sessions_spawn(runtime="acp", agentId="gemini")` to create a dedicated, named session.
2. Conversational Feedback Loops: Use `sessions_send(sessionKey, message)` to append Reviewer's feedback directly into the existing Coder's conversation thread.
3. Physical Sandboxing: Constrain the ACP session to the target project directory.
4. Lifecycle Teardown: Kill/terminate the specific Gemini CLI session once a PR is successfully merged.

## Scope
Target project absolute directory: `/root/.openclaw/workspace/projects/leio-sdlc`.
The migration applies specifically to `spawn_coder.py` and the SDLC pipeline orchestrator logic for spawning, communicating with, and terminating Coder sessions.

## Testing Strategy
Autonomous Test Strategy: Define Unit/Integration testing with mocks for the `spawn_coder.py` script to ensure correct session spawning, message sending, and teardown behavior. 
TDD Guardrail: The implementation and its failing test MUST be delivered in the same PR contract.
