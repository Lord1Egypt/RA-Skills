# PRD: Implement Graceful Aborts and JIT Prompts for Orchestrator (ISSUE-1039 v2)

## Context
When the SDLC `orchestrator.py` script exits unexpectedly (e.g., Python exceptions, SIGTERM, SIGINT, or logical fatal errors), it currently terminates abruptly with raw `sys.exit(1)` calls. This lacks structured `HandoffPrompter` tags and fails to provide actionable Just-In-Time (JIT) instructions to the Manager agent. Furthermore, the orchestrator lacks a unified way for the Manager to safely tear down a corrupted environment manually without typing raw Git commands.

Based on recent architectural audits, **automated teardowns (e.g., `git reset --hard`) during unexpected crashes are strictly forbidden**, as they destroy forensic evidence ("作案现场") required for debugging and the self-healing loop. Instead, we must preserve the dirty state, emit accurate JIT prompts, and provide an explicit `--cleanup` interface for the Manager to invoke deliberately.

## Requirements

1. **Standalone Cleanup Flag (`--cleanup`)**:
   - Add a new command-line argument `--cleanup` to `orchestrator.py`.
   - When executed with `python3 scripts/orchestrator.py --cleanup`, the script MUST immediately execute a full teardown sequence: `git reset --hard HEAD`, `git clean -fd`, and `git checkout master` (and optionally delete any leftover `feature/*` branches or `PR_*.md` temporary branches).
   - This provides the Manager with a deterministic, safe tool to reset the environment explicitly.

2. **Signal Handling & Graceful Exit (`SIGINT` & `SIGTERM`)**:
   - Use the `signal` module to intercept `SIGINT` (Ctrl+C) and `SIGTERM` (Kill commands).
   - Upon receiving a termination signal, the script MUST NOT execute any Git reset or cleanup. Instead, it must print a specific `HandoffPrompter` message (`fatal_interrupt`) to inform the Manager that the process was killed, and the workspace remains dirty for inspection.

3. **Handoff Prompter & Self-Explanation Adjustments**:
   - **Success Signal (`happy_path`)**: Before exiting with code 0 (queue empty), MUST print `HandoffPrompter.get_prompt("happy_path")`.
   - **Exit Point Linking**: Every `sys.exit(1)` throughout `orchestrator.py` MUST be accompanied by a corresponding `HandoffPrompter` call. No silent deaths.
   - **Prompt Updates in `scripts/handoff_prompter.py`**:
     - `git_checkout_error`: Update to `[FATAL_GIT] Git checkout failed. Workspace preserved for forensic inspection. Please review logs and resolve branch conflicts manually or via --cleanup.`
     - `blocked_fatal`: Link to existing `dead_end` prompt.
     - `fatal_crash` (New): `[FATAL_CRASH] An unexpected error occurred. Workspace preserved for forensic inspection. Read the traceback. You may invoke --cleanup to reset.`
     - `fatal_interrupt` (New): `[FATAL_INTERRUPT] Process aborted via SIGINT/SIGTERM. Workspace preserved for forensic inspection.`
     - `fatal_timeout` (New): `[FATAL_TIMEOUT] Sub-agent execution timed out. Review task size and workspace state.`

4. **Global Exception Handling (`try...except`)**:
   - Wrap the main execution loop in a high-level `try...except Exception` block. If an unhandled Python exception occurs, it must print the traceback followed by `HandoffPrompter.get_prompt("fatal_crash")` before exiting with code 1. It MUST NOT clean up the workspace.

## Framework Modifications
- `scripts/handoff_prompter.py`
- `scripts/orchestrator.py`

## Architecture
This design prioritizes forensic observability and explicit human/Manager agency over dangerous autonomous resets. By mapping all exits to JIT prompts and providing a dedicated `--cleanup` entry point, the system achieves predictable state management without violating the project's governance protocols.

## Acceptance Criteria
- [ ] Running `python3 scripts/orchestrator.py --cleanup` safely restores the repository to a clean `master` state.
- [ ] Unhandled Python exceptions result in a traceback + `[FATAL_CRASH]` prompt without altering the Git working tree.
- [ ] Sending a `SIGTERM` results in a `[FATAL_INTERRUPT]` prompt without altering the Git working tree.
- [ ] Successful completion outputs the `[SUCCESS_HANDOFF]` prompt.
- [ ] All `sys.exit(1)` calls are preceded by a relevant `HandoffPrompter` output.