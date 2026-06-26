# CLAUDE.md

**项目：huo15-knowledge-base** — Karpathy LLM Knowledge Base

## 背景

Karpathy 方案：不用向量数据库，用 LLM 做"研究图书馆员"，把原始文档**增量地**编译并维护进一个**人类可读的 Wiki 百科**。LLM 全职做：摘要、交叉引用、index、log、lint。

```
raw/        ← 原始素材（只读）
  ↓ LLM 编译（按 wiki/SCHEMA.md 规范）
wiki/       ← 原子条目 + 强双链 + 三件套（index/log/SCHEMA）
  ↓ obsidian-sync
Obsidian Vault（可选） vault/知识库/<scope>/
```

**核心原则（v2.6.0 起严格执行）**：
- 一个 wiki 页 = 一个概念（不是"一篇文章 = 一页"）
- 一篇 raw 文档应该影响 5-15 个 wiki 页（创建少量 + 更新大量）
- 任何概念第一次提到必须 `[[]]` 双链
- 每次 ingest/compile/ask/lint 都写 log.md，每次 compile 都重建 index.md
- `kb-ask` 用 LLM 合成答案 + 引用，不是 grep——并且可以把答案归档回 wiki（"explorations compound"）

**v2.7.0 schema 升级**（对齐 LLM Wiki v2）：
- **Typed Relations**：frontmatter `relations:` 字段把 `[[]]` 双链按 uses/depends-on/extends/part-of/contradicts/supersedes/superseded-by/related 类型化
- **Confidence**：每条 wiki 带 0.0-1.0 可信度；≥0.9 才能 stable，<0.5 必须 TODO 注释
- **Supersession**：新事实推翻旧事实 → 双向 supersedes/superseded-by 标注，不删旧条目（保留证据链）
- **kb-graph** 按关系类型给 Mermaid 边上不同箭头；**kb-lint** 校验关系合法性 + 双向一致性 + 信度/状态匹配；**kb-index** 标 ✅🟡⚡🚧；**kb-ask** 优先采信高 confidence + 自动跳新页

**v2.8.0 Obsidian 深度集成**（结合 Karpathy 原方案 + Obsidian 1.9.10+ Bases）：
- **kb-bases**：生成 5 个 Obsidian Bases `.base` 文件（by-confidence / by-status / by-type / stub-orphan / recent），把 v2.7 的 frontmatter 字段变成开箱即用的数据库视图
- **kb-daily**：Obsidian Daily Note ↔ KB 双向打通；`ingest` 抓日记里的 URL/`==高亮==` 入库；`ask --append` 把问答结果追加回当天日记，落地"人类只负责 sourcing 和 asking"
- **obsidian-sync.sh --with-bases**：同步时自动生成 .base 到 `vault/知识库/<scope>/.bases/`
- **wiki 子目录推荐（不强制）**：在 wiki-schema §11 加入 Karpathy 原方案的 entities/concepts/sources/synthesis 4 子目录路由规则；旧平铺 wiki 继续合规

## 架构原则

- **双作用域**：
  - `agent` 作用域：每个 Agent 数据在 `~/.openclaw/agents/{agent-id}/agent/kb/`（默认，私有）
  - `shared` 作用域：跨 Agent 共享数据在 `~/.openclaw/kb/shared/`（通过 `--scope shared` 写入）
- **代码共享**：Skill 代码在技能目录，所有 Agent 共用
- **纯 Markdown**：不用数据库，wiki 是纯 .md 文件
- **无硬编码凭证**：LLM 凭据从 `models.json` 运行时加载
- **共享 KB 的对接**：@huo15/openclaw-enhance 会把 `~/.openclaw/kb/shared/wiki/` 注册为龙虾 memory 的 corpus（corpus="kb"），使 `memory_search` 能同时搜到共享知识库内容，而无需单独调用 `kb-search`

## 三层记忆/知识库协调

```
L1 龙虾原生 memory（~/.openclaw/memory/*.sqlite, per-agent）
    ├── L2 enhance 结构化记忆（短规则，enhance-memory.sqlite，corpus="enhance"）
    └── L3 共享知识库（长文档，~/.openclaw/kb/shared/wiki/, corpus="kb")
```

**内容归属判断**：
- **一句话能说清 + 关于「怎么做」** → L2 enhance_memory_store
- **整篇文档 + 关于「是什么」** → L3 kb-ingest --scope shared
- **Agent 个人实验性笔记** → L3 kb-ingest（默认 agent scope，不会被其它 agent 看到）

## 脚本清单

**核心（kb-* 前缀）：**
- `kb-ingest` — 入库，支持 URL/文件/文本，自动抓取；自动写 log.md
- `kb-compile` — 调用 LLM，raw → wiki；用外置 prompt（scripts/prompts/compile.md）+ 注入 SCHEMA + 现有 wiki 列表；编译后自动重建 index.md
- `kb-ask` — **合成式问答**：候选页 → LLM → 带 [[]] 引用的答案；`--save` 归档为新条目
- `kb-search` — 关键词搜索 wiki + Obsidian vault
- `kb-index` — 扫 wiki/，按 concepts 分组生成 wiki/index.md
- `kb-log` — 追加 log.md（事件 ingest/compile/ask/lint），支持 `--tail N`
- `kb-lint` — 体检：frontmatter / 断链 / stub / orphan / stale / 缺出处
- `kb-graph` — 生成 graph.mermaid（Mermaid 知识图谱）
- `kb-fetch` — 独立网页抓取（Python stdlib）
- `kb-llm.py` — LLM API 调用器（从 models.json 加载）

**模板与 prompt：**
- `templates/wiki-schema.md` — 首次激活时种入 `wiki/SCHEMA.md`，是给 LLM 看的图书馆员守则
- `scripts/prompts/compile.md` — kb-compile 的外置 prompt（Karpathy librarian 模式）

**Obsidian（可选）：**
- `obsidian-sync.sh` — wiki → vault 同步；支持 `--scope agent|shared` / `--shared` / `--all-scopes` / `--with-bases` (v2.8)
  - agent scope  → `vault/知识库/agent/`
  - shared scope → `vault/知识库/shared/`
  - `--with-bases` → 同步后跑 `kb-bases --vault-out` 生成 5 个 .base 视图
- `kb-bases` (v2.8) — 生成 Obsidian Bases `.base` 数据库视图（基于 v2.7 frontmatter 字段）
- `kb-daily` (v2.8) — Obsidian Daily Note ↔ KB 双向打通（ingest / ask --append）

**其他（已废弃/合并）：**
- `compile.sh`, `ingest.sh`, `search.sh`, `lint.sh` — 废弃，勿用
- `init.sh`, `activate.sh` — 被 kb-ingest 自动激活取代

## 开发规范

- Python 脚本仅用标准库，无第三方依赖
- LLM 调用走 `kb-llm.py`，不直接调用 API
- 配置走 `config.json`，敏感信息不上传
- 核心脚本不超过 200 行
