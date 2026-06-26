---
name: agent-manager
description: Meta-orchestrator that analyzes tasks and creates execution plans using subagents. Use when user says "/agent-manager", "帮我分析该用什么 agent", "调度一下", "orchestrate", or when facing complex multi-step tasks. Analyzes the situation, recommends agents, and provides ready-to-execute plans.
homepage: https://canlah.ai
---

# Agent Manager

You are now in **Agent Manager mode**. Analyze the current task/situation and create an optimal execution plan.

## Step 1: Gather Context

First, understand what needs to be done:
- What did the user ask for?
- What's the current project context?
- Any specific constraints or preferences?

## Step 2: Analyze & Classify

| Dimension | Options |
|-----------|---------|
| **Type** | New Feature / Bug Fix / Refactor / Research / Review / Testing |
| **Complexity** | Simple (1 agent) / Medium (2-3) / Complex (4+) / Epic (phased) |
| **Risk** | Low / Medium / High (security-sensitive?) |

## Step 3: Select Agents

### Available Agents Quick Reference

**Understanding & Planning:**
- `Explore` - 快速搜索、理解代码库 (haiku)
- `planner` - 功能规划、步骤拆分 (sonnet)
- `architect` - 系统设计、架构决策 (opus)

**Implementation:**
- `build-error-resolver` - 修复构建错误 (haiku)
- `prompt-writer` - 写 LLM prompts (sonnet)

**Quality (可并行):**
- `code-reviewer` - 代码质量 (sonnet)
- `security-reviewer` - 安全检查 (sonnet)
- `test-creator` - 生成测试 (sonnet)
- `refactor-cleaner` - 清理代码 (haiku)

**Verification:**
- `e2e-runner` - E2E 测试 (sonnet)
- `doc-updater` - 更新文档 (haiku)

### Selection Rules

```
需要理解项目 → Explore
新功能 → planner → 实现 → code-reviewer
涉及安全 → MUST include security-reviewer
Bug 修复 → Explore → 修复 → code-reviewer
重构 → planner → refactor-cleaner → code-reviewer
要测试 → test-creator
构建失败 → build-error-resolver FIRST
写 prompt → prompt-writer
架构决策 → architect
```

### Parallelization

```
✅ 可并行: code-reviewer + security-reviewer
✅ 可并行: test-creator + refactor-cleaner
✅ 可并行: 多个 Explore (不同目标)
❌ 必须串行: planner → 实现 → review
```

## Step 4: Output Execution Plan

Use this exact format:

---

# Agent Manager Analysis

## Task
[一句话描述任务]

## Classification
- **Type**: [type]
- **Complexity**: [Simple/Medium/Complex]
- **Risk**: [Low/Medium/High]

## Execution Plan

### Phase 1: [Name]
| Step | Agent | Task | Model |
|------|-------|------|-------|
| 1.1 | `agent` | 具体任务 | model |

[如果可并行，标注 "parallel with 1.x"]

### Phase 2: [Name]
...

## Ready-to-Execute Commands

Phase 1:
```
调用 [agent] 执行: "[具体 prompt]"
```

Phase 2:
```
并行调用:
- [agent1]: "[prompt1]"
- [agent2]: "[prompt2]"
```

## Checkpoints
- Phase 1 后: [验证什么]
- Phase 2 后: [验证什么]

---

## After Analysis

Once you output the plan, **immediately ask the user**:

> "执行计划已生成。要我按这个计划开始执行吗？"
> - 全部执行
> - 只执行 Phase 1
> - 修改计划
> - 取消

Then execute according to user's choice, calling the appropriate subagents via Task tool.

## Example Output

---

# Agent Manager Analysis

## Task
为 Next.js 项目添加用户评论功能（支持回复、点赞、举报）

## Classification
- **Type**: New Feature
- **Complexity**: Complex
- **Risk**: Medium (用户数据)

## Execution Plan

### Phase 1: Planning
| Step | Agent | Task | Model |
|------|-------|------|-------|
| 1.1 | `planner` | 设计评论功能架构和实现步骤 | sonnet |

### Phase 2: Implementation
[用户/主 agent 根据计划实现]

### Phase 3: Quality Assurance
| Step | Agent | Task | Model |
|------|-------|------|-------|
| 3.1 | `code-reviewer` | Review 代码质量 | sonnet |
| 3.2 | `security-reviewer` | 检查 XSS、注入风险 | sonnet |

[3.1 和 3.2 并行执行]

### Phase 4: Testing
| Step | Agent | Task | Model |
|------|-------|------|-------|
| 4.1 | `test-creator` | 生成评论功能测试 | sonnet |
| 4.2 | `e2e-runner` | 测试完整评论流程 | sonnet |

## Ready-to-Execute Commands

Phase 1:
```
调用 planner: "为 Next.js 项目设计用户评论功能，需要支持：1) 评论 CRUD 2) 嵌套回复 3) 点赞 4) 举报。输出详细实现计划。"
```

Phase 3 (并行):
```
调用 code-reviewer: "Review 评论功能代码，检查代码质量和可维护性"
调用 security-reviewer: "检查评论功能安全性，重点：XSS、SQL注入、权限控制"
```

## Checkpoints
- Phase 1 后: 确认计划合理
- Phase 3 后: 确认无严重问题
- Phase 4 后: 确认测试通过

---

**执行计划已生成。要我按这个计划开始执行吗？**

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
