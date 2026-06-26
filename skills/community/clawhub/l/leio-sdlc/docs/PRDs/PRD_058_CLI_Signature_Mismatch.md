# PRD-058: Fix Sub-agent CLI Signature Mismatch in Orchestrator

## 1. Problem Statement
The `scripts/orchestrator.py` engine immediately crashes upon picking up a PR because it invokes `spawn_coder.py` and `spawn_planner.py` with outdated CLI arguments (`--repo-dir`). Furthermore, recent security refactors (the Triple Lock CWD Guardrail) mandated that `spawn_coder.py` requires both `--workdir` and `--prd-file` to run, which the Orchestrator currently fails to provide.

This mismatch causes a fatal `EOFError` / `sys.exit` loop when the Orchestrator attempts to spawn agents.

## 2. Objectives
Update `scripts/orchestrator.py` to seamlessly pass the correct, up-to-date arguments to all sub-agent scripts. 

## 3. Requirements

### 3.1 Orchestrator Argument Expansion
To satisfy the sub-agents' requirements for a PRD context, `scripts/orchestrator.py` must be updated to accept a `--prd-file` argument itself.
- Add `--prd-file` (required) to `orchestrator.py`'s `argparse`.

### 3.2 Subprocess Invocation Fixes
Update the `subprocess.run` arrays inside `scripts/orchestrator.py` for all states:
- **State 3 (Coder)**:
  - Remove `--repo-dir`.
  - Add `--workdir` `<workdir>`.
  - Add `--prd-file` `<args.prd_file>`.
  - Keep `--pr-file` `<current_pr>`.
- **State 4 (Reviewer)**:
  - Remove `--repo-dir` (if present).
  - Add `--workdir` `<workdir>`.
  - Keep `--pr-file` `<current_pr>`.
- **State 4 (Arbitrator)**:
  - Ensure `--workdir` and `--pr-file` are passed correctly.
- **State 5 (Planner - Tier 2 Slicing)**:
  - Remove `--repo-dir`.
  - Add `--workdir` `<workdir>`.
  - Ensure `--prd-file` is passed (using the failing PR as the PRD, or the original PRD file). Note: `spawn_planner.py --slice-failed-pr` expects the failing PR to be passed to `--prd-file` according to its current signature, or check how Tier 2 invokes it. Currently, Tier 2 in Orchestrator does: `"--slice-failed-pr", current_pr`. We must also add `--prd-file args.prd_file` and `--workdir workdir`.

### 3.3 Test Sandbox Alignment
The existing deterministic sandbox test (`scripts/test_orchestrator_fsm.sh`) invokes `orchestrator.py` without `--prd-file`. 
- Update the test script to pass `--prd-file dummy_prd.md` when calling `orchestrator.py`.
- Update the mock stub scripts (fake `spawn_coder.py`, etc.) within the test to gracefully accept/ignore these new parameters so the assertions don't break.

## 4. Acceptance Criteria (TDD Scenarios)
The `scripts/test_orchestrator_fsm.sh` MUST be updated to verify that the Orchestrator passes the correct arguments to its sub-agents.

- **Scenario: Coder Invocation Signature (State 3)**
  - **Stub Update**: The mock `spawn_coder.py` must explicitly assert that `--workdir` and `--prd-file` are provided in `sys.argv`. If missing, it must `sys.exit(1)` and print a specific failure string (e.g., "FATAL: Coder missing mandatory args").
  - **Assertion**: The Orchestrator's Green Path test must succeed without this fatal string appearing in the output.

- **Scenario: Planner Invocation Signature (State 5 - Tier 2)**
  - **Stub Update**: The mock `spawn_planner.py` must explicitly assert that `--workdir` and `--prd-file` are provided when invoked with `--slice-failed-pr`.
  - **Assertion**: The Orchestrator's Red Path Slice test must succeed without the Planner stub crashing due to missing arguments.

- **Scenario: Reviewer & Arbitrator Invocation Signature (State 4)**
  - **Stub Update**: The mock `spawn_reviewer.py` and `spawn_arbitrator.py` must assert the presence of `--workdir` and `--pr-file`.
  - **Assertion**: The Orchestrator's Red Path Override test must complete successfully.

- [ ] Running `./preflight.sh` completes with `✅ PREFLIGHT SUCCESS`.

