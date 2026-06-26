# PRD: Implement Graceful Aborts and Forensic Cleanup for Orchestrator (ISSUE-1039 v3)

## Context
When the SDLC `orchestrator.py` script exits unexpectedly (e.g., Python exceptions, SIGTERM, SIGINT, or logical fatal errors), it currently terminates abruptly with raw `sys.exit(1)` calls. This leaves the Git repository in a "dirty" state (checked out on a temporary branch with uncommitted modified/untracked files) and fails to provide actionable Just-In-Time (JIT) instructions to the Manager agent.

Previous designs for a `--cleanup` flag failed architectural audits because they mandated `git reset --hard` and `git clean -fd`. According to `organization_governance.md` Section 3.2, `git reset` is strictly forbidden because it irreversibly destroys forensic evidence ("作案现场") needed for debugging and the self-healing loop. We must provide a safe cleanup mechanism that clears the workspace for the next run *without* destroying the evidence.

## Requirements

1. **Forensic Cleanup Flag (`--cleanup`)**:
   - Add a new command-line argument `--cleanup` to `orchestrator.py`.
   - When executed with `python3 scripts/orchestrator.py --cleanup`, the script MUST immediately execute a safe teardown sequence that preserves evidence:
     1. Determine the current branch.
     2. Run `git stash --include-untracked -m "Forensic backup of crashed state"` to sweep all dirty modifications and untracked artifacts into the stash.
     3. Run `git checkout master` (or `main`).
     4. If the previous branch was a feature/PR branch (not master/main), forcefully delete it using `git branch -D <branch_name>` to isolate the toxic branch (as per Governance Section 4.2).
   - **Crucial**: Absolutely NO `git reset --hard` or `git clean -fd` is allowed.

2. **Signal Handling & Graceful Exit (`SIGINT` & `SIGTERM`)**:
   - Use the `signal` module to intercept `SIGINT` (Ctrl+C) and `SIGTERM` (Kill commands).
   - Upon receiving a termination signal, the script MUST NOT execute any cleanup. Instead, it must print a specific `HandoffPrompter` message (`fatal_interrupt`) to inform the Manager that the process was killed, leaving the workspace dirty for inspection.

3. **Handoff Prompter & Self-Explanation Adjustments**:
   - **Success Signal (`happy_path`)**: Before exiting with code 0 (queue empty), MUST print `HandoffPrompter.get_prompt("happy_path")`.
   - **Exit Point Linking**: Every `sys.exit(1)` throughout `orchestrator.py` MUST be accompanied by a corresponding `HandoffPrompter` call. No silent deaths.
   - **Prompt Updates in `scripts/handoff_prompter.py`**:
     - `git_checkout_error`: Update to `[FATAL_GIT] Git checkout failed. Workspace preserved for forensic inspection. Please review logs and resolve branch conflicts manually or via --cleanup.`
     - `blocked_fatal`: Link to existing `dead_end` prompt.
     - `fatal_crash` (New): `[FATAL_CRASH] An unexpected error occurred. Workspace preserved for forensic inspection. Read the traceback. You may invoke --cleanup to stash the evidence and reset.`
     - `fatal_interrupt` (New): `[FATAL_INTERRUPT] Process aborted via SIGINT/SIGTERM. Workspace preserved for forensic inspection.`
     - `fatal_timeout` (New): `[FATAL_TIMEOUT] Sub-agent execution timed out. Review task size and workspace state.`

4. **Global Exception Handling (`try...except`)**:
   - Wrap the main execution loop in a high-level `try...except Exception` block. If an unhandled Python exception occurs, it must print the traceback followed by `HandoffPrompter.get_prompt("fatal_crash")` before exiting with code 1. It MUST NOT automatically clean up the workspace.

## Framework Modifications
- `scripts/handoff_prompter.py`
- `scripts/orchestrator.py`

## Architecture
This design rigorously adheres to the "no git reset" rule in `organization_governance.md`. By utilizing `git stash --include-untracked`, we achieve the operational goal of returning the system to a clean `master` state (ready for new tasks) while 100% preserving the exact "crime scene" artifacts safely in the Git stash for later forensic analysis.

## Acceptance Criteria
- [ ] Running `python3 scripts/orchestrator.py --cleanup` safely stashes dirty files, checks out `master`, and deletes the toxic branch.
- [ ] Unhandled Python exceptions result in a traceback + `[FATAL_CRASH]` prompt without altering the Git working tree.
- [ ] Sending a `SIGTERM` results in a `[FATAL_INTERRUPT]` prompt without altering the Git working tree.
- [ ] Successful completion outputs the `[SUCCESS_HANDOFF]` prompt.
- [ ] `git reset` and `git clean` are absolutely not used in the cleanup logic.