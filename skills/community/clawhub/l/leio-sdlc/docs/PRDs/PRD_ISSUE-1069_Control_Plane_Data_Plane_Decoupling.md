---
Affected_Projects: [leio-sdlc]
---

# PRD: ISSUE-1069 Control Plane Data Plane Decoupling

## 1. Context & Problem (业务背景与核心痛点)
Currently, the SDLC Orchestrator mixes runtime state files (e.g., `.sdlc_runs`, `.coder_session`, `Review_Report.md`) inside the target repository's working directory. This blending of the Control Plane (runtime engine state) and the Data Plane (business code repository) leads to catastrophic collisions during Git branch resets, dirty workspace conflicts, and complex `git clean -fd` edge cases (e.g., ISSUE-1068 where PR contracts are physically destroyed by State 5 Escalation reset).

## 2. Requirements & User Stories (需求定义)
1. **Global Control Center**: Relocate all `.sdlc_runs` (and associated artifacts like PR contracts, session files, and review reports) out of the target project workspace into a global isolated execution directory (e.g., `/root/.openclaw/workspace/.sdlc_runs/<project_name>`).
2. **Double Parameter Passing**: Update the SDLC Orchestrator and all `spawn_*.py` sub-agent executors to strictly enforce two separate paths:
   - `--workdir` (Data Plane): The target project directory (managed by VCS).
   - `--run-dir` (Control Plane): The absolute path to the global isolated execution directory.
3. **Sub-Agent Vision Isolation**:
   - Planner writes PR slice contracts directly to the global `--run-dir`.
   - Coder reads PR slice and session from `--run-dir` but executes within and modifies `--workdir`.
   - Reviewer reads code from `--workdir` but saves the `Review_Report.md` exclusively to `--run-dir`.
4. **Resilience**: The SDLC pipeline must survive aggressive VCS resets (`git reset --hard`, `git clean -fd`) without losing its internal execution state.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
- **Script Refactoring Target**: `orchestrator.py`, `spawn_planner.py`, `spawn_coder.py`, `spawn_reviewer.py`, `spawn_manager.py`, `spawn_arbitrator.py`.
- **Logic Updates**:
  - In `orchestrator.py`, initialize a global `SDLC_GLOBAL_RUN_BASE` (defaulting to a shared location or dynamically derived, like `os.path.join(PROJECT_ROOT, '.sdlc_runs')` or a true global path like `/root/.openclaw/workspace/.sdlc_runs`). Currently, `orchestrator.py` creates `.sdlc_runs` locally. We need to pass `--global-dir` to `orchestrator.py` or default to a safe external path, and create `.sdlc_runs/<target_project_name>` there.
  - In `orchestrator.py`, refactor `initialize_sandbox()` to completely remove the logic that appends `.sdlc_runs/`, `.coder_session`, `.coder_state.json`, and `Review_Report.md` to `.git/info/exclude`. These root-level artifacts will no longer exist in the local workspace.
  - Sub-agent Python execution commands inside `orchestrator.py` must include `--run-dir` mapping to this external path.
  - The `spawn_*.py` CLI arguments must be updated to accept `--run-dir`.
  - All paths within `spawn_*.py` and `agent_driver.py` that hardcode local `.sdlc_runs/` must be transitioned to use `args.run_dir`.

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1: Orchestrator Pipeline Separation**
  - **Given** an SDLC pipeline is triggered on a project
  - **When** the Planner, Coder, and Reviewer execute their phases
  - **Then** the local project workspace `.git/info/exclude` does NOT need `.sdlc_runs/`
  - **And** all generated markdown artifacts, JSON states, and PR directories exist solely in the external `--run-dir`.

- **Scenario 2: State 5 Reset Safety**
  - **Given** an active execution with intermediate PR contracts in the `--run-dir`
  - **When** the workspace triggers a Tier 1 State Reset (`git reset --hard` and `git clean -fd`)
  - **Then** the workspace is completely wiped of untracked files
  - **And** the Orchestrator successfully continues because the PR contracts in `--run-dir` remain fully intact.

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- E2E Integration tests like `test_orchestrator_logs.sh`, `e2e_test_forensic_quarantine.sh`, and `e2e_test_state5_tier1_reset.sh` will need their assertions updated since `.sdlc_runs` will no longer exist in the local mock repository.
- Mocking Strategy: In sandbox e2e tests, define `--global-dir /tmp/mock_global` and assert that the artifact directories are properly created inside `/tmp/mock_global/.sdlc_runs/`.

## 6. Framework Modifications (框架防篡改声明)
- `scripts/orchestrator.py`
- `scripts/spawn_planner.py`
- `scripts/spawn_coder.py`
- `scripts/spawn_reviewer.py`
- `scripts/spawn_manager.py`
- `scripts/spawn_arbitrator.py`
- `scripts/e2e/e2e_test_forensic_quarantine.sh`
- `scripts/e2e/e2e_test_state5_tier1_reset.sh`
- `scripts/e2e/e2e_test_github_sync_integration.sh`
- `scripts/e2e/e2e_test_orchestrator_fsm.sh`
- `scripts/test_manager_queue_polling.sh`
- `scripts/test_planner_slice_failed_pr.sh`
- `scripts/test_escalation_clean.sh`
- `scripts/test_orchestrator_logs.sh`
- `scripts/e2e/e2e_test_reviewer_artifact_guardrail.sh`
- `scripts/e2e/e2e_test_yellow_path.sh`

---

## Appendix: Architecture Evolution Trace (架构演进与审查追踪)
- **v1.0**: Initial PRD drafted to address ISSUE-1068 and ISSUE-1069 via Control Plane / Data Plane decoupling.
- **Audit Rejection (v1.0)**: Rejected due to incomplete blast radius. Missed several e2e test files and the `initialize_sandbox` function in `orchestrator.py` that modifies `.git/info/exclude`.
- **v2.0 Revision Rationale**: Added explicit modification paths for `test_manager_queue_polling.sh`, `test_planner_slice_failed_pr.sh`, `test_escalation_clean.sh`, `test_orchestrator_logs.sh`, `e2e_test_reviewer_artifact_guardrail.sh`, and `e2e_test_yellow_path.sh`. Detailed the exact removal strategy for the local `initialize_sandbox` git exclusion logic.