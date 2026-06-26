---
Affected_Projects: [leio-sdlc]
---

# PRD: Workspace_Cleanup

## 1. Context & Problem (业务背景与核心痛点)
The `leio-sdlc` workspace currently suffers from severe pollution, containing over 1,200 files. The majority of these are temporary artifacts generated during SDLC runs, tests, and deployments. The most critical issue is an infinite nesting bug (the "Russian doll" effect) caused by deployment and build scripts copying `dist/` into itself (e.g., `dist/dist/root/...`). This pollution has leaked into the production runtime via `kit-deploy.sh`, bloating the system and increasing deployment times.

## 2. Requirements & User Stories (需求定义)
1. **Hard Cleanup**: Physically remove all existing temporary directories, sandbox residuals, and nested deployment folders from the `leio-sdlc` workspace.
2. **Fix Rsync Rule Propagation**: Ensure `scripts/build_release.sh` utilizes `.gitignore` in addition to `.release_ignore` during the `rsync` packaging step, preventing duplicate maintenance of ignore rules and natively solving the infinite nesting issue.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
- **Target Files**: `scripts/build_release.sh`.
- **Cleanup Execution**: Provide a one-off aggressive cleanup script or execute the cleanup directly via PR to reset the workspace to a pristine state.
- **Rule Engine**: `rsync` supports multiple `--exclude-from` arguments. By injecting `--exclude-from='.gitignore'` into `build_release.sh`, we inherit all development ignores (like `dist/`, `.sdlc_runs/`, etc.) automatically, adhering to the DRY (Don't Repeat Yourself) principle.

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1:** Running deployment does not nest `dist/`
  - **Given** an existing `dist/` directory with previous build artifacts
  - **When** `build_release.sh` is executed
  - **Then** the new `.dist/` directory does not contain the old `dist/` inside it.
- **Scenario 2:** Temporary files are ignored by release natively
  - **Given** SDLC temporary files exist in the workspace and are listed in `.gitignore`
  - **When** `build_release.sh` creates the `.dist/` package
  - **Then** these temporary files are absent from `.dist/`.

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- Run `build_release.sh` locally and verify `tree -a .dist` does not contain `.sdlc_runs/` or `dist/`.

## 6. Framework Modifications (框架防篡改声明)
- `scripts/build_release.sh`

## 7. Hardcoded Content (硬编码内容)
### Exact Text Replacements:
- **For `scripts/build_release.sh` (Modify the rsync line)**:
```text
rsync -av --exclude-from='.gitignore' --exclude-from='.release_ignore' --exclude="$DIST_DIR/" ./ "$DIST_DIR/"
```

### Cleanup Script (For Coder Execution):
**Anti-Hallucination Guard**: To execute the "Hard Cleanup", the Coder MUST strictly use the following commands. Do not invent other deletion logic.
```bash
# Physical cleanup of known temporary artifacts
rm -rf .dist/ dist/ .pytest_cache/ __pycache__/ .tmp/ .sdlc_runs/
rm -f *.diff *.log .coder_state.json .sdlc_repo.lock .sdlc_lock_manifest.json Review_Report.md pr*.md tmp_pr*.md
```