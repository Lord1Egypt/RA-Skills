# PRD_044: Strict Git Branch Isolation Guardrail for Coder

## 1. Problem Statement
The SDLC pipeline relies on a Trio Model (Planner -> Coder -> Reviewer). The intended workflow mandates that the Coder operates on an isolated feature branch, submits code for review, and the Manager merges it via `merge_code.py` ONLY after a `[LGTM]` review. 
Currently, `scripts/spawn_coder.py` lacks branch awareness. If invoked on the `master` or `main` branch, the Coder writes and commits directly to the production timeline, bypassing the Reviewer entirely and risking catastrophic repository corruption.

## 2. Solution
Implement a strict branch isolation guardrail inside `scripts/spawn_coder.py`. The script must physically refuse to spawn the Coder if the current Git branch is `master` or `main`.

### 2.1 Implementation Details
1. **Branch Detection**: In `scripts/spawn_coder.py`, use Python's `subprocess` to execute `git rev-parse --abbrev-ref HEAD` within the locked `--workdir`.
2. **Fail-Fast with AI-Actionable Error**: If the branch is `master` or `main`, the script MUST `sys.exit(1)`.
3. **Self-Explanatory AI Output**: To ensure the autonomous Manager Agent can self-correct, the error message printed to `stderr` must be highly prescriptive:
   `[FATAL] Branch Isolation Guardrail: Coder agent cannot be spawned on the 'master' or 'main' branch.`
   `[ACTION REQUIRED]: You must create and checkout a new feature branch before assigning work to the Coder.`
   `Fix this by executing: git checkout -b feature/<pr_name>`

## 3. Testing Strategy (TDD)
Create a new test script: `scripts/test_branch_isolation.sh`.

- **Scenario 1: Rejection on Master**
  - Save current branch state. Ensure the workspace is on `master`.
  - Attempt to run `spawn_coder.py --workdir $(pwd) --pr-file dummy.md --prd-file dummy.md`.
  - **Assert**: Exit code is `1`.
  - **Assert**: Output contains the exact string `[ACTION REQUIRED]: You must create and checkout a new feature branch`.
- **Scenario 2: Acceptance on Feature Branch**
  - Execute `git checkout -b test_isolation_dummy_branch`.
  - Run `spawn_coder.py` in mock mode (`SDLC_TEST_MODE=true`).
  - **Assert**: Exit code is `0`.
  - **Assert**: Output contains `{"status": "mock_success", "role": "coder"}`.
  - Cleanup: Checkout the original branch and delete the dummy branch.
- **Preflight Integration**: Hook `test_branch_isolation.sh` into `preflight.sh` to ensure it runs on every build.

## 4. Acceptance Criteria
- [ ] `spawn_coder.py` actively blocks execution on `master` and `main`.
- [ ] The error message provides an exact shell command for the AI to fix the issue (`git checkout -b ...`).
- [ ] `scripts/test_branch_isolation.sh` covers both negative and positive branch states.
- [ ] `./preflight.sh` runs successfully.