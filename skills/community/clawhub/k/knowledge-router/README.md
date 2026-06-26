# Knowledge Router

[中文说明](#中文说明)

Knowledge Router is a lightweight routing layer across existing knowledge sources such as `MEMORY.md`, daily memory files, self-improving notes, skill references, and audit records.

It is designed to help decide **where to read first** before doing broad search or loading too much context.

## What it does
- classifies knowledge sources by role
- infers query intent
- recommends primary and secondary sources
- emits simple promotion hints when knowledge looks mature enough to move upward into a more durable layer

## Current scope
This first version focuses on:
- source typing
- query intent inference
- source ranking
- routing reports
- lightweight promotion hints

It does **not** create a new knowledge database or rewrite existing knowledge files.

## Usage
```bash
scripts/knowledge_router.py "<query>" [--scope default|memory-only|skills-only|audit-only|improvement-only] [--output report.txt]
```

Example:
```bash
scripts/knowledge_router.py "ClawHub 发布失败时之前怎么处理的？"
```

## Output
The report includes:
- query intent
- primary sources
- secondary sources
- why these sources were chosen
- promotion hints

---

## 中文说明

Knowledge Router 是一个建立在现有知识层之上的**轻量知识路由层**。

它不会新建一套知识库，也不会重写现有记忆；它做的事情是：
**在读太多之前，先判断该去哪里找。**

## 它会做什么
- 按角色给知识源分类
- 推断 query intent
- 推荐 primary / secondary sources
- 当某类知识已经成熟时，给出简单的 promotion hints

## 当前范围
这一版主要聚焦：
- source typing
- query intent inference
- source ranking
- routing reports
- 轻量 promotion hints

它**不会**替代现有的 `MEMORY.md`、daily memory、self-improving 或 audit 系统。

## 用法
```bash
scripts/knowledge_router.py "<query>" [--scope default|memory-only|skills-only|audit-only|improvement-only] [--output report.txt]
```

示例：
```bash
scripts/knowledge_router.py "ClawHub 发布失败时之前怎么处理的？"
```

## 输出内容
报告会包含：
- query intent
- primary sources
- secondary sources
- 选择这些来源的原因
- promotion hints
