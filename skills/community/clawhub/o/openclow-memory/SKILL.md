---
name: memory-system
description: "OpenClaw 长期记忆管理系统。提供结构化记忆、向量记忆、语义搜索功能。Use when: 用户需要 AI 记住长期上下文、偏好、决策，或需要从记忆中进行语义搜索。"
metadata:
  {
    "openclaw": { "emoji": "🧠" },
    "version": "1.0.0",
    "author": "damien"
  }
---

# Memory System Skill

OpenClaw 长期记忆管理系统

## 功能

### 1. 结构化记忆 (PostgreSQL)
- 目标 (Goals)
- 决策 (Decisions)  
- 状态 (Status)
- 偏好 (Preferences)
- 参考资料 (Reference)

### 2. 向量记忆 (pgvector)
- 支持语义搜索
- 中文 embedding (bge-large-zh)
- 相似度匹配

### 3. 自动归档
- 本地文件保留 7 天
- 自动导入 PostgreSQL

## 数据库

| 数据库 | 端口 | 用途 |
|--------|------|------|
| Postgres.app | 5432 | 结构化记忆 |
| Homebrew PG | 5433 | 向量搜索 |

## 连接

```bash
# 结构化记忆
psql -h localhost -p 5432 -U damien -d postgres

# 向量记忆  
psql -h localhost -p 5433 -U damien -d postgres
```

## 表结构

### memory_structured (结构化)
```sql
CREATE TABLE memory_structured (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50),  -- goals, decisions, status, preferences, reference
    title VARCHAR(200),
    content TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### longterm_memory (向量)
```sql
CREATE TABLE longterm_memory (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(1024),
    source VARCHAR(100),
    tags TEXT[],
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX ON longterm_memory USING hnsw (embedding vector_cosine_ops);
```

## 脚本

- `scripts/memory_manager.py` - 归档脚本（每周自动运行）
- `scripts/memory_search.py` - 向量搜索工具

## 使用

### 读取记忆
```bash
# 读取目标
psql -h localhost -p 5432 -U damien -d postgres -c "SELECT * FROM memory_structured WHERE category='goals';"

# 语义搜索
python scripts/memory_search.py "我之前说过我喜欢什么编程语言"
```

### 更新记忆
```bash
python scripts/memory_manager.py --add "goals" "新目标" "内容"
```

## 四种记忆方法

根据视频教程配置：
1. **结构化文件夹** - Markdown 文件 (~/.openclaw/workspace/memory/)
2. **Memory Search** - bge-large-zh embedding
3. **MEM0 插件** - 待配置
4. **SQLite/PostgreSQL** - 已配置

---
更新于: 2026-03-08
