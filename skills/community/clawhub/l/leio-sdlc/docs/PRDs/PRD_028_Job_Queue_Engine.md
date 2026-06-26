# PRD_028: SDLC Job Queue Engine (Deterministic State & CRUD)

## 1. Problem Statement
To support "Micro-Slicing" (breaking a single PRD into multiple PR contracts), the Manager agent needs to process a queue of tasks. Relying on the LLM to use bash commands (`ls`, `cat`, `sed`) to manage this queue is highly error-prone, leading to context hallucination and file corruption. We need a deterministic, script-based Job Queue Engine to handle the CRUD operations of PR states (`open`, `closed`, `blocked`) safely and provide LLM-friendly guardrails.

## 2. Solution: Deterministic Queue Scripts (In-Repo / GitOps Ready)
We will build two Python scripts that act as the "Hands" for queue management. They will operate on a specific Job Directory (`--job-dir` passed as an argument) containing PR contracts (Markdown files). This architecture supports the "In-Repo" (Option B) GitOps model, where the engine is stateless and operates directly inside the target business project's `.sdlc/jobs/<Feature_X>/` directory. Each PR contract must contain a `status: <state>` field in its header/content.

### 2.1 `scripts/get_next_pr.py`
- **Purpose**: Polls the job directory for the next available open PR.
- **Arguments**: `--job-dir <path_to_job_dir>` (Required)
- **Logic**:
  1. Guardrail: If `--job-dir` does not exist, print `[Pre-flight Failed] Job directory '{job_dir}' does not exist.` and exit 1.
  2. Scan all `*.md` files in the directory.
  3. Sort files alphabetically (e.g., `PR_001.md`, `PR_002.md`).
  4. Read files in order. The first file containing the string `status: open` is the winner.
  5. If found, print the relative path to the PR file and exit 0.
  6. If no open PRs are found, print `[QUEUE_EMPTY] All PRs in {job_dir} are closed or blocked.` and exit 0.

### 2.2 `scripts/update_pr_status.py`
- **Purpose**: Safely mutates the status of a specific PR contract.
- **Arguments**: `--pr-file <path_to_pr>` (Required), `--status <open|closed|blocked>` (Required)
- **Logic**:
  1. Guardrail: If `--status` is not one of the allowed choices, exit 1.
  2. Guardrail: If `--pr-file` does not exist, print `[Pre-flight Failed] Cannot update status. PR file '{pr_file}' not found.` and exit 1.
  3. Read the file content.
  4. Guardrail: If the file does not contain a line matching `status: <something>`, print `[Pre-flight Failed] File '{pr_file}' does not contain a 'status: ...' field.` and exit 1.
  5. Use string replacement or regex to update the status line to `status: {new_status}`.
  6. Write the updated content back to the file.
  7. Print `[STATUS_UPDATED] {pr_file} is now {new_status}.` and exit 0.

## 3. Testing Strategy (TDD Approach)
We will follow Test-Driven Development. We will create a bash test script first, which will fail until the Python scripts are correctly implemented.

**Test Script**: `scripts/test_job_queue_engine.sh`
- **Setup**: Create an isolated sandbox directory (`tests/e2e_job_queue_XXXX`). Create a dummy `--job-dir`.
- **Test 1 (Negative - get_next_pr)**: Run `get_next_pr.py` on a missing dir. Assert exit code 1 and exact `[Pre-flight Failed]` message.
- **Test 2 (Negative - update_status)**: Run `update_pr_status.py` on a missing file. Assert exit code 1 and exact message.
- **Test 3 (Negative - update_status)**: Run `update_pr_status.py` on a file without a status field. Assert exit code 1 and exact message.
- **Test 4 (Positive Flow)**:
  - Create `01_DB.md` with `status: closed`.
  - Create `02_API.md` with `status: open`.
  - Create `03_UI.md` with `status: open`.
  - Run `get_next_pr.py`. Assert output is `02_API.md`.
  - Run `update_pr_status.py --pr-file 02_API.md --status closed`. Assert output `[STATUS_UPDATED]`.
  - Run `get_next_pr.py`. Assert output is `03_UI.md`.
  - Run `update_pr_status.py --pr-file 03_UI.md --status closed`. Assert output `[STATUS_UPDATED]`.
  - Run `get_next_pr.py`. Assert output is `[QUEUE_EMPTY]`.
- **Teardown**: Cleanup sandbox.

## 4. Acceptance Criteria
- [ ] TDD script `test_job_queue_engine.sh` perfectly validates the positive queue flow and all negative guardrails.
- [ ] `get_next_pr.py` implements alphabetical sorting and `[QUEUE_EMPTY]` logic.
- [ ] `update_pr_status.py` safely mutates file states without corrupting markdown content.
- [ ] Both Python scripts include LLM-friendly `[Pre-flight Failed]` error messages on failure.