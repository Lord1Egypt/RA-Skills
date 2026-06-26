---
name: harness-engineering
description: "Harness Engineering — Generator/Evaluator 双 Agent 编码工作流。用于任何需要规划、编码、评审、质量门禁的编程任务。将做事的 Agent 和评判的 Agent 分开，每个阶段通过质量门禁才能进入下一阶段。"
---

# Harness Engineering — 编码工作流体系

> "如果它不能被机械化地执行，Agent 就会偏离。"

## 核心理念

Harness Engineering 是一套**项目约束体系**，用于规范化 AI 辅助编程流程。核心原则：

1. **Generator ≠ Evaluator** — 写代码的 Agent 和审代码的 Agent 必须分开
2. **质量门禁** — 每个阶段必须通过检查才能进入下一阶段
3. **变更审计链** — 每次需求都有完整的规划 → 编码 → 评审 → 交付记录
4. **工程化纠错** — 每发现一个错误，就消除它再次发生的可能性

---

## 项目结构

每个使用 Harness 的项目，根目录下有 `.harness/` 目录：

```
project/
├── .harness/
│   ├── rules/              # 编码规范、工作流、质量门禁（始终加载）
│   │   ├── quality-gates.md  # 各阶段门禁标准
│   │   └── <project>-rules.md # 项目特定规则
│   ├── skills/             # 可复用 SOP（如 evaluator.md 独立评审）
│   ├── wiki/               # 项目知识库（按需查询）
│   ├── changes/            # 变更审计链（每次需求自动创建）
│   │   └── {type}-{name}-{date}/
│   │       ├── planning/
│   │       │   ├── spec.md   # 需求规格
│   │       │   └── tasks.md  # 任务拆分清单
│   │       ├── review/
│   │       │   ├── code_review_v1.md  # Evaluator 评审报告
│   │       │   └── revision_report.md # Generator 修复报告
│   │       └── summary.md    # 变更摘要（SSOT）
│   └── agents/
│       └── project-agent.md  # Agent Index & Map（启动必读）
└── ...
```

### 变更目录命名规则

```
.harness/changes/{type}-{简述}-{日期}/
```

- `type`: feat | fix | refactor | chore | docs
- `简述`: 短横线分隔的英文描述
- `日期`: YYYYMMDD 格式

---

## 五阶段工作流

```
规划 → 评审 → 编码 → 自审 → 独立评审 → 修复 → 交付
```

### 阶段 1：规划（Planning）

Generator Agent 负责：

1. **需求规格**（`planning/spec.md`）
   - 目标、范围、验收标准、非目标
2. **任务拆分**（`planning/tasks.md`）
   - 每个任务：描述、输入、输出、验收标准
3. **变更摘要**（`summary.md`）
   - 基本信息表、阶段状态表

**质量门禁**：
- [ ] spec.md 包含目标、范围、验收标准
- [ ] tasks.md 每个任务有明确的输入/输出/验收标准
- [ ] summary.md 已创建并填入基本信息

### 阶段 2：编码（Coding）

Generator Agent 按 tasks.md 逐条实现：

1. 先读现有代码，理解模式
2. 写代码前说明计划（改什么、为什么、风险）
3. 完成后产出 `coding_report.md`
4. 完成 `self_review.md` 自查

**质量门禁**：
- [ ] 每个任务都有对应的代码实现
- [ ] 自审 checklist 全部通过
- [ ] 没有遗漏文件、破损 import、未测试路径

### 阶段 3：独立评审（Review）

**关键**：必须用**不同的 Agent**（Evaluator）评审 Generator 的产出。

Evaluator Agent 负责：

1. 读取 spec.md、tasks.md 理解需求
2. 审查 Generator 的代码改动
3. 产出 `review/code_review_v1.md`，问题分级：

| 级别 | 含义 | 处理 |
|------|------|------|
| **MUST FIX** | 安全漏洞、功能缺陷、数据损坏 | 必须修复，否则不能交付 |
| **SHOULD FIX** | 边界情况、可维护性问题 | 强烈建议修复 |
| **LOW** | 代码风格、小优化 | 建议修复 |
| **INFO** | 观察、建议、未来改进 | 记录即可 |

**质量门禁**：
- [ ] 所有 MUST FIX 问题必须修复
- [ ] SHOULD FIX 问题需说明不修复的理由
- [ ] 健康检查/API 测试通过

### 阶段 4：修复（Revision）

Generator Agent 根据评审报告修复：

1. 逐条修复 MUST FIX 和 SHOULD FIX 问题
2. 产出 `review/revision_report.md`，说明每个问题的修复方案
3. 最多 2 轮修复循环

**质量门禁**：
- [ ] 所有 MUST FIX 已修复并验证
- [ ] revision_report.md 逐条对应评审意见
- [ ] 健康检查再次通过

### 阶段 5：交付（Delivery）

1. Evaluator 确认修复通过 → 状态改为 APPROVED
2. Generator 执行 git commit + push
3. 更新 `summary.md` 为 DELIVERED 状态
4. 向用户报告交付结果

---

## Dispatch Routing — 任务分级

根据任务复杂度选择不同流程：

| 级别 | 判断标准 | 流程 |
|------|---------|------|
| **SIMPLE** | <10 行代码，单文件 | 直接 spawn 执行 |
| **MEDIUM** | 多文件，方案明确 | gstack-lite（规划 + 自审） |
| **HEAVY** | 需要特定方法论 | 运行对应 gstack skill |
| **FULL** | 完整功能，多日工作量 | 双 Agent（Generator + Evaluator） |
| **PLAN** | 先规划后实现 | 只产出计划，不写代码 |

### 决策启发式

```
<10 行代码？ → SIMPLE
多文件但方案明显？ → MEDIUM
用户指定了 skill（/qa, /review）？ → HEAVY
功能/项目/目标（不是任务）？ → FULL
用户只想规划不想实现？ → PLAN
```

---

## gstack-lite 规划纪律

注入到所有编码 Agent 的基础纪律：

```markdown
# gstack-lite Planning Discipline

1. Read every file you will modify. Understand existing patterns first.
2. Before writing code, state your plan: what, why, which files, test case, risk.
3. When ambiguous, prefer:
   - completeness over shortcuts
   - existing patterns over new ones
   - reversible choices over irreversible ones
   - safe defaults over clever ones
4. Self-review your changes before reporting done.
   Check for: missed files, broken imports, untested paths, style inconsistencies.
5. Report when done: what shipped, what decisions you made, anything uncertain.
```

---

## 模板文件

### spec.md 模板

```markdown
# 需求规格：{功能名}

## 目标
{一句话描述要实现什么}

## 范围

### 包含
- {功能点 1}
- {功能点 2}

### 不包含
- {明确排除的内容}

## 验收标准
1. {可验证的标准 1}
2. {可验证的标准 2}

## 非目标
- {不在此范围内的内容}
```

### tasks.md 模板

```markdown
# 任务拆分清单

## Task 1: {任务名}

- **描述**: {具体做什么}
- **输入**: {依赖什么}
- **输出**: {产出什么文件/功能}
- **验收标准**:
  - {可验证的检查点 1}
  - {可验证的检查点 2}
```

### summary.md 模板

```markdown
# {type}-{name} — 变更摘要

> Single Source of Truth for this change.
> 创建时间: YYYY-MM-DD
> 状态: PLANNING | CODING | IN_REVIEW | FIXED | DELIVERED

## 基本信息

| 字段 | 值 |
|------|-----|
| 类型 | feat/fix/refactor/chore/docs |
| 需求描述 | {一句话} |
| 负责人 | Generator Agent + Evaluator Agent |
| 创建时间 | {时间} |
| 最后更新 | {时间} |

## 阶段状态

| 阶段 | 状态 | 完成时间 | 备注 |
|------|------|---------|------|
| 1. 规划 | ⏳ 进行中 | — | — |
| 2. 评审 | ⏸ 待开始 | — | — |
| 3. 编码 | ⏸ 待开始 | — | — |
| 4. 自审 | ⏸ 待开始 | — | — |
| 5. 独立评审 | ⏸ 待开始 | — | — |
| 6. 修复 | ⏸ 待开始 | — | — |
| 7. 交付 | ⏸ 待开始 | — | — |
```

### code_review.md 模板

```markdown
# 代码评审报告 v1

**评审对象**: {功能名}
**评审时间**: YYYY-MM-DD
**评审 Agent**: 独立 Code Reviewer

## 评审结论

**状态**: APPROVED | REVISION_REQUIRED

## 发现的问题

### 问题 N: {问题标题}

- **严重程度**: MUST FIX / SHOULD FIX / LOW / INFO
- **位置**: `文件路径` — 描述
- **描述**: {问题说明}
- **当前代码**:
  ```{language}
  {当前代码}
  ```
- **建议**:
  ```{language}
  {建议代码}
  ```
```

### revision_report.md 模板

```markdown
# Revision Report v2

**日期**: YYYY-MM-DD
**作者**: Generator Agent
**评审版本**: code_review_v1.md

## 修复摘要

根据 Evaluator Agent 的评审报告，共修复 **N 个问题**。

## 🔴 MUST FIX 修复

### 1. {问题标题}

**影响文件**:
- `path/to/file1`
- `path/to/file2`

**修复方案**: {说明}

**为什么选择这个方案**: {理由}
```

---

## 核心原则详解

### 1. Generator ≠ Evaluator

- **Generator Agent**：负责规划、编码、自审、修复
- **Evaluator Agent**：负责独立评审，发现 Generator 遗漏的问题
- **为什么分开**：Generator 会对自己写的代码有盲点；独立的 Evaluator 能发现安全隐患、边界情况等

### 2. 质量门禁

每个阶段必须满足门禁标准才能进入下一阶段。不允许跳过门禁。

### 3. 变更审计链

每次需求都创建 `.harness/changes/{type}-{name}-{date}/` 目录，包含：
- 规划文档（spec + tasks）
- 评审报告（code_review + revision_report）
- 变更摘要（summary.md = SSOT）

### 4. 工程化纠错

"每发现一个错误，就工程化地消除它再次发生的可能性。"
- 不只是修复 bug，而是修复**产生 bug 的流程**
- 例如：发现 XSS → 不只是修一处，而是添加 escapeHtml 工具函数并更新规则

---

## 使用方式

当用户要求执行编程任务时：

1. **判断任务级别**（SIMPLE/MEDIUM/HEAVY/FULL/PLAN）
2. **创建变更目录**（MEDIUM 及以上）
3. **按工作流执行**
4. **每个阶段检查质量门禁**
5. **交付后更新 summary.md**

### 简单任务（SIMPLE）

直接执行，不需要创建变更目录和走完整流程。

### 中等任务（MEDIUM）

1. 创建变更目录
2. 写 planning/spec.md + planning/tasks.md
3. 编码 + 自审
4. 更新 summary.md

### 完整任务（FULL）

1. 创建变更目录
2. Generator Agent: spec.md + tasks.md
3. Generator Agent: 编码 + coding_report.md + self_review.md
4. Evaluator Agent: code_review_v1.md
5. 如果有 MUST FIX → Generator Agent 修复 → revision_report.md
6. Evaluator Agent: 确认通过
7. git commit + push
8. 更新 summary.md

---

## 轻量级变体：网站项目

对于单文件 HTML 网站等简单项目，使用轻量流程：

```
规划（3 个问题）→ 实施+自审 → 交付（git commit + 报告）
```

详见 `.harness/rules/website-workflow.md`。

---

## 常见错误

### ❌ 错误：Generator 自己评审自己的代码
**正确做法**：spawn 新的 Agent 作为 Evaluator

### ❌ 错误：跳过规划直接编码
**正确做法**：MEDIUM 及以上任务必须先写 spec.md

### ❌ 错误：评审报告没有分级
**正确做法**：必须按 MUST FIX / SHOULD FIX / LOW / INFO 分级

### ❌ 错误：修复后不验证
**正确做法**：修复后必须重新运行健康检查

### ❌ 错误：summary.md 不更新
**正确做法**：每个阶段完成后更新 summary.md 的阶段状态表

---

## 与其他 gstack 技能的关系

Harness Engineering 是**工作流编排层**，gstack 是**方法论层**：

| gstack 技能 | 用途 | 在 Harness 中的位置 |
|------------|------|-------------------|
| `gstack-openclaw-office-hours` | 产品思考、需求分析 | 阶段 1（规划）前可选 |
| `gstack-openclaw-ceo-review` | 战略挑战、范围审查 | 阶段 1 完成后可选 |
| gstack-lite/full | 规划纪律、编码流程 | 嵌入阶段 2-3 |
| `gstack-openclaw-investigate` | 系统化调试 | 阶段 4 发现问题时使用 |
| `gstack-openclaw-retro` | 工程回顾 | 交付后复盘 |
