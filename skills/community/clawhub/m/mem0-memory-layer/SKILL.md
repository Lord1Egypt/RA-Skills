---
name: mem0-memory-layer
description: |-
  Mem0 长期记忆层：为 LLM agent / chatbot 提供事实级记忆——抽取、嵌入、去重、存储 + 混合检索（语义 + BM25 + 实体加权），覆盖 17 个核心用例。自托管 Memory 与托管 MemoryClient 双形态。
  Mem0 long-term memory layer for LLM agents and chatbots: extract, embed, dedup, store, and hybrid-retrieve (semantic + BM25 + entity boost). Ships both self-hosted Memory and hosted MemoryClient.
license: MIT-0
compatibility: AI engineering knowledge skill — host AI consumes seed.yaml directly. No installation required.
metadata:
  version: "v0.1.0"
  blueprint_id: "finance-bp-131"
  blueprint_source: "mem0ai/mem0"
  blueprint_commit: "693e709389526b45cfadfd06d89a0e13af7c7345"
  category: ai-engineering
  doramagic_url: "https://doramagic.ai/zh/crystal/mem0-memory-layer"
  openclaw:
    skillKey: mem0-memory-layer
    category: ai-engineering
    primaryEnv: knowledge
---
# 这个 skill 适合什么用户？能做哪些任务？

## 概览

Mem0 是一个 Python 长期记忆框架（github.com/mem0ai/mem0），为 LLM 应用和 agent 提供个性化记忆层。自托管 Memory 类内置 V3 阶段化抽取-存储流水线（Phase 0 上下文采集 → Phase 8 消息持久化），可插拔 vector store / embedding / LLM / reranker provider。混合检索结合语义相似度 + 可选 BM25 / 后端原生 FTS 关键词搜索 + 实体加权评分。

另有独立托管 SaaS 路径 MemoryClient（api.mem0.ai）共享公开 API，但抽取下沉到平台。OSS...

**Doramagic 晶体页**: https://doramagic.ai/zh/crystal/mem0-memory-layer

## 知识规模

- **52 条约束** (1 fatal + 51 non-fatal)
- 上游源码: `mem0ai/mem0` @ commit `693e7093`
- 蓝图 ID: `finance-bp-131`

## 用法

Host AI（Claude Code / Cursor / OpenClaw）读 `references/seed.yaml`，按其中的：
- `intent_router` 匹配用户意图
- `architecture` 理解项目架构
- `constraints` 应用 anti-pattern 约束
- `business_decisions` 参考核心设计决策

## FAQ 摘要

### 这个 skill 适合什么用户？能做哪些任务？
适合需要给 LLM agent / chatbot 加长期记忆的工程师：用户偏好持久化、多轮会话上下文延续、跨 session 事实复用。覆盖 17 个用例（个性化助手、客服、教育等）。访问 doramagic.ai/r/mem0 查看完整目录。

### 需要准备什么环境？依赖什么？
Python 3.10+，至少一个 LLM provider（默认 OpenAI）、一个 embedding provider（默认 OpenAI）、一个 vector store（默认 Qdrant）。本地 SQLite 文件位于 MEM0_DIR（默认 ~/.mem0/）。可选 MEM0_API_KEY 用于托管 MemoryClient。

### 会踩哪些坑？这个 skill 怎么防护？
本 skill 内置 52 条约束，最典型的 4 个：(1) OSS v2.0.0 中传入 graph_store 配置会被 pydantic 静默丢弃，graph 查询无效；(2) PostHog 遥测默认开启，需显式设 MEM0_TELEMETRY=false；

---

完整文档: 见 `references/seed.yaml` (v6.1 schema). 浏览页: https://doramagic.ai/zh/crystal/mem0-memory-layer
