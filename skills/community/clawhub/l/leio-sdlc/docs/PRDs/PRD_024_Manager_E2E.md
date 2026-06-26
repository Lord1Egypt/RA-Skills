# PRD_024: Full Lifecycle Orchestration E2E Test (Manager Auto-Pilot)

## 1. Problem Statement
The current Triad tests (ISSUE-023) verify that sub-agents correctly respond to well-formed prompts and file states. However, the overarching state machine—the Manager (i.e., the main agent orchestrating the SDLC pipeline)—remains untested. We need a system-level Integration Test to ensure the Manager can successfully string together PRD creation -> Planning -> Coding -> Reviewing -> Merging without human intervention or breaking down.

## 2. Goals
- Develop an isolated E2E testing sandbox (`tests/e2e_sandbox/`).
- Force a test instance of the Manager agent into an "Auto-Pilot" mode.
- The Manager must execute the entire 5-Layer QA funnel autonomously to create a simple "Hello World" Python script.
- Assert the final Git branch merge and physical code creation.

## 3. Implementation Plan
### 3.1 Sandbox Initialization (`scripts/test_manager_e2e.sh`)
- Create and `cd` into a clean directory: `tests/e2e_sandbox/`.
- Initialize a local git repository (`git init`, `git commit --allow-empty -m "init"`).
- Symlink or copy the necessary infrastructure (`scripts/`, `playbooks/`, `docs/`, `TEMPLATES/`) into the sandbox so the Manager's standard tool calls work.

### 3.2 Auto-Pilot Prompt Injection
Run the Manager via the OpenClaw CLI, pointing it at the sandbox:
```bash
MANAGER_PROMPT="You are the leio-sdlc Manager in Auto-Pilot mode.
Working directory: tests/e2e_sandbox/ (Always cd here first).
Task: Create a simple hello world python script.
Constraints: 
1. Do not ask the user for permission to proceed to the next phase.
2. Execute the full pipeline sequentially:
   - Create PRD.
   - Run spawn_planner.py to get PR Contract.
   - Run spawn_coder.py to write code.
   - Run spawn_reviewer.py to verify code.
   - Run merge_code.py to merge.
3. When the merge is successful, output exactly: [E2E_MANAGER_SUCCESS] and stop."

openclaw agent --session-id "e2e-manager-$(uuidgen)" -m "$MANAGER_PROMPT" > tests/manager_e2e.log 2>&1
```

### 3.3 System-Level Assertions
After the Manager exits:
- `grep -q "\[E2E_MANAGER_SUCCESS\]" tests/manager_e2e.log`
- `[ -f tests/e2e_sandbox/hello.py ]`
- `grep -q "print" tests/e2e_sandbox/hello.py`

## 4. Acceptance Criteria
- [ ] `scripts/test_manager_e2e.sh` is created and executable.
- [ ] Sandbox isolates the git history from the main workspace.
- [ ] Manager successfully completes the end-to-end SDLC loop autonomously.
- [ ] Test automatically cleans up `tests/e2e_sandbox/` upon success.