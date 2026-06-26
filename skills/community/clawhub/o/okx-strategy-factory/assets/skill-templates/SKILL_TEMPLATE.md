---
name: <skill-name>
description: "<一句话描述 Skill 的核心能力、适用场景和触发关键词。用于 AI agent 路由匹配，写得越精确越好。>"
license: Apache-2.0
metadata:
  author: <作者>
  version: "<major.minor.patch>"
  pattern: "<tool-wrapper | generator | reviewer | inversion | pipeline>"
  # 复合模式用逗号分隔: "pipeline, tool-wrapper"
  # 可选字段（按 pattern 需要添加）:
  # output-format: "markdown"          # generator 用
  # severity-levels: "error,warning,info"  # reviewer 用
  # interaction: "multi-turn"          # inversion 用
  # steps: "N"                         # pipeline 用
---

# <Skill 名称>

一句话概述：Skill 做什么、怎么触发、输出到哪里。

<!--
选择你的设计模式，从 Skills/templates/ 目录获取对应模板：

| Pattern        | 适用场景                           | 模板文件                  |
|----------------|-----------------------------------|--------------------------|
| tool-wrapper   | 按需加载 API/库的上下文             | templates/tool-wrapper.md |
| generator      | 强制一致的输出结构                  | templates/generator.md    |
| reviewer       | 分离"检查什么"和"如何检查"          | templates/reviewer.md     |
| inversion      | Agent 先采访用户再行动              | templates/inversion.md    |
| pipeline       | 严格顺序多步工作流+硬检查点          | templates/pipeline.md     |

模式可以组合：
- Pipeline + Tool Wrapper: 多步工作流，每步加载不同 API 文档
- Generator + Inversion: 先收集变量，再填充模板
- Pipeline + Reviewer: 工作流中包含审查步骤

组合模式时，在 metadata.pattern 用逗号分隔，然后从各模板中挑选需要的章节合并。
-->

## Architecture

```
<系统架构图 - 用 ASCII art 展示数据流>
```

**依赖的外部服务/Skill**:
- <服务1>: `<调用方式>` -> `<具体命令>`

## Instructions

<!--
这是 Skill 的核心指令区。根据 pattern 不同，结构差异很大。
请参考对应的 templates/*.md 获取该 pattern 的标准指令结构。
-->

## Directory Structure

```
<skill-name>/
├── SKILL.md              # 主文件（必需）
├── references/           # API 规范、风格指南、检查清单等（按需）
│   └── <context-file>.md
└── assets/               # 输出模板、脚手架等（按需）
    └── <template-file>.md
```

## Anti-Patterns

| Pattern | Problem |
|---|---|
| <反模式1> | <为什么有问题> |
