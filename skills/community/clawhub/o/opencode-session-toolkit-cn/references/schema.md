# 实时 schema 兼容

以实际数据库为权威来源。OpenCode 会持续新增表和字段，因此 CLI 在运行时探测能力，不假定某个 migration 快照永久有效。

## 核心要求

| 命令 | 必需结构 |
| --- | --- |
| `list` 和标题搜索 | `session`：`id`、`project_id`、`directory`、`title`、`time_created`、`time_updated` |
| 消息搜索 | 上述 `session` 字段，以及 `message`：`id`、`session_id`、`time_created`、`data` |
| `show` 和 `export` | 上述结构，以及 `part`：`id`、`message_id`、`session_id`、`time_created`、`data` |

`project` 表以及 `session.version`、摘要统计、归档时间等字段属于可选增强。缺失时不得影响无需这些字段的命令。

## 检查实际数据库

首先运行：

```bash
./scripts/opencode_sessions.py doctor --format json
./scripts/opencode_sessions.py schema --format json
```

调查单个表时限制输出：

```bash
./scripts/opencode_sessions.py schema --table session --table message
```

CLI 只报告四个核心表。高级回退场景可以只检查指定核心表，不读取数据：

```bash
DB_PATH="$(opencode db path)"
sqlite3 -readonly "$DB_PATH" ".schema session"
sqlite3 -readonly "$DB_PATH" ".indexes session"
```

## 数据约定

- 时间字段是 Unix 毫秒；CLI 输出统一使用 UTC ISO-8601。
- 仅日期的 `--start` 从本地当天零点开始。
- 仅日期的 `--end` 包含本地当天的全部时间。
- `message.data` 和 `part.data` 是 JSON 文本；payload 结构会随 OpenCode 版本和 part 类型变化。
- `project` 可用时，通过 `session.project_id = project.id` 关联。
- message 按 `(time_created, id)` 排序；每个 message 内的 part 按 `(time_created, id)` 排序。不要依赖可能在相同时间戳下交错消息的 join 顺序。

缺少必需字段时，停止并报告 `doctor` 输出。不得猜测旧版或未来 schema，也不得修改数据库来适配工具。
