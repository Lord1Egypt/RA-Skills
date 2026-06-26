---
name: insight-tracker
version: 1.0.2
description: Track, categorize, search, and analyze insights, patterns, and observations discovered during OpenClaw sessions. Use when the user wants to record, retrieve, or analyze insights from conversations, research, or task execution. Supports tagging, priority marking, and cross-referencing with existing knowledge.
---

# Insight Tracker

## 🚀 First-Success Path (30秒上手)

**记录一条洞察：**
```
insight add "用户更喜欢简洁的回复风格，长篇大论反而降低满意度" --tags user-preference,learning --priority high
```

**查询已有洞察：**
```
insight list --tag user-preference
```

三步即用：添加 → 打标签 → 随时检索。

## Sample Prompts（输入→输出示例）

### Sample 1: 记录新洞察

**用户输入：**
```
记一下：我发现当回复中包含具体代码示例时，用户的满意度明显更高
```

**Expected Output：**
> ✅ 洞察已记录
> ```
> INS-0042: 包含具体代码示例的回复满意度更高
> Tags: learning, pattern
> Priority: medium
> Status: active
> ```
> 
> 是否需要关联已有洞察或添加更具体的标签？

### Sample 2: 按标签检索洞察

**用户输入：**
```
查一下所有关于用户偏好的高优先级洞察
```

**Expected Output：**
> 📋 高优先级洞察 (标签: user-preference)
> ---------
> 1. **INS-0010** | 用户更倾向中文回复，即使提问是英文 | 2026-04-10
> 2. **INS-0022** | 用户不喜欢重复确认，偏好直接执行 | 2026-05-03
> 3. **INS-0035** | 工作日晚上用户响应最快 | 2026-05-28
> 4. **INS-0042** | 代码示例提升满意度 | 2026-06-01
> ---------
> 共 4 条。是否需要导出或进一步分析趋势？

### Sample 3: 关联分析

**用户输入：**
```
把这些洞察按主题分组，看看有什么规律
```

**Expected Output：**
> 📊 洞察主题聚类
> ---------
> **主题：回复风格偏好**（4条相关）
> - 用户偏好简洁回复
> - 代码示例提升满意度
> - 分点式比段落式更受欢迎
> - 避免过度礼貌用语
> 
> **主题：响应时机**（3条相关）
> - 工作日晚上响应最快
> - 周末上午适合推送
> - 重复确认降低响应意愿
> ---------
> 
> 💡 建议：这几个主题可以整理成一份"用户交互指南"供后续参考。

### Sample 4: 归档陈旧洞察

**用户输入：**
```
INS-0003 那个洞察已经过时了，归档吧
```

**Expected Output：**
> ✅ INS-0003 已归档
> 原内容：用户反馈图片加载较慢（2025-12-01创建）
> 归档原因：已确认该问题已修复，不再相关

### Sample 5: 生成洞察摘要

**用户输入：**
```
帮我总结一下这周记录的所有洞察
```

**Expected Output：**
> 📅 本周洞察摘要（2026-06-09 ~ 2026-06-16）
> ---------
> **新增洞察：** 5条
> - 高优先级：2条
> - 中优先级：2条
> - 低优先级：1条
> 
> **热门标签：** pattern(3), learning(2), user-preference(2)
> 
> **值得关注：**
> - INS-0042：代码示例提升满意度（已验证2次）
> - INS-0043：傍晚时分搜索意图最明确（待验证）
> ---------
> 
> 是否需要将本周高价值洞察同步到知识库？

## Overview

This skill provides structured insight management for OpenClaw workflows. It captures observations, patterns, and learnings that emerge during sessions, making them searchable, referenceable, and actionable.

## Quality Upgrade: Evidence Lifecycle

Treat every new insight as a claim with a lifecycle, not as a finished fact.

### Status Values

- `candidate`: plausible but not yet checked against repeated evidence.
- `active`: useful enough to influence current work.
- `validated`: supported by repeated observations, direct feedback, or measured outcomes.
- `contradicted`: later evidence challenges the claim.
- `archived`: no longer useful, stale, or merged into a better insight.

### Evidence Grades

- `observed-once`: one session, one event, or one user comment.
- `repeated`: seen across multiple sessions or examples.
- `measured`: backed by logs, counts, or explicit evaluation.
- `user-confirmed`: confirmed directly by the user.

### Recording Gate

Before adding a new insight:

1. Search for near-duplicates and possible conflicts.
2. Capture the source, date, and evidence grade.
3. Keep the wording falsifiable; avoid broad personality claims from one event.
4. If the insight affects future agent behavior, mark what behavior should change.
5. Ask before exporting to a second-brain or other persistent knowledge base.

Preferred output:

```text
Insight: <short falsifiable claim>
Evidence grade: <observed-once | repeated | measured | user-confirmed>
Status: <candidate | active | validated | contradicted | archived>
Related/conflicting insights: <ids or none found>
Behavior change: <what the agent should do differently>
```

## When to Use

Use this skill when:
- A user mentions "note this down" or "remember this insight"
- Patterns emerge across multiple sessions that should be tracked
- Research or analysis reveals findings worth preserving
- The user asks to "track" or "record" something for future reference
- Cross-referencing insights with existing knowledge is needed

## Core Concepts

### Insight
An insight is a discrete observation, pattern, or learning with the following attributes:
- **Content**: The actual observation or finding
- **Source**: Where it came from (session, research, user input)
- **Tags**: Categories for organization
- **Priority**: Importance level (high/medium/low)
- **Status**: Current state (active/validated/archived)
- **Created**: Timestamp
- **References**: Links to related insights or knowledge

### Tags
Standard tags for categorization:
- `pattern`: Recurring behaviors or structures
- `learning`: New understanding or skill acquired
- `decision`: Choices made and their rationale
- `risk`: Potential issues or concerns
- `opportunity`: Potential improvements or wins
- `user-preference`: User-specific preferences
- `technical`: Technical findings or constraints
- `process`: Workflow or methodological insights

## Input

Accepts insights in various formats:
- Direct text input
- Session transcript excerpts
- Memory file references
- Research findings

## Output

Produces:
- Dated insight records (Markdown)
- Tagged insight summaries
- Cross-reference reports
- Insight search results

## Workflow

### Recording an Insight

1. **Capture**: Extract the core observation
2. **Tag**: Apply relevant category tags
3. **Prioritize**: Mark importance level
4. **Link**: Connect to related insights
5. **Store**: Save to dated record

### Retrieving Insights

1. **Search**: By tag, keyword, date, or priority
2. **Filter**: Narrow by status or category
3. **Present**: Show matching insights with context

### Analyzing Insights

1. **Cluster**: Group related insights
2. **Trend**: Identify patterns over time
3. **Validate**: Check against new evidence
4. **Archive**: Mark outdated insights

## Commands

### Add Insight
```
insight add "Content of the insight" --tags pattern,learning --priority high
```

### List Insights
```
insight list --tag pattern --since 2024-01-01
```

### Search Insights
```
insight search "keyword" --priority high
```

### Show Insight
```
insight show <insight-id>
```

### Archive Insight
```
insight archive <insight-id>
```

## Output Format

### Dated Insight Record

```markdown
# Insights - YYYY-MM-DD

## New Insights

### INS-001: Title
- **Content**: The insight content
- **Source**: Session/user/research
- **Tags**: pattern, learning
- **Priority**: high
- **Status**: active
- **Created**: 2024-01-15T10:30:00Z
- **References**: INS-003, knowledge-distillation-2024-01-10

## Summary
- Total insights: 5
- High priority: 2
- New tags: user-preference
```

## Quality Rules

- Be specific: avoid vague generalizations
- Include source: always note where insight came from
- Tag consistently: use standard tags
- Link related insights: build knowledge networks
- Review regularly: archive outdated insights
- Prioritize honestly: not everything is high priority

## Good Trigger Examples

- "Track this insight: users prefer X over Y"
- "Note down that we discovered a pattern in Z"
- "Search for insights about deployment issues"
- "Show me all high priority insights from last week"
- "Archive insight INS-005, it's no longer relevant"

## 真实任务示例

| 场景 | 用户会说 | Skill 执行 |
|------|---------|-----------|
| 记录发现 | "记下来，用户更喜欢分步确认" | 创建洞察 → 打标签 → 设置优先级 |
| 回顾分析 | "之前有没有分析过类似模式" | 按标签搜索 → 列出相关洞察 → 关联分析 |
| 趋势发现 | "看看最近在哪些方面有重复模式" | 聚类分析 → 统计标签频率 → 提取趋势 |
| 知识清理 | "帮我把过时的洞察清理一下" | 列出旧洞察 → 确认归档 → 保持数据库整洁 |
| 报告生成 | "把关于 deployment 的洞察整理成报告" | 过滤相关条目 → 格式化为报告 → 输出摘要 |

## Resources

### references/
- `references/tag-taxonomy.md`: Full tag definitions and usage guidelines
- `references/output-examples.md`: Sample insight records
