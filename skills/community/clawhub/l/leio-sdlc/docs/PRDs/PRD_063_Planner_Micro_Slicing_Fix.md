# PRD-063: Planner Micro-Slicing Logic (Tier 2 Escalation Fix)

## 1. Problem Statement
The Orchestrator's Tier 2 Escalation protocol is designed to rescue a failing PR by breaking it down into smaller, more manageable micro-PRs using `scripts/spawn_planner.py`. However, `spawn_planner.py` currently throws an `unrecognized arguments: --slice-failed-pr` error because the micro-slicing functionality was never implemented. This fatally halts the entire self-healing State Machine when a Coder agent encounters an overly complex task.

## 2. Critical User Journeys (CUJs)
This fix must support and elegantly handle the following scenarios to achieve full TDD coverage without invoking real LLMs during tests:

- **CUJ 1: Standard PRD Planning (Regression/Happy Path)**
  - *User Action*: Runs `spawn_planner.py --prd-file PRD.md` (without `--slice-failed-pr`).
  - *System Response*: Planner behaves exactly as it did before, generating micro-PRs for the entire project.
- **CUJ 2: Micro-Slicing a Failed PR (Mock Mode / Valid File)**
  - *User Action*: Orchestrator runs `spawn_planner.py --prd-file PRD.md --slice-failed-pr docs/PRs/Failed_PR.md` in test mode (`SDLC_TEST_MODE=true`).
  - *System Response*: The script reads the failed PR, outputs a mock success response, and generates at least two smaller mock PRs in the output directory.
- **CUJ 3: Missing or Empty Failed PR File (Graceful Halt)**
  - *User Action*: Orchestrator runs `spawn_planner.py --slice-failed-pr does_not_exist.md`.
  - *System Response*: Script detects the file is missing or empty, prints a clear error message, and gracefully exits with code `1`.
- **CUJ 4: Micro-Slicing a Failed PR (Real LLM Execution - Architecture Only)**
  - *User Action*: Orchestrator runs `spawn_planner.py --slice-failed-pr Failed_PR.md` in real execution mode.
  - *System Response*: The script successfully constructs a distinct LLM prompt instructing the AI to slice the specific `Failed_PR.md` into smaller pieces, using `PRD.md` only for context.

## 3. Functional Requirements

### 3.1 CLI Argument Expansion
- Update `argparse` in `scripts/spawn_planner.py` to include `--slice-failed-pr` (optional, default: `None`).

### 3.2 Pre-flight Validation
- If `--slice-failed-pr` is provided:
  - Check if the file exists and its size is `> 0`.
  - If not, print `[Pre-flight Failed] Planner cannot start. Failed PR file not found or empty at '<PATH>'.` and `sys.exit(1)`.
  - Read the contents of the failed PR into a variable (e.g., `failed_pr_content`).

### 3.3 Prompt & Logic Routing
- **Test Mode (`SDLC_TEST_MODE=true`)**:
  - If `--slice-failed-pr` is present, log the call and generate two mock files (`PR_Slice_1.md`, `PR_Slice_2.md`) containing `status: open\n`. Exit `0`.
- **Real Mode**:
  - If `--slice-failed-pr` is `None`: Retain the existing `task_string` (global project slicing).
  - If `--slice-failed-pr` is provided: Override the `task_string`. The prompt must explicitly state:
    > "The following PR has failed multiple times because it is too complex for the Coder. Your task is to break THIS SPECIFIC PR down into at least 2 smaller, sequential Micro-PRs. Do not change the overall goal of the project, just reduce the scope per PR. Use the original PRD for context.\n\nFAILED PR:\n{failed_pr_content}\n\nORIGINAL PRD:\n{prd_content}"
  - Ensure the prompt still mandates the use of `create_pr_contract.py` and `status: open`.

## 4. Testing Strategy (TDD)
A new hermetic test script `scripts/test_planner_slice_failed_pr.sh` must be created.
It must use `setup_sandbox` and set `export SDLC_TEST_MODE=true`.

- **Test Scenario 1 (Regression)**: Run planner normally. Assert mock files (e.g., `PR_A.md`, `PR_B.md`) are created.
- **Test Scenario 2 (File Missing)**: Run with `--slice-failed-pr fake.md`. Assert exit code is `1` and error string matches `[Pre-flight Failed]`.
- **Test Scenario 3 (Successful Slice)**: Create a valid `Failed_PR.md`. Run with `--slice-failed-pr Failed_PR.md`. Assert the script exits `0` and generates mock slice files (e.g., `PR_Slice_1.md`, `PR_Slice_2.md`).

Update `scripts/run_sdlc_tests.sh` (or `preflight.sh`) to include `./scripts/test_planner_slice_failed_pr.sh`.

## 5. Acceptance Criteria
- [ ] `scripts/spawn_planner.py` parses `--slice-failed-pr` without throwing `unrecognized arguments`.
- [ ] Invalid/missing failed PR files are caught before hitting the LLM.
- [ ] `scripts/test_planner_slice_failed_pr.sh` is fully implemented and covers all CUJs using deterministic test modes.
- [ ] Running `./preflight.sh` successfully executes the new test suite and exits with `✅ PREFLIGHT SUCCESS`.