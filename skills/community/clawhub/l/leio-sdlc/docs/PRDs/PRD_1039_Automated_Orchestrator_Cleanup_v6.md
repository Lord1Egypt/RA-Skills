# PRD: Implement Graceful Aborts and Forensic Quarantine for Orchestrator (ISSUE-1039 v6)

## Context
When the SDLC `orchestrator.py` script exits unexpectedly (e.g., Python exceptions, SIGTERM, SIGINT, or logical fatal errors), it currently terminates abruptly with raw `sys.exit(1)` calls. This leaves the Git repository in a "dirty" state and orphans child processes (e.g., Coder subagents, test scripts), causing race conditions that corrupt the workspace in the background.

Previous designs failed architectural audits because they relied on synchronous `subprocess.run` tracking (impossible to reap grandchildren), destructive Git commands (`git reset --hard`), indiscriminate stashing (`git stash` saving ephemeral daemon locks), and global bans on `git branch -D` (which violated successful merge lifecycle rules). We must implement process group isolation and a WIP-commit-based quarantine tool.

## Requirements

1. **Process Group Isolation & Reaper (`SIGINT`, `SIGTERM`, and Exceptions)**:
   - **Refactor Launch Mechanism**: In `orchestrator.py`, refactor the invocations of long-running subagents (`spawn_coder.py`, `spawn_reviewer.py`, `spawn_planner.py`) from synchronous `subprocess.run` to asynchronous `subprocess.Popen(..., start_new_session=True)`. This creates an isolated Process Group (PGID) for the subagent and all its descendants (grandchildren).
   - **Global Reaper**: Wrap the main execution loop in a `try...except Exception` block. Use the `signal` module to intercept `SIGINT` and `SIGTERM`.
   - **Full Process Tree Kill**: Upon catching a fatal exception or termination signal, the orchestrator MUST immediately reap active subagents using `os.killpg(os.getpgid(proc.pid), signal.SIGTERM)` (and optionally wait/SIGKILL). This ensures no orphaned grandchild processes survive to corrupt the workspace.
   - After reaping, print a specific `HandoffPrompter` message (`fatal_interrupt` or `fatal_crash`) and exit. Do NOT execute any automated Git cleanup during a crash.

2. **Forensic Quarantine Flag (`--cleanup`)**:
   - Add a new command-line argument `--cleanup` to `orchestrator.py`.
   - When invoked, this flag MUST bypass the normal SDLC pipeline and execute a safe quarantine sequence:
     1. Determine the current branch. If it is `master` or `main`, exit with an error (do not quarantine the main branch).
     2. Run `git add -A` to stage all modifications. This respects `.gitignore`, ensuring ephemeral lock files (like `.coder_session`) are NOT preserved.
     3. Run `git commit -m "WIP: 🚨 FORENSIC CRASH STATE"` to permanently lock the "crime scene" into the Git history.
     4. Run `git branch -m <current_branch_name>_crashed_$(date +%s)` to quarantine the toxic branch.
     5. Run `git checkout master` to return the workspace to a clean slate.
   - **Absolute Boundary**: `git stash`, `git reset`, and `git branch -D` are strictly forbidden within this `--cleanup` logic.

3. **Handoff Prompter & Exit Point Linking**:
   - Every `sys.exit(1)` throughout `orchestrator.py` MUST be mapped to a specific `HandoffPrompter` call.
   - **Success Signal**: Before exiting with code 0 (queue empty), MUST print `HandoffPrompter.get_prompt("happy_path")`.
   - **Prompt Updates in `scripts/handoff_prompter.py`**:
     - `git_checkout_error`: `[FATAL_GIT] Git checkout failed. Workspace preserved. Invoke --cleanup to quarantine.`
     - `fatal_crash` (New): `[FATAL_CRASH] Orchestrator crashed. Process groups reaped. Workspace preserved. Read traceback. Invoke --cleanup to quarantine the branch.`
     - `fatal_interrupt` (New): `[FATAL_INTERRUPT] Aborted via SIGINT/SIGTERM. Process groups reaped. Workspace preserved.`

4. **Governance Constitution Update (Section 4.2 Amendment)**:
   - Update `/root/.openclaw/workspace/projects/docs/TEMPLATES/organization_governance.md`.
   - Amend Section 4.2 ("Toxic Branch Anti-Manual Merge"). The current rule mandates `git branch -D` for killed pipelines, which destroys forensic commit history (contradicting Section 3.2). Amend it to mandate the "WIP Commit & Rename" quarantine protocol instead for aborted/crashed pipelines.
   - *Note: Section 4.1's mandate to `git branch -D` after a SUCCESSFUL merge remains entirely intact.*

## Framework Modifications
- `scripts/handoff_prompter.py`
- `scripts/orchestrator.py`
- `/root/.openclaw/workspace/projects/docs/TEMPLATES/organization_governance.md`

## Architecture
By migrating from `subprocess.run` to `Popen(start_new_session=True)`, we leverage Unix Process Groups to guarantee total termination of runaway agent clusters. By replacing `git stash` with a committed "WIP" state that respects `.gitignore`, we perfectly preserve the forensic environment without polluting the stash stack or saving ephemeral daemon locks. This design flawlessly aligns with the amended organizational governance.

## Acceptance Criteria
- [ ] Subagents are launched via `Popen` with `start_new_session=True`.
- [ ] `os.killpg` successfully reaps all grandchild processes on SIGINT/SIGTERM/Exception.
- [ ] `--cleanup` creates a WIP commit, renames the branch, and checks out `master` without using `git stash` or `git branch -D`.
- [ ] `organization_governance.md` Section 4.2 is updated to reflect the new quarantine protocol.