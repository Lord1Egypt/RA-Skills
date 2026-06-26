# PRD_074: Fix Orchestrator Review Report Path and Security Bypass Bug

## 1. Problem Statement
The Orchestrator (`scripts/orchestrator.py`) has a critical logic flaw where it expects the Reviewer to output its verdict to an outdated, hardcoded file path (`review_report.txt`), while the Reviewer (`scripts/spawn_reviewer.py`) is hardcoded to output to `Review_Report.md`. This architectural disconnect (an "Information Silo") causes the Orchestrator to always read an empty or stale file, falsely triggering an "Invalid Reviewer output" escalation and an infinite loop of pipeline failures.

## 2. Solution (The Architectural Fix)
Instead of just fixing the hardcoded string, the Orchestrator MUST be the single source of truth for the artifact path, passing it down to the Reviewer explicitly as an argument.

1. **Parameterize the Reviewer**: 
   - Modify `scripts/spawn_reviewer.py` to accept a new argument `--out-file <path>`. The script must use this path (instead of hardcoding `Review_Report.md`) when prompting the AI agent to write its evaluation.
2. **Orchestrator Injection**:
   - Modify `scripts/orchestrator.py`. When spawning the Reviewer (State 4), it MUST pass the desired artifact path (e.g., `Review_Report.md`) via the `--out-file` argument.
   - The Orchestrator must then read the verdict from this exact same path.
3. **Stale File Cleanup**:
   - Before spawning the Reviewer, the Orchestrator MUST proactively delete the artifact file at this path (handling `FileNotFoundError` securely) to prevent reading a stale `[LGTM]` from a previous run.

## 3. Scope
- Target project absolute directory: `/root/.openclaw/workspace/projects/leio-sdlc`
- Files Affected:
  - `scripts/orchestrator.py`
  - `scripts/spawn_reviewer.py`

## 4. Testing Strategy
- Create/update a test script (e.g., `tests/test_074_review_report_path.sh`) to verify that the Orchestrator correctly passes the `--out-file` argument, and that the Orchestrator successfully reads the `[LGTM]` or `[ACTION_REQUIRED]` verdict from the specified file.
- TDD Guardrail: The implementation and its failing test MUST be delivered in the same PR contract.
