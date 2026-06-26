# PRD_074: Fix Orchestrator Review Report Path via Dependency Injection

## 1. Problem Statement
The Orchestrator (`scripts/orchestrator.py`) suffers from a critical "Information Silo" bug. After running the Reviewer (State 4), it expects the verdict in a hardcoded legacy file (`review_report.txt`). However, the Reviewer (`scripts/spawn_reviewer.py`) is hardcoded to write its verdict to `Review_Report.md`. 
Because the Orchestrator never finds the verdict it's looking for, it always assumes an "Invalid Reviewer output". This forces the pipeline into an infinite loop of Tier 1 resets and Tier 2 micro-slicing, ultimately crashing the system.

## 2. Solution (Dependency Injection)
The Orchestrator MUST be the Single Source of Truth for the review report file path.
1. **Parameterize the Reviewer**: Modify `scripts/spawn_reviewer.py` to accept a new argument `--out-file <path>`. It must inject this exact path into the prompt so the AI Reviewer writes its evaluation there (instead of hardcoding `Review_Report.md`).
2. **Orchestrator Injection**: Modify `scripts/orchestrator.py`. In State 4, it MUST pass a desired artifact path (e.g., `Review_Report.md`) to the Reviewer via the `--out-file` argument. The Orchestrator must then read the verdict from this exact path.
3. **Stale File Cleanup**: Before spawning the Reviewer (State 4), the Orchestrator MUST proactively delete the artifact file at this path (handling `FileNotFoundError` securely) to ensure a clean slate and prevent reading a stale `[LGTM]` from a previous run.

## 3. Scope
- **Target Project:** `/root/.openclaw/workspace/projects/leio-sdlc`
- **Files to Modify:**
  - `scripts/orchestrator.py`
  - `scripts/spawn_reviewer.py`

## 4. Testing Strategy
- **Autonomous Test Strategy**: Update `tests/test_071_reviewer_history_scope.sh` or create a new mock test to verify that `spawn_reviewer.py` accepts `--out-file` and writes to the correct injected path, and that `orchestrator.py` successfully reads from it after cleaning up stale files.
- **TDD Guardrail**: The implementation and its failing test MUST be delivered in the same PR contract.
