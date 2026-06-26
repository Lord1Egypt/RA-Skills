---
Affected_Projects: [leio-sdlc]
---

# PRD: ISSUE-1085 Fix Planner Path Traversal Defense Deadlock

## 1. Context & Problem (业务背景与核心痛点)
The SDLC process is currently deadlocked. During "State 0: Auto-slicing", the Planner attempts to write PR contracts into a decoupled job directory (typically located in `~/.openclaw/skills/leio-sdlc/.sdlc_runs/`). However, the `create_pr_contract.py` script enforces a strict `SecurityError` path traversal check: it asserts that any file being written must reside within the target project's `workdir`. 

Since our modern architecture decouples the "Control Plane" (running in the skill directory) from the "Data Plane" (the project being modified), this security check causes a Catch-22: the Planner is forbidden from writing the instructions it needs to proceed, resulting in a `[FATAL] Planner failed to generate any PRs.` error.

## 2. Requirements & User Stories (需求定义)
1.  **Resolved Deadlock**: The Planner must be able to write PR contracts into the authorized `.sdlc_runs` directory, even if that directory is outside the project `workdir`.
2.  **Maintain Security**: The path traversal defense must not be entirely removed. It should be refined to permit writes only to two authorized zones: the project `workdir` OR the specific `job_dir` allocated for the current run.
3.  **No Manager Intervention**: This fix must be implemented via the SDLC pipeline, not by direct manual edits by the Manager.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
-   **Modify `scripts/create_pr_contract.py`**:
    -   Identify the blocks where `SecurityError` is raised based on `os.path.commonpath([workdir, ...])`.
    -   Update the validation logic to allow the `job_dir_path` (passed as an argument) as an additional "safe zone".
    -   Ensure that the final PR file path is validated against this expanded safe zone.

## 4. Acceptance Criteria (BDD 黑盒验收标准)
-   **Scenario 1: Slicing into External Directory**
    -   **Given** `create_pr_contract.py` is invoked with a `--job-dir` that is outside the `--workdir`.
    -   **When** the script attempts to write a PR markdown file.
    -   **Then** it should successfully write the file without raising a `SecurityError`, provided the path is within the specified `job-dir`.
-   **Scenario 2: Malicious Path Traversal**
    -   **Given** `create_pr_contract.py` is invoked with a filename containing `../`.
    -   **When** the script validates the target path.
    -   **Then** it must still raise a `SecurityError` if the resulting path tries to escape both the `workdir` and the `job_dir`.

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
-   **Unit Testing**: The Coder must add or update a test case (potentially in `tests/test_create_pr_contract.py` or a new standalone test) that explicitly mimics the decoupled directory structure and confirms the `SecurityError` is no longer triggered for authorized external job directories.
-   **Isolation**: No changes to the global OpenClaw API are required; this is strictly a local SDLC logic fix.

## 6. Framework Modifications (框架防篡改声明)
-   `scripts/create_pr_contract.py`
-   `tests/test_create_pr_contract.py` (if it exists) or relevant test script.

---
## 7. HARDCODED CONTENT (CODER MUST COPY EXACTLY)
> [CRITICAL INSTRUCTION TO CODER] No hardcoded string literals are mandated for this logic fix. Focus on the path validation logic refinement.
