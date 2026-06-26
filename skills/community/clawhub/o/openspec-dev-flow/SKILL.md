---
name: openspec-workflow
description: 基于 OpenSpec 的迭代开发流程。适用于任何创建任务，包括 skill 开发、功能开发、重构、bug 修复等。当用户要求创建、开发、实现任何东西时，或当用户说"按 OpenSpec 流程来"、"走 spec 流程"、"按规范开发"时触发此技能。
---

# OpenSpec 迭代开发流程

基于 [OpenSpec](https://github.com/Fission-AI/OpenSpec) 的规范驱动开发流程，适用于一切创建和迭代任务。

## 核心哲学

```
→ 流动而非僵化 — Actions, not phases。命令是你可做的事，不是你被困住的阶段
→ 迭代而非瀑布 — 边建边学，随时修正。依赖关系是使能器，不是强制门控
→ 简单而非复杂 — 最轻量的规范，按需加深（Progressive Rigor）
→ 增量而非全量 — delta spec 描述变更，不重写全部
→ 先同意再构建 — 任何产物写出前必须与用户确认
→ Brownfield-first — 面向现有代码库的变更优先，而非全新系统
```

## 工作模式

OpenSpec 支持两种工作模式，本 skill 默认使用 **Core Profile**（快速路径），但支持 Expanded Workflow 的完整功能。

### 模式对比

| 特性 | Core Profile (默认) | Expanded Workflow |
|-----|-------------------|-------------------|
| 流程 | `/opsx:propose → /opsx:apply → /opsx:archive` | `/opsx:new → /opsx:ff/continue → /opsx:apply → /opsx:verify → /opsx:archive` |
| 适用场景 | 清晰需求，快速执行 | 需要逐步控制，复杂变更 |
| 创建方式 | 一步创建所有规划产物 | 逐步创建，每步确认 |
| 验证步骤 | 可选 | 推荐（`/opsx:verify`） |

### 模式选择原则

- **使用 Core Profile（`/opsx:propose`）**：需求明确，可以直接描述完整范围
- **使用 Expanded（`/opsx:new + /opsx:continue`）**：边探索边规划，需要逐步审查
- **使用 Fast-Forward（`/opsx:ff`）**：Expanded 模式下，范围清晰但想要显式控制开始

## 目录结构

每次变更在工作区 `openspec/` 下维护：

```
openspec/
├── specs/                  # 系统真相（当前行为描述）
│   └── <domain>/           # 按领域组织
│       └── spec.md
├── changes/                # 活跃变更（一个变更一个文件夹）
│   └── <change-name>/
│       ├── .openspec.yaml  # 变更元数据（可选）
│       ├── proposal.md     # 意图、范围、方案
│       ├── design.md       # 技术方案
│       ├── tasks.md        # 实现清单
│       └── specs/          # Delta specs（变更内容）
│           └── <domain>/
│               └── spec.md
├── changes/archive/        # 已归档变更
│   └── YYYY-MM-DD-<name>/  # 按日期归档
└── config.yaml             # 项目配置（可选）
```

### Spec 组织方式（Domain）

按领域组织 spec，选择适合项目的策略：

| 策略 | 示例 | 适用场景 |
|-----|------|---------|
| **按功能区域** | `auth/`, `payments/`, `search/` | 大多数项目 |
| **按组件** | `api/`, `frontend/`, `workers/` | 技术架构清晰 |
| **按限界上下文** | `ordering/`, `fulfillment/`, `inventory/` | DDD 风格 |

**关键原则**：
- 一个 domain = 一个逻辑分组
- spec 描述**行为契约**，不是实现计划
- 避免在 spec 中包含：内部类/函数名、库/框架选择、逐步实现细节

## 流程步骤

### Step 1: Explore（可选）

需求不明确时先探索。

- 调查代码库、分析现状
- 列出可选方案
- 明确需求边界
- **不产生任何 artifact**

### Step 2: Propose — 创建变更 + 规划产物

⚠️ **关键：这是交互式流程，不是一步到位的。必须分阶段与用户确认。**

#### 2.1 信息收集（必须）

在创建任何文件之前，先与用户讨论并确认以下信息：

1. **意图（Intent）**：为什么要做这件事？解决什么问题？
2. **范围（Scope）**：
   - 做什么？（In scope）
   - 不做什么？（Out of scope）
3. **方案（Approach）**：高层面怎么做？

**收集方式：**
- 如果用户需求描述已经很清晰，可以直接整理成 proposal 草稿让用户确认
- 如果用户需求模糊，必须先追问关键问题：
  - "这个功能的预期用户是谁？"
  - "有没有参考示例或竞品？"
  - "哪些边界情况需要处理？"
  - "有没有不想做的部分？"
  - "对技术栈有偏好吗？"
- 用简洁的列表展示收集到的信息，请用户确认或补充

**确认话术示例：**
```
我来确认一下需求：
- 意图：...
- 范围：...
- 方案：...

这样理解对吗？有需要补充或修改的吗？
```

#### 2.2 创建 proposal.md（用户确认后）

收到用户确认后，创建 `proposal.md` 并**再次请用户审阅**：

```
我写了一个 proposal，核心要点：
- ...
- ...
- ...

请看看有没有遗漏或需要调整的。
```

#### 2.3 创建其余产物（用户确认 proposal 后）

proposal 确认后，依次创建：

```
openspec/changes/<change-name>/
├── proposal.md     # 已确认
├── specs/          # Delta specs — 需求变更（ADDED/MODIFIED/REMOVED）
├── design.md       # 技术方案
└── tasks.md        # 实现清单（checkbox）
```

**创建完后展示任务清单摘要，请用户确认可以开始实现。**

### Artifact 依赖关系

产物按依赖顺序创建，依赖关系是**使能器**（什么可以创建），不是**强制门控**（必须创建什么）：

```
                    proposal
                   (root node)
                        │
          ┌─────────────┴─────────────┐
          │                           │
          ▼                           ▼
       specs                       design
   (requires:                  (requires:
    proposal)                   proposal)
          │                           │
          └─────────────┬─────────────┘
                        │
                        ▼
                     tasks
                 (requires:
                 specs, design)
```

**关键理解**：
- `specs` 和 `design` 可以并行创建（都只依赖 proposal）
- `tasks` 需要 `specs` 和 `design` 都完成后才能创建
- 可以跳过 `design`（如果不需要）
- 任何时候都可以回退更新已创建的产物

**proposal.md 格式：**

```markdown
# Proposal: <标题>

## Intent（意图）
为什么做这件事？

## Scope（范围）
### In scope
- ...

### Out of scope
- ...

## Approach（方案）
高层面怎么做？
```

**Delta specs 格式（specs/下）：**

```markdown
# Delta for <Domain>

## ADDED Requirements

### Requirement: <名称>
The system SHALL/MUST/SHOULD ...

#### Scenario: <场景名>
- GIVEN ...
- WHEN ...
- THEN ...

## MODIFIED Requirements
### Requirement: <名称>
(Previously: ...)

## REMOVED Requirements
### Requirement: <名称>
(原因)
```

### Spec 写作规范

**RFC 2119 关键词**（表示需求强度）：

| 关键词 | 含义 | 使用场景 |
|-------|------|---------|
| `MUST` / `SHALL` | 绝对要求 | 不可偏离的核心行为 |
| `SHOULD` | 推荐 | 允许例外，但需充分理由 |
| `MAY` | 可选 | 真正可选的功能 |

**Scenario 格式**（Given/When/Then）：
- `GIVEN` - 初始状态/前置条件
- `WHEN` - 触发动作/事件
- `THEN` - 预期结果/后置条件
- `AND` - 补充条件

**示例**：

```markdown
### Requirement: User Authentication
The system MUST issue a JWT token upon successful login.

#### Scenario: Valid credentials
- GIVEN a user with valid credentials
- WHEN the user submits login form
- THEN a JWT token is returned
- AND the user is redirected to dashboard

#### Scenario: Invalid credentials
- GIVEN invalid credentials
- WHEN the user submits login form
- THEN an error message is displayed
- AND no token is issued
```

**Progressive Rigor（渐进严谨度）**：

大多数变更使用 **Lite spec**（默认），保持轻量：

- ✅ 短小精悍的行为优先需求
- ✅ 清晰的范围和非目标
- ✅ 几个具体的验收检查

仅在以下情况使用 **Full spec**：

- 跨团队/跨仓库变更
- API/合约变更、迁移、安全/隐私相关
- 模糊可能导致昂贵返工的变更

**design.md 格式：**

```markdown
# Design: <标题>

## Technical Approach
技术方案概述

## Architecture Decisions
### Decision: <决策标题>
选择 X 因为...

## Data Flow / File Changes
...
```

**tasks.md 格式：**

```markdown
# Tasks

## 1. <分组名>
- [ ] 1.1 <任务描述>
- [ ] 1.2 <任务描述>

## 2. <分组名>
- [ ] 2.1 <任务描述>
```

### Step 3: Apply — 逐项实现

1. 读取 `tasks.md`
2. 按顺序实现每个未完成的任务
3. 每完成一组任务后向用户汇报进度
4. 完成后标记 `[x]`
5. 实现中发现问题可回退更新 design.md / proposal.md（需告知用户）
6. 中断后可从上次进度继续

**实现原则：**
- 严格按 tasks.md 顺序执行
- 每完成一组任务汇报一次进度
- 发现方案问题时先更新 artifact 再继续，并告知用户变更原因
- 保持上下文干净，避免偏离

### Step 4: Verify — 验证实现（推荐）

从三个维度验证并**向用户汇报结果**：

| 维度 | 英文 | 检查内容 |
|------|------|---------|
| **完整性** | Completeness | 所有 task 已完成，所有需求有对应代码，场景已覆盖 |
| **正确性** | Correctness | 实现符合 spec 意图，边界情况已处理，错误状态匹配 |
| **一致性** | Coherence | 设计决策反映在代码中，命名与设计一致 |

**验证输出示例**：

```markdown
Verifying add-auth...

COMPLETENESS
✓ All 12 tasks in tasks.md are checked
✓ All requirements in specs have corresponding code
⚠ Scenario "Session timeout after inactivity" not tested

CORRECTNESS
✓ Implementation matches spec intent
✓ Edge cases from scenarios are handled
✓ Error states match spec definitions

COHERENCE
✓ Design decisions reflected in code structure
✓ Naming conventions consistent with design.md
⚠ Design mentions "event-driven" but implementation uses polling

SUMMARY
─────────────────────────────
Critical issues: 0
Warnings: 2
Ready to archive: Yes (with warnings)

Recommendations:
1. Add test for session timeout scenario
2. Consider refactoring to event-driven as designed, or update design.md
```

验证不阻塞归档，但应修复 Critical 问题。

### Step 5: Archive — 归档变更

1. 合并 delta specs 到 `openspec/specs/`
2. 移动变更文件夹到 `openspec/changes/archive/YYYY-MM-DD-<name>/`
3. 保留完整历史用于审计
4. 通知用户变更已归档

## 工作流模式

### Quick Feature（快速功能）

需求明确，直接执行：

```yaml
触发: /opsx:propose add-dark-mode
流程: propose → apply → archive
适用: 小到中等功能、简单 bug 修复
```

### Exploratory（探索式）

需求不清晰，先调查：

```yaml
触发: /opsx:explore
流程: explore → /opsx:new → /opsx:continue → ... → /opsx:apply
示例对话:
  User: /opsx:explore
  AI: What would you like to explore?
  User: I want to improve page load performance but not sure where bottlenecks are.
  AI: [Analyzes bundle sizes, queries, render patterns]
      Found three bottlenecks:
      1. Large unoptimized images
      2. Synchronous data fetching in ProductList
      3. Re-renders from context changes
      Which to address first?
适用: 性能优化、调试、架构决策、需求模糊
```

### Parallel Changes（并行变更）

同时处理多个变更：

```yaml
场景: 正在 add-dark-mode，被 pull 去修 bug
流程:
  Change A: /opsx:propose → /opsx:apply (进行中)
                                        │ context switch
                                        │
  Change B: /opsx:propose → ──────────→ /opsx:apply

完成后: /opsx:bulk-archive 批量归档
适用: 并行工作流、紧急中断、团队协作
```

**`/opsx:bulk-archive` 示例**：

```yaml
AI: Found 3 completed changes:
   - add-dark-mode (all tasks done)
   - fix-login-redirect (all tasks done)
   - update-footer (all tasks done)

   Checking for spec conflicts...
   ⚠ add-dark-mode and update-footer both touch specs/ui/

   Inspecting codebase to resolve...
   Both changes are implemented. Will apply in chronological order.

   Archive all 3 changes?
适用: 多变更并行完成后，自动检测冲突并解决
```

### `/opsx:onboard`（引导式教程）

首次使用或学习完整流程：

```yaml
功能: 使用实际代码库的完整工作流教程
阶段:
  1. 扫描代码库找改进机会
  2. 创建真实变更
  3. 实现真实工作（小而安全的变更）
  4. 完成归档
  5. 每步都有讲解
时间: 15-30 分钟
结果: 获得一个真实的已归档变更
```

## 更新 vs 新建

| 情况 | 操作 |
|------|------|
| 同一意图，方案微调 | 更新现有变更 |
| 范围收窄（先 MVP） | 更新然后归档，再新建后续 |
| 意图根本改变 | 新建变更 |
| 范围膨胀超 50% | 新建变更 |
| 原变更可以独立完成 | 归档原变更，新建后续 |

## 命令速查

本 skill 在 Claude Code 环境中不使用 `/opsx:*` 斜杠命令，而是由 agent 直接执行文件操作。映射关系：

| OpenSpec 命令 | 本 skill 对应操作 |
|--------------|-----------------|
| `/opsx:explore` | 调查分析，不创建文件 |
| `/opsx:propose` | 信息收集 → 用户确认 → 创建 proposal → 用户确认 → 创建其余产物 |
| `/opsx:new` | 创建变更 scaffold，等待 /opsx:continue 或 /opsx:ff |
| `/opsx:continue` | 逐步创建下一个 artifact（基于依赖关系） |
| `/opsx:ff` | Fast-forward，一次性创建所有规划产物 |
| `/opsx:apply` | 逐项实现 tasks.md，分组汇报进度 |
| `/opsx:verify` | 三维度验证实现（Completeness/Correctness/Coherence），汇报结果 |
| `/opsx:sync` | 可选命令，提前合并 delta specs 到 main（归档时会自动处理） |
| `/opsx:archive` | 合并 specs + 移动到 archive/YYYY-MM-DD-<name>/，通知用户 |
| `/opsx:bulk-archive` | 批量归档多个完成变更，自动检测和解决 spec 冲突 |
| `/opsx:onboard` | 引导式教程，使用实际代码库完成完整工作流 |

**注意**：
- Core Profile 默认路径：`propose → apply → archive`
- Expanded Workflow 支持更细粒度的控制
- 不同 AI 工具的命令语法可能不同（Cursor 用 `/opsx-propose`）

### `/opsx:ff` vs `/opsx:continue` 选择指南

| 场景 | 使用 |
|-----|------|
| 需求明确，准备好构建 | `/opsx:ff` |
| 探索中，想逐步审查 | `/opsx:continue` |
| 想 specs 之前迭代 proposal | `/opsx:continue` |
| 时间压力，需要快速推进 | `/opsx:ff` |
| 复杂变更，需要控制 | `/opsx:continue` |

**经验法则**：如果可以提前描述完整范围，用 `/opsx:ff`；如果边做边摸索，用 `/opsx:continue`。

## 适用场景

- ✅ Skill 开发
- ✅ 功能开发
- ✅ Bug 修复（复杂 bug）
- ✅ 重构
- ✅ 架构调整
- ✅ 任何需要 > 1 步的创建任务

## 不适用场景

- ❌ 单行命令执行
- ❌ 简单问答
- ❌ 信息查询

## 注意事项

- 变更命名用 kebab-case：`add-dark-mode`、`fix-login-redirect`
- Delta spec 只写变更部分，不重写全部 spec
- tasks.md 要细分到单次可完成的粒度
- 长任务中保持上下文卫生，避免累积过多无关信息
- **每个阶段都要与用户确认，不要自作主张**
- 如果用户说"直接搞"或"不用确认"，可以跳过确认环节快速执行

## 术语表

| 术语 | 定义 |
|-----|------|
| **Artifact** | 变更文件夹中的文档（proposal、design、tasks、delta specs） |
| **Archive** | 完成变更的过程，将 delta specs 合并到 main specs |
| **Change** | 系统的提议修改，打包为一个包含 artifacts 的文件夹 |
| **Delta spec** | 描述相对于当前 specs 的变更（ADDED/MODIFIED/REMOVED） |
| **Domain** | spec 的逻辑分组（如 `auth/`、`payments/`） |
| **Requirement** | 系统必须具备的特定行为 |
| **Scenario** | 需求的具体示例，通常使用 Given/When/Then 格式 |
| **Schema** | artifact 类型及其依赖关系的定义 |
| **Spec** | 描述系统行为的规范，包含 requirements 和 scenarios |
| **Source of truth** | `openspec/specs/` 目录，包含当前约定的行为 |

## 参考资源

- [OpenSpec 官方文档](https://github.com/Fission-AI/OpenSpec)
- Getting Started: https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md
- Workflows: https://github.com/Fission-AI/OpenSpec/blob/main/docs/workflows.md
- Commands: https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md
- Concepts: https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md
