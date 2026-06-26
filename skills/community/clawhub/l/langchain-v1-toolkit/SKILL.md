---
name: langchain-v1-toolkit
description: |-
  LangChain v1：把 LLM、prompt、tool、retriever、parser 暴露为 Runnable，用 `|` 操作符（LCEL）组合成统一 invoke / stream / batch 接口的链。
  LangChain v1: exposes LLMs, prompts, tools, retrievers, and parsers as Runnables composed via the `|` operator (LCEL) into chains with uniform invoke / stream / batch semantics. create_agent returns a LangGraph CompiledStateGraph.
license: MIT-0
compatibility: AI engineering knowledge skill — host AI consumes seed.yaml directly. No installation required.
metadata:
  version: "v0.1.0"
  blueprint_id: "finance-bp-132"
  blueprint_source: "langchain-ai/langchain"
  blueprint_commit: "87ba30f09773b8e9ec549841c57906f343b35ed8"
  category: ai-engineering
  doramagic_url: "https://doramagic.ai/zh/crystal/langchain-v1-toolkit"
  openclaw:
    skillKey: langchain-v1-toolkit
    category: ai-engineering
    primaryEnv: knowledge
---
# 这个 skill 适合什么用户？能做哪些任务？

## 概览

LangChain 是构建 LLM 应用的事实标准 Python 框架（github.com/langchain-ai/langchain）。v1 包（v1.2.15）有意保持精简：核心是 `agents.create_agent`（返回 LangGraph CompiledStateGraph）、`chat_models.init_chat_model` 工厂、message types 重导出和 tools/embeddings shim。

历史 `Chain` / `LLMChain` / `Memory` / `AgentExecutor` 接口已迁到 `langchain-clas...

**Doramagic 晶体页**: https://doramagic.ai/zh/crystal/langchain-v1-toolkit

## 知识规模

- **51 条约束** (1 fatal + 50 non-fatal)
- 上游源码: `langchain-ai/langchain` @ commit `87ba30f0`
- 蓝图 ID: `finance-bp-132`

## 用法

Host AI（Claude Code / Cursor / OpenClaw）读 `references/seed.yaml`，按其中的：
- `intent_router` 匹配用户意图
- `architecture` 理解项目架构
- `constraints` 应用 anti-pattern 约束
- `business_decisions` 参考核心设计决策

## FAQ 摘要

### 这个 skill 适合什么用户？能做哪些任务？
适合用 LangChain 构建 LLM 应用的工程师：tool-calling agent、结构化输出、RAG pipeline、流式输出、模型 fallback、PII 脱敏等。v1 后 agent 走 LangGraph 路径，旧 AgentExecutor 仍可用但建议迁移。访问 doramagic.ai/r/langchain 查看完整用例。

### 需要准备什么环境？依赖什么？
Python（具体版本见 langchain_v1/pyproject.toml），`pip install langchain` 自动带 LangGraph 作为硬运行时依赖。每个 provider 需单独安装 partner 包（如 langchain-openai、langchain-anthropic）。

### 会踩哪些坑？这个 skill 怎么防护？
本 skill 内置 51 条约束。典型踩坑：(1) BaseMemory 与所有 Conversation*Memory 已 @deprecated，BaseMemory 已从 langchain_core 删除；

---

完整文档: 见 `references/seed.yaml` (v6.1 schema). 浏览页: https://doramagic.ai/zh/crystal/langchain-v1-toolkit
