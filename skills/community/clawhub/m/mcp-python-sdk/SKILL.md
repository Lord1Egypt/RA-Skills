---
name: mcp-python-sdk
description: |-
  MCP Python SDK：Anthropic 主导的 Model Context Protocol 参考实现。2 server 层 + 3 transport + 3 原语 + 4 协议版本 + 50 条约束。
  MCP Python SDK: reference Python implementation of the Model Context Protocol (Anthropic-led). Two server surfaces (low-level Server / high-level MCPServer, formerly FastMCP), three transports (stdio / SSE / streamable-http), and three primitives (Tools / Resources / Prompts).
license: MIT-0
compatibility: AI engineering knowledge skill — host AI consumes seed.yaml directly. No installation required.
metadata:
  version: "v0.1.0"
  blueprint_id: "finance-bp-140"
  blueprint_source: "modelcontextprotocol/python-sdk"
  blueprint_commit: "3d7b311de07aade1281d18aa7b04689a81ab8793"
  category: ai-engineering
  doramagic_url: "https://doramagic.ai/zh/crystal/mcp-python-sdk"
  openclaw:
    skillKey: mcp-python-sdk
    category: ai-engineering
    primaryEnv: knowledge
---
# 这个 skill 适合什么用户？能做哪些任务？

## 概览

MCP Python SDK 是 Model Context Protocol 的参考实现（github.com/modelcontextprotocol/python-sdk）—— Anthropic 主导的开放标准，让 AI host（Claude / Cursor 等）通过 JSON-RPC 2.0 跟工具服务端对话。

两个 server 接口：低层 Server（构造器注入 handler）和高层 MCPServer（装饰器 API，原名 FastMCP）。三个传输共享结构化 (read_stream, write_stream) AnyIO 契约：stdio（行分隔 JSON）、传...

**Doramagic 晶体页**: https://doramagic.ai/zh/crystal/mcp-python-sdk

## 知识规模

- **50 条约束** (1 fatal + 49 non-fatal)
- 上游源码: `modelcontextprotocol/python-sdk` @ commit `3d7b311d`
- 蓝图 ID: `finance-bp-140`

## 用法

Host AI（Claude Code / Cursor / OpenClaw）读 `references/seed.yaml`，按其中的：
- `intent_router` 匹配用户意图
- `architecture` 理解项目架构
- `constraints` 应用 anti-pattern 约束
- `business_decisions` 参考核心设计决策

## FAQ 摘要

### 这个 skill 适合什么用户？能做哪些任务？
适合需要给 Claude / Cursor 等 AI host 提供工具服务的工程师：发布公司内部 API 给 AI 调用、暴露文件 / 数据库为 Resources、提供 prompt 模板等。本 skill 覆盖 stdio（本地）/ SSE（旧）/ streamable-http（推荐）三种 server 形态。访问 doramagic.ai/r/mcp-python-sdk 查看完整说明。

### 需要准备什么环境？依赖什么？
Python 3.10+，AnyIO（asyncio 或 trio 后端），Pydantic v2（type schema 生成），Starlette（HTTP/SSE/streamable-http 托管），OpenTelemetry（可选，分布式追踪）。Windows 客户端 stdio 需 pywin32 用于 Job Object 进程树终止；POSIX 用 os.killpg。

### 会踩哪些坑？这个 skill 怎么防护？
本 skill 内置 50 条约束（1 条 fatal）。典型踩坑：(1) commit 3d7b311 的 README 仍 import 改名前的 FastMCP（26 处 import 行 + 10 处文件路径失效），照抄 quickstart 必失败；

---

完整文档: 见 `references/seed.yaml` (v6.1 schema). 浏览页: https://doramagic.ai/zh/crystal/mcp-python-sdk
