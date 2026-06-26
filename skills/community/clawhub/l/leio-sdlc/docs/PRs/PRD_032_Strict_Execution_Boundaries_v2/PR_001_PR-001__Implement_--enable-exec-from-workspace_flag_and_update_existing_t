status: closed

# PR-001: Implement `--enable-exec-from-workspace` flag and update existing tests

## 1. Objective
Add the `--enable-exec-from-workspace` CLI flag to `scripts/orchestrator.py` without yet enforcing the runtime boundary, and update all existing test scripts and preflight execution paths to include this flag. This prevents breaking CI when the strict boundary is enforced in the next PR.

## 2. Scope & Implementation Details
- Update `scripts/orchestrator.py` to parse the new `--enable-exec-from-workspace` boolean flag using `argparse`.
- Do not yet implement the path validation logic (this will be done in PR-002).
- Update `tests/test_runtime_boundary_allowed.sh` to execute `python3 scripts/orchestrator.py --enable-exec-from-workspace` and ensure it runs without failing due to unrecognized arguments.
- Update any other test scripts or preflight pipelines that execute `scripts/orchestrator.py` to pass the `--enable-exec-from-workspace` flag.

## 3. TDD & Acceptance Criteria
- [ ] `scripts/orchestrator.py` accepts `--enable-exec-from-workspace` without throwing an error.
- [ ] `tests/test_runtime_boundary_allowed.sh` is created and passes.
- [ ] All existing preflight tests continue to pass.