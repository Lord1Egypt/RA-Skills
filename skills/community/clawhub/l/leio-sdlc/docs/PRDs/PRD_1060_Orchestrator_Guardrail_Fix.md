# PRD 1060: Orchestrator Guardrail Fix & Anti-Reward Hacking Mechanism

## 1. Project & Context
- **Project:** leio-sdlc
- **Goal:** Fix Orchestrator Guardrail Issue (PRD 1060), avoid Git tracking for forensic data, enforce strict test repair, fix parameter mismatch bugs, and add debug tracing. 

## 2. Background & Architectural Decision
The SDLC Orchestrator recently encountered an infinite loop and pipeline failure. The root cause is that `scripts/orchestrator.py` forcefully runs `git add -f` to track the globally ignored `.sdlc_runs` folder. This pollutes the Git index and trips the Reviewer Guardrail.

We must keep `.sdlc_runs` entirely OUT of Git. Removing this explicit `git add` behavior will cause older test cases to fail, so they must be properly repaired without reward hacking.
When crashes occur, we must preserve forensic evidence by copying the state, but we must NOT use `os.rename` or `shutil.move` inside State 5 Tier 1 because the original directory must remain intact for the retry loop. We will use `shutil.copytree`. (Note: `os.rename` in the `--cleanup` block must be preserved).
Additionally, `merge_code.py` crashes because it receives an unsupported `--run-dir` parameter. This must be fixed. Lastly, tracing capabilities will be enhanced by adding a `--debug` mode to `orchestrator.py`. Auto-commit logic is strictly forbidden.

## 3. Requirements

### 3.1. Fix Git Tracking for `.sdlc_runs`
Remove explicit `git add` and `git commit` commands that are currently inside the State 5 Tier 1 fallback block targeting `.sdlc_runs` in `scripts/orchestrator.py`. Do not perform a blanket removal of git commands (e.g. leave git commands for PRD commit intact).

### 3.2. State 5 Forensic Crash Preservation
Use `shutil.copytree(src, dst, dirs_exist_ok=True)` ONLY in the State 5 error handling block (Tier 1 retry loop) to create a snapshot of the `.sdlc_runs/<PR_Name>` directory when a crash occurs. NEVER use `os.rename` or `shutil.move` in this specific block because the original directory MUST remain intact so the retry loop can still find the PR contract.
EXPLICIT MANDATE: The `os.rename` inside the `if args.cleanup:` block MUST remain completely intact. A blanket ban on `os.rename` is forbidden.

### 3.3. Test Repair
Update tests (e.g. `tests/test_pr_002_immutability.py`) to align with the removed git tracking without reward hacking.

### 3.4. Fix merge_code.py Parameter Mismatch
Remove the `--run-dir` argument from BOTH instances of the `merge_code.py` subprocess call in `scripts/orchestrator.py`.

### 3.5. Add --debug trace mode
Add a `--debug` CLI argument to `scripts/orchestrator.py`. When enabled, it outputs detailed trace logs for state transitions and subprocess calls. Default execution must remain silent.

## 4. Technical Specifications
- **Files Modified:**
  - `scripts/orchestrator.py`: 
    - Remove `git add`/`git commit` ONLY for the State 5 Tier 1 block targeting `.sdlc_runs`.
    - Update State 5 error handling to snapshot the local directory via `shutil.copytree(src, dst, dirs_exist_ok=True)`. Ensure `os.rename` or `shutil.move` are NOT used in Tier 1.
    - Preserve the `os.rename` logic inside the `--cleanup` block.
    - Remove `--run-dir` argument from BOTH `merge_code.py` calls.
    - Add `--debug` CLI argument and tracing logic.
    - (CRITICAL) Do NOT include any auto-commit logic anywhere in the approval blocks.
  - `tests/test_pr_002_immutability.py`, etc.: Update expectations and legitimately fix assertions.

## 5. Success Metrics
- Orchestrator completes PR flow without Guardrail violations regarding `.sdlc_runs`.
- Crashed runs successfully copy the local folder without deleting the original and without polluting git history.
- The quarantine feature (`--cleanup`) correctly uses `os.rename` and continues to function.
- Test suite passes with full assertions intact (no removed/disabled tests).
- `merge_code.py` executes successfully without crashing due to invalid arguments.
- Debug mode works correctly.
- No auto-commit behavior exists in the orchestration script.

## Appendix: Architecture Evolution Trace

**WARNING: The Planner is strictly forbidden from bringing this Appendix into SDLC execution or implementation tasks.**

**Documented Trade-offs & Decisions:**
- **Copy vs. Move for Crash Preservation:** We explicitly chose `shutil.copytree` instead of `os.rename` or `shutil.move` when handling State 5 crashes. While moving the directory might save a negligible amount of space, doing so destroys the original state directory required for the subsequent retry loop. Copying ensures forensic evidence is captured safely while keeping the retry flow intact.
- **Dropping Auto-Commit Logic:** We are actively forbidding any auto-commit logic inside the pipeline approval blocks. Attempting to auto-commit `.sdlc_runs` or other artifact states polluted git history and repeatedly caused pipeline Guardrail crashes. Requiring explicit state transitions without automated git manipulation is vastly safer.
- **Strict Git Ignorance:** Dropping the explicit `git add -f` for `.sdlc_runs` breaks older immutability tests. The trade-off is spending developer cycles repairing the test suite properly in exchange for a cleaner, untainted source repository index that no longer flags false positives in the Reviewer.
