# PRD: ISSUE-1066 Orchestrator State Contamination Fix

## Problem
The Orchestrator's `--force-replan` flag is currently optional and defaults to false (resume mode). This causes state contamination when a PRD is re-executed after updates or reverts, because the system silently resumes the old, outdated PR contracts instead of starting fresh.

## Solution
Make `--force-replan` a REQUIRED choice ("true" or "false") via string inputs to force the user/agent to explicitly declare whether they are resuming an existing PRD execution or starting a fresh execution.

## Detailed Requirements

### 1. Modify Argparse for `--force-replan`
In `scripts/orchestrator.py`, update the `parser.add_argument("--force-replan", ...)` definition:
- Remove `action="store_true"`.
- Add `choices=["true", "false"]`.
- Set `default=None`.
- Set the `help` text EXACTLY to the following Chinese string:
  "只有明确的知道是要继续同一个prd的执行，保留原有的pr，继续完成未完成的pr，才把force-replan设成false。如果明确的是要重新执行一个prd，比如在prd更新之后，或者在prd的sdlc执行已经被明确的完全revert之后，就应该把force-replan设成true。如果不确定应该是true还是false，应该停下来征求boss的意见。"

### 2. Conditional Requirement Enforcement
In `scripts/orchestrator.py`:
- Immediately after parsing args (`args = parser.parse_args()`) and immediately after processing the `--cleanup` early exit block, manually check if `args.force_replan` is `None`.
- Allow the check to bypass if `--test-sleep` is set.
- This validation MUST occur BEFORE any state-mutating actions (like `validate_prd_is_committed`, `initialize_sandbox`, or `acquire_global_locks`).
- If `args.force_replan` is `None`, perform the following steps:
  1. Print a `[FATAL]` error explaining it is required.
  2. Include a call to `print(HandoffPrompter.get_prompt("startup_validation_failed"))` to adhere strictly to the Silent Death Violation rule.
  3. Call `sys.exit(1)`.
- Before passing `args.force_replan` to the State 0 block, convert the string "true" to boolean `True` and "false" to boolean `False`.

### 3. Targeted Update of Command Invocations
Update all execution references to match the new required argument:
- Search ALL files in `scripts/`, `tests/`, `TEMPLATES/`, and `skills/` for any command-line invocation of `orchestrator.py` (e.g., `python3 scripts/orchestrator.py --prd-file ...`).
- Also search for Python unit tests that patch `sys.argv` (e.g., `@patch('sys.argv', ['orchestrator.py', ...])`).
- **For shell scripts:** Append `--force-replan true` (or `false` if specifically testing resuming). If `--force-replan` already exists, replace the flag and its value instead of duplicating it.
- **For Python tests:** Add `"--force-replan", "true"` to the mock `sys.argv` list. If it already exists, replace it.
- **CRITICAL GUARDRAIL:** Do NOT use global search-and-replace. Selectively update only the actual invocations.
- **ABSOLUTE REDLINE:** You must NEVER modify files within the `.sdlc_runs/` or `.test_tmp/` directories.

## Mandatory File I/O Policy
All agents MUST use the native `read`, `write`, and `edit` tool APIs for all file operations whenever possible. NEVER use shell commands (e.g., `exec` with `echo`, `cat`, `sed`, `awk`) to read, create, or modify file contents. This is a strict, non-negotiable requirement to prevent escaping errors, syntax corruption, and context pollution.