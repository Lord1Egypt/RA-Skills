---
name: memory-tree-universal
description: "Memory Tree 记忆树架构 — 通用版，适用于任何 AI Agent 的长期记忆系统。包含三棵树设计、热冷路径管道、14 条打分规则、数据库 Schema、检索 API 和坑点总结。当用户需要记忆系统、长期记忆、AI Agent 记忆架构时加载此技能。"
tags:
  - memory
  - architecture
  - agent-design
  - retrieval
  - long-term-memory
metadata:
  openclaw:
    emoji: 🌳
    homepage: ""
    requires:
      bins:
        - python3
      env: []
      config: []
---

# Memory Tree 记忆树架构 — 通用版

> 源自 OpenHuman Memory Tree 设计理念，经 Hermes Agent 实战验证后抽象为通用架构。
> 适用于任何需要长期记忆、多轮对话、信息压缩的 AI Agent 系统。

## 一、核心思想

**问题**：传统 Agent 记忆是"碎片袋"——所有对话塞进 context，越聊越慢，重要信息被淹没。

**答案**：Memory Tree 把记忆变成"大脑"——有层次、有分类、有热度、有压缩。

### 三棵树，三个作用域

| 树 | 作用域 | 功能 |
|---|---|---|
| **Source Tree** | 每个来源（QQ/飞书/文档） | 滚动缓冲区，L0→L1→L2 级联压缩 |
| **Topic Tree** | 每个实体（人/项目/概念） | 热度驱动，越频繁越深入 |
| **Global Tree** | 全局 | 每日摘要，跨来源聚合 |

### 为什么是树，不是向量库？

向量库只能回答"什么与查询相似"。树能回答：
- "今天发生了什么？" → Global Tree
- "这个人的最新动态？" → Topic Tree + hotness
- "上周二下午 3 点说了什么？" → Source Tree + provenance

**结构让记忆可导航，嵌入保证语义搜索。**

## 二、架构流程

```
输入源（聊天/文档/邮件）
    ↓
Canonicalize → 标准化 Markdown + 来源元数据
    ↓
Chunker → 确定性 ID, ≤3k token/块
    ↓
Fast Score → 14 条规则快速打分（无 LLM）
    ↓
Persist → SQLite 持久化（chunks + FTS5 索引）
    ↓
┌─────────────────────────────────────┐
│         冷路径（异步后台）            │
├─────────────────────────────────────┤
│ Deep Score → LLM 判断 admitted/dropped │
│ Entity Extract → 提取实体             │
│ Topic Route → 自动分类               │
│ Hotness Engine → 热度追踪            │
│ Sealer → L0→L1 摘要压缩              │
└─────────────────────────────────────┘
    ↓
检索 → 中文 LIKE / 英文 FTS5 MATCH + 热度排序
```

## 三、热路径管道（无 LLM，<50ms）

### 1. Canonicalize（标准化）

每条消息转为统一 Markdown 格式：

```markdown
[role: user] [source: qqbot] [time: 2026-05-19 01:16]

记住：项目预算 5 万，9 月 15 日前完成。
```

元数据字段：source, role, timestamp, session_id, message_id

### 2. Chunk（分块）

- 语义分块，≤3000 token/块
- 确定性 ID：`{session_id[:12]}-{role[:3]}-{index:03d}-{hash_suffix}`
- hash_suffix = SHA256(content)[:16]
- `INSERT OR IGNORE` 自动去重

### 3. Fast Score（14 条规则，无 LLM）

| 规则 | 分值 | 示例 |
|---|---|---|
| 用户明确要求记忆 | +0.25 | "记住"、"保存" |
| 用户偏好信息 | +0.25 | "喜欢"、"讨厌" |
| 金额信息 | +0.20 | "5 万"、"100 元" |
| 重要标记 | +0.20 | "重要"、"必须" |
| 情感/需求 | +0.15 | "需要"、"想要" |
| 错误/异常 | +0.15 | "bug"、"报错" |
| 版本信息 | +0.10 | "v0.14.0" |
| 项目相关 | +0.10 | "yinmei 项目" |
| 配置信息 | +0.10 | "config" |
| 首次事件 | +0.10 | 第一次提到 |
| 成功/完成 | +0.10 | "完成"、"成功" |
| 凭证相关 | +0.05 | "API key" |
| 时间信息 | +0.05 | "2026-05-19" |
| 短文本惩罚 | ×0.5 | <20 字 |

### 4. 数据库 Schema

```sql
-- 记忆块
CREATE TABLE memory_chunks (
  id TEXT PRIMARY KEY,
  session_id TEXT,
  message_id INTEGER,
  content TEXT,
  content_hash TEXT,
  token_count INTEGER,
  source TEXT,
  role TEXT,
  timestamp REAL,
  score REAL,
  is_admitted INTEGER,  -- 0=dropped, 1=admitted, 2=sealed
  score_reasons TEXT    -- JSON 数组
);

-- 主题/实体
CREATE TABLE memory_topics (
  id INTEGER PRIMARY KEY,
  name TEXT,
  entity_type TEXT,
  hotness REAL,
  summary TEXT,
  last_updated REAL
);

-- Chunk-Topic 关联
CREATE TABLE memory_chunk_topics (
  chunk_id TEXT,
  topic_id INTEGER,
  relevance REAL
);

-- 摘要（L1/L2）
CREATE TABLE memory_summaries (
  id INTEGER PRIMARY KEY,
  topic_id INTEGER,
  level INTEGER,  -- 1=L1, 2=L2
  content TEXT,
  child_chunk_ids TEXT,
  sealed_at REAL
);

-- FTS5 全文索引（外部内容表）
CREATE VIRTUAL TABLE memory_chunks_fts USING FTS5(
  content='memory_chunks',
  content_rowid='rowid'
);

-- Trigram 索引（中文搜索）
CREATE VIRTUAL TABLE memory_chunks_fts_trigram USING fts5tokenize=trigram(...);
```

## 四、冷路径管道（异步，有 LLM）

### 1. JobQueue（SQLite 轻量队列）

```sql
CREATE TABLE memory_jobs (
  id INTEGER PRIMARY KEY,
  job_type TEXT,       -- deep_score / entity_extract / digest
  payload TEXT,        -- JSON
  dedupe_key TEXT,
  status TEXT,         -- pending / running / completed / failed
  worker_id TEXT,
  lease_expires REAL,
  retry_count INTEGER
);
```

### 2. DeepScorer（LLM 判断）

兜底规则（不调用 LLM 时）：
- 含"记住/偏好/预算" → admitted
- <15 字 → dropped

### 3. EntityExtractor（正则提取）

| 实体类型 | 正则模式 |
|---|---|
| 仓库 | github\.com/[^/\s]+/[^/\s]+ |
| 网站 | https?://[^\s]+ |
| 版本 | v?\d+\.\d+\.\d+ |
| 日期 | \d{4}-\d{2}-\d{2} |
| 金额 | \d+[万块元]+ |
| 项目名 | [a-zA-Z][a-zA-Z0-9_-]+ |
| 人名 | [一-龯]{2,4} |

### 4. TopicRouter（自动分类）

实体 → 主题路由规则：
- `github.com/...` → `repo:<org>/<name>`
- `v1.2.3` → `version:<name>`
- `5 万` → `budget:<project>`
- 首次出现 → 自动创建主题

### 5. HotnessEngine（热度追踪）

```
每次提及: hotness += 0.05
每日衰减: hotness *= 0.95
活跃阈值: 0.5（高于此值优先检索）
归档阈值: 0.1（低于此值压缩为摘要）
```

### 6. Sealer（摘要压缩）

```
L0 chunk 累积到阈值（如 10 个）→ 触发 seal
  ↓
LLM 生成 L1 摘要
  ↓
标记子 chunk is_admitted=2（已密封）
  ↓
L1 摘要存入 memory_summaries
```

## 五、检索 API

### 搜索（中文 LIKE + 英文 FTS5 MATCH）

```python
def search(query, limit=10, min_score=0.1, topic=None, days=None):
    has_cjk = bool(re.search(r'[\u4e00-\u9fff]', query))
    
    if has_cjk:
        # 中文：LIKE（准确但慢）
        sql = """
            SELECT c.*, t.name as topic_name, t.hotness
            FROM memory_chunks c
            LEFT JOIN memory_chunk_topics ct ON c.id = ct.chunk_id
            LEFT JOIN memory_topics t ON ct.topic_id = t.id
            WHERE c.content LIKE ? AND c.is_admitted >= 1
            AND c.score >= ?
            ORDER BY c.score DESC, t.hotness DESC
            LIMIT ?
        """
        params = [f'%{query}%', min_score, limit]
    else:
        # 英文：FTS5 MATCH（快）
        sql = """
            SELECT c.*, t.name as topic_name, t.hotness
            FROM memory_chunks c
            JOIN memory_chunks_fts f ON c.rowid = f.rowid
            LEFT JOIN memory_chunk_topics ct ON c.id = ct.chunk_id
            LEFT JOIN memory_topics t ON ct.topic_id = t.id
            WHERE f MATCH ? AND c.is_admitted >= 1
            AND c.score >= ?
            ORDER BY c.score DESC, t.hotness DESC
            LIMIT ?
        """
        params = [query, min_score, limit]
```

### 其他检索方法

| 方法 | 说明 |
|---|---|
| `search(query)` | 全文搜索 |
| `get_topic_summary(topic_id)` | 主题详情（hotness、chunk 数、摘要） |
| `get_hot_topics(limit)` | 热门主题排行 |
| `search_by_session(session_id)` | 按会话检索 |
| `get_global_stats()` | 全局统计 |

## 六、与 Hermes Agent 集成

### 配置

```yaml
# config.yaml
agent:
  memory_tree_enabled: true
```

### 集成点

1. **AIAgent.__init__**：初始化 MemoryTreeBridge
2. **_build_system_prompt_parts**：注入检索到的相关记忆
3. **run_conversation**：每轮对话后调用 `bridge.ingest_turn()`

### CLI 命令

```
/memory-tree stats     # 统计信息
/memory-tree search <q> # 搜索记忆
/memory-tree topics    # 主题列表
/memory-tree clear     # 清除数据（需确认）
```

## 七、关键坑点（血泪教训）

### 1. is_admitted 存的是 0/1，不是 score

**错**：`is_admitted = score`
**对**：`is_admitted = 1`（单独存 score 列）

### 2. INSERT 参数数量必须匹配列数

每增加一列，VALUES 必须增加一个参数。否则 `INSERT OR IGNORE` 静默失败。

### 3. NOT IN 遇到 NULL 返回空

```sql
-- 错：所有行被过滤
WHERE id NOT IN (SELECT chunk_id FROM memory_jobs)

-- 对：显式排除 NULL
WHERE payload->>'chunk_id' IS NOT NULL
```

### 4. FTS5 外部内容表删除需特殊处理

```python
# 先清空 FTS5 索引
c.execute("INSERT INTO memory_chunks_fts(memory_chunks) VALUES('delete')")
# 再删除父表
c.execute("DELETE FROM memory_chunks WHERE ...")
```

### 5. 中文搜索不能用 FTS5 MATCH

SQLite FTS5 对中文逐字分词，"预算"分成"预"和"算"，MATCH 返回 0 结果。
**唯一可靠方案**：LIKE `%预算%`

### 6. SQLite WAL 锁冲突

清理数据用独立进程，清理前关闭所有 Python 连接。

## 八、通用适配指南

### 适配到非 Hermes 项目

1. **数据库**：替换 SQLite 路径为你的项目路径
2. **来源适配器**：实现 `canonicalize()` 方法，适配你的输入源
3. **LLM 调用**：替换 DeepScorer 的 LLM 调用为你的模型
4. **检索集成**：在 prompt 构建时调用 `search()` 注入上下文

### 最小可用版本（MVP）

只需实现：
1. `memory_chunks` 表 + FTS5 索引
2. `ingest(messages)` → 分块 + 打分 + 入库
3. `search(query)` → LIKE/MATCH 检索

冷路径（LLM 深度处理）可选。

## 九、扩展方向

- **L2 全局摘要**：每日 digest，跨所有来源
- **Web UI**：可视化主题树、热度趋势
- **跨会话聚合**：相似 session 自动合并主题
- **向量嵌入**：在 FTS5 基础上增加向量相似度检索
- **多语言支持**：针对不同语言优化分词策略

## 十、参考实现

Hermes Agent 完整实现（~1944 行）：
- `agent/memory_tree.py` — 热路径管道
- `agent/memory_tree_cold.py` — 冷路径管道
- `agent/memory_tree_retrieval.py` — 检索 API
- `agent/memory_tree_clean.py` — 清理脚本
- `agent/memory_tree_integration.py` — Hermes 桥接器

测试脚本：`scripts/quick_test.py`
调试记录：`references/debug-log.md`
快速上手：`references/quickstart.md`