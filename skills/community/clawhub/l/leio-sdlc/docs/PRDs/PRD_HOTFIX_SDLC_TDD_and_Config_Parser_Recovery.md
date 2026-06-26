---
Affected_Projects: [leio-sdlc]
---

# PRD: HOTFIX_SDLC_TDD_and_Config_Parser_Recovery

## 1. Context & Problem (业务背景与核心痛点)
当前 SDLC 流水线存在两个阻断性的基础问题，导致流水线瘫痪，需要紧急 Hotfix：
1. **运行时路径混用灾难 (Path Chaos)**：核心启动脚本（如 `spawn_planner.py`, `spawn_coder.py`, `spawn_reviewer.py`, `agent_driver.py` 等）在 `runtime_dir`（技能代码目录）、`global_dir`（全局运行状态目录）和 `workdir`（目标代码工作区）的使用上极其混乱。这导致资源文件路径、动态输出路径、工作区代码路径被搞混，例如 Reviewer 找不到评估模板文件。
2. **测试模式配置误判污染代码区 (Config Pollution)**：在 `scripts/orchestrator.py` 的配置加载机制 `load_or_merge_config` 中，如果没有找到配置，会默认向 `sdlc_root/config/` 写入新配置。在本地开发测试时，`sdlc_root` 就是当前源码目录。在自动化测试环境（`SDLC_TEST_MODE=true`）下，这会导致向 Git 源码树物理写入 `config/sdlc_config.json`，污染了 Git 工作区，直接触发严苛的脏状态守卫导致流水线熔断。

## 2. Requirements & User Stories (需求定义)
1. **全面实施路径三权分立**：在所有 Agent 驱动脚本和核心底层库中：
   - 模板/资源读取**必须**锚定在 `RUNTIME_DIR`。
   - 所有的 PR 契约生成、日志写入、审查报告等中间态文件**必须**锚定在 `GLOBAL_DIR` 或传入的 `run_dir`/`job_dir`。
   - 只有业务代码读写和 Git 操作**必须且只能**发生在 `WORKDIR`。
2. **阻断测试模式下物理写盘**：在 `scripts/orchestrator.py` 的配置加载机制中，如果检测到测试模式（`os.environ.get("SDLC_TEST_MODE") == "true"`），系统必须仅在内存中合并和返回配置字典，**绝对禁止**向磁盘物理写入任何配置文件。

## 3. Architecture & Technical Strategy (架构设计与技术路线)
> **[Instruction to Main Agent/Architect]**
本 Hotfix 必须在一个自包含的 PR 内完成所有实现与验证：
1. **彻底排查与修复路径解耦**：
   - 将所有底层脚本中的相对路径（如 `docs/TEMPLATES/...`）替换为通过 `__file__` 反推的绝对安全 `RUNTIME_DIR` 路径。
   - 梳理所有 `open(..., "w")` 和 `subprocess.run(cwd=...)`，确保精准命中对应的目录逻辑。
   - 编写自动化测试（例如 `tests/test_path_decoupling.py`）来覆盖各核心脚本的目录分配逻辑，验证模板读取和输出路径的隔离。
2. **修复配置写盘拦截**：
   - 定位 `scripts/orchestrator.py` 中的 `load_or_merge_config` 函数。在执行 `os.makedirs` 和 `open(..., "w")` 等操作前，包裹条件守卫 `if os.environ.get("SDLC_TEST_MODE") != "true":`。
   - 创建 `scripts/test_1094_config_pollution.sh`。设置 `export SDLC_TEST_MODE=true`，触发一次 `orchestrator.py` 加载逻辑，随后断言无文件生成。

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1: 路径三权分立隔离成功**
  - **Given** 工作区、全局运行区和运行时代码区完全独立分离
  - **When** 启动 Coder/Reviewer 等 Agent 脚本
  - **Then** Agent 能正确从 Runtime 目录读取系统模板，且其生成的任何中间报告文件均严格保存在 Global 目录中，不污染 Workdir。
- **Scenario 2: 测试模式下配置不发生物理污染**
  - **Given** 当前环境下设置了 `SDLC_TEST_MODE=true`
  - **When** 触发 `orchestrator.py` 的配置加载逻辑
  - **Then** 源码工作区内不会物理创建出 `config/sdlc_config.json` 文件。
- **Scenario 3: 测试脚本正确挂载与断言输出**
  - **Given** 新增了验证用的测试脚本 `scripts/test_1094_config_pollution.sh`
  - **When** 运行该测试脚本
  - **Then** 脚本在成功断言无文件生成后，控制台需精准输出指定成功提示词。

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- **路径隔离覆盖测试**：必须用 Python 单元测试验证核心脚本对 `open()` 和模板加载的绝对路径计算。发现问题并使用 TDD 闭环解决。
- **Git 污染断言**：在 Bash 测试中执行配置加载操作后，必须通过 `[ ! -f "config/sdlc_config.json" ]` 进行严格断言，从而保证不污染 Git 状态树。

## 6. Framework Modifications (框架防篡改声明)
- `scripts/orchestrator.py`
- `scripts/agent_driver.py`
- `scripts/spawn_planner.py`
- `scripts/spawn_coder.py`
- `scripts/spawn_reviewer.py`
- `scripts/spawn_auditor.py`
- 新增 `scripts/test_1094_config_pollution.sh`
- 新增 `tests/test_path_decoupling.py` (单元测试)

## 7. Hardcoded Content (硬编码内容)
### Exact Text Replacements:
- **`test_config_pollution_success_message` (For scripts/test_1094_config_pollution.sh)**:
  `"[PASS] test_1094_config_pollution passed successfully"`
