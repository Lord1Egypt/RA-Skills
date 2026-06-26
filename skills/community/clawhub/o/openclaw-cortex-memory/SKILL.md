# Openclaw Cortex Memory

OpenClaw 长期记忆插件，专为 OpenClaw AI 助手设计的智能记忆系统。

面向 OpenClaw 的长期记忆插件，集成多路检索、事件归档、图谱关系、向量化与反衰减排序，支持历史增量导入、规则反思和可观测诊断，可以将会话中零碎的记忆去噪整理、分层存储，支持对话中自动搜索回忆，吸收了 LLM wiki 的概念，帮助 Agent 在跨会话中持续积累并稳定调用高价值记忆。

## 核心能力

### 1) 语义检索
- 多路召回：`keyword / BM25 / vector / graph` 混合检索
- 排序融合：加权打分 + RRF + 可选 reranker
- 结果融合：可选 `readFusion`，支持权威融合返回
- 时序建模：`memoryDecay` + 命中反衰减（anti-decay）

### 2) 事件存储
- 分层写入：`active`（会话）与 `archive`（结构化事件）
- 摘要优先：归档记录保留 `summary` 与 `source_text`
- 向量分块：支持 summary/evidence 双通道向量记录
- 增量同步：按状态文件增量导入历史会话

### 3) 图谱关系
- 图谱独立层：`graph/memory.jsonl` 独立于 archive 文本层
- 关系追溯：每条关系可追溯 `source_event_id`
- 关系查询：`query_graph` 支持方向、关系类型、路径搜索
- 冲突治理：单值事实冲突进入队列，支持人工 `accept/reject` 闭环
- 可视化导出：`export_graph_view` 输出状态化图谱快照（含来源证据）
- 质量门禁：`graphQualityMode` 支持 `off/warn/strict`

### 4) 规则演进
- 反思沉淀：`reflect_memory` 将事件抽象为规则
- 去重治理：规则与事件均有去重控制，避免污染
- 规则复用：规则写入 `CORTEX_RULES.md` 供后续任务复用

### 5) 运维诊断
- `cortex_diagnostics`：模型连通、层级状态、字段对齐检查
- `backfill_embeddings`：支持 `incremental / vector_only / full`
- `lint_memory_wiki`：Wiki/图谱一致性巡检与修复建议
- 完整状态文件：便于快速定位同步、回填、质量问题

---
name: cortex-memory
description: Independent skill for Cortex Memory operations in OpenClaw. Use when users ask for cross-session memory continuity, prior decisions, preferences, relationship tracing, or memory maintenance. If the memory plugin is not installed, guide users to install and enable openclaw-cortex-memory first, then continue with normal memory workflows.
homepage: https://github.com/deki18/openclaw-cortex-memory
metadata: { "openclaw": { "os": ["darwin", "linux", "win32"], "primaryEnv": "EMBEDDING_API_KEY" } }
---

Use this runtime flow:

1. Check whether plugin `openclaw-cortex-memory` is available.
2. If missing or disabled, run the install bootstrap guide in `{baseDir}/references/agent-manual.md` with README-consistent install order.
3. After plugin is enabled, run memory retrieval or write operations.

After plugin is ready, use this default workflow:

1. Retrieve candidate memory with `search_memory`.
2. If the user asks about entity links or dependency paths, use `query_graph`.
3. If `query_graph` returns `conflict_hint`, use `list_graph_conflicts` and ask user confirmation before `resolve_graph_conflict`.
4. For graph status snapshots or projection consistency checks, use `export_graph_view` and `lint_memory_wiki`.
5. Answer with retrieved evidence first, then add reasoning.
6. If the turn introduces durable new information, persist it with `store_event`.
7. For maintenance windows or session wrap-up, run `sync_memory` and optionally `reflect_memory`.

If tool calls fail:

1. Check plugin availability first (`openclaw plugins list` / `openclaw plugins inspect openclaw-cortex-memory`).
2. If visible, run `cortex_diagnostics` (or legacy alias `diagnostics`).
3. Tell the user the plugin is unavailable or misconfigured.
4. Continue with a normal answer without fabricating memory hits.

Do not use this skill for:

- Real-time web facts (weather, stock, breaking news).
- One-off temporary context that should not be persisted.

Use these local references when needed:

- Install and bootstrap playbook: `{baseDir}/references/agent-manual.md`
- System prompt template: `{baseDir}/references/system-prompt-template.md`
- Tool details: `{baseDir}/references/tools.md`
- Config and dependency setup: `{baseDir}/references/configuration.md`
- Publish and validation checklist: `{baseDir}/references/publish-checklist.md`

For environment preflight, use `{baseDir}/references/publish-checklist.md`.
