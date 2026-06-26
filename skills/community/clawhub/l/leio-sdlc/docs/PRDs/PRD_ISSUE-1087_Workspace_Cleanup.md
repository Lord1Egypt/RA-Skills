---
Affected_Projects: [leio-sdlc]
Context_Workdir: /root/.openclaw/workspace/projects/leio-sdlc
---

# PRD: ISSUE-1087 Workspace Artifact Cleanup & Validation

## 1. Context & Problem (业务背景与核心痛点)
The `leio-sdlc` root directory is severely polluted with ghost directories, temporary PR fragments, legacy audit reports, and one-off debug scripts. Many of these were erroneously committed to Git in past milestones (e.g., `AMS/`, `projects/`). Additionally, the release artifact directory `dist` is visible and not standardized as a hidden folder. We need a safe, verifiable cleanup via Git, and an update to the deployment pipeline to use `.dist`.

## 2. Requirements & User Stories (需求定义)
- **R1: Clean up Tracked Ghost Directories**: Safely remove `AMS/` and `projects/` from the repository using `git rm`.
- **R2: Clean up Untracked Ghost Directories**: Remove `root/` which was caused by absolute path resolution failures.
- **R3: Clean up Legacy/Debug scripts and PR fragments**: Remove obsolete files like `debug_orchestrator.py`, `hello.py`, and `pr_*.md` fragments.
- **R4: Rename Dist Directory**: Change the build directory from `dist` to `.dist` across the deployment pipeline.
- **R5: Gitignore Update**: Ensure `.dist/` is added to `.gitignore`.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
- **One-Time Script**: Coder must create `scripts/one_time_cleanup.sh`. It will use precise `git rm -rf` for tracked garbage and `rm -rf` for untracked garbage based on the detailed audit list. 
- **Strict Guardrail**: No wildcard deletions (e.g., `rm *.md`) in the root directory. `README.md`, `STATE.md`, `SKILL.md`, and `ARCHITECTURE.md` must be preserved.
- **Pipeline Modification**: 
    - Update `scripts/build_release.sh` to build into `.dist` instead of `dist`.
    - Update `deploy.sh` to sync from `.dist` instead of `dist` and update `.gitignore` injection.
    - Update `.gitignore` to ignore `.dist/`.

**Targeted Deletion List**:
- *Tracked Directories*: `AMS/`, `projects/`
- *Untracked Directories*: `root/`
- *PR Fragments*: `content_pr1.md`, `content_pr2.md`, `final_pr_contracts.md`, `pr_001.md`, `pr001_tmp.md`, `pr_002.md`, `pr002_tmp.md`, `pr1_draft.md`, `pr1_temp.md`, `pr2_draft.md`, `pr2_temp.md`, `pr3_temp.md`, `pr4.md`, `pr4_temp.md`, `tmp_pr1_final.md`, `tmp_pr3.md`, `tmp_pr4.md`
- *Legacy Logs/Reports*: `Architectural_Audit_Report_v5.md`, `independent_audit_report.md`, `native_audit_report.md`, `polyrepo_audit_report.md`, `polyrepo_v4_audit_report.md`, `polyrepo_v5_audit_report.md`, `polyrepo_v6_audit_report.md`, `polyrepo_v7_audit_report.md`, `arbitration_report.txt`, `audit_prompt.txt`, `audit_verdict.json`, `dummy_chat_context_074.txt`, `polyrepo_plan.md`
- *One-off Scripts*: `debug_orchestrator.py`, `hello.py`, `patch_guardrails.sh`, `patch_test_branch_isolation.sh`, `rollback.sh`, `run_independent_audit.sh`, `server.py`, `spawn_native_auditor.sh`

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1: Cleanup**: Given `scripts/one_time_cleanup.sh` is executed, When checking `git status`, Then the specified ghost directories and legacy files must be removed from the working tree.
- **Scenario 2: Dist Renaming**: Given `deploy.sh --preflight` is executed, When checking the file system, Then `.dist/` must be generated and `git status` must not show `.dist/` as untracked (must be ignored).

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
1. **Static Dependency Check (`preflight.sh`)**: After executing cleanup and pipeline changes, the Coder must run `./preflight.sh` to ensure no syntax errors or missing architecture files.
2. **Dynamic E2E Execution Check (`test_sdlc_cujs.sh`)**: The Coder must execute `bash scripts/test_sdlc_cujs.sh` to ensure SDLC orchestrator logic does not depend on any deleted script.
- **Quality Goal**: Both `preflight.sh` and `test_sdlc_cujs.sh` must pass cleanly.

## 6. Framework Modifications (框架防篡改声明)
- `scripts/one_time_cleanup.sh` (Create)
- `scripts/build_release.sh`
- `deploy.sh`
- `.gitignore`

## 7. Hardcoded Content (硬编码内容)
- None