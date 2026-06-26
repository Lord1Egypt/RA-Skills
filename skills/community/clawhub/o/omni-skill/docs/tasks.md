# 任务分解 (Tasks)

1. [x] **基础设施搭建**
   - [x] 创建 `omni-skill` 目录与标准子目录结构。
   - [x] 编写 `src/core/interfaces.py` 统一定义 Schema 与 ErrorCode。
2. [x] **核心逻辑实现**
   - [x] 实现微内核 `src/core/kernel.py` 与插件生命周期管理。
   - [x] 实现配置中心 `src/core/config.py`。
   - [x] 实现熔断与限流 `src/core/metrics.py`。
3. [x] **交付物生成**
   - [x] 生成 `templates/plugin_template.py` 模板。
   - [x] 编写 `docs/architecture_and_deployment.md`（含架构图与性能基准）。
   - [x] 编写统一的 `SKILL.md`。
4. [x] **自动化测试与回归**
   - [x] 编写 pytest 单元测试，覆盖核心逻辑。
   - [x] 测试覆盖率达标（已达到 95%）。
5. [x] **环境清理与切换**
   - [x] 删除原有的分散 Skill 目录（如 `character-biographer`, `logic-auditor` 等）。
   - [x] 明确后续所有 Hook 指向 `omni-skill`，旧 SKILL.md 迁移至 `prompts/` 目录方案设计。
