# CLI 指南

在 skill 目录中运行命令。需要覆盖自动解析的 `opencode db path` 时，把 `--db-path` 放在子命令之后。

## 按意图选择

| 需求 | 命令 |
| --- | --- |
| 验证数据库是否可用 | `doctor` |
| 按元数据查找会话 | `list` |
| 读取单个会话 | `show SESSION_ID` |
| 查找字面文本 | `search TEXT` |
| 写出归档 | `export` |
| 诊断字段或索引 | `schema` |

以 `<command> --help` 为选项权威来源。

## 先诊断

```bash
./scripts/opencode_sessions.py doctor
./scripts/opencode_sessions.py schema --table session --format json
```

`doctor` 只读取 schema 元数据，不读取转录内容。

## 发现会话

```bash
./scripts/opencode_sessions.py list
./scripts/opencode_sessions.py list --project toolkit --start 2026-08-01
./scripts/opencode_sessions.py list --directory /path/to/worktree --format json
./scripts/opencode_sessions.py list --archived only
```

同类过滤器的重复值按 OR 组合，不同类别按 AND 组合。文本过滤是忽略大小写的字面子串；`%` 和 `_` 不是 SQL 通配符。

`list` 默认排除已归档会话，按更新时间和 session ID 排序，最多返回 20 条。

## 读取或搜索

```bash
./scripts/opencode_sessions.py show ses_example
./scripts/opencode_sessions.py show ses_example --format json
./scripts/opencode_sessions.py search 'exact % text' --scope all
./scripts/opencode_sessions.py search 'tool name' --scope messages --format json
```

`show` 默认只输出文本和精简工具摘要，省略 reasoning、完整工具输入输出、原始 message JSON 及其他非展示 part。

仅当用户明确要求完整 payload 时使用：

```bash
./scripts/opencode_sessions.py show ses_example --include-sensitive
```

搜索只报告命中的会话，不自动打印消息上下文。先确定目标 session，再用 `show` 读取。

## 导出

使用与 `list` 相同的过滤器选择会话：

```bash
./scripts/opencode_sessions.py export \
  --project opencode-session-toolkit \
  --output-dir ./exports/toolkit

./scripts/opencode_sessions.py export \
  --start 2026-08-01 \
  --end 2026-08-09 \
  --group-by-project \
  --output-dir ./exports/week
```

无过滤全量导出必须显式传入 `--all`。仅日期的 `--end` 包含本地当天全部时间。

不创建文件，仅预览匹配路径和冲突状态：

```bash
./scripts/opencode_sessions.py export \
  --project opencode-session-toolkit \
  --output-dir ./exports/toolkit \
  --dry-run
```

Markdown 为每个 session 生成一个文件，文件名包含清洗后的标题、UTC 创建时间和 session ID。JSONL 生成 `sessions.jsonl`。

写文件前会完整预检：

- 内容相同的已有文件记为 unchanged。
- 发现内容不同的已有文件时，在写任何新文件前停止整个导出。
- `--overwrite` 显式允许通过同目录原子替换覆盖文件。

`--include-sensitive` 使用与 `show` 相同的显式授权边界，并向 stderr 输出警告。

## 输出规则

- 展示时间统一为 UTC ISO-8601。
- 无时区 datetime 和仅日期边界按机器本地时区解释。
- 表格用于人工阅读；JSON 用于后续工具消费。
- 错误退出码为 2，并在 stderr 输出简洁的 `error:` 信息。
