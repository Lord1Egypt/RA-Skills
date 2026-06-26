status: closed

# PR-002: Implement Coder Session Strategy and Teardown Logic

## 1. Objective
Implement the `--coder-session-strategy` CLI argument and integrate the `teardown_coder_session(workdir)` logic across the FSM states to manage LLM cognitive bias and path dependency.

## 2. Scope & Implementation Details
- `scripts/orchestrator.py`:
  - Add `--coder-session-strategy` with choices `["always", "per-pr", "on-escalation"]` and `default="on-escalation"`.
  - **always**: Call `teardown_coder_session(workdir)` at the start of the `while True` loop in State 3.
  - **per-pr**: Call `teardown_coder_session(workdir)` after `current_pr` selection but before the inner retry loop.
  - **on-escalation**: Call `teardown_coder_session(workdir)` upon entering State 5 (3-Tier Escalation Protocol).

## 3. TDD & Acceptance Criteria
- `tests/test_orchestrator_session_strategy.py`: Write tests with mocked `teardown_coder_session` to verify it is called at the correct exact FSM state transitions for all three strategies.
- Verify that providing an invalid strategy string results in an argparse error.
