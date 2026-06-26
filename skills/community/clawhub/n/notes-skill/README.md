# Notes Skill / 笔记技能

[English](#english) | [中文](#中文)

---

## English

A SQLite-based notes management skill for **OpenClaw** AI assistant, powered by an AI agent (霜糖/Shuangtang).

### Features

- **Create notes** — Quick note-taking with automatic timestamp
- **Search notes** — Full-text search across all notes
- **List notes** — View all notes with archiving status
- **Archive notes** — Mark notes as organized/archived
- **Backup** — Automated daily backups with rotation

### Database

- Location: `~/.openclaw/workspace/notes/notes.db`
- Backup: `~/.openclaw/workspace/notes/backups/`
- Auto-backup: Daily at 02:00 AM (retains 3 backups)

### Schema

```sql
CREATE TABLE notes (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    content    TEXT    NOT NULL,
    archived   INTEGER DEFAULT 0,
    created_at TEXT    DEFAULT CURRENT_TIMESTAMP
);
```

### Trigger Scenarios

| User Says | Action |
|-----------|--------|
| "笔记..." / "记一下..." | Create a new note |
| "找一下..." / "搜一下..." | Search notes |
| "列出笔记" / "有哪些笔记" | List all notes |
| "标记已整理" / "归档" | Archive note |
| "备份笔记" | Manual backup |

### Tech Stack

- SQLite (no external dependencies)
- Shell scripting for automation
- OpenClaw skill framework

---

## 中文

基于 SQLite 的笔记管理技能，为 **OpenClaw** 数字生命管家（霜糖）打造。

### 功能

- **创建笔记** — 快速记笔记，自动添加时间戳
- **搜索笔记** — 全文搜索所有笔记
- **列出笔记** — 查看所有笔记及归档状态
- **归档笔记** — 将笔记标记为已整理
- **备份** — 每日自动备份，保留 3 份

### 数据库

- 位置：`~/.openclaw/workspace/notes/notes.db`
- 备份：`~/.openclaw/workspace/notes/backups/`
- 自动备份：每日凌晨 2 点（保留 3 份）

### 表结构

```sql
CREATE TABLE notes (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    content    TEXT    NOT NULL,
    archived   INTEGER DEFAULT 0,
    created_at TEXT    DEFAULT CURRENT_TIMESTAMP
);
```

### 触发场景

| 用户说 | 动作 |
|--------|------|
| "笔记..." / "记一下..." | 创建笔记 |
| "找一下..." / "搜一下..." | 搜索笔记 |
| "列出笔记" / "有哪些笔记" | 列出所有笔记 |
| "标记已整理" / "归档" | 归档笔记 |
| "备份笔记" | 手动备份 |

### 技术栈

- SQLite（无外部依赖）
- Shell 脚本实现自动化
- OpenClaw skill 框架
