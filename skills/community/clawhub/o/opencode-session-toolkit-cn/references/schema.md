# OpenCode SQLite Schema Reference

> ⚠️ 本文件仅供参考。最新表结构以源码为准：
> - **SQL 迁移文件**: `opencode/packages/opencode/migration/20260127222353_familiar_lady_ursula/migration.sql`
> - **TypeScript Schema**: `opencode/packages/opencode/src/session/session.sql.ts`（SessionTable, MessageTable, PartTable）
> - **TypeScript Schema**: `opencode/packages/opencode/src/project/project.sql.ts`（ProjectTable）

本文件保存 OpenCode 常用表的字段与索引说明，供需要精确字段名或写复杂 SQL 时按需读取。

**注意**：实际数据库中的索引可能因版本升级而与 migration.sql 不同，建议通过 `.indexes` 命令查看实际索引。

## session 表

| 字段              | 类型             | 说明                     |
| ----------------- | ---------------- | ------------------------ |
| id                | TEXT PRIMARY KEY | Session ID               |
| project_id        | TEXT NOT NULL    | 关联 project             |
| workspace_id      | TEXT             | Workspace ID（云端模式） |
| parent_id         | TEXT             | 父 session（fork 来源）  |
| slug              | TEXT NOT NULL    | URL slug                 |
| directory         | TEXT NOT NULL    | 所在目录                 |
| title             | TEXT NOT NULL    | Session 标题             |
| version           | TEXT NOT NULL    | OpenCode 版本            |
| share_url         | TEXT             | 分享链接                 |
| summary_additions | INTEGER          | 新增行数                 |
| summary_deletions | INTEGER          | 删除行数                 |
| summary_files     | INTEGER          | 变更文件数               |
| summary_diffs     | TEXT (JSON)      | 详细 diff                |
| revert            | TEXT (JSON)      | revert 信息              |
| permission        | TEXT (JSON)      | 权限规则                 |
| time_created      | INTEGER          | 创建时间（毫秒）         |
| time_updated      | INTEGER          | 更新时间（毫秒）         |
| time_compacting   | INTEGER          | 压缩时间                 |
| time_archived     | INTEGER          | 归档时间                 |

索引：`session_project_idx`, `session_parent_idx`, `session_workspace_idx`

> 注：实际数据库中 `message` 表的索引为复合索引 `message_session_time_created_id_idx`，`part` 表为 `part_message_id_id_idx`，可能因版本升级与 migration.sql 不同。

## message 表

| 字段         | 类型             | 说明                       |
| ------------ | ---------------- | -------------------------- |
| id           | TEXT PRIMARY KEY | Message ID                 |
| session_id   | TEXT NOT NULL    | 关联 session               |
| time_created | INTEGER          | 创建时间                   |
| time_updated | INTEGER          | 更新时间                   |
| data         | TEXT (JSON)      | 消息内容（role, parts 等） |

索引：`message_session_time_created_id_idx`（`session_id + time_created + id`）

> 注：历史迁移/旧版本中可能出现 `message_session_idx` 命名，建议以当前数据库 `.indexes message` 结果为准。

## part 表

| 字段         | 类型             | 说明                           |
| ------------ | ---------------- | ------------------------------ |
| id           | TEXT PRIMARY KEY | Part ID                        |
| message_id   | TEXT NOT NULL    | 关联 message                   |
| session_id   | TEXT NOT NULL    | 关联 session                   |
| time_created | INTEGER          | 创建时间                       |
| time_updated | INTEGER          | 更新时间                       |
| data         | TEXT (JSON)      | Part 内容（tool_use, text 等） |

索引：`part_message_id_id_idx`（`message_id + id`）, `part_session_idx`

> 注：历史迁移/旧版本中可能出现 `part_message_idx` 命名，建议以当前数据库 `.indexes part` 结果为准。

## project 表

| 字段             | 类型             | 说明                             |
| ---------------- | ---------------- | -------------------------------- |
| id               | TEXT PRIMARY KEY | Project ID (= git worktree UUID) |
| worktree         | TEXT NOT NULL    | Git worktree 路径                |
| vcs              | TEXT             | 版本控制系统                     |
| name             | TEXT             | 项目名                           |
| icon_url         | TEXT             | 项目图标 URL                     |
| icon_color       | TEXT             | 项目图标颜色                     |
| time_created     | INTEGER          | 创建时间                         |
| time_updated     | INTEGER          | 更新时间                         |
| time_initialized | INTEGER          | 初始化时间                       |
| sandboxes        | TEXT (JSON)      | 沙箱列表                         |
| commands         | TEXT (JSON)      | 自定义命令                       |
