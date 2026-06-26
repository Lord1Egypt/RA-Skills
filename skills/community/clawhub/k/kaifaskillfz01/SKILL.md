---
name: dev-workflow
description: |
  结构化开发工作流，强制执行 Plan → Implement → Review 流程。
  触发条件：
  (1) 用户输入 KAIFA## 命令
  (2) 自然语言包含开发类关键词："开发"+"SKILL/APP/应用/系统/模块/功能/工具"、"实现"+"功能/模块"、"写"+"模块/系统/服务"、"重构"、"新建"+"项目/模块"
  (3) 不确定时反问用户确认
  不触发：简单单文件修改、配置更新、查询类请求、小bug修复
  支持多角色子 agent 协作（Architect/Developer/Reviewer），自动按复杂度分配模型（pro=深度推理，flash=确定性执行），产出的 Plan 和 Review 归档到 plans/ 目录。
---

# Dev Workflow — 结构化开发流程

强制 Plan → Implement → Review 的结构化开发流程，支持多角色子 agent 协作和模型成本优化。

## 触发判断

### 显式触发
用户输入 `KAIFA##`（可带描述文本）→ 无条件进入开发模式。

### 自然语言触发
匹配以下模式时自动进入：
- `开发` + `SKILL/APP/应用/系统/模块/功能/工具`
- `实现` + 功能描述
- `写` + `模块/系统/服务`
- `重构` + 代码/模块
- `新建` + `项目/模块`

### 不触发
- "修复一个小bug"、"改一下配置"、"帮我查一下"、"解释这段代码"
- 单文件修改、查询类请求
- 纯咨询/讨论类问题

### 不确定时
发确认卡：
```
🤔 这个需求是否需要走开发模式（Plan→Implement→Review）？
```

---

## 核心流程（强制，不可跳过）

```
PHASE 0: ASSESS    → 评估复杂度 + 决定团队 + 分配模型
PHASE 1: PLAN      → 产出设计方案文档
     ⛔ APPROVAL   → 用户一次性审批，通过才继续
PHASE 2: IMPLEMENT → spawn Developer 子 agent 编码
PHASE 3: REVIEW    → spawn Reviewer 子 agent 审查
     ⛔ BLOCKER?   → 有 BLOCKER 标记给用户决策
PHASE 4: REPORT    → 汇总结果，归档
```

---

## PHASE 0: ASSESS（评估）

由 PM（主 agent）完成，输出简短评估卡：

```
📊 复杂度评估
- 级别: 简单 / 中等 / 复杂
- 理由: (一句话)
- 团队: PM → Developer → Reviewer  |  PM → Architect → Developer → Reviewer
- 模型分配:
  · Architect: pro (如果需要)
  · Developer: flash
  · Reviewer: pro / flash
```

### 复杂度判断标准

| 维度 | 简单 | 中等 | 复杂 |
|------|------|------|------|
| 文件数 | 1-2 | 3-5 | 5+ |
| 依赖关系 | 无外部依赖 | 有外部依赖 | 多系统协调 |
| 架构影响 | 局部修改 | 模块级别 | 系统级别 |
| 技术风险 | 低 | 中 | 高 |

### 模型分配规则

| 角色 | 简单 | 中等 | 复杂 |
|------|------|------|------|
| **Architect** | 不启用 | 不启用(PM 兼) | `deepseek-v4-pro` |
| **Developer** | `deepseek-v4-flash` | `deepseek-v4-flash` | `deepseek-v4-flash` |
| **Reviewer** | `deepseek-v4-flash` | `deepseek-v4-pro` | `deepseek-v4-pro` |

**原则**：
- flash：确定性执行（已知输入 + 明确方案 → 写代码），省钱
- pro：深度推理（多维度权衡、对照分析、风险评估）
- Reviewer 在简单场景可用 flash（快速扫一眼），中等及以上必须用 pro

---

## PHASE 1: PLAN（方案设计）

由 PM（主 agent）完成，输出到 `plans/YYYY-MM-DD-<slug>-plan.md`。

### 输出内容

参照 `references/plan-template.md`，必须包含：
1. 需求分析（目标 + 使用场景）
2. 架构设计（模块划分、数据流、技术选型）
3. API/接口定义（输入输出、边界条件）
4. 数据模型（核心实体和关系）
5. 边界情况 & 风险
6. 模型分配方案

### Slug 安全规则

从用户需求中提取 slug（功能名缩写），仅允许 `[a-z0-9-]+`，长度 ≤ 50。不能提取时 fallback 为 `unnamed-task`。

### 输出方式

1. 将完整 Plan 写入 `plans/YYYY-MM-DD-<slug>-plan.md`（slug 必须经过规范化）
2. 在对话中输出结构化的 Plan 摘要
3. 末尾带审批提示

---

## ⛔ APPROVAL GATE（审批闸门）

Plan 输出后，必须等待用户审批。提示格式：

```
⛔ APPROVAL REQUIRED
完整 Plan: plans/YYYY-MM-DD-<slug>-plan.md
请确认：
  ✅ Approved → 进入 Implement
  ✏️ Modify  → 需要调整…
  ❌ Reject  → 回到 Phase 1 重新 Plan
```

**规则**：
- 用户明确说 "Approved"/"OK"/"通过"/"开始实现" → 进入 Implement
- 用户说修改意见 → 更新 Plan 后再次审批
- 用户 Reject → 回到 Phase 1 重新 Plan
- **未审批通过，绝不进入 Implement**

---

## PHASE 2: IMPLEMENT（编码实现）

审批通过后，spawn Developer 子 agent 执行。

### Developer 子 agent 参数

```yaml
runtime: subagent
context: isolated
model: deepseek-v4-flash  # 默认，复杂场景可在 Assess 阶段覆盖
label: "developer-<slug>"
task: |
  你是 Developer，基于以下 Plan 实现代码：
  
  [Plan 文档内容]
  
  要求：
  1. 严格按 Plan 中的架构和接口定义实现
  2. 处理 Plan 中列出的所有边界情况
  3. 不引入 Plan 之外的依赖
  4. 代码风格清晰，关键逻辑加注释
  5. 完成后列出所有修改/新建的文件清单
  6. 如有已知限制，明确列出
```

### 输出要求

Developer 完成后应输出：
- 修改/新建的文件清单
- 关键实现说明
- 已知限制（如有）

### 失败处理

- Developer 子 agent 出错 → PM 检查错误原因，修复后重新 spawn（最多重试 2 次）
- 2 次重试后仍失败 → 标记给用户，附带已尝试的方案和错误信息
- 重试时使用相同的 Plan（不修改方案，除非用户要求）

---

## PHASE 3: REVIEW（代码审查）

Implement 完成后，spawn Reviewer 子 agent 审查。

### Reviewer 子 agent 参数

```yaml
runtime: subagent
context: isolated
model: deepseek-v4-pro  # 默认，简单场景可用 flash
label: "reviewer-<slug>"
task: |
  你是 Reviewer，对照以下 Plan 审查实现代码：
  
  ## Plan
  [Plan 文档内容]
  
  ## 实现
  [Developer 输出的文件清单 + 代码]
  
  使用 references/review-checklist.md 中的检查清单逐项审查。
  对每个问题标注严重程度：🔴 BLOCKER / 🟡 MAJOR / 🟢 MINOR
```

### Review 输出

写入 `plans/YYYY-MM-DD-<slug>-review.md`，格式参照 `references/review-checklist.md`。

---

## ⛔ BLOCKER 处理

Review 完成后：

| 最高严重度 | 处理 |
|-----------|------|
| 🔴 BLOCKER | **停止流程**，输出 Review Report，标记给用户决策 |
| 🟡 MAJOR | 输出 Review Report，建议修复，给用户两个选项：A) 回到 Implement 修复 B) 标记已知问题继续 |
| 🟢 MINOR | 记录在 Report 中，进入 Report 阶段 |
| 无问题 | 进入 Report 阶段 |

### 循环计数器

每次 Review 发现 BLOCKER 后进入修复循环，PM 需跟踪循环次数：
- 第 1-2 次：正常处理，给用户 A/B/C 选项
- 第 3 次及以上：**强制标记用户**，提示"已修复 N 次仍存在 BLOCKER，建议重新评估方案"

### 用户决策选项（有 BLOCKER 时）

```
🔴 Review 发现 BLOCKER 级别问题，无法继续。
完整 Report: plans/YYYY-MM-DD-<slug>-review.md
修复循环: 第 N 次

请决策：
  A) 回到 Implement → 修复问题
  B) 回到 Plan → 重新设计
  C) 接受风险 → 继续进入 Report（记录已知问题）
```

---

## PHASE 4: REPORT（汇总报告）

汇总全部产出，给出最终报告：

```
📋 开发报告 — <功能名称>

| 阶段 | 状态 | 产出 |
|------|------|------|
| Plan | ✅ | plans/<slug>-plan.md |
| Implement | ✅ | (文件清单) |
| Review | ✅/⚠️/❌ | plans/<slug>-review.md |

遗留问题: (Review 中的 MINOR/MAJOR 项)
后续建议: (如有)
```

---

## 流程变体

详见 `references/workflow-variants.md`。

### 快速模式
用户说"快速开发"/"简单开发" → Plan 精简（跳过架构设计章节），Review 用 flash

### 严格模式
用户说"严格模式"/"核心功能" → 启用 Architect 子 agent（由 Architect 产出 Plan 方案，PM 审批后传递给 Developer）+ 深度 Review

### 仅审查
用户说"审查这段代码"/"review this" → 跳过 Assess/Plan/Implement，直接 Review（不使用 Plan 对照，仅审查代码质量本身）

### 重构模式
用户说"重构" → Plan 阶段聚焦重构方案（现状分析 + 目标架构 + 迁移步骤 + 兼容性考虑）

---

## 归档规范

```
plans/
├── YYYY-MM-DD-<slug>-plan.md     # Plan 文档
├── YYYY-MM-DD-<slug>-review.md   # Review Report
└── ...
```

- slug: 功能名缩写，仅允许小写字母、数字和连字符 `[a-z0-9-]+`，长度 ≤ 50，如 `user-login`, `payment-refactor`
- slug 不能包含路径分隔符（`/`、`..`），提取时自动过滤
- 无法提取功能名时 fallback 为 `unnamed-task`
- 如果 slug 同一天重复（罕见），追加数字后缀

---

## 子 Agent 执行期间的中断处理

- 用户在 Implement 或 Review 期间发送新消息 → PM 等待子 agent 完成后统一响应
- 用户明确要求中断（"停止"/"取消"） → PM kill 子 agent，记录当前状态，等待用户下一步指令
- 子 agent 超时无响应 → 标记用户，询问是否重试或调整

## 约束与原则

1. **审批闸门不可绕过** — Plan 未审批通过，绝不进入 Implement
2. **Plan 优先于代码** — 先想清楚再写
3. **Review 对照 Plan** — 不只审查代码，还要检查是否偏离设计
4. **成本意识** — 能用 flash 的不用 pro，Reviewer 质量不妥协
5. **追溯归档** — 每次开发都有 Plan + Review 记录
6. **不确定时反问** — 不要假装确定触发条件
