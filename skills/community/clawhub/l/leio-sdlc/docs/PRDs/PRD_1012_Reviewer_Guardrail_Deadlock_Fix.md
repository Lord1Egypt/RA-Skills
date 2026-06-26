# PRD-1012: Reviewer Guardrail Deadlock and Empty Diff Vulnerability Fix

## 1. Metadata
- **ID**: ISSUE-1012
- **Title**: Refactor Reviewer Guardrail and Diff Generation Logic to Prevent Deadlocks and Reward Hacking
- **Project**: leio-sdlc
- **Target Path**: `/root/.openclaw/workspace/projects/leio-sdlc`
- **Status**: Open
- **Type**: Bugfix / Security
- **Priority**: Critical
- **Date**: 2026-03-23

## 2. Problem Statement
A system-level contradiction exists between the Orchestrator's mandatory commit enforcement and the Reviewer's blind diff mechanism, leading to a Historical Guardrail Deadlock.
1. The Orchestrator forces the Coder to `git commit` all changes before review.
2. The Reviewer preflight script (`scripts/spawn_reviewer.py`) erroneously uses `git diff HEAD` to check for uncommitted changes. Since the workspace is forced clean, it returns empty, generating a synthetic `[EMPTY DIFF]`, hiding all actual code.
3. Previous band-aids provided `recent_history.diff` to the LLM and blindly fed it into the Python `check_guardrails` scanner.
4. Any legitimate historical modification to a protected framework file merged into `master` remains in `recent_history.diff`. The scanner reads this history, misinterprets it as a current unauthorized tamper, and permanently kills all subsequent PRs.

## 3. Scope & Solution
**Target File:** `/root/.openclaw/workspace/projects/leio-sdlc/scripts/spawn_reviewer.py`

**Fix 1: Restore True Diff Visibility (Remove Empty Diff Illusion)**
- **Remove** the `if not diff_out:` block that checks `git diff HEAD`.
- **Implement Unconditional Diff**: `subprocess.run(f"git diff {args.diff_target} --no-color > {diff_file}", shell=True)`
- This extracts the true accumulative diff against `master`, regardless of whether changes are committed.

**Fix 2: Break the Guardrail Historical Deadlock**
- **From**: `check_guardrails(..., [diff_file, "recent_history.diff"])`
- **To**: `check_guardrails(..., [diff_file])`
- The Python security scanner must only audit the current accumulative diff, ignoring history. The LLM will still receive `recent_history.diff` for "over-delivery" evaluations.

## 4. Autonomous Test Strategy
The Coder MUST autonomously implement the following Bash E2E/Integration tests (e.g., in `tests/test_1012_reviewer_guardrail_deadlock.sh` or similar):
1. **Committed Changes Visibility Test**: Ensure that if a Coder commits changes locally, `spawn_reviewer.py` correctly captures the committed changes in `current_review.diff` and does NOT output `[EMPTY DIFF]`.
2. **Historical Immunity Test**: Modify a protected file on `master`, commit it, then run `spawn_reviewer.py` on a feature branch with benign changes. Assert that `check_guardrails` does NOT fail.
3. **Active Tamper Test (Baseline Defense)**: Maliciously modify a protected file on a feature branch (without PR authorization) and commit it. Assert that `spawn_reviewer.py` successfully detects the tamper and kills the process.

## 5. TDD Guardrail
The implementation and its failing tests MUST be delivered in the same PR contract. No logic changes can be merged without the accompanying green tests.
