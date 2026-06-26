# PRD: Implement Graceful Aborts and Forensic Quarantine for Orchestrator (ISSUE-1039 v11)

## Context & The "Death Loop" Dilemma
When the SDLC `orchestrator.py` script exits unexpectedly (e.g., Python exceptions, SIGTERM, SIGINT, or logical fatal errors), it terminates abruptly with raw `sys.exit(1)` calls. This leaves the Git repository in a "dirty" state and orphans child processes (e.g., Coder subagents, test scripts), causing race conditions that corrupt the workspace in the background.

**CRITICAL NOTE FOR CODER (The Death Loop):**
You are modifying the very engine that governs your own lifecycle. The *current* (old) orchestrator logic deletes your `feature/` branch if your tests fail (Reviewer rejection). 
**If you receive an `ACTION_REQUIRED` from the Reviewer, YOUR PREVIOUS CODE WAS DELETED ALONG WITH THE BRANCH. You must re-write the entire solution (Code + Tests) from scratch on every attempt.** Do not assume your previous partial progress still exists on disk.

Previous designs failed architectural audits due to synchronous `subprocess.run` tracking limitations, destructive Git commands (`git reset --hard`), indiscriminate stashing, global bans on `git branch -D` (which violated successful merge rules), Python sub-process shell injection risks, `BaseException` hierarchy bugs (missing `SystemExit` coverage), and bleeding ignored toxic artifacts via catastrophic `git clean -x` commands. 

The most recent iteration (v10) failed because it introduced a `finally` block that could crash itself (`UnboundLocalError` or `ProcessLookupError` if the subprocess wasn't initialized or already died), masking the original crash. It also violated concurrency rules by allowing the `--cleanup` flag to blindly delete the repository lock, potentially corrupting active concurrent pipelines. We must implement a crash-proof `finally` reaper and a lock-aware `--cleanup` tool.

## Required Expertise
- **Deep Python Subprocess Management:** Understanding of `start_new_session=True`, process groups (`os.getpgid`, `os.killpg`), and asynchronous vs synchronous blocking (`proc.wait()`).
- **Python Exception Hierarchies:** Mastery of the difference between `Exception` and `BaseException` (specifically how `sys.exit()` raises `SystemExit` and Ctrl+C raises `KeyboardInterrupt`).
- **Distributed Concurrency:** Knowledge of Unix file locks (`fcntl.flock`, `LOCK_EX | LOCK_NB`).
- **Git Forensics:** Deep understanding of Git state, `git branch -m`, empty commits (`--allow-empty`), and why `git clean -fdx` is a dangerous blast-radius weapon.

## Requirements

1. **Process Group Isolation & Guaranteed Crash-Proof Reaper**:
   - **Refactor Launch Mechanism**: In `orchestrator.py`, refactor the invocations of long-running subagents (`spawn_coder.py`, `spawn_reviewer.py`, `spawn_planner.py`) from synchronous `subprocess.run` to `subprocess.Popen(..., start_new_session=True)`. Assign the result to a variable initialized as `proc = None` before the `try` block.
   - **Crucial Synchronous Block**: The orchestrator MUST explicitly call `proc.wait()` (with an optional timeout matching the subagent's SLA) immediately after `Popen`. The state machine must remain strictly sequential.
   - **Global Reaping Architecture**: Wrap the main execution loop in a `try...finally` structure.
   - **Crash-Proof Reaper Logic**: The `finally` block MUST safely reap active subagent process groups without raising secondary exceptions. It must implement defensive checks:
     ```python
     if 'proc' in locals() and proc is not None and proc.poll() is None:
         try:
             os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
         except OSError:
             pass # Process already dead or pgid not found
     ```
   - **Why `finally`?**: This guarantees that whether the orchestrator exits via a normal return, an unhandled `Exception`, a `KeyboardInterrupt` (SIGINT), or an explicit `sys.exit(1)` (which raises `SystemExit`, a `BaseException`), the subagents are ALWAYS killed before the process dies.
   - **Signal Handling**: Use the `signal` module to intercept `SIGTERM` and raise a custom exception or `SystemExit` to trigger the `finally` reaper.
     ```python
     # Example Signal Handler:
     def sig_handler(signum, frame):
         raise SystemExit(1)
     signal.signal(signal.SIGTERM, sig_handler)
     signal.signal(signal.SIGINT, sig_handler)
     ```
   - After reaping, ensure the specific `HandoffPrompter` message is printed for the specific exit vector.

2. **Lock-Aware Forensic Quarantine Flag (`--cleanup`)**:
   - Add a new command-line argument `--cleanup` to `orchestrator.py`.
   - When invoked, this flag MUST bypass the normal SDLC pipeline and execute a safe quarantine sequence:
     1. **Concurrency Guard (Crucial)**: The script MUST attempt to acquire an exclusive, non-blocking lock (`fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)`) on `.sdlc_repo.lock`. If it fails (raises `BlockingIOError`), another legitimate Orchestrator is currently running. The cleanup script MUST exit immediately with a fatal error `[FATAL_LOCK] Cannot clean up while another SDLC pipeline is active.`
     2. Determine the current branch. If it is `master` or `main`, exit with an error (do not quarantine the main branch).
     3. Run `git add -A` to stage all modifications (respecting `.gitignore`).
     4. Run `git commit --allow-empty -m "WIP: 🚨 FORENSIC CRASH STATE"` to permanently lock the "crime scene" into Git history, preventing empty commit crashes.
     5. Calculate a timestamp natively in Python using `int(time.time())` (Do NOT use Bash string interpolation).
     6. Rename the current toxic branch using Python f-strings: `git branch -m {current_branch_name}_crashed_{timestamp}`.
     7. Run `git checkout master`.
     8. **Targeted Artifact Obliteration**: With the lock safely acquired or verified stale, use Python's native `os.remove()` to explicitly delete ephemeral daemon locks (`.coder_session`, `.sdlc_repo.lock`) if they exist. Do NOT use `git clean -fdx`.
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
By leveraging a global, defensive `try...finally` reaper, we guarantee that all subagent process groups are reaped regardless of the exit vector without causing secondary crashes. The `--cleanup` flag provides a hermetically sealed quarantine mechanism that strictly enforces `fcntl` concurrency checks before safely deleting stale locks and quarantining the toxic branch.

## Acceptance Criteria
- [ ] Subagents are launched via `Popen` with `start_new_session=True` and immediately `wait()`ed upon.
- [ ] The `finally` block successfully reaps all grandchild processes on ALL exit paths (including `sys.exit`) and uses `try/except OSError` to prevent secondary crashes.
- [ ] `--cleanup` explicitly checks `fcntl` locks to prevent destroying active pipelines.
- [ ] `--cleanup` creates a WIP commit, uses Python timestamps to rename the branch, checks out `master`, and safely targets ephemeral locks via `os.remove()`.
- [ ] `organization_governance.md` Section 4.2 is updated.