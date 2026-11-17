---
name: harness-engineering
description: "Agent Harness 构建规范——当 AI 通过编程构建 harness agent（coding agent / 自动化 agent / 长时运行 agent）时，读取本 skill 作为参考标准，确保产出符合 harness 工程架构：Loop / Provider / Tools / Permissions / Session / Compaction / Prompts & Skills / Extensions 七层 + Delivery。覆盖设计决策、可运行 Python 代码模板、长时运行模式。触发词：coding agent、agent loop、tool calling、context management、session persistence、agent harness、构建 agent。Use this skill when the user asks to build a coding agent / automation agent / long-running agent / agent harness."
description_zh: "Agent Harness 构建规范——当 AI 通过编程构建 harness agent（coding agent / 自动化 agent / 长时运行 agent）时，读取本 skill 作为参考标准，确保产出符合 harness 工程架构：Loop / Provider / Tools / Permissions / Session / Compaction / Prompts & Skills / Extensions 七层 + Delivery。覆盖设计决策、可运行 Python 代码模板、长时运行模式。触发场景：用户要求写一个 coding agent、agent loop、tool calling、context management、session persistence、或构建 harness。"
description_en: "Agent Harness engineering spec — load this skill when building a harness agent (coding agent / automation agent / long-running agent) in code, to ensure the output follows the harness architecture: Loop + 7 Rings (Provider, Tools, Permissions, Session, Compaction, Prompts & Skills, Extensions) + Delivery. Covers design decisions, runnable Python code templates, and long-running patterns. Triggers: user asks to build a coding agent, agent loop, tool calling, context management, session persistence, or a harness."
version: 2.2.0
agent_created: true
---

## Purpose

本 skill 是**构建规范**，不是学习材料。当 AI 通过编程方式构建一个 harness agent 时，读取本 skill 作为参考标准，确保产出的 agent 符合 harness 工程架构。

**典型使用场景**：用户说"帮我写一个 coding agent / 自动化 agent / 长时运行 agent"，AI 在编码前加载本 skill，按规范构建。

## What is an Agent Harness

包裹 LLM 的运行时编排层——管工具调用、上下文、记忆、权限、交付，让模型从"一次性问答"变成"能干活的自主系统"。

> **"A harness is not 'a loop that calls a model'. It is a context-management system with a loop at its centre."**

### Harness != Framework != Runtime

| 层 | 职责 | 代表 |
|---|------|------|
| **Framework** | 定义 agent 逻辑（prompt、工具定义、编排模式） | LangChain, CrewAI, OpenAI Agents SDK |
| **Runtime** | 管执行（持久化、重试、并发、故障恢复） | LangGraph, Temporal, Inngest |
| **Harness** | 包裹一切：工具集、权限、上下文策略、交付界面、扩展 | Claude Code, Codex, Pi, OpenCode |

**叠加关系**：Framework（定义逻辑） -> Runtime（管执行） -> Harness（包一切，给用户用）

## Architecture: The Loop + 7 Rings

一个 harness 就是以 agent loop 为中心，向外扩展七层"环"（ring）。每层解决一个独立问题，可单独理解和替换。

### 核心文件索引

| 主题 | 文件 | 何时读 | 行数 |
|------|------|--------|------|
| 架构总览 + 7 Rings | `references/architecture.md` | 理解整体架构时 | ~552 |
| 设计决策清单 | `references/design-decisions.md` | 做技术选型时 | ~455 |
| 代码模板 | `references/code-templates.md` | 开始编码时 | ~960 |
| 长时运行 Agent 模式 | `references/long-running-patterns.md` | 构建跨小时 agent 时 | ~397 |
| 主流 Harness 对比 | `references/harness-comparison.md` | 选型参考时 | ~271 |

## Core Principles

1. **Prompts 是软引导，Extensions 是硬护栏** —— 安全关键逻辑必须用 extension，不能用 prompt
2. **Skills 扩展 prompt，Extensions 扩展 loop** —— 对称性：一个在 prompt 层，一个在 loop 层
3. **Append-only，不原地改写** —— Session 树、Compaction entry 都是追加，原始数据不丢
4. **Catalogue vs Body 分离** —— Skill 只注目录进 prompt，body 按需 read
5. **Neutral Hook Boundary** —— Runtime 提供中性 hook，不内置 sub-agents / MCP / plan-mode

## Build Checklist

### 构建前（必须完成）

- [ ] 确认目标：coding agent / 自动化 agent / 长时运行 agent
- [ ] 选择 provider 策略：深度绑定 vs 多 provider（见 `design-decisions.md` D4）
- [ ] 选择 session 策略：不可变树 vs 扁平 list（见 `design-decisions.md` D15）
- [ ] 选择扩展策略：内置一切 vs 全推给扩展（见 `design-decisions.md` D28）
- [ ] 读取 `references/architecture.md` 理解 7 Rings 架构
- [ ] 读取 `references/design-decisions.md` 做完所有技术选型

### 构建中（按阶段）

- [ ] Phase 1 MVP：Agent loop + 1 个 provider + 3 个核心工具（read/write/bash）+ 基础 CLI
- [ ] Phase 2 可用：完整 7 件套工具 + Pydantic 校验 + Session 持久化 + 流式输出 + 取消机制
- [ ] Phase 3 生产可用：Session 树 + Compaction + 权限 hook + Extension API + TUI
- [ ] Phase 4 进阶：Sub-agents + Plan mode + MCP adapter + 长时运行模式 + 多 provider

### 构建后（验证）

- [ ] 每个 tool 都有 Pydantic schema + 参数校验
- [ ] max_iterations 安全阀存在
- [ ] cancel_event 取消机制存在
- [ ] compaction 80% 阈值触发
- [ ] 权限 hook（authorize + process_result）存在
- [ ] extension API 三动词（on / register_tool / register_command）存在
- [ ] 至少一种 delivery shell（TUI / CLI / Web）

## Build Phases（分阶段实施）

| 阶段 | 目标 | 核心交付 | 参考文件 |
|------|------|---------|---------|
| Phase 1 | MVP | Agent loop + 1 provider + 3 工具 + CLI | `code-templates.md` 第 0-1 节 + 第 2 节（read/write/bash） |
| Phase 2 | 可用 | 7 工具 + Pydantic + Session JSONL + 流式 + 取消 | `code-templates.md` 第 0-3 节 |
| Phase 3 | 生产可用 | Session 树 + Compaction + 权限 hook + Extension API + TUI | `code-templates.md` 第 0-5 节 + `architecture.md` |
| Phase 4 | 进阶 | Sub-agents + Plan mode + MCP + 长时运行 + 多 provider | `code-templates.md` 全部 + `long-running-patterns.md` |

每阶段都可独立使用。先跑通再优化。

## Scope

This skill ONLY:
- 提供 harness agent 的构建规范、设计决策、代码模板
- 对比主流 harness 的架构选择供参考
- 引导 AI 按标准构建符合工程规范的 harness agent

This skill NEVER:
- 执行代码或调用 LLM
- 访问网络或外部服务
- 自动修改用户项目文件
- 替代真正的 harness 实现（需 AI 根据模板编码）


