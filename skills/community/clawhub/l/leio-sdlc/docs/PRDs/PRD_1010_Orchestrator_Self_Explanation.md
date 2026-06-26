# PRD-1010: Orchestrator Self-Explanation & Manager Handoff Matrix

## 1. Problem Statement
The Orchestrator (`orchestrator.py`) currently acts like an isolated script rather than a cooperative Agent. When it finishes its tasks (successfully or after a failure), it quietly exits. This breaks the CI/CD pipeline because the "Manager Agent" (the LLM overseeing the SDLC) does not receive a clear "Prompt" indicating what to do next. We need to implement the "Tool-as-Prompt" pattern, forcing the Orchestrator to emit strict, self-documenting instructions upon exit.

## 2. Parameter Hardening (CLI)
The CLI arguments must be explicit to remove ambiguity and prevent infinite runaway loops.
1. **`--workdir`**: Must be `required=True`.
2. **`--prd-file`**: Must be `required=True`.
3. **`--max-prs-to-process`**: Must be `required=True` (renamed from `--max-runs`).
   - Add `help="Maximum number of PRs to process in this run. Acts as a safety circuit breaker against runaway agent loops. Recommended value: 50."`
4. **`--coder-session-strategy`**: Must be `required=True` (`choices=["per-pr", "always", "on-escalation"]`).
   - Add `help="Coder session reset strategy. Recommended: 'on-escalation'."`
5. **Deprecated Parameters**: Remove `--job-dir`, `--notify-channel`, and `--notify-target` from `argparse`.
   - The notification channel logic should fetch from `os.environ.get("OPENCLAW_SESSION_KEY")` or `os.environ.get("OPENCLAW_CHANNEL_ID")`.

## 3. Exit Points & Handoff Matrix
The Orchestrator must intercept the 5 major exit conditions and print standardized `[ACTION_REQUIRED_FOR_MANAGER]` blocks to `stdout` before calling `sys.exit()`.

### 3.1 Happy Path (Success)
- **Condition**: Queue is empty; all `.md` files in the job dir are `status: closed` or `completed`.
- **Output Standard**: `[SUCCESS_HANDOFF]` + Instructions to update PRD/Issue and STATE.md.

### 3.2 Startup Fatal: Dirty Workspace
- **Condition**: `git status --porcelain` is not empty at startup.
- **Output Standard**: `[FATAL_STARTUP]` + Instructions to `git commit/stash`.

### 3.3 Startup Fatal: Planner Failure
- **Condition**: Planner returns 0 files after State 0 slicing.
- **Output Standard**: `[FATAL_PLANNER]` + Instructions to read planner logs and refine the PRD.

### 3.4 Runtime Fatal: Branch Checkout Error
- **Condition**: `git checkout` fails (e.g., locking issues).
- **Output Standard**: `[FATAL_GIT]` + Instructions to run `git branch -D` and `git clean -fd`.

### 3.5 Runtime Fatal: Dead End (Tier 3 Escalation)
- **Condition**: Rejection count hits the limit (e.g., 5).
- **Output Standard**: `[FATAL_ESCALATION]` + Instructions to read `Review_Report.md` and alert the Boss explicitly.

## 4. TDD / Acceptance Criteria
The Coder must write unit/integration tests in `scripts/test_orchestrator_fsm.sh` to validate the new CLI arguments and the exact string outputs for all 5 exit points.
- **AC 1**: Running `orchestrator.py` without `--max-prs-to-process` throws a native `argparse` missing argument error.
- **AC 2**: The `test_orchestrator_fsm.sh` validates that a clean exit (no more PRs) outputs the exact `[SUCCESS_HANDOFF]` block.
- **AC 3**: The sandbox test for "Dirty Workspace" outputs the exact `[FATAL_STARTUP]` block.
