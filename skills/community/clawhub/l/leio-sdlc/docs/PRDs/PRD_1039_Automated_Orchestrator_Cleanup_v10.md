# PRD: Implement Graceful Aborts and Forensic Quarantine for Orchestrator (ISSUE-1039 v10)

## Context
When the SDLC `orchestrator.py` script exits unexpectedly (e.g., Python exceptions, SIGTERM, SIGINT, or logical fatal errors), it terminates abruptly with raw `sys.exit(1)` calls. This leaves the Git repository in a "dirty" state and orphans child processes (e.g., Coder subagents, test scripts), causing race conditions that corrupt the workspace in the background.

Previous designs failed architectural audits due to synchronous `subprocess.run` tracking limitations, destructive Git commands (`git reset --hard`), indiscriminate stashing, and global bans on `git branch -D` (which violated successful merge rules). They also failed due to Python sub-process shell injection risks, `BaseException` hierarchy bugs (missing `SystemExit` coverage), and bleeding ignored toxic artifacts via catastrophic `git clean -x` commands. We must implement synchronous process group isolation with a guaranteed `finally` reaper and a targeted, robust WIP-commit quarantine tool.

## Requirements

1. **Process Group Isolation & Guaranteed Reaper (`finally` Block Mechanism)**:
   - **Refactor Launch Mechanism**: In `orchestrator.py`, refactor the invocations of long-running subagents (`spawn_coder.py`, `spawn_reviewer.py`, `spawn_planner.py`) from synchronous `subprocess.run` to `subprocess.Popen(..., start_new_session=True)`. 
   - **Crucial Synchronous Block**: The orchestrator MUST explicitly call `proc.wait()` (with an optional timeout matching the subagent's SLA) immediately after `Popen`. The state machine must remain strictly sequential.
   - **Global Reaping Architecture**: Wrap the main execution loop in a `try...finally` structure.
   - **The Reaper Logic**: The `finally` block MUST contain the logic to check for active subagent process groups. If found, it MUST immediately reap them using `os.killpg(os.getpgid(proc.pid), signal.SIGTERM)` (and optionally `SIGKILL`).
   - **Why `finally`?**: This guarantees that whether the orchestrator exits via a normal return, an unhandled `Exception`, a `KeyboardInterrupt` (SIGINT), or an explicit `sys.exit(1)` (which raises `SystemExit`, a `BaseException`), the subagents are ALWAYS killed before the process dies.
   - **Signal Handling**: Use the `signal` module to intercept `SIGTERM` and raise a custom exception to trigger the `finally` reaper.
   - After reaping, ensure the specific `HandoffPrompter` message is printed for the specific exit vector.

2. **Forensic Quarantine Flag (`--cleanup`)**:
   - Add a new command-line argument `--cleanup` to `orchestrator.py`.
   - When invoked, this flag MUST bypass the normal SDLC pipeline and execute a safe quarantine sequence:
     1. Determine the current branch. If it is `master` or `main`, exit with an error (do not quarantine the main branch).
     2. Run `git add -A` to stage all modifications (respecting `.gitignore`).
     3. Run `git commit --allow-empty -m "WIP: 🚨 FORENSIC CRASH STATE"` to permanently lock the "crime scene" into Git history, preventing empty commit crashes.
     4. Calculate a timestamp natively in Python using `int(time.time())` (Do NOT use Bash string interpolation).
     5. Rename the current toxic branch using Python f-strings: `git branch -m {current_branch_name}_crashed_{timestamp}`.
     6. Run `git checkout master`.
     7. **Targeted Artifact Obliteration**: Use Python's native `os.remove()` to explicitly delete ephemeral daemon locks (`.coder_session`, `.sdlc_repo.lock`) if they exist. Do NOT use `git clean -fdx`.
   - **Absolute Boundary**: `git stash`, `git reset`, `git clean`, and `git branch -D` are strictly forbidden within this `--cleanup` logic.

3. **Handoff Prompter & Exit Point Linking**:
   - Every `sys.exit(1)` throughout `orchestrator.py` MUST be mapped to a specific `HandoffPrompter` call.
   - **Success Signal**: Before exiting with code 0 (queue empty), MUST print `HandoffPrompter.get_prompt("happy_path")`.
   - **Prompt Updates in `scripts/handoff_prompter.py`**:
     - `git_checkout_error`: `[FATAL_GIT] Git checkout failed. Workspace preserved. Invoke --cleanup to quarantine.`
     - `fatal_crash` (New): `[FATAL_CRASH] Orchestrator crashed. Process groups reaped. Workspace preserved. Read traceback. Invoke --cleanup to quarantine the branch.`
     - `fatal_interrupt` (New): `[FATAL_INTERRUPT] Aborted via SIGINT/SIGTERM. Process groups reaped. Workspace preserved.`

4. **Governance Constitution Update (Section 4.2 Amendment)**:
   - Amend Section 4.2 ("Toxic Branch Anti-Manual Merge") in `/root/.openclaw/workspace/projects/docs/TEMPLATES/organization_governance.md`. 
   - Mandate the "WIP Commit & Rename Quarantine" protocol for aborted/crashed pipelines.
   - *Note: Section 4.1's mandate to `git branch -D` after a SUCCESSFUL merge remains intact.*

## Framework Modifications
- `scripts/handoff_prompter.py`
- `scripts/orchestrator.py`
- `/root/.openclaw/workspace/projects/docs/TEMPLATES/organization_governance.md`

## Architecture
By leveraging a global `try...finally` reaper, we guarantee that all subagent process groups are reaped regardless of the exit vector (Exceptions, SIGINT, or explicit `sys.exit`). The `--cleanup` flag provides a hermetically sealed quarantine mechanism that protects the master branch from ghost artifacts via targeted `os.remove()`, safely preserving the forensic environment without polluting the stash stack.

## Acceptance Criteria
- [ ] Subagents are launched via `Popen` with `start_new_session=True` and immediately `wait()`ed upon.
- [ ] The `finally` block successfully reaps all grandchild processes on ALL exit paths (including `sys.exit`).
- [ ] `--cleanup` creates a WIP commit, uses Python timestamps to rename the branch, checks out `master`, and safely targets ephemeral locks via `os.remove()`.
- [ ] `organization_governance.md` Section 4.2 is updated.