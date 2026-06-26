# PRD_023_CLI_Sync: Refactoring Subagent Spawns for Production-Test Parity

## 1. Problem Statement
The current Python spawn scripts (`spawn_planner.py`, `spawn_coder.py`, `spawn_reviewer.py`) attempt to use `subprocess.run(["openclaw", "sessions_spawn", ...])`. This command does not exist in the OpenClaw CLI namespace. It is a native LLM tool masquerading as a shell command, leading to crashes in production execution and deep Triad tests.

## 2. Architectural Goal (Production-Test Parity)
As queried by the Boss, the solution to this bug unlocks a higher architectural principle: **Production and Test environments must execute the exact same underlying mechanics.** By switching our Python scripts to use the valid `openclaw agent` CLI command, the Manager (in Production) will spawn subagents exactly the same way the bash scripts spawn the tests. This unifies the framework.

## 3. Implementation Details
The Coder must modify the `subprocess.run` execution block in the following files:
1. `scripts/spawn_planner.py`
2. `scripts/spawn_coder.py`
3. `scripts/spawn_reviewer.py`

### 3.1 The Modification
- **Locate**: Find the `subprocess.run(["openclaw", "sessions_spawn", task_string])` line inside the exponential backoff `for` loop.
- **Replace with**: A secure call to the `openclaw agent` CLI, specifying a unique session ID to guarantee sandbox isolation (e.g., using `uuid` to prevent history contamination).
- **Code Template**:
```python
import uuid
# ... inside the loop ...
session_id = f"subtask-{uuid.uuid4().hex[:8]}"
result = subprocess.run(
    ["openclaw", "agent", "--session-id", session_id, "-m", task_string],
    capture_output=True,
    text=True
)
```
*(Note: Ensure `import uuid` is added to the top of each file).*

## 4. Acceptance Criteria
- [ ] All three `spawn_*.py` scripts import `uuid`.
- [ ] The `subprocess.run` command array is updated from `["openclaw", "sessions_spawn", ...]` to `["openclaw", "agent", "--session-id", <dynamic_uuid>, "-m", task_string]`.
- [ ] The Triad Test `scripts/test_triad_reviewer.sh` is executed and no longer fails with `unknown command 'sessions_spawn'`.
- [ ] No changes made to the exponential backoff logic or the `SDLC_TEST_MODE` blocks.