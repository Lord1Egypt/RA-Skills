status: closed

# PR-002: Implement Runtime Boundary Enforcement

## 1. Objective
Enforce the strict execution boundary by checking `__file__` inside `scripts/orchestrator.py` to prevent execution directly from the development workspace without explicit authorization.

## 2. Scope & Implementation Details
- Inject a path validation check into `scripts/orchestrator.py`. If the script's `__file__` path starts with `/root/.openclaw/workspace/projects/`, immediately `sys.exit(1)`.
- Bypass this validation check if `--enable-exec-from-workspace` is provided.
- The error message upon exit must be: `[FATAL] Security Violation: Unless for testing purposes, skills must be executed from the ~/.openclaw/skills/ runtime directory. If you are intentionally running from source for testing, you must explicitly add the parameter: --enable-exec-from-workspace`
- Add `tests/test_runtime_boundary_blocked.sh` to execute the script from the workspace without the flag and assert that the script exits with code 1 and prints the specified fatal error message.

## 3. TDD & Acceptance Criteria
- [ ] Running `python3 scripts/orchestrator.py` directly from the workspace without the flag causes a non-zero exit status and displays the exact actionable error.
- [ ] Running the same command with the flag successfully bypasses the path validation check.
- [ ] The implementation does not break any existing preflight tests.