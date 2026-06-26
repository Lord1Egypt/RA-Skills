---
name: llama-index-rag
description: |-
  LlamaIndex：把任意文档变 LLM 可查询知识的 Python 框架。4 大支柱（Index/Retriever/QueryEngine/Synthesizer）+ 52 条 anti-pattern 约束（5 fatal）。
  LlamaIndex: a Python framework that turns arbitrary documents into queryable, LLM-grounded knowledge. The four-pillar core (Index / Retriever / QueryEngine / ResponseSynthesizer) wires a configurable retrieve-then-synthesize loop;
license: MIT-0
compatibility: AI engineering knowledge skill — host AI consumes seed.yaml directly. No installation required.
metadata:
  version: "v0.1.0"
  blueprint_id: "finance-bp-135"
  blueprint_source: "run-llama/llama_index"
  blueprint_commit: "0a6c90bfd610dcc66dcb89ed3e1d905c5e9bf6dc"
  category: ai-engineering
  doramagic_url: "https://doramagic.ai/zh/crystal/llama-index-rag"
  openclaw:
    skillKey: llama-index-rag
    category: ai-engineering
    primaryEnv: knowledge
---
# 这个 skill 适合什么用户？能做哪些任务？

## 概览

LlamaIndex 是把任意文档变成 LLM 可查询知识的 Python 框架（github.com/run-llama/llama_index）。四大支柱（Index / Retriever / QueryEngine / ResponseSynthesizer）配置化检索-合成循环；Ingestion pipeline 处理 Document → Node → Embedding → Index 转换，带 content-hash 缓存；workflow / agent 子模块（FunctionAgent / ReActAgent / CodeActAgent / multi-agent...

**Doramagic 晶体页**: https://doramagic.ai/zh/crystal/llama-index-rag

## 知识规模

- **52 条约束** (5 fatal + 47 non-fatal)
- 上游源码: `run-llama/llama_index` @ commit `0a6c90bf`
- 蓝图 ID: `finance-bp-135`

## 用法

Host AI（Claude Code / Cursor / OpenClaw）读 `references/seed.yaml`，按其中的：
- `intent_router` 匹配用户意图
- `architecture` 理解项目架构
- `constraints` 应用 anti-pattern 约束
- `business_decisions` 参考核心设计决策

## FAQ 摘要

### 这个 skill 适合什么用户？能做哪些任务？
适合做企业知识库、文档问答、RAG 应用的工程师：从 PDF / Markdown / 网页等异构文档构建索引，结合 retrieve-then-synthesize 给 LLM 提供外部知识。覆盖 FunctionAgent / ReActAgent / CodeActAgent 等 agent 范式。访问 doramagic.ai/r/llama-index 查看完整用例。

### 需要准备什么环境？依赖什么？
Python 3.9+，至少一个 LLM provider（默认隐式 OpenAI gpt-3.5-turbo）和一个 embedding provider（默认隐式 OpenAI text-embedding-ada-002 → 1536 维）。默认用内存 SimpleVectorStore，持久化需安装对应集成包。

### 会踩哪些坑？这个 skill 怎么防护？
本 skill 内置 52 条约束（5 条 fatal）。典型踩坑：(1) ServiceContext 已硬删除（不是 deprecated），3 个入口直接 raise ValueError；(2) SentenceSplitter chunk_overlap 默认 200（与文档常引用的 constants.DEFAULT_CHUNK_OVERLAP=20 不一致）；

---

完整文档: 见 `references/seed.yaml` (v6.1 schema). 浏览页: https://doramagic.ai/zh/crystal/llama-index-rag
