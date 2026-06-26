---
name: iterative-code-review
displayName: Iterative Code Review
description: |
  Iterative code review using multiple independent subagent reviews. Use when user asks to review PR, code, or mentions "review", "审查", "检查代码", "代码质量". Assists with code review through parallel subagent analysis and optional automated fixes.
license: MIT
version: 1.2.0
metadata:
  {"openclaw":{"emoji":"🔍","category":"code-quality"}}
compatibility: |
  Required tools: git, gh (GitHub CLI), jq, node/npm
  Optional: openclaw CLI
---

# Code Review Skill

Iterative code review through **parallel independent subagent reviews** with user confirmation at each step.

## ⚠️ 用户控制 vs 自动化

**默认行为（安全模式）**：
- ✅ 每一步都需要用户确认
- ❌ 不会自动修改代码

**可选：自动化模式（需手动启用）**：

用户可通过配置文件启用 `autoFix` 和 `autoContinue`。详见 [references/automation.md](references/automation.md)。

```
┌─────────────────────────────────────────────────────────┐
│  默认：安全模式                                          │
│  - 每步都需要用户确认                                    │
│  - 适合：重要项目、首次使用                               │
│                                                          │
│  可选：自动化模式（需要手动配置启用）                      │
│  - autoFix=true: 发现问题后自动修复                       │
│  - autoContinue=true: 修复后自动继续下一轮                │
│  ⚠️ 警告：会自动修改代码！                                │
└─────────────────────────────────────────────────────────┘
```

---

## Pre-flight Checks

开始 Review 前，必须执行以下检查：

| Check | 说明 |
|-------|------|
| **Model Selection** | 用户选择或确认使用的模型 |
| **maxSpawnDepth** | `≥1` 才能继续 |
| **变更规模检测** | 根据文件数调整超时时间 |
| **新增代码识别** | 审查新增代码的安全性 |
| **PR 历史检查** | 避免重复发现已修复的问题 |
| **Review 模式** | Full Review 或 Delta Review |

详见 [references/preflight.md](references/preflight.md)。

---

## Workflow

### Round Structure

```
┌─────────────────────────────────────────────────────────┐
│  Review Round N                                          │
│                                                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                  │
│  │Reviewer1│  │Reviewer2│  │Reviewer3│  ← 并行 3 个      │
│  └────┬────┘  └────┬────┘  └────┬────┘                  │
│       └────────────┼────────────┘                        │
│                    ▼                                     │
│            ┌──────────────┐                              │
│            │ 汇总问题列表  │                              │
│            └──────┬───────┘                              │
│                   ▼                                      │
│            ┌──────────────┐                              │
│            │  用户确认    │  ← 是否继续修复？            │
│            └──────┬───────┘                              │
│                   ▼                                      │
│            ┌──────────────┐                              │
│            │   Fixer      │  ← 用户同意后才执行          │
│            └──────────────┘                              │
└─────────────────────────────────────────────────────────┘
```

### Reviewer 关注点

| Reviewer | 关注点 |
|----------|--------|
| Reviewer-1 | 功能正确性、测试覆盖 |
| Reviewer-2 | 代码质量、最佳实践 |
| Reviewer-3 | 安全性、边界情况 |

详见 [references/workflow.md](references/workflow.md)。

---

## 退出标准

- 连续 **两轮** 无 >= severityThreshold 的问题
- 或达到 maxRounds 限制
- 用户决定结束

---

## Final Round 特殊要求

**Final Round 必须采用 Full Review 模式！**

1. **必须 Full Review** - 不是 Delta Review
2. **必须验证编译和测试** - `npm run build` + `npm test`
3. **使用更长超时** - 全量审查需要更多时间
4. **审查所有历史修复** - 确认所有 Round 的问题都已修复

---

## Issue Severity

| Level | Definition | Fix |
|-------|------------|-----|
| P0 | Critical | 建议 |
| P1 | High | 建议 |
| P2 | Medium | 建议 |
| P3 | Low | 可选 |

---

## Key Points

1. **用户控制** - 默认每一步都需要用户确认
2. **自动化可选** - 通过配置启用自动修复
3. **PR 历史检查** - 避免重复发现已修复的问题
4. **Final Round 必须 Full Review** - 全量审核
5. **3 个 reviewer 并行** - 最大化问题发现
6. **MAX_ROUNDS = 10** - 防止无限循环

---

## Safety Boundaries

**✅ 允许**：读取代码、运行只读命令、Spawn subagent 分析、报告问题

**⚠️ 需确认**：修改文件、git commit、npm install/build、Spawn Fixer

**❌ 禁止**：未经同意修改代码、自主运行多轮修复、自主提交

---

## References

- [automation.md](references/automation.md) - 自动化偏好配置详解
- [preflight.md](references/preflight.md) - Pre-flight Checks 详细步骤
- [workflow.md](references/workflow.md) - Workflow 详细说明
- [checklist.md](references/checklist.md) - 审查清单
- [issue-severity.md](references/issue-severity.md) - Issue 严重级别
- [final-round.md](references/final-round.md) - Final Round 详细指南