# PRD-054: State 0 - PRD Ingestion & Auto-Slicing (v0.2.3 Aligned)

## 1. Problem Statement
The current `orchestrator.py` (v0.2.3) is still a "Passive Executor" at the very beginning of its lifecycle. It requires a human to manually run `spawn_planner.py` to generate PR contracts before the state machine can start polling. This breaks the autonomous "Black Box" experience where a user should only need to provide a PRD to initiate an entire project lifecycle.

## 2. Architectural Alignment (v0.2.3)
In v0.2.3, `orchestrator.py` was upgraded to dynamically compute an isolated `job_dir` (e.g., `docs/PRs/<PRD_Name>`) from the `--prd-file` argument. 
State 0 must leverage this isolated `job_dir`. Instead of the orchestrator exiting when `job_dir` is empty, it should act proactively to populate it by invoking the Planner.

## 3. Critical User Journeys (CUJs)
To achieve full autonomy, the system must elegantly handle the following scenarios:

- **CUJ 1: Fresh Start (The Happy Path)**
  - *User Action*: Runs `python3 scripts/orchestrator.py --prd-file docs/PRDs/MyProject.md`.
  - *System Response*: Detects `docs/PRs/MyProject` is empty/missing. Enters **State 0**, automatically calls Planner, waits for micro-PRs to be generated, and naturally transitions to State 1 (Polling).
- **CUJ 2: Idempotency & Resume (Crash Recovery)**
  - *User Action*: Runs the same command after the Orchestrator previously crashed on PR #3.
  - *System Response*: Detects `docs/PRs/MyProject` contains `open` or `in_progress` PRs. Skips Planner invocation (State 0) to prevent overwriting, and resumes from State 1 directly.
- **CUJ 3: Force Replan (Requirement Change)**
  - *User Action*: Runs with a new flag `--force-replan`.
  - *System Response*: Warns the user, physically purges the existing `docs/PRs/MyProject` directory, invokes the Planner to slice the PRD anew, and starts fresh.
- **CUJ 4: Planner Malfunction (Graceful Halt)**
  - *User Action*: Runs with a completely empty or invalid PRD.
  - *System Response*: Planner fails or outputs 0 PRs. Orchestrator detects the empty output, refuses to enter an infinite loop, and gracefully halts with a `FatalError`.

## 4. Functional Requirements

### 4.1 CLI Argument Expansion
- Add `--force-replan` boolean flag (`action="store_true"`) to `scripts/orchestrator.py`.

### 4.2 State 0: Automated Planning Logic
Insert **State 0** logic immediately after `job_dir` is calculated, before the main `while True` loop:
1. **Idempotency Check**: 
   - Check if `job_dir` exists and contains any `.md` files.
   - If it contains files and `--force-replan` is `False`, print `State 0: Existing PRs detected. Resuming queue...` and skip to State 1.
2. **Purge (If Forced)**:
   - If `--force-replan` is `True` and `job_dir` exists, use `shutil.rmtree(job_dir)` to wipe it clean.
3. **Auto-Invocation**:
   - Print `State 0: Auto-slicing PRD...`.
   - Execute: `subprocess.run([sys.executable, "scripts/spawn_planner.py", "--prd-file", args.prd_file, "--workdir", workdir], check=True)`.
4. **Elastic Slicing Validation**:
   - Check if `job_dir` now contains at least one `.md` file.
   - If count `== 0`, print `[FATAL] Planner failed to generate any PRs.` and `sys.exit(1)`.

## 5. Testing Strategy & TDD Best Practices
**Industry Best Practice for Agentic CI**: Hermetic sandbox testing with Deterministic Stubs. 
We do not invoke the real LLM (Planner) during unit tests. We use bash to dynamically generate a fake `spawn_planner.py` (a stub) that outputs predictable files, ensuring 100% path coverage without network flakiness.

The Coder must append the following 4 deterministic test scenarios to `scripts/test_orchestrator_fsm.sh`. Each must run in an isolated sandbox (`setup_sandbox`).

- **Test 1: Pure State 0 Start**
  - *Setup*: Stub Planner to create `PR_001_Mock.md` in `job_dir`.
  - *Action*: Run Orchestrator without `--force-replan`.
  - *Assert*: Orchestrator logs "State 0: Auto-slicing PRD", successfully calls Planner, and processes `PR_001_Mock.md`.
- **Test 2: Idempotency (Resume)**
  - *Setup*: Pre-create `PR_001_Existing.md` in `job_dir`. Stub Planner to throw an exception if called.
  - *Action*: Run Orchestrator.
  - *Assert*: Orchestrator logs "Resuming queue", does NOT call the Planner (no exception thrown), and processes the existing PR.
- **Test 3: Force Replan**
  - *Setup*: Pre-create `PR_Old.md` in `job_dir`. Stub Planner to create `PR_New.md`.
  - *Action*: Run Orchestrator with `--force-replan`.
  - *Assert*: `PR_Old.md` is deleted. Planner is called. `PR_New.md` is processed.
- **Test 4: Planner Failure**
  - *Setup*: Stub Planner to do absolutely nothing (exit 0, but no files created).
  - *Action*: Run Orchestrator.
  - *Assert*: Orchestrator exits with code 1 and logs "[FATAL] Planner failed".

## 6. Acceptance Criteria
- [ ] `scripts/orchestrator.py` implements `--force-replan` and State 0 logic.
- [ ] Orchestrator no longer exits immediately if `job_dir` doesn't exist; it creates it via Planner.
- [ ] `scripts/test_orchestrator_fsm.sh` includes the 4 new CUJ tests.
- [ ] Running `./preflight.sh` exits with `✅ PREFLIGHT SUCCESS`.