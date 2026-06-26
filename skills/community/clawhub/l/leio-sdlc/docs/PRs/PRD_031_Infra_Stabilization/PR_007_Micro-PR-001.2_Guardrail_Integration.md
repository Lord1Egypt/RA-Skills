# Micro-PR-001.2: Orchestrator Git Guardrail Integration

## 1. Objective
Integrate the Git validation utility into the SDLC Orchestrator's startup sequence to ensure it only processes clean, committed PRD files.

## 2. Scope & Implementation Details
- Update the Orchestrator startup logic (e.g., in `scripts/orchestrator.py`) to call the Git validation utility created in the previous PR.
- The Orchestrator MUST pass the PRD file path to the validator during startup.
- If the validation fails (file is untracked or has uncommitted modifications), the Orchestrator should cleanly exit and output an informative error message.
- Ensure the error message clearly states why the execution was halted.

## 3. TDD & Acceptance Criteria
- Integration tests (e.g., in `scripts/test_orchestrator_cli.py`) must verify that starting the Orchestrator with an untracked or modified PRD results in a validation failure and process exit.
- Integration tests must verify that providing a committed, clean PRD allows the Orchestrator process to continue its normal startup sequence.
- All tests must pass (GREEN).