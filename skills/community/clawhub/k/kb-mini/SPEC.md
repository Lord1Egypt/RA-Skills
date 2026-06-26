# Knowledge Base Skill - 设计规格文档

**版本**: v1.0.0
**日期**: 2026-03-22
**状态**: `draft`
**仓库**: https://github.com/ThomasLiu/knowledge-base-skill

---

## 1. 概述

### 1.1 目标

创建一个通用的 **Knowledge Base Skill**，为 OpenClaw Agent 提供知识存储和检索能力。

### 1.2 核心定位

- **只负责怎么存、怎么取**
- **不内置采集逻辑**（collector 由外部 Agent 决定）
- **支持私有 KB 和共享 KB**
- **轻量级、零外部依赖**

### 1.3 三大核心功能

| 功能 | 触发时机 | 说明 |
|------|----------|------|
| **Collect** | Agent 主动调用 | 存入数据到 KB |
| **Recall** | 每次对话前 (before_agent_start) | 自动检索相关知识 |
| **Capture** | 每次回复后 (after_turn) | 自动记忆重要内容 |

### 1.4 借鉴的设计

基于 GitHub/Skill 市场调研，借鉴以下项目：

| 项目 | 借鉴点 |
|------|--------|
| **obsidian-agent-memory-skills** | Proactive session orientation, Token 优化, Bidirectional relationships |
| **openclaw-superpowers** | SQLite + FTS5, DAG-based memory compaction, Integrity checker |
| **para-memory** | Lifecycle management, Daily memory log |

---

## 2. 目录结构

```
knowledge-base/
├── SKILL.md                    # Skill 定义（触发条件、接口说明）
├── scripts/
│   ├── storage.sh              # 存储核心 API
│   │   ├── store               # 存入单条
│   │   ├── search              # 检索
│   │   ├── retrieve            # 按 topic_key 取
│   │   └── batch_store         # 批量存入
│   ├── hooks.sh                # Hooks 集成
│   │   ├── before_agent_start  # 对话前：recall（借鉴 proactive orientation）
│   │   └── after_turn         # 对话后：capture
│   ├── retriever.sh            # 检索排序
│   │   ├── fuse_rank           # RRF 融合
│   │   ├── time_decay          # 时间衰减
│   │   └── dag_compactor       # DAG 层级摘要（借鉴 openclaw-superpowers）
│   ├── lifecycle.sh            # 生命周期管理（借鉴 para-memory）
│   │   ├── archive             # 归档旧记录
│   │   └── cleanup             # 清理过期数据
│   └── config.sh               # 路径配置
├── references/
│   ├── db-schema.md            # 数据库 Schema
│   ├── api-spec.md             # API 接口规范
│   └── retrieval-pipeline.md  # 检索流程详解
├── tests/
│   └── *_test.sh               # TDD 测试
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
  status TEXT DEFAULT 'active',  -- active/stale/archived
  created_at TEXT,
  updated_at TEXT,
  archived_at TEXT,
  metadata TEXT
);

CREATE INDEX idx_entries_status ON entries(status);
CREATE INDEX idx_entries_created_at ON entries(created_at);
CREATE INDEX idx_entries_topic_key ON entries(topic_key);
```

### 3.2 生命周期状态

| 状态 | 说明 | 转换条件 |
|------|------|----------|
| `active` | 活跃记录 | 默认状态 |
| `stale` | 陈旧但未归档 | 90 天无更新 |
| `archived` | 已归档 | 365 天前创建 + stale |

---

## 4. 检索机制

### 4.1 Pipeline

```
Query → 解析 → FTS5 搜索 → RRF 融合 → 时间衰减 → DAG 摘要 → 分层加载 → Top-K
```

### 4.2 RRF (Reciprocal Rank Fusion)

多策略结果融合：

| 策略 | 说明 |
|------|------|
| 关键词匹配 | FTS5 直接匹配 |
| 标签匹配 | 命中的 tags |
| 来源偏好 | 同一来源加权 |
| 时间衰减 | 最近的内容排名更高 |

### 4.3 DAG 层级摘要（借鉴 openclaw-superpowers）

```
d3 (Root)     - 高层次洞察
   ↓
d2 (Summary)  - 摘要层
   ↓
d1 (Overview) - 概览层
   ↓
d0 (Leaf)     - 原始内容
```

- **d0**: 完整内容（L2）
- **d1**: 概览 + 要点（L1, < 1000 tokens）
- **d2**: 简短摘要（L0, < 200 tokens）
- **d3**: 高层次洞察（可选）

### 4.4 时间衰减

```
decay = e^(-λ * days_ago)
```

- λ = 0.1
- 7 天前权重 ≈ 0.5

---

## 5. Hooks 集成

### 5.1 before_agent_start（借鉴 obsidian proactive orientation）

```
用户发送消息
       ↓
Hook 拦截 → 调用 kb recall
       ↓
解析用户消息，提取关键词
       ↓
检索相关知识（只取 L0/L1，限制 token）
       ↓
注入上下文到 Agent
```

**优化点**：
- 只读 L0/L1 层（< 200 tokens 总计）
- 最多读 3 个相关条目
- frontmatter-first scanning

### 5.2 after_turn

```
Agent 生成回复
       ↓
Hook 拦截 → 调用 kb capture
       ↓
分析本次对话，提取：
  - 新决策/结论
  - 用户偏好/配置
  - 重要上下文
       ↓
判断是否值得记忆（阈值 0.7）
       ↓
store() 存入知识库
```

---

## 6. 配置

### 6.1 路径配置

```bash
# 模式
export KNOWLEDGE_KB_MODE="${KNOWLEDGE_KB_MODE:-private}"

# 私有 KB
export KNOWLEDGE_DB_PRIVATE="$AGENT_DIR/knowledge.db"

# 共享 KB
export KNOWLEDGE_DB_SHARED="$HOME/.openclaw/shared/knowledge-bases/<kb-name>/knowledge.db"
```

### 6.2 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| KNOWLEDGE_KB_MODE | private/shared | private |
| KNOWLEDGE_DB | 数据库路径 | AGENT_DIR/knowledge.db |
| KNOWLEDGE_RECALL_LIMIT | recall 最大条目数 | 3 |
| KNOWLEDGE_RECALL_MAX_TOKENS | recall 最大 token | 500 |
| KNOWLEDGE_ARCHIVE_DAYS | 归档阈值（天） | 365 |
| KNOWLEDGE_STALE_DAYS | 陈旧阈值（天） | 90 |

---

## 7. API 接口

### 7.1 store

```bash
kb store --title "..." --content "..." --tags "tag1,tag2" --source "manual"
```

### 7.2 search

```bash
kb search --query "openclaw hooks" --limit 5 --level 1
```

### 7.3 recall（Hook 调用）

```bash
kb recall --context "用户问如何配置 hooks"
```

**输出**：
```json
{
  "injected_context": "相关知识：\n1. OpenClaw Hooks 配置指南\n...",
  "entries_used": 3,
  "tokens_used": 450
}
```

### 7.4 capture（Hook 调用）

```bash
kb capture --turn "用户问... Agent 回复..."
```

**输出**：
```json
{
  "captured": true,
  "topic_key": "openclaw-hooks-001",
  "decision": "值得记忆：新决策"
}
```

### 7.5 lifecycle

```bash
# 归档旧记录
kb lifecycle archive

# 清理过期数据
kb lifecycle cleanup
```

---

## 8. 与 Agent 的集成

### 8.1 Cron Job 集成

```
Agent 创建定时任务时：
1. 询问是否需要存入知识库
2. 如果是，选择存储模式（私有/共享）
3. Cron job 包含调用 kb store 的逻辑
```

### 8.2 Hook 集成

```bash
# 在 OpenClaw 配置 hooks.sh
before_agent_start → kb recall
after_turn → kb capture
```

---

## 9. 知识库共享模式

### 9.1 私有 KB

- 路径：`~/.openclaw/agents/<agent-id>/knowledge.db`
- 用途：仅该 Agent 使用

### 9.2 共享 KB

- 路径：`~/.openclaw/shared/knowledge-bases/<kb-name>/knowledge.db`
- 用途：多 Agent 共享

---

## 10. TDD 开发流程

| 阶段 | 测试 | 实现 |
|------|------|------|
| RED | 写测试用例 | 验证失败 |
| GREEN | 最小实现 | 测试通过 |
| REFACTOR | 重构代码 | 保持测试通过 |

---

## 11. 验收标准

### Phase 1: 核心存储
- [ ] storage.sh store/search/retrieve 实现
- [ ] SQLite FTS5 索引建立
- [ ] TopicKey upsert 逻辑

### Phase 2: 检索增强
- [ ] RRF 融合
- [ ] 时间衰减
- [ ] 分层加载

### Phase 3: Hooks 集成
- [ ] before_agent_start recall
- [ ] after_turn capture
- [ ] Token 优化

### Phase 4: 生命周期
- [ ] DAG 摘要生成
- [ ] 归档策略
- [ ] 清理策略

---

## 12. 参考项目

| 项目 | Stars | 链接 | 借鉴点 |
|------|-------|------|--------|
| obsidian-agent-memory-skills | 27 | github.com/AdamTylerLynch/... | Proactive orientation, Token 优化 |
| openclaw-superpowers | 25 | github.com/ArchieIndian/... | SQLite + FTS5, DAG compaction |
| para-memory | 4 | github.com/theSamPadilla/... | Lifecycle management |
| awesome-openclaw-skills | 40.6k | github.com/VoltAgent/... | Skill 收录集合 |

---

## 13. 变更记录

| 日期 | 版本 | 变更内容 |
|------|------|----------|
| 2026-03-22 | 1.0.0 | 初始版本，基于调研结果优化设计 |
