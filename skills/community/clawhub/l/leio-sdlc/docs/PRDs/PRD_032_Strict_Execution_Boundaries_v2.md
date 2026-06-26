# PRD: Strict Execution Boundaries & Guardrails v2 (PRD-032)

## Context
To prevent operational paradoxes and enforce a strict separation between the development workspace and the production runtime, we must implement a guardrail that blocks the execution of AgentSkill scripts directly from their source directory. This measure addresses the core requirement of ISSUE-1026 while decoupling it from the more complex (and now manually handled) identity/governance modifications. Execution from the workspace should only be possible for explicit testing purposes.

## Requirements
1. **Runtime Execution Boundary (ISSUE-1026)**:
   - Inject a path validation check into the main entry point of the `leio-sdlc` orchestrator script (`scripts/orchestrator.py`).
   - The script must evaluate its own execution path (`__file__`). If the path is found to be within `/root/.openclaw/workspace/projects/`, the script MUST immediately `sys.exit(1)`.
   - **Exception/Test Flag**: A new CLI parameter, `--enable-exec-from-workspace`, must be introduced, defaulting to `False`. The path validation check is bypassed if this flag is explicitly provided.
   - **Actionable Error Message**: The error message upon exit must be clear and self-explanatory: `[FATAL] Security Violation: Unless for testing purposes, skills must be executed from the ~/.openclaw/skills/ runtime directory. If you are intentionally running from source for testing, you must explicitly add the parameter: --enable-exec-from-workspace`

## Architecture
- **Python Guardrail Logic**: `scripts/orchestrator.py` will be modified to use the `argparse` module to support the new `--enable-exec-from-workspace` flag. The `__file__` path check will be implemented at the start of the main execution block.

## Framework Modifications
To implement this guardrail, the Coder is explicitly authorized to modify the following protected framework file:
- `scripts/orchestrator.py`

## Test Strategy
- **Test Case 1 (Block)**: A new test script (`tests/test_runtime_boundary_blocked.sh`) will be created. It will execute `python3 scripts/orchestrator.py` from the workspace *without* the flag and assert that the script exits with code 1 and prints the specified fatal error message.
- **Test Case 2 (Allow)**: A new test script (`tests/test_runtime_boundary_allowed.sh`) will be created. It will execute `python3 scripts/orchestrator.py --enable-exec-from-workspace` from the workspace and assert that the script bypasses the path check (it may fail later due to other missing arguments, but not because of the boundary guardrail).

## Acceptance Criteria
- [ ] Running `python3 scripts/orchestrator.py` directly from the `leio-sdlc` workspace without the flag causes the process to exit with a non-zero status and display the specified actionable error.
- [ ] Running the same command with the `--enable-exec-from-workspace` flag successfully bypasses the path validation check.
- [ ] The implementation does not break any existing preflight tests.