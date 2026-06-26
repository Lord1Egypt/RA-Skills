---
name: opencode-session-toolkit
description: 读取本地 OpenCode SQLite 数据库，支持跨目录会话查询、消息检查与 Markdown 导出。
---

# OpenCode Session Toolkit

读取本地 OpenCode SQLite 数据库，支持跨目录检索 session、message、part、project。

以下命令默认都在当前 `SKILL.md` 所在目录执行。导出 Markdown 时，直接运行内置脚本：

```bash
./scripts/export_opencode_sessions.py --help
```

## 适用场景

- 列出最近会话、按目录过滤、按标题搜索
- 读取某个 session 的 message JSON
- 将匹配的会话导出为一个会话一个 Markdown 文件
- 查看 OpenCode 数据库结构和索引（按需读取 `references/schema.md`）

## 工作流程

1. 通过 `opencode db path` 解析数据库路径。
2. 所有查询只读执行，避免误写。
3. 需要字段细节时再读取 `references/schema.md`。

## 1. 解析数据库路径

```bash
if ! command -v opencode >/dev/null 2>&1; then
  echo "opencode command not found in PATH" >&2
  exit 1
fi

if ! DB_PATH="$(opencode db path 2>/dev/null)"; then
  echo "Failed to resolve OpenCode DB path via: opencode db path" >&2
  exit 1
fi

if [ -z "${DB_PATH:-}" ] || [ ! -f "$DB_PATH" ]; then
  echo "OpenCode DB not found: $DB_PATH" >&2
  exit 1
fi

echo "Using DB: $DB_PATH"
```

列出当前存在的 DB 文件（无匹配也不会报错）：

```bash
find "${XDG_DATA_HOME:-$HOME/.local/share}/opencode" -maxdepth 1 -name '*.db' -print 2>/dev/null
```

## 2. 时间转换与格式化

**时间转换**：所有时间字段为毫秒级 Unix timestamp，可用 `datetime()` 直接在 SQL 中转换。

```bash
# 在 SQL 中转换（推荐，无需外部命令）
datetime(time_updated/1000, 'unixepoch', 'localtime')

# 用 shell 辅助变量计算时间范围
NOW_MS=$(date +%s000)
LAST_7D=$((NOW_MS - 7*86400*1000))   # 最近 7 天
LAST_30D=$((NOW_MS - 30*86400*1000))  # 最近 30 天
```

**表格对齐**：普通字段查询可通过 `column -t -s '|'` 对齐（SQLite 默认列分隔符为 `|`）；包含 `message.data` 这类长 JSON 字段时建议使用 `-json` 输出。

```bash
sqlite3 -readonly "$DB_PATH" "SELECT id, title, time_updated FROM session LIMIT 5;" | column -t -s '|'
```

## 3. 常用只读查询

> 💡 不含长 JSON 字段的查询可追加 `| column -t -s '|'` 以对齐输出表格。

**列出最近 20 个 session（按更新时间倒序）**

```bash
sqlite3 -readonly "$DB_PATH" \
  "SELECT id, title, directory,
          datetime(time_updated/1000,'unixepoch','localtime') as updated
   FROM session
   ORDER BY time_updated DESC
   LIMIT 20;" | column -t -s '|'
```

**按目录过滤 session**

```bash
sqlite3 -readonly "$DB_PATH" \
  "SELECT id, title, datetime(time_updated/1000,'unixepoch','localtime') as updated
   FROM session
   WHERE directory LIKE '/path/to/project%'
   ORDER BY time_updated DESC
   LIMIT 20;" | column -t -s '|'
```

**按 project_id 过滤 session（最精确的目录关联方式）**

```bash
sqlite3 -readonly "$DB_PATH" \
  "SELECT s.id, s.title, s.directory,
          datetime(s.time_updated/1000,'unixepoch','localtime') as updated
   FROM session s
   WHERE s.project_id = 'your-project-id'
   ORDER BY s.time_updated DESC
   LIMIT 20;" | column -t -s '|'
```

> project_id 对应 `project` 表的 `id` 字段，可通过 `SELECT id, worktree, name FROM project;` 查看项目列表。

**跨所有目录全量列出 session（带 project 信息）**

```bash
sqlite3 -readonly "$DB_PATH" \
  "SELECT s.id, s.title, s.directory, p.worktree,
          datetime(s.time_updated/1000,'unixepoch','localtime') as updated
   FROM session s
   LEFT JOIN project p ON s.project_id = p.id
   ORDER BY s.time_updated DESC
   LIMIT 50;" | column -t -s '|'
```

**按时间范围过滤**

```bash
# 最近 7 天活跃的 session
sqlite3 -readonly "$DB_PATH" \
  "SELECT id, title, datetime(time_updated/1000,'unixepoch','localtime') as updated
   FROM session
   WHERE time_updated > $(( $(date +%s000) - 7*86400*1000 ))
   ORDER BY time_updated DESC
   LIMIT 20;" | column -t -s '|'

# 今天创建的 session
sqlite3 -readonly "$DB_PATH" \
  "SELECT id, title, datetime(time_created/1000,'unixepoch','localtime') as created
   FROM session
   WHERE date(time_created/1000,'unixepoch','localtime') = date('now','localtime')
   ORDER BY time_created DESC
   LIMIT 20;" | column -t -s '|'
```

**查看某 session 的消息内容**

```bash
sqlite3 -readonly -json "$DB_PATH" \
  "SELECT m.id, datetime(m.time_created/1000,'unixepoch','localtime') as created, m.data
   FROM message m
   WHERE m.session_id = 'your-session-id'
   ORDER BY m.time_created ASC;"
```

**解析 message.data JSON 字段**

```bash
# 提取 role、modelID 等关键字段（json_extract）
sqlite3 -readonly "$DB_PATH" \
  "SELECT id,
          json_extract(data, '$.role') as role,
          json_extract(data, '$.modelID') as model,
          datetime(time_created/1000,'unixepoch','localtime') as created
   FROM message
   WHERE session_id = 'your-session-id'
   ORDER BY time_created ASC;" | column -t -s '|'

# 搜索 message 内容（full-text like）
sqlite3 -readonly "$DB_PATH" \
  "SELECT id, json_extract(data, '$.role') as role, time_created
   FROM message
   WHERE data LIKE '%keyword%'
   ORDER BY time_created DESC
   LIMIT 20;" | column -t -s '|'
```

**搜索 session 标题**

```bash
sqlite3 -readonly "$DB_PATH" \
  "SELECT id, title, directory, datetime(time_updated/1000,'unixepoch','localtime') as updated
   FROM session
   WHERE title LIKE '%keyword%'
   ORDER BY time_updated DESC
   LIMIT 20;" | column -t -s '|'
```

**查看会话统计**

```bash
sqlite3 -readonly "$DB_PATH" \
  "SELECT title, summary_additions, summary_deletions, summary_files,
          datetime(time_created/1000,'unixepoch','localtime') as created
   FROM session
   ORDER BY time_updated DESC
   LIMIT 20;" | column -t -s '|'
```

## 4. 导出会话为 Markdown

导出脚本会将每个会话写成一个独立的 Markdown 文件。默认行为：

- 文件名 = `会话标题 + 创建时间`
- 时间过滤默认使用 `time_updated`，除非显式传入 `--time-field created`
- 默认跳过 `step-start` / `step-finish`，减少噪声
- 当 `project.name` 为空时，导出分组目录会回退到 `worktree` 的目录名，再不行就用 `global`

**按某个 project 导出**

```bash
./scripts/export_opencode_sessions.py \
  --project opencode-session-toolkit \
  --output-dir ./exports/opencode-session-toolkit
```

`--project` 会对 `project_id`、`project.name`、`project.worktree`、`session.directory` 做子串匹配。

**按时间段导出**

```bash
./scripts/export_opencode_sessions.py \
  --start 2026-03-01 \
  --end 2026-03-24T23:59:59 \
  --time-field updated \
  --output-dir ./exports/march
```

支持的时间格式：

- ISO 日期：`2026-03-24`
- ISO 日期时间：`2026-03-24T22:35:37`
- Unix 秒级 / 毫秒级时间戳

**全量导出并按 project 分组**

```bash
./scripts/export_opencode_sessions.py \
  --all \
  --group-by-project \
  --output-dir ./exports/all
```

输出结构示例：

```text
exports/all/
  OrchAI/
    Migration work planning with subagent discussion_2026-03-23_23-48-07.md
  global/
    opencode-session-toolkit 命令验证与优化_2026-03-24_22-35-37.md
```

**其他常用过滤条件**

- `--session-id ses_xxx`：按精确 session id 导出
- `--title-contains keyword`：按会话标题匹配
- `--directory-contains keyword`：按工作目录匹配
- `--archived include|exclude|only`：过滤归档状态
- `--filename-time-field created|updated`：控制文件名里拼接哪一个会话时间
- `--include-part-type text --include-part-type tool`：只导出指定 part 类型
- `--exclude-part-type reasoning`：排除噪声 part 类型
- `--overwrite`：目标文件已存在时直接覆盖，而不是自动追加 session id 避免重名

如果不传任何过滤条件，脚本会要求显式加 `--all`，避免误触发全量导出。

## 5. 查看 schema

```bash
sqlite3 -readonly "$DB_PATH" ".schema session"
sqlite3 -readonly "$DB_PATH" ".schema message"
sqlite3 -readonly "$DB_PATH" ".schema part"
sqlite3 -readonly "$DB_PATH" ".schema project"
```

完整字段与索引说明见 `references/schema.md`。

## 6. 查看所有表

```bash
sqlite3 -readonly "$DB_PATH" ".tables"
```

## 7. 示例输出

```
id          title                     directory                   updated
----------  -----------------------  --------------------------  -------------------
ses_abc123  My Session - 2026-03-24  /home/user/project         2026-03-24 10:00:00
ses_def456  Another Session          /home/user/other           2026-03-23 15:30:00
```

（配合 `| column -t -s '|'` 对齐后的效果）

## 8. 注意事项

- 数据库使用 WAL 模式，会产生 `.db-wal` 和 `.db-shm` 文件
- 所有时间字段为**毫秒级 Unix timestamp**，用 `datetime(ts/1000,'unixepoch','localtime')` 在 SQL 中直接转换
- `data` 字段为 JSON：做结构化抽取时用 `json_extract(data, '$.field')`，查看原始消息时优先 `sqlite3 -json`
- Session 隔离按 `project_id`，跨目录检索时建议关联 `project.worktree`
- 直接修改数据库可能导致数据损坏，操作前建议备份
- `account` / `control_account` 表含敏感凭证，查询时注意脱敏
