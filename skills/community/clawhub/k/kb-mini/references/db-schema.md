# 数据库 Schema 详解

## 1. 主表结构

### 1.1 entries 表

```sql
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

### 1.2 FTS5 虚拟表

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
  content='entries',
  content_rowid='rowid'
);
```

## 2. 字段详解

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | UUID | 唯一标识 | `550e8400-e29b-41d4-a716-446655440000` |
| topic_key | String | 主题 key，用于 upsert | `openclaw-hooks-config` |
| title | String | 标题 | `OpenClaw Hooks 配置指南` |
| content | Text | 完整内容 | 详细配置说明... |
| source | Enum | 来源 | `rss/github/huggingface/manual` |
| tags | JSON | 标签数组 | `["openclaw", "hooks"]` |
| access_level | Int | 加载层级 | `0=L0, 1=L1, 2=L2` |
| created_at | ISO8601 | 创建时间 | `2026-03-22T10:00:00Z` |
| updated_at | ISO8601 | 更新时间 | `2026-03-22T10:00:00Z` |
| metadata | JSON | 扩展字段 | `{"url": "...", "author": "..."}` |

## 3. TopicKey 生成规则

```
topic_key = slugify(title)
          = lowercase
          = replace spaces with hyphens
          = remove special characters
          = truncate to 50 chars
```

**示例**：
- `OpenClaw Hooks 配置指南` → `openclaw-hooks`

**冲突处理**：
- 同一 topic_key 的内容 → 追加到现有记录，更新 updated_at
- 不同 topic_key → 新建记录

## 4. Access Level 分层

| Level | 名称 | 内容 | Token 限制 |
|-------|------|------|-----------|
| 0 | L0 摘要 | 标题 + 简短摘要 | < 200 tokens |
| 1 | L1 概览 | 标题 + 摘要 + 要点 | < 1000 tokens |
| 2 | L2 详情 | 完整内容 | 无限制 |

## 5. Source 枚举值

| 值 | 说明 |
|-----|------|
| `rss` | RSS 订阅源抓取 |
| `github` | GitHub 项目监测 |
| `huggingface` | HuggingFace 模型追踪 |
| `manual` | 用户手动输入 |
| `capture` | Hook 自动捕获 |
| `import` | 外部导入 |

## 6. 索引

```sql
-- 提升常见查询性能
CREATE INDEX idx_entries_source ON entries(source);
CREATE INDEX idx_entries_created_at ON entries(created_at);
CREATE INDEX idx_entries_topic_key ON entries(topic_key);
```

## 7. 数据保留策略

```sql
-- 删除超过 365 天且 access_level = 0 的 L0 摘要
DELETE FROM entries 
WHERE access_level = 0 
AND created_at < datetime('now', '-365 days');
```

## 8. Upsert 逻辑

```sql
INSERT INTO entries (id, topic_key, title, content, source, tags, access_level, created_at, updated_at, metadata)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(topic_key) DO UPDATE SET
  content = content || chr(10) || excluded.content,
  updated_at = excluded.updated_at,
  metadata = excluded.metadata;
```

**注意**：Upsert 时内容是**追加**而非覆盖，保留历史版本。

## 9. JSON 字段处理

### 9.1 tags 存储

```sql
-- 存入
INSERT INTO entries (tags) VALUES (json.dumps(["tag1", "tag2"]));

-- 查询 tag 包含某值
SELECT * FROM entries WHERE json_each(tags) = 'tag1';
```

### 9.2 metadata 存储

```sql
-- 存入
INSERT INTO entries (metadata) VALUES (json.dumps({"url": "...", "stars": 100}));

-- 查询特定字段
SELECT * FROM entries WHERE json_extract(metadata, '$.stars') > 50;
```

## 10. 迁移脚本模板

```sql
-- v0.1.0 -> v0.2.0 迁移
ALTER TABLE entries ADD COLUMN language TEXT DEFAULT 'zh';

-- 重建 FTS 索引
INSERT INTO knowledge_entries(knowledge_entries) VALUES('rebuild');
```
