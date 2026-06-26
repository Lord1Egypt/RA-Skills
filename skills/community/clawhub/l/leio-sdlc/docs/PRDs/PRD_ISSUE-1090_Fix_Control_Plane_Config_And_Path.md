---
Affected_Projects: [leio-sdlc]
---

# PRD: ISSUE-1090_Fix_Control_Plane_Config_And_Path

## 1. Context & Problem (业务背景与核心痛点)
The SDLC Orchestrator architecture (Data Plane vs. Control Plane decoupling) was introduced to isolate runtime artifacts (like `.sdlc_runs`) from the target project's workspace. However, three design flaws and implementation bugs cause the `.sdlc_runs` directory to leak back into the project root or pollute the global environment:
1. **Fallback Logic Overlap:** When executing `leio-sdlc` upon itself, the default `global_dir` falls back to the `leio-sdlc` root, reintroducing the artifact collision. 
2. **State 5 Escalation Hardcoding:** In `orchestrator.py`, the State 5 crash recovery logic contains a hardcoded relative path `os.path.join('.sdlc_runs', parent_dir_name)`, which forcefully writes `.sdlc_runs` into the current working directory regardless of global isolation configurations.
3. **Configuration Stagnation & Test Pollution:** `sdlc_config.json` lacks a dynamic merge mechanism, causing new keys like `GLOBAL_RUN_DIR` to be ignored on updates. Additionally, test suites mock runs directly into static directories without a dedicated `test_tmp` namespace, threatening to pollute the actual global runs folder.

## 2. Requirements & User Stories (需求定义)
1. **Dynamic Config Merge:** `orchestrator.py` MUST parse `config/sdlc_config.json.template` on startup. If `sdlc_config.json` does not exist or is missing keys, it must merge the default keys (e.g., `GLOBAL_RUN_DIR`) into memory and save the updated configuration back to disk.
2. **Fail-Fast Global Dir Resolution:** The `global_dir` in `orchestrator.py` MUST be resolved by: (1) CLI argument `--global-dir`, (2) Config value `GLOBAL_RUN_DIR`, (3) If neither is present, raise a `RuntimeError` (Fail Fast). It must NEVER fall back to the project root or runtime script directory.
3. **State 5 Path Fix:** The State 5 recovery block in `orchestrator.py` must use the absolute `global_dir` when defining `run_dir` (e.g., `os.path.join(global_dir, '.sdlc_runs', ...)`).
4. **Test Sandboxing (`test_tmp`):** All test scripts (`tests/*.py`, `e2e_test_*.sh`) MUST be updated to pass a dedicated temporary path (e.g., `/tmp/mock_sdlc_global_$$` or `test_tmp`) to `--global-dir`.
5. **Legacy Directory Warning:** Emit a non-blocking `WARNING` during initialization if an old `.sdlc_runs` directory is detected in the project working directory to prompt manual cleanup.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
> **[Instruction to Main Agent/Architect]** 
- **Configuration Management:** Implement a `load_or_merge_config(global_dir)` function inside `orchestrator.py`. This reads `.template`, merges it with the local `sdlc_config.json`, and saves it back if changes are detected.
- **Path Logic Refactoring:** Update the `global_dir` initialization in `orchestrator.py` to enforce the strict priority (CLI > Config > Fatal Error). Update line ~243 `run_dir = os.path.join('.sdlc_runs', parent_dir_name)` to use the resolved `global_dir`.
- **Warning Injection:** Inside `initialize_sandbox(workdir)`, add an `os.path.exists(os.path.join(workdir, '.sdlc_runs'))` check and use `logging.warning()` or print a high-visibility warning.
- **Test Suite Updates:** Perform a sweeping update across `scripts/test_*.sh`, `scripts/e2e/*.sh`, and `tests/*.py` to replace any hardcoded `MOCK_GLOBAL_DIR=".sdlc_runs"` with explicit isolated temporary paths via CLI.

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1: Dynamic Config Merge**
  - **Given** an existing `sdlc_config.json` missing the `GLOBAL_RUN_DIR` key
  - **When** the orchestrator starts
  - **Then** the file is automatically updated with the missing key from the template.

- **Scenario 2: Fail Fast on Missing Global Dir**
  - **Given** no CLI `--global-dir` is passed and `sdlc_config.json` lacks `GLOBAL_RUN_DIR`
  - **When** the orchestrator is executed
  - **Then** the process immediately exits with a fatal error instead of falling back to the project root.

- **Scenario 3: Non-Blocking Legacy Warning**
  - **Given** an old `.sdlc_runs` directory exists in the target project root
  - **When** the orchestrator is executed
  - **Then** a visible WARNING is printed to the console, and execution continues.

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- **Unit Tests:** Verify the `load_or_merge_config` logic correctly updates missing keys without destroying existing overridden values (e.g., `YELLOW_RETRY_LIMIT`).
- **E2E Tests:** Ensure all existing E2E Bash tests explicitly pass `--global-dir` and verify that no test suite creates a `.sdlc_runs` folder in the project root.
- **Mock Isolation:** No test artifacts should persist in the actual `GLOBAL_RUN_DIR`.

## 6. Framework Modifications (框架防篡改声明)
- `scripts/orchestrator.py`
- `config/sdlc_config.json.template`
- `tests/*` and `scripts/e2e/*` (to pass `--global-dir`)

## 7. Hardcoded Content (硬编码内容)

### Exact Text Replacements:
- **`legacy_warning_msg`**:
```text
WARNING: Found legacy .sdlc_runs in project root. Please clean it up manually.
```

- **`config_missing_error`**:
```text
RuntimeError: No global run directory defined. Must provide --global-dir CLI argument or set GLOBAL_RUN_DIR in sdlc_config.json.
```