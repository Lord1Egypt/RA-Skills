# PRD: Implement Graceful Aborts and Forensic Quarantine for Orchestrator (ISSUE-1039 v4)

## Context
When the SDLC `orchestrator.py` script exits unexpectedly (e.g., Python exceptions, SIGTERM, SIGINT, or logical fatal errors), it currently terminates abruptly with raw `sys.exit(1)` calls. This leaves the Git repository in a "dirty" state and fails to provide actionable Just-In-Time (JIT) instructions to the Manager agent. Furthermore, abrupt exits leave active child processes (e.g., Coder subagents, test scripts) running as orphans, causing race conditions that corrupt the workspace after the orchestrator has died.

Previous designs failed architectural audits because they mandated destructive commands (`git reset --hard`, `git branch -D`) which violated the organization's strict evidence preservation policy (`organization_governance.md` Section 3.2: "DO NOT git reset"). We must implement a comprehensive process-reaping mechanism and a non-destructive forensic quarantine tool (`--cleanup`).

## Requirements

1. **Process Reaper & Signal Handling (`SIGINT`, `SIGTERM`, and Global Exceptions)**:
   - Implement a global active subprocess tracker in `orchestrator.py`. Every time a `subprocess.Popen` or `subprocess.run` is invoked for a long-running subagent/task, its PID must be tracked.
   - Use the `signal` module to intercept `SIGINT` (Ctrl+C) and `SIGTERM` (Kill commands).
   - Wrap the main execution loop in a high-level `try...except Exception` block.
   - **Crucial Reaper Logic**: Upon receiving a termination signal OR catching a fatal Python exception, the orchestrator MUST immediately send `SIGTERM` (and subsequently `SIGKILL` if needed) to all tracked child processes and `wait()` for their termination. This guarantees no orphaned agents continue modifying the workspace in the background.
   - After reaping children, the orchestrator must print a specific `HandoffPrompter` message (`fatal_interrupt` or `fatal_crash`) and exit. It MUST NOT execute any Git reset or cleanup.

2. **Forensic Quarantine Flag (`--cleanup`)**:
   - Add a new command-line argument `--cleanup` to `orchestrator.py`.
   - When executed, this flag MUST bypass the normal SDLC pipeline and execute a safe quarantine sequence:
     1. Determine the current branch. If it is `master` or `main`, exit with an error (do not quarantine the main branch).
     2. Sweep all uncommitted changes (dirty/untracked files) into a stash: `git stash --include-untracked -m "Forensic backup of crashed state"`.
     3. Rename the current toxic branch to quarantine it: `git branch -m <current_branch_name>_crashed_$(date +%s)`.
     4. Safely checkout the main line: `git checkout master`.
   - **Absolute Boundary**: `git reset --hard`, `git clean -fd`, and `git branch -D` are strictly forbidden in this script.

3. **Handoff Prompter & Self-Explanation Adjustments**:
   - **Success Signal**: Before exiting with code 0 (queue empty), MUST print `HandoffPrompter.get_prompt("happy_path")`.
   - **Exit Point Linking**: Every `sys.exit(1)` throughout `orchestrator.py` MUST be accompanied by a corresponding `HandoffPrompter` call. No silent deaths.
   - **Prompt Updates in `scripts/handoff_prompter.py`**:
     - `git_checkout_error`: Update to `[FATAL_GIT] Git checkout failed. Workspace preserved for forensic inspection. Review logs and invoke --cleanup to quarantine the broken branch.`
     - `blocked_fatal`: Link to existing `dead_end` prompt.
     - `fatal_crash` (New): `[FATAL_CRASH] Orchestrator crashed. Child processes reaped. Workspace preserved for forensic inspection. Read the traceback. You may invoke --cleanup to quarantine the branch.`
     - `fatal_interrupt` (New): `[FATAL_INTERRUPT] Process aborted via SIGINT/SIGTERM. Child processes reaped. Workspace preserved for forensic inspection.`
     - `fatal_timeout` (New): `[FATAL_TIMEOUT] Sub-agent execution timed out. Review task size.`

5. **Governance Constitution Update (Section 4.2 Amendment)**:
   - Modify the global governance constitution `/root/.openclaw/workspace/projects/docs/TEMPLATES/organization_governance.md`.
   - Update Section 4.2 ("Toxic Branch Anti-Manual Merge"). The current mandate to use `git branch -D` inherently destroys forensic commit history on crashed feature branches, contradicting the "DO NOT git reset" preservation spirit of Section 3.2.
   - Amend Section 4.2 to strictly forbid `git branch -D` during unexpected aborts. It must mandate isolating the toxic branch via renaming (`git branch -m <name>_crashed_...`) to preserve the "crime scene" (作案现场) while keeping the main branch clean for future runs.

## Framework Modifications
- `scripts/handoff_prompter.py`
- `scripts/orchestrator.py`
- `/root/.openclaw/workspace/projects/docs/TEMPLATES/organization_governance.md`

## Architecture
This design strictly enforces the "no evidence destruction" mandate in `organization_governance.md`. By actively reaping child processes, we prevent zombie modifications and concurrent data corruption. By amending the constitution to replace branch deletion with branch renaming quarantine, we preserve the exact sequence of bad commits that led to the crash. This allows human/agent investigators to inspect the "crime scene" safely without blocking future SDLC runs.

## Acceptance Criteria
- [ ] Throwing a Python exception mid-execution correctly reaps all child processes and outputs `[FATAL_CRASH]`.
- [ ] Sending a `SIGTERM` correctly reaps all child processes and outputs `[FATAL_INTERRUPT]`.
- [ ] Running `python3 scripts/orchestrator.py --cleanup` safely stashes uncommitted files, renames the toxic branch to a `_crashed_` suffix, and checks out `master`.
- [ ] Destructive Git commands (`reset`, `clean`, `branch -D`) are entirely absent from the cleanup sequence.
- [ ] Successful completion outputs the `[SUCCESS_HANDOFF]` prompt.
- [ ] `organization_governance.md` is updated to replace branch deletion with the new quarantine protocol.