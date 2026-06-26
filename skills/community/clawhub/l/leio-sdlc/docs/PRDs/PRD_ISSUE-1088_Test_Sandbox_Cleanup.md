---
Affected_Projects: [leio-sdlc]
Context_Workdir: /root/.openclaw/workspace/projects/leio-sdlc
---

# PRD: ISSUE-1088 Fix Test Sandbox Leakage & Auto-Cleanup

## 1. Context & Problem (业务背景与核心痛点)
Currently, several shell-based test scripts create temporary sandbox directories using the process ID ($$). These scripts lack a safe `trap` to clean up these directories upon completion, leaving ghost directories behind. Furthermore, legacy sandboxes have accumulated locally.

## 2. Requirements & User Stories (需求定义)
- **R1: CI-Integrated Retroactive Cleanup**: The `preflight.sh` script must automatically prune any legacy `tests/planner_sandbox_*` and `tests/manager_sandbox_*` directories before running tests.
- **R2: Safe Automated Leakage Prevention**: Modify testing scripts to securely delete their own sandbox directories upon completion, ensuring no CWD-deletion errors or relative path vulnerabilities.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
- **Preflight Integration**: 
    - Modify `preflight.sh` to include a step that finds and safely `rm -rf` legacy test sandboxes in the `tests/` directory.
- **Script Hardening**:
    - Update `scripts/test_planner_micro_slicing.sh` and `scripts/test_manager_queue_polling.sh`.
    - Use absolute paths for the `SANDBOX` variable (e.g. `SANDBOX="$(pwd)/tests/planner_sandbox_$$"`).
    - Implement a defensively coded `trap` pattern that changes directory before deletion: `trap 'cd / && [[ -n "$SANDBOX" ]] && rm -rf "$SANDBOX"' EXIT`.

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1: Preflight Cleanup**
    - **Given** legacy sandboxes exist in `tests/`
    - **When** `preflight.sh` is executed
    - **Then** those legacy sandboxes are deleted.
- **Scenario 2: Safe Sandbox Auto-Destruction**
    - **Given** I run `bash scripts/test_planner_micro_slicing.sh`
    - **When** the script completes (Pass or Fail)
    - **Then** the directory `tests/planner_sandbox_<PID>` is deleted without throwing CWD-related shell errors.

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- **Validation**: Manual execution of tests confirms sandboxes are purged safely.
- **Regression**: `preflight.sh` passes successfully.

## 6. Framework Modifications (框架防篡改声明)
- `preflight.sh` (Modify to add cleanup logic)
- `scripts/test_planner_micro_slicing.sh` (Modify trap and path)
- `scripts/test_manager_queue_polling.sh` (Modify trap and path)
- **NOTE**: No new standalone cleanup scripts should be created.

## 7. Hardcoded Content (硬编码内容)
- `trap 'cd / && [[ -n "$SANDBOX" ]] && rm -rf "$SANDBOX"' EXIT`

## 8. Rollback / Feature Flag Strategy (回滚策略)
- **Rollback**: Revert via `git revert`. Legacy sandboxes are local untracked files; they do not need `git rm`.