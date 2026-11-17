---
name: mcp-server-generation
description: 生成 Python MCP Server（stdio/streamable-http）：脚手架、tool/resource/prompt 定义与 MCP Inspector 调试
source:
  type: derived
  repo: skills-repo/machine-learning-engineer
  path: skills/mcp-server-generation/SKILL.md
  url: https://skills.sh/github/awesome-copilot/python-mcp-server-generator
  version: 1.0.0
  updated: 2026-09-08
metadata:
  author: hope
  category: ML
  platform: 通用
  difficulty: 进阶
  version: 1.0.0
  created: 2026-09-08
tags:
  - mcp
  - model-context-protocol
  - tool-use
  - agent
  - fastmcp
  - python
---

# MCP Server 生成 — 用 Python 造一个能被 Agent 调用的 Server

> 把你的数据、API、本地能力，封装成标准 MCP Server，让 Claude Desktop / Claude Code / 任意 MCP 客户端当工具调用。

衍生自社区技能 `github/awesome-copilot/python-mcp-server-generator`（skills.sh 10.3K 安装，
GitHub 38.7K stars，官方 MCP Python SDK 导向）。本技能只做路由与能力索引，完整脚手架命令、
transport 选型、装饰器写法、坑与检查清单见
[mcp-server-generation playbook](../../references/mcp-server-generation.md)。

## 能力

- **项目脚手架**：用 `uv` 拉起带 `mcp[cli]` 依赖的标准 Python 工程（目录结构 + `.gitignore`）
- **传输选型**：本地用 `stdio`，远程用 `streamable-http`（可选 host/port/stateless）
- **能力定义**：用装饰器声明 tool / resource / prompt，类型提示 + docstring 自动生成 schema
- **工程质量**：async/await、Pydantic 入参校验、上下文管理器做资源清理、统一错误处理
- **联调验证**：MCP Inspector 跑端到端、接 Claude Desktop 配置、示例 tool 调用与排错

## 何时用 / 何时不用

- **用**：想让 Agent 调用你私有的函数、数据库、内部 API 或本地文件；要把能力做成可复用、可发现的工具。
- **不用**：只给大模型一次性的上下文（直接用 prompt 即可）；纯 ML 训练建模（见 `machine-learning` /
  `deep-learning-pytorch`）；只想在代码里直接调 Claude（见 `claude-agent-sdk`）。

## 使用方式

```
/mcp-server-generation 给我一个读取本地 SQLite 的 MCP server 脚手架（stdio）
/mcp-server-generation 生成一个 streamable-http 的天气 MCP server，带 host/port
/mcp-server-generation 这个 tool 的 schema 为什么没生成？帮我排查
```

## 工作流

1. 判定要不要做 MCP Server（见 playbook 决策树）。
2. 用 `uv` 脚手架工程 + 装 `mcp[cli]`。
3. 选 transport（stdio / streamable-http），写第一个带类型提示的 tool。
4. 用 MCP Inspector 跑通，再接 Claude Desktop / Claude Code 验证。
5. 按 playbook 检查清单收尾（错误处理、schema、资源清理、鉴权）。

## 与其他技能协作

- 想在 Agent 里直接调用 Claude 能力 → `claude-agent-sdk`
- 想把模型做成服务/产品 → `skills-repo/ai-fullstack-engineer`
