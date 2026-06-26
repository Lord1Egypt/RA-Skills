status: closed

# PR-002: Integrate defensive force commit before State 4

## 1. Objective
Integrate the force-commit helper into the orchestrator's state machine to ensure no dirty files crash the pipeline or evade the Reviewer's audit.

## 2. Scope & Implementation Details
- **File:** `scripts/orchestrator.py`
- Locate the transition logic from State 3 (Coder) to State 4 (Reviewer).
- Invoke `force_commit_untracked_changes()` immediately before the mock or real Reviewer is spawned.

## 3. TDD & Acceptance Criteria
- **File:** `tests/test_076_e2e_force_commit.sh`
- Write an end-to-end integration test that simulates the orchestrator pipeline. Inject an untracked file after State 3, run the transition, and verify that the file is committed before State 4 starts.
