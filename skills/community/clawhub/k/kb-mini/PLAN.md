# Knowledge Base Skill 设计方案

**版本**: v0.1.0
**日期**: 2026-03-22
**状态**: 调研中

---

## 1. 概述

### 1.1 目标
创建一个通用的 **Knowledge Base Skill**，为 OpenClaw Agent 提供知识存储和检索能力。

### 1.2 核心定位
- **只负责怎么存、怎么取**
- **不内置采集逻辑**（collector 由外部 Agent 决定）
- **支持私有 KB 和共享 KB**

### 1.3 三大核心功能

| 功能 | 触发时机 | 说明 |
|------|----------|------|
| **Collect** | Agent 主动调用 | 存入数据到 KB |
| **Recall** | 每次对话前 (before_agent_start) | 自动检索相关知识 |
| **Capture** | 每次回复后 (after_turn) | 自动记忆重要内容 |

---

## 2. 目录结构

```
knowledge-base/
├── SKILL.md                    # Skill 定义（触发条件、接口说明）
├── scripts/
│   ├── storage.sh              # 存储核心 API
│   │   ├── store              # 存入单条
│   │   ├── search             # 检索
│   │   ├── retrieve           # 按 topic_key 取
│   │   └── batch_store        # 批量存入
│   ├── hooks.sh                # Hooks 集成
│   │   ├── before_agent_start  # 对话前：recall
│   │   └── after_turn         # 对话后：capture
│   ├── retriever.sh            # 检索排序
│   │   ├── fuse_rank           # RRF 融合
│   │   └── time_decay          # 时间衰减
│   └── config.sh               # 路径配置
├── references/
│   ├── db-schema.md            # 数据库 Schema
│   ├── api-spec.md             # API 接口规范
│   └── retrieval-pipeline.md  # 检索流程详解
└── README.md                   # 使用说明
```

---

## 3. 数据库设计

### 3.1 Schema

```sql
CREATE VIRTUAL TABLE knowledge_entries USING fts5(
  id,
  topic_key,
  title,
  content,
  source,
  tags,
  access_level,
  created_at,
  updated_at,
  metadata
);

CREATE TABLE entries (
  id TEXT PRIMARY KEY,
  topic_key TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  source TEXT NOT NULL,
  tags TEXT,
  access_level INTEGER DEFAULT 2,
  created_at TEXT,
  updated_at TEXT,
  metadata TEXT
);
```

### 3.2 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 唯一标识 |
| topic_key | String | 主题 key，同一主题 upsert |
| title | String | 标题 |
| content | Text | 完整内容 |
| source | Enum | rss, github, huggingface, manual |
| tags | JSON | 标签数组 |
| access_level | Int | 0:L0摘要, 1:L1概览, 2:L2详情 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |
| metadata | JSON | 扩展字段 |

---

## 4. 存储接口 (storage.sh)

### 4.1 store - 存入单条

```bash
kb store --title "..." --content "..." --tags "tag1,tag2" --source "manual"
```

**参数**：
- `--title`: 标题
- `--content`: 完整内容
- `--topic-key`: 可选，默认自动生成
- `--tags`: 逗号分隔的标签
- `--source`: 来源 (rss/github/huggingface/manual)
- `--level`: 加载层级 (0/1/2)

**输出**：
```json
{"status": "ok", "id": "uuid", "topic_key": "..."}
```

### 4.2 search - 检索

```bash
kb search --query "openclaw hooks" --limit 5 --level "L1"
```

**参数**：
- `--query`: 搜索关键词
- `--limit`: 返回数量
- `--level`: 加载层级
- `--time-decay`: 时间衰减因子

**输出**：
```json
{
  "results": [...],
  "total_hits": 12,
  "query_time_ms": 45
}
```

### 4.3 retrieve - 按 topic_key 取

```bash
kb retrieve --topic-key "openclaw-hooks-001"
```

### 4.4 batch_store - 批量存入

```bash
kb batch_store --file "/path/to/entries.jsonl"
```

---

## 5. 检索机制 (retriever.sh)

### 5.1 Pipeline

```
Query → 解析 → FTS5 搜索 → RRF 融合 → 时间衰减 → 分层加载 → Top-K
```

### 5.2 RRF (Reciprocal Rank Fusion)

多策略结果融合：

| 策略 | 说明 |
|------|------|
| 关键词匹配 | FTS5 直接匹配 |
| 标签匹配 | 命中的 tags |
| 来源偏好 | 同一来源加权 |
| 时间衰减 | 最近的内容排名更高 |

**公式**：
```
score = Σ (1 / (k + rank_i)) for each strategy i
```

### 5.3 时间衰减

```
decay = e^(-λ * days_ago)
```

- λ 通常取 0.1
- 7 天前的内容权重 ≈ 0.5

### 5.4 分层加载 (L0/L1/L2)

| 层级 | 内容 | Token 限制 |
|------|------|-----------|
| L0 | 标题 + 摘要 | < 200 tokens |
| L1 | 概览 + 要点 | < 1000 tokens |
| L2 | 完整内容 | 无限制 |

---

## 6. Hooks 集成 (hooks.sh)

### 6.1 before_agent_start - 对话前 Recall

```
用户发送消息
       ↓
Hook 拦截 → 调用 knowledge-base skill
       ↓
分析用户消息，提取关键词
       ↓
search() 检索相关知识
       ↓
注入 L0/L1 上下文到 Agent
```

### 6.2 after_turn - 对话后 Capture

```
Agent 生成回复
       ↓
Hook 拦截 → 调用 knowledge-base skill
       ↓
分析本次对话，提取：
  - 新决策/结论
  - 用户偏好/配置
  - 重要上下文
       ↓
store() 存入知识库
```

---

## 7. 配置 (config.sh)

### 7.1 路径配置

```bash
# 模式：private 或 shared
export KNOWLEDGE_KB_MODE="${KNOWLEDGE_KB_MODE:-private}"

# 私有 KB 路径
export KNOWLEDGE_DB_PRIVATE="$AGENT_DIR/knowledge.db"

# 共享 KB 路径
export KNOWLEDGE_DB_SHARED="$HOME/.openclaw/shared/knowledge-bases/<kb-name>/knowledge.db"

# 最终路径
if [ "$KNOWLEDGE_KB_MODE" = "shared" ]; then
  export KNOWLEDGE_DB="$KNOWLEDGE_DB_SHARED"
else
  export KNOWLEDGE_DB="$KNOWLEDGE_DB_PRIVATE"
fi
```

### 7.2 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| KNOWLEDGE_KB_MODE | private/shared | private |
| KNOWLEDGE_DB | 数据库路径 | AGENT_DIR/knowledge.db |
| KNOWLEDGE_FTS_WEIGHT_TITLE | 标题权重 | 2.0 |
| KNOWLEDGE_FTS_WEIGHT_CONTENT | 内容权重 | 1.0 |

---

## 8. 知识库共享模式

### 8.1 私有 KB

- 路径：`~/.openclaw/agents/<agent-id>/knowledge.db`
- 用途：仅该 Agent 使用
- 特点：数据完全隔离

### 8.2 共享 KB

- 路径：`~/.openclaw/shared/knowledge-bases/<kb-name>/knowledge.db`
- 用途：多 Agent 共享同一知识库
- 特点：数据集中存储，组内所有 Agent 可读写

### 8.3 目录结构

```
~/.openclaw/
├── shared/
│   └── knowledge-bases/
│       ├── coding-kb/         # AI Coding 共享知识库
│       │   └── knowledge.db
│       └── research-kb/       # 研究类共享知识库
│           └── knowledge.db
├── agents/
│   ├── agent-a/
│   │   └── knowledge.db  ──────────→ shared/coding-kb/
│   ├── agent-b/
│   │   └── knowledge.db  ──────────→ shared/coding-kb/
```

---

## 9. Skill 触发条件

### 9.1 触发关键词

- "加入知识库" / "存到 KB"
- "knowledge base" / "知识库"
- "记得这个" / "保存上下文"
- "检索知识库" / "查一下 KB"

### 9.2 自动触发场景

1. **定时任务创建时**：询问是否需要采集信息到 KB
2. **before_agent_start**：自动 recall 相关知识
3. **after_turn**：自动 capture 新内容

---

## 10. 与 Agent 的集成方式

### 10.1 Cron Job 集成

```
Agent 创建定时任务时：
1. 询问是否需要存入知识库
2. 如果是，选择存储模式（私有/共享）
3. Cron job 包含调用 kb store 的逻辑
```

### 10.2 Hook 集成

```
1. 在 OpenClaw 配置 hooks.sh
2. before_agent_start → kb recall
3. after_turn → kb capture
```

---

## 11. 下一步

- [ ] 步骤 2：补充详细参考文档
- [ ] 步骤 3：调研 GitHub 和 Skill 市场
- [ ] 步骤 4：分析参考方案
- [ ] 步骤 5：优化并发布到 GitHub

---

## 附录

### A. 输出格式示例

**search 输出**：
```json
{
  "results": [
    {
      "topic_key": "openclaw-hooks-001",
      "title": "OpenClaw Hooks 配置指南",
      "level": "L1",
      "summary": "OpenClaw 支持 before_agent_start...",
      "url": "optional-link",
      "relevance_score": 0.85,
      "source": "manual",
      "updated_at": "2026-03-22"
    }
  ],
  "total_hits": 12,
  "query_time_ms": 45
}
```

### B. 参考项目

- [engram](https://github.com/khulnasoft/engram) - SQLite FTS5、TopicKey Upsert
- [MemOS](../Projects/MemOS) - RRF+MMR 检索、SkillEvolver
- [OpenViking](../Projects/OpenViking) - 分层加载、Context Engine
- [MemMachine](../Projects/MemMachine) - 四级隔离、Auto Hooks
