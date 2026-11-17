---
name: claude-agent-sdk
description: 用 Anthropic Claude API / Agent SDK 构建 AI 应用与 Agent：Messages API、流式输出、工具调用、Agent 循环与子 Agent 编排
source:
  type: derived
  repo: skills-repo/machine-learning-engineer
  path: skills/claude-agent-sdk/SKILL.md
  url: https://skills.sh/bobmatnyc/claude-mpm-skills/anthropic-sdk
  version: 1.0.0
  updated: 2026-08-12
metadata:
  author: hope
  category: ML
  platform: 通用
  difficulty: 进阶
  version: 1.0.0
  created: 2026-08-12
tags:
  - claude-api
  - anthropic
  - agent-sdk
  - llm
  - tool-use
---

# Claude Agent SDK — 用 Claude API 构建 AI 应用与 Agent

> 把 Claude 接进你的产品：从单次 Messages 调用，到带工具、能自主循环的 Agent。

衍生自社区技能 `bobmatnyc/claude-mpm-skills@anthropic-sdk`（skills.sh 257 安装，
官方 Claude AI 集成导向），并参考 `rysweet/amplihack@claude-agent-sdk`（Agent 循环模式）。
本技能只做路由与能力索引，完整代码骨架、决策树与踩坑清单见
[claude-api-playbook playbook](../../references/claude-api-playbook.md)。

## 能力

- **Claude API SDK（Python / TypeScript）**：Messages API、多轮对话、系统提示、流式输出
- **工具调用（tool use）**：让模型调用函数、外部 API、本地脚本，形成「思考 → 调用 → 回收结果」闭环
- **Agent 模式**：工具循环、规划-执行、子 Agent 编排（Agent SDK / 自管循环）
- **可靠性增强**：提示缓存（prompt caching）、速率限制与重试、成本与 token 预算护栏

## 使用方式

在 Claude Code 中用 `/claude-agent-sdk` 调用，或直接读 playbook 取可复制代码：

```
/claude-agent-sdk 给我一个 Python 调用 Claude 做流式输出的最小例子
/claude-agent-sdk 怎么让 Claude 调用我的搜索 API（tool use）？
/claude-agent-sdk 用 Agent SDK 搭一个能循环调用工具的 Agent
```

## 何时用 / 何时不用

- **用**：把 Claude 能力嵌进应用或脚本；需要模型调用外部函数/API（RAG、搜索、执行动作）；
  构建能多步自主完成任务的 Agent。
- **不用**：纯 ML 训练与建模（见 `machine-learning` / `deep-learning-pytorch`）；只是想聊天
  （直接用客户端即可，无需写代码）。

## 工作流

1. **划边界**：明确任务目标与退出条件，防止 Agent 无限循环。
2. **选接入方式**：单次调用 / 流式 / 工具循环 / Agent SDK（决策树见 playbook）。
3. **装 SDK、配 Key**：API Key 走环境变量，绝不硬编码。
4. **写最小可用调用** → 加工具 → 加循环/编排。
5. **加缓存与限流**：提示缓存降本、指数退避抗 rate limit、给 token 与成本设上限。

## 适用场景

- 把 LLM 能力嵌进现有产品 / 脚本（摘要、抽取、对话、生成）
- 需要模型调用外部 API 或函数（RAG、搜索、数据库查询、执行命令）
- 构建能多步自主完成任务的 Agent（编码助手、研究助理、运维 Agent）

## 限制

- 需要 Anthropic API Key（或兼容网关）；本技能不负责密钥管理。
- 模型 ID 会更新，以 [官方文档](https://docs.anthropic.com) 最新模型为准。
- 不应让 Agent 无边界循环，或在未经确认时执行高风险操作（删库、转账、发信）。
