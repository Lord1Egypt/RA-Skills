# Product Requirements Document (PRD)

## 1. Meta Information
- **Document Title**: PRD_ISSUE-1063_Orchestrator_Stability_and_Notifier
- **Target Audience**: Leio-SDLC Coder Agent, Reviewer Agent
- **Version**: 1.0.1
- **Status**: Completed

## 2. Executive Summary
This PRD addresses two critical stability and usability issues (ISSUE-1063 and ISSUE-1062) in the SDLC Orchestrator pipeline. 
First, when a Coder sub-agent hangs and triggers a timeout, the Orchestrator fails to reap the spawned daemon process correctly. Instead of gracefully transitioning to State 5 (Forensic Quarantine), the orchestrator crashes, leaving zombie processes.
Second, the system uses restrictive regex and splitting logic that truncates names of micro-sliced PRs (e.g., `PR_003_1_Fix`), causing confusion in Slack updates and, more critically, fatal session collisions in the Coder's session ID assignment.

## 3. Detailed Requirements

### 3.1. Orchestrator Suicide & Zombie Coder Fix
- **Modify Coder Spawn**: In `scripts/spawn_coder.py`, modify the command that spawns the Coder agent to attach it locally by adding the `--local` flag to the `openclaw agent` call. This ensures the agent dies when its CLI wrapper is killed. Also update the corresponding tests (`tests/test_spawn_coder.py`).
- **Fix Timeout Exceptions**: In `scripts/orchestrator.py`, locate the two `subprocess.TimeoutExpired` exception handling blocks where the Coder is spawned. 
- Remove any `raise` statements within these exception blocks. 
- Explicitly trigger the transition to State 5 by setting the appropriate boolean flags (e.g., `state_5_trigger = True`) seamlessly without relying on the process return code. 
- When terminating the child process (`os.killpg`), use `signal.SIGTERM`, followed by a bounded wait timeout. If it does not terminate, fallback to `signal.SIGKILL` to prevent eternal deadlocks.

### 3.2. Micro-Sliced PR Index & Session Crossover Fix
- **Formatter Fix**: In `scripts/notification_formatter.py`, update the regex parsing logic for PR ID extraction. It must extract the pure numeric sequence and internal underscores using a regex pattern, replacing internal underscores with dashes (so `PR_003_1_Fix` properly becomes `[pr-003-1]`). Update `tests/test_notification_formatter.py` accordingly.
- **Session Crossover Fix**: In `scripts/spawn_coder.py`, update the `extract_pr_id` function to handle micro-sliced PR names similarly. Ensure the session ID correctly reflects the full micro-slice index (e.g., `sdlc_coder_PR_003_1`) to prevent context crossover and session bleeding between independent micro-sliced PRs. Update `tests/test_spawn_coder.py` accordingly.

## 4. Acceptance Criteria
1. The Coder agent process is properly terminated and reaped when a timeout occurs, leaving no zombie processes, using a bounded wait with SIGKILL fallback.
2. The orchestrator gracefully transitions to State 5 on timeout instead of crashing.
3. The notification formatter successfully translates micro-sliced PR names into dashed sequences (e.g., `[pr-003-1]`).
4. Micro-sliced PRs are assigned unique session IDs in `spawn_coder.py` to prevent context collision.
5. All existing tests pass (`GREEN`), including the newly updated ones.

## 5. Framework Modifications
- `scripts/spawn_coder.py`
- `scripts/orchestrator.py`
- `scripts/notification_formatter.py`
- `tests/test_spawn_coder.py`
- `tests/test_notification_formatter.py`
- `tests/test_orchestrator_stability.py`
