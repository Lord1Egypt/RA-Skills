status: closed

# PR-001: Enforce Mandatory Workdir in Orchestrator CLI

## 1. Objective
Enforce explicit project selection by making the `--workdir` argument mandatory in `orchestrator.py` to prevent project context leakage.

## 2. Scope & Implementation Details
- `scripts/orchestrator.py`: Modify `argparse` configuration for `--workdir`. Remove `default="."` and add `required=True`. Add help text: "Absolute path to the target project workspace".
- `preflight.sh` (or `leio-sdlc/preflight.sh`): Update the orchestrator invocation to explicitly pass `--workdir "$(pwd)"`.

## 3. TDD & Acceptance Criteria
- `tests/test_orchestrator_cli.py`: Write a test that invokes `orchestrator.py` without `--workdir` and asserts it exits with a CLI usage error (SystemExit).
- `preflight.sh` must run successfully without CLI usage errors when triggered natively.


> [Escalation] Tier 1 Reset triggered due to Coder failure or Arbitrator rejection.
