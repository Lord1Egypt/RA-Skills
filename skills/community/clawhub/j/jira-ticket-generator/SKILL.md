---
name: jira-ticket-generator
description: "Generate bilingual (Chinese/English) JIRA ticket descriptions from user input. Use when user asks to create a JIRA ticket, write ticket description, or needs to format a task/issue for JIRA. Supports various issue types including Bug, Task, Story, and Epic."
---

# JIRA Ticket Generator

Generate professional, bilingual JIRA ticket descriptions with consistent formatting.

## Quick Start

When user provides a task description, generate a bilingual ticket description with:
- **Title** - Concise summary with `[PREFIX]` tag
- **Description** - Structured content in both Chinese and English
- **Sections** - Objective, Requirements, Acceptance Criteria (as applicable)

## Ticket Types and Templates

### Bug Report
Use for defects, errors, or unexpected behavior.

**Structure:**
- Title: `[BUG] Brief issue description`
- Problem description
- Steps to reproduce
- Expected vs actual behavior
- Environment/context

### Task
Use for general work items, technical tasks, documentation updates.

**Structure:**
- Title: `[TASK] Brief task description`
- Objective
- Requirements
- Acceptance criteria

### Story
Use for user-facing features or requirements.

**Structure:**
- Title: `[STORY] Brief feature description`
- User story (As a... I want... So that...)
- Requirements
- Acceptance criteria

### Epic
Use for large bodies of work that span multiple stories/tasks.

**Structure:**
- Title: `[EPIC] Brief epic description`
- Objective
- Scope
- Key deliverables

## Bilingual Format

All ticket titles and descriptions must include both Chinese and English versions.

### Title Format

The title line must contain **both Chinese and English**, separated by a pipe `|`:

```
[PREFIX] 中文标题 | English Title
```

**Examples:**
- `[TASK] 启用 Hermes API Server 并部署 Web Chat 前端 | Enable Hermes API Server and Deploy Web Chat Frontend`
- `[STORY] 汽车行业知识库 RAG + 知识图谱混合架构建设 | Automotive Knowledge Base RAG + Knowledge Graph Hybrid Architecture`
- `[BUG] 飞书文件发送偶发超时 | Feishu File Send Intermittent Timeout`
- `[EPIC] Q3 性能优化专项 | Q3 Performance Optimization Initiative`

### Description Format

```
## 🇨🇳 中文描述

**目标 / Objective:**
[Chinese description]

**需求 / Requirements:**
- [Requirement 1 in Chinese]
- [Requirement 2 in Chinese]

**验收标准 / Acceptance Criteria:**
- [Criterion 1 in Chinese]
- [Criterion 2 in Chinese]

---

## 🇬🇧 English Description

**Objective:**
[English description]

**Requirements:**
- [Requirement 1 in English]
- [Requirement 2 in English]

**Acceptance Criteria:**
- [Criterion 1 in English]
- [Criterion 2 in English]
```

## Workflow

1. **Understand** - Read the user's input to determine ticket type (Bug/Task/Story/Epic)
2. **Classify** - If unclear, ask the user to clarify the ticket type
3. **Generate** - Create bilingual ticket description following the appropriate template
4. **Review** - Ensure formatting is consistent and content is complete
5. **Output** - Present the ticket to the user in a copy-ready format

## Title Conventions

Titles must be **bilingual (Chinese | English)** with `[PREFIX]` tag:

```
[PREFIX] 中文标题 | English Title
```

| Type | Prefix | Example |
|------|--------|---------|
| Bug | `[BUG]` | `[BUG] 飞书文件发送偶发超时 \| Feishu File Send Intermittent Timeout` |
| Task | `[TASK]` | `[TASK] 更新 API 文档至 v2.0 \| Update API Documentation for v2.0` |
| Story | `[STORY]` | `[STORY] 用户可导出 PDF 报告 \| User Can Export Reports to PDF` |
| Epic | `[EPIC]` | `[EPIC] Q3 性能优化专项 \| Q3 Performance Optimization Initiative` |

### Rules
- Chinese title comes first, then ` | `, then English title
- Both sides should be concise but descriptive (each under 80 characters)
- Use action verbs for tasks and stories (启用, 部署, 实现, 设计 / Enable, Deploy, Implement, Design)

## Best Practices

1. Keep titles concise but descriptive (under 100 characters)
2. Use action verbs for tasks and stories (Implement, Update, Fix, Design)
3. Make acceptance criteria specific and testable
4. Include context that helps developers understand the "why"
5. For bugs, always include reproduction steps
6. Prioritize clarity over completeness — a clear ticket is more useful than an exhaustive one
