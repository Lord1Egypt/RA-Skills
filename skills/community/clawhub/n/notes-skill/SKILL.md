---
name: notes-skill
description: |
  SQLite 笔记管理系统。由 AI agent（霜糖）代为管理和操作笔记。
  触发场景：
  - 用户说"笔记..."、"记一下..."、"帮我记..."、"存一条笔记"
  - 用户说"找一下..."、"搜一下关于...的笔记"
  - 用户说"列出笔记"、"有哪些笔记"
  - 用户说"标记已整理"、"归档"
  - 用户说"备份笔记"
  **任何和笔记相关的场景，都应当检查该skill**
  笔记数据存储在 ~/.openclaw/workspace/notes/notes.db
---

# SQLite 笔记系统

## 数据库位置

~/.openclaw/workspace/notes/notes.db

## 初始化

首次使用时运行初始化脚本：

```bash
python3 ~/.agents/skills/notes-skill/scripts/init.py
```

该脚本会创建目录和表结构。

## 表结构

```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    archived INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT (datetime('now', 'localtime'))
);
CREATE INDEX idx_notes_created ON notes(created_at DESC);
CREATE INDEX idx_notes_archived ON notes(archived);
```

## 写入笔记前的处理

收到笔记内容后，**先优化再写入**：

1. **结构优化**：适当分段、补充标点、整理格式，使笔记更易读
2. **错别字处理**：修正明显的拼写错误，保持原意不变
3. **不损失内容**：不删减、不曲解原文，只优化表达方式

**示例**：
- 用户输入：`今天学到了git clone 问题 报错 could not read Username`
- 优化后：`今天学到了 GitHub clone 的问题：报错 "could not read Username"。原因是非 TTY 环境下 git 的凭证读取机制有问题...`

## SQL 示例

### 添加笔记

收到笔记内容后，**先优化再写入**（见上方处理规则）。优化完成后写入：

```sql
INSERT INTO notes (content) VALUES ('优化后的笔记内容');
```

### 搜索（LIKE 模糊搜索）
```sql
SELECT * FROM notes WHERE content LIKE '%关键词%';
```

### 列出全部（按时间倒序）
```sql
SELECT * FROM notes ORDER BY created_at DESC;
```

### 筛选未归档
```sql
SELECT * FROM notes WHERE archived = 0;
```

### 标记已归档
```sql
UPDATE notes SET archived = 1 WHERE id = 3;
```

### 查看单条
```sql
SELECT * FROM notes WHERE id = 1;
```

## 定时备份任务

每天凌晨 2 点自动备份（通过 OpenClaw cron 触发）。

Agent 收到 `backup_notes` 事件时，执行：
```bash
python3 ~/.agents/skills/notes-skill/scripts/backup.py 3
```

## 手动备份

运行备份脚本：

```bash
python3 ~/.agents/skills/notes-skill/scripts/backup.py [保留份数]
```

- 不传参数：默认保留 7 份
- 传参数：如 `python3 backup.py 10` 保留 10 份

备份文件保存在 ~/.openclaw/workspace/notes/backups/。
