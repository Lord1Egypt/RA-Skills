---
name: lobster-compact
description: "Summarize long conversations to preserve context. Automatically triggered when context window approaches limits, or manually with /compact."
allowed-tools:
  - read
  - write
  - edit
  - memory_search
  - memory_get
when_to_use: "Use when the conversation becomes very long and context may be lost. Examples: 'summarize so far', 'compact', '我们聊了太多了', '总结一下'."
---

# Compact — 长会话压缩

## Inputs
- `$args`: Optional focus area for the summary

## Goal
Create a detailed summary of the conversation so far that preserves all critical context for continuing work.

## Steps

### 1. Analyze the Conversation
Chronologically analyze each exchange:
- User's explicit requests and intents
- Approach taken to address requests
- Key decisions, technical concepts, code patterns
- Specific details: file names, code snippets, function signatures
- Errors encountered and how they were fixed
- User feedback and corrections

### 2. Generate Summary
Write a summary with these sections:

```markdown
# 会话摘要

## 1. 主要请求和意图
[用户的核心需求]

## 2. 关键技术概念
[涉及的技术、框架、工具]

## 3. 文件和代码
[涉及的文件和关键代码片段]

## 4. 错误和修复
[遇到的问题及解决方案]

## 5. 用户反馈
[用户给出的指导、纠正、偏好]

## 6. 待办任务
[尚未完成的任务]

## 7. 当前工作
[最近在做什么，精确到文件和代码]

## 8. 下一步
[紧接着应该做什么]
```

### 3. Update Memory
- Save critical long-term info to MEMORY.md
- Save today's log to memory/YYYY-MM-DD.md
- Use `memory_search` to avoid duplicates

**Success criteria**: Summary captures all critical context; memory files updated.
