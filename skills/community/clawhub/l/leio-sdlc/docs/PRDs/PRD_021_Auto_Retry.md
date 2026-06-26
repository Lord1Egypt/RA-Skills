# PRD_021: Auto-Retry Mechanism for LLM API Flakiness

## 1. Problem Statement
Sub-agent spawn scripts (`spawn_planner.py`, `spawn_coder.py`, `spawn_reviewer.py`) currently call `subprocess.run(["openclaw", "sessions_spawn", ...])` exactly once. If the Gateway is temporarily unavailable, the LLM API times out, or the CLI crashes with a non-zero exit code due to network issues, the entire pipeline halts immediately.

## 2. Goals
- Implement an Exponential Backoff and Retry wrapper around the `sessions_spawn` calls.
- Keep it simple: this is a "quick win" infrastructure patch.

## 3. Key Features
### 3.1 Shared Retry Logic
- Instead of duplicating code, create a shared utility function inside `scripts/`. Since we want to keep it simple, we will refactor the 3 `spawn_*.py` scripts to use a robust retry loop directly, or extract it to `scripts/utils.py`.
- **Retry Logic**:
  - Max Retries: 3
  - Base Sleep: 3 seconds. Multiplier: 2 (e.g., 3s, 6s, 12s).
  - Condition: If `subprocess.call` returns `!= 0`, trigger retry.
  - If all retries fail, `sys.exit(1)`.

### 3.2 Implementation
- Update `scripts/spawn_planner.py`
- Update `scripts/spawn_coder.py`
- Update `scripts/spawn_reviewer.py`

## 4. Acceptance Criteria
- [ ] The `subprocess.run` or `subprocess.call` in the 3 spawn scripts is wrapped in a retry loop.
- [ ] The loop handles non-zero exit codes.
- [ ] Uses `time.sleep` with exponential backoff.
- [ ] No changes to `SDLC_TEST_MODE` blocks (testing should still execute instantly without retries).
