---
name: muniu-liuma
description: SDD（规范驱动开发）步骤质量工具箱总览——管理 5 个独立步骤 SKILL（spec-writer / arch-designer / task-planner / impl-guide / audit-trace）的能力清单、选择指引与分发安装说明。输入：用户询问工具箱能力、某个 SKILL 的用途、如何选择/安装/分发 SKILL。输出：能力清单、SKILL 选择建议、安装与分发指引。典型触发词：这个工具箱有什么、用哪个 SKILL、怎么安装、分发 SKILL、工具列表。
version: 1.2.0
---

# MuniuLiuma（木牛流马）— SDD 步骤质量工具箱

将产品开发全流程拆分为 5 个**独立、自包含、即插即用**的步骤 SKILL，聚焦每一步的质量方法论。可独立使用，也可嵌入 Gentle-AI / OpenSpec 等既有流程作为"质量放大器"。

## 工具箱构成

| SKILL | 输入 | 产出 | 典型触发词 |
|-------|------|------|-----------|
| [spec-writer](skills/spec-writer/SKILL.md) | 需求文档 / 想法 / 已有 Spec | 结构化 Spec + 追问清单 | 解析 PRD、帮我写 Spec、检查这个 Spec |
| [arch-designer](skills/arch-designer/SKILL.md) | 已有完成的 Spec | 架构设计方案 + 风险 + ADR | 根据 Spec 做架构、设计系统架构 |
| [task-planner](skills/task-planner/SKILL.md) | 已有架构方案 | 任务清单（含验收条件、证据要求） | 把架构拆成任务、拆任务 |
| [impl-guide](skills/impl-guide/SKILL.md) | 已有任务清单 + 架构 | 实现指导规范 + 可执行测试骨架 | 生成实现指导、怎么开始写代码 |
| [audit-trace](skills/audit-trace/SKILL.md) | 产物 + 实现代码 | 完工审计报告（八维 + 三层门控） | 审计完成情况、完工审计、交付检查 |

> **TEST-SKELETON-SPEC.md**：测试骨架规范（V-01~V-04），被 impl-guide / task-planner / audit-trace 引用，随本包分发，需与其保持同目录。
>
> **自测集**：每个独立 SKILL 均含 `eval/evals.json` 最小自测集（触发正负样本 + 过程断言 + 安全检查），随包分发；完整评测集（项目 `eval/` 目录）为开发侧资产，不随包分发。

## 使用方式

### 选择哪个 SKILL（按现有产物阶段）

| 当前状态 | 使用 |
|---------|------|
| 只有需求文档 / 想法 / 不完整的 Spec | spec-writer |
| 已有完成的 Spec | arch-designer |
| 已有架构方案 | task-planner |
| 已有任务清单 + 架构 | impl-guide |
| 已有产物 + 实现代码（要验收） | audit-trace |

**边界互斥**：每个 SKILL 要求明确的前置产物；前置缺失时 SKILL 会主动追问，不得越界执行（详见各 SKILL 的"何时使用"）。

### 独立运行

5 个 SKILL 均为单文件自包含（`skills/<name>/SKILL.md`），可单独拷贝使用，不依赖本总览 SKILL 或其他文件。

## 安装与分发

本包（muniu-liuma）安装后呈单 SKILL 形态。要获得 5 个独立步骤 SKILL，将 `skills/` 下的子目录分发到平台的 skills 目录（平铺安装，不支持嵌套结构）：

| 平台 | 目标目录 |
|------|---------|
| Claude Code | `~/.claude/skills/` |
| Qoder | 本地 skills 目录（见平台文档） |
| OpenClaw | `~/.openclaw/skills/`（或工作区 `./skills`） |

分发后每个 SKILL 作为独立目录被宿主识别与触发；`TEST-SKELETON-SPEC.md` 拷贝至与 SKILL 同级目录（impl-guide / task-planner / audit-trace 的规范引用）。

## 不做什么

- 本 SKILL 不承载任何 Phase 执行逻辑——具体方法论在 5 个独立 SKILL 中
- 不做流程编排与状态管理（那是 Gentle-AI / OpenSpec 等流程引擎的职责）
- 不评估 SKILL 质量（完整评测集为开发侧资产，不随包分发；各 SKILL 自带最小自测集 eval/evals.json）
