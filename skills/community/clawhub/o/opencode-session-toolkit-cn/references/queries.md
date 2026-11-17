# 高级只读查询

仅当内置 CLI 无法回答问题时读取本文件。先检查 `references/schema.md` 和实际数据库 schema。

## 防护规则

```bash
DB_PATH="$(opencode db path)"
test -f "$DB_PATH"
sqlite3 -readonly "$DB_PATH" "PRAGMA query_only = ON; SELECT sqlite_version();"
```

- 保留 `-readonly` 并设置 `PRAGMA query_only = ON`。
- 除非用户明确指定其他非凭证表，否则只查询 `session`、`message`、`part`、`project`。
- 禁止查询 `account`、`control_account`、`credential`。
- 用户提供的文本优先交给 CLI 过滤；必须写原始 SQL 时绑定参数，不直接插值。
- 探索性查询必须先设置明确 `LIMIT`。
- JSON 或长文本使用 `-json`；短表格使用 `-header -column`。

## Session 父子关系

列出直接子 session：

```bash
sqlite3 -readonly -header -column "$DB_PATH" \
  "PRAGMA query_only = ON;
   SELECT id, title, parent_id,
          datetime(time_updated / 1000, 'unixepoch') AS updated_utc
   FROM session
   WHERE parent_id = 'ses_parent_id'
   ORDER BY time_updated DESC, id ASC
   LIMIT 50;"
```

可信 ID 中的单引号必须替换为 `''`。普通 ID 查询优先使用 `list --session-id`。

## Part 类型分布

为专用导出设计格式前，先查看实际 part 类型：

```bash
sqlite3 -readonly -header -column "$DB_PATH" \
  "PRAGMA query_only = ON;
   SELECT json_extract(data, '$.type') AS part_type, COUNT(*) AS count
   FROM part
   GROUP BY part_type
   ORDER BY count DESC
   LIMIT 100;"
```

## 工具使用摘要

```bash
sqlite3 -readonly -header -column "$DB_PATH" \
  "PRAGMA query_only = ON;
   SELECT json_extract(data, '$.tool') AS tool, COUNT(*) AS uses
   FROM part
   WHERE json_extract(data, '$.type') = 'tool'
   GROUP BY tool
   ORDER BY uses DESC
   LIMIT 100;"
```

这里只报告工具名。除非用户明确要求敏感内容，否则不要查询完整工具 payload。

## 项目活跃度摘要

```bash
sqlite3 -readonly -header -column "$DB_PATH" \
  "PRAGMA query_only = ON;
   SELECT s.project_id,
          COALESCE(p.name, p.worktree, s.project_id) AS project,
          COUNT(*) AS sessions,
          datetime(MAX(s.time_updated) / 1000, 'unixepoch') AS latest_utc
   FROM session AS s
   LEFT JOIN project AS p ON p.id = s.project_id
   GROUP BY s.project_id, project
   ORDER BY MAX(s.time_updated) DESC
   LIMIT 100;"
```

## 完整性诊断

查找父记录缺失的 message 或 part：

```bash
sqlite3 -readonly -header -column "$DB_PATH" \
  "PRAGMA query_only = ON;
   SELECT 'message_without_session' AS issue, COUNT(*) AS count
   FROM message AS m LEFT JOIN session AS s ON s.id = m.session_id
   WHERE s.id IS NULL
   UNION ALL
   SELECT 'part_without_message', COUNT(*)
   FROM part AS p LEFT JOIN message AS m ON m.id = p.message_id
   WHERE m.id IS NULL;"
```

只报告发现，不修复 OpenCode 数据库。

## 查询计划诊断

```bash
sqlite3 -readonly "$DB_PATH" \
  "PRAGMA query_only = ON;
   EXPLAIN QUERY PLAN
   SELECT id FROM message
   WHERE session_id = 'ses_example'
   ORDER BY time_created, id;"
```

将结果与 `./scripts/opencode_sessions.py schema --table message` 比较。不得在实时数据库中新建索引。
