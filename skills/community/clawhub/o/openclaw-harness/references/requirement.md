# 01-requirement.md - 需求文档

## 项目概述

- **项目名称**: openclaw-harness
- **项目类型**: OpenClaw Skill（通用任务执行上下文管理器）
- **目标用户**: OpenClaw Agent（混沌团队自用 + 开源社区）

## 需求背景

- **解决的问题**: Harness Engineering 三大支柱——
  1. **上下文工程**：跨会话进度追踪（Context Engineering）、知识版本控制、上下文压缩
  2. **架构约束**：自定义 Linter 配置规范检查、Build-Verify-Fix 闭环、门禁模板
  3. **熵管理**：GC Agent 自动清理过期记忆和冗余文件、状态持久化

- **用户痛点**：
  - **Agent 无状态**：每次新 Session 从零开始，不知道项目做到哪了、任务卡在哪
  - **Context Rot**：会话越来越长，Agent 越来越慢，上下文噪声累积
  - **验证缺失**：配置靠人工检查，质量参差不齐，无 Build-Verify-Fix 闭环
  - **进度断层**：跨会话无法恢复工作进度，危险操作前无状态快照，回滚能力缺失

## 功能需求

### P0 必须

- [ ] **检查点（Checkpoint）管理**：创建/列出/恢复/删除任务快照，包含 TASKS.md、任务元数据、声明文件 manifest，支持标签和回滚
- [ ] **验证（Verify）检查**：验证任务完成情况，默认检查 TASKS.md 存在+元数据有效，支持自定义验证规则（file/command/pattern 三种类型）
- [ ] **熵管理（GC）**：自动清理超过保留期限/数量限制的检查点、过多验证报告、孤立临时文件；支持干运行预览（--dry-run）
- [ ] **初始化（init）**：创建 `.harness/` 目录结构，生成 `.initialized` 标记，支持强制重新初始化
- [ ] **状态查看（status）**：显示当前 Harness 状态，支持 verbose 和 JSON 输出格式

### P1 重要

- [ ] **进度追踪（progress）**：跨会话进度持久化到 `.agent-progress.json`，记录项目阶段、里程碑、阻塞项，下次会话可恢复
- [ ] **上下文压缩**：当 MEMORY.md 超过 200 行时，自动压缩归档历史记忆，保留核心信息（安全规则、联系方式、重要决策）
- [ ] **Git 集成**：Git pre-commit 钩子卡点入仓，commit message 规范检查
- [ ] **自动修复（fix）**：Linter 发现问题时，自动修复已知问题（占位符清理、空行压缩等）
- [ ] **配置 Linter**：SOUL.md、IDENTITY.md、AGENTS.md 规范检查，发现问题同时给出修复建议

### P2 可选

- [ ] **CI 严格模式**：Linter error 级别阻塞入仓，warning 仅提醒
- [ ] **多 Agent 协作视图**：中央进度面板，查看所有 Agent 当前任务和阻塞状态
- [ ] **Skill 分发包**：封装为可安装 Skill，发布到 Clawhub，开源社区可用
- [ ] **增量检查点**：仅保存变更文件，而非全量快照，降低存储占用

## 非功能需求

- **性能**：
  - 检查点创建 < 2 秒（100 个文件以内）
  - GC 干运行 < 5 秒
  - 单次验证 < 1 秒
  - 无外部 API 依赖，纯本地执行

- **安全**：
  - 永不删除 SOUL.md、IDENTITY.md、USER.md、安全规则文件
  - 所有删除操作记录到 GC 日志
  - 删除前强制归档，不直接抹除
  - 误删可从 Git 历史恢复

- **兼容性**：
  - Bash 4.0+ 兼容
  - 依赖 `jq`（可选，无 jq 时部分功能降级）、`openssl`（可选，用于生成随机 ID）
  - 跨平台兼容（Linux/macOS）

## 验收标准

- [ ] `harness init` 可在任意目录初始化 `.harness/` 目录结构，生成 `.initialized` 标记
- [ ] `harness checkpoint <label>` 可创建带标签检查点，`harness checkpoint -l` 列出所有检查点
- [ ] `harness checkpoint -r <cp-id>` 可恢复到指定检查点，TASKS.md 和 manifest 文件完整还原
- [ ] `harness verify` 执行默认验证，检查 TASKS.md 存在且元数据有效，输出验证报告
- [ ] `harness verify -r '[{"name":"Build OK","type":"command","path":"npm run build"}]'` 支持自定义 JSON 验证规则
- [ ] `harness gc --dry-run` 预览待清理项，不实际删除；`harness gc` 执行清理
- [ ] `harness gc --max-cp 5` 可配置每任务最大检查点数（默认 10）
- [ ] `harness gc --max-age 7` 可配置检查点最大保留天数（默认 7）
- [ ] `harness status` 显示当前 Harness 状态，`-v` 显示详细信息，`-j` 输出 JSON
- [ ] `harness gc -s` 显示 Harness 目录大小
- [ ] 目录结构符合规范：`.harness/tasks/<task-id>/meta.json`、`checkpoints/<cp-id>/`、`reports/verify-*.json`、`tmp/`
- [ ] GC 永不删除：SOUL.md、IDENTITY.md、USER.md、安全规则文件
- [ ] 所有删除操作记录到 GC 日志

## 里程碑

| 阶段 | 目标 | 预计时间 | 负责人 |
|------|------|----------|--------|
| Phase 1 | **基础骨架**：Harness 核心脚本（init/status/checkpoint/verify/gc），目录结构，`SKILL.md` 初稿 | 2 天 | 祝融（开发） |
| Phase 2 | **进度追踪**：`.agent-progress.json` Schema，跨会话状态持久化，上下文压缩逻辑 | 2 天 | 祝融 |
| Phase 3 | **Linter + Verify-Fix**：配置 Linter（SOUL/IDENTITY/AGENTS），verify-fix.sh 闭环，pre-commit 钩子 | 2 天 | 祝融 |
| Phase 4 | **GC Agent 完善**：gc-agent.sh，GC 规则定义，记忆归档+压缩流程 | 1 天 | 祝融 |
| Phase 5 | **文档 + 示例**：README.md、使用文档、`examples/` 示例目录、Skill 封装发布 | 2 天 | 荧惑 |
| Phase 6 | **试点 + 推广**：毕方 workspace 试点、全 team 推广、持续优化 | 持续 | 祝融 |

---

> 📌 **填写人**：炎晖
> 📌 **评审结论**：✅ 通过
> 📌 **评审日期**：2026-03-27
