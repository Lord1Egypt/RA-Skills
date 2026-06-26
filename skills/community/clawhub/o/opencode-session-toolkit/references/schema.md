# OpenCode SQLite Schema Reference

Warning: This file is reference material only. Treat source code as the canonical definition:
- SQL migration file: `opencode/packages/opencode/migration/20260127222353_familiar_lady_ursula/migration.sql`
- TypeScript schema: `opencode/packages/opencode/src/session/session.sql.ts` (`SessionTable`, `MessageTable`, `PartTable`)
- TypeScript schema: `opencode/packages/opencode/src/project/project.sql.ts` (`ProjectTable`)

This document captures commonly used OpenCode tables, fields, and indexes for precise field lookups and advanced SQL queries.

Note: Actual indexes in your live database may differ from `migration.sql` after upgrades. Use `.indexes` to verify what exists.

## `session` table

| Field             | Type             | Description                     |
| ----------------- | ---------------- | ------------------------------- |
| id                | TEXT PRIMARY KEY | Session ID                      |
| project_id        | TEXT NOT NULL    | Linked project                  |
| workspace_id      | TEXT             | Workspace ID (cloud mode)       |
| parent_id         | TEXT             | Parent session (fork source)    |
| slug              | TEXT NOT NULL    | URL slug                        |
| directory         | TEXT NOT NULL    | Working directory               |
| title             | TEXT NOT NULL    | Session title                   |
| version           | TEXT NOT NULL    | OpenCode version                |
| share_url         | TEXT             | Share URL                       |
| summary_additions | INTEGER          | Added lines                     |
| summary_deletions | INTEGER          | Deleted lines                   |
| summary_files     | INTEGER          | Changed file count              |
| summary_diffs     | TEXT (JSON)      | Detailed diffs                  |
| revert            | TEXT (JSON)      | Revert metadata                 |
| permission        | TEXT (JSON)      | Permission rules                |
| time_created      | INTEGER          | Created time (milliseconds)     |
| time_updated      | INTEGER          | Updated time (milliseconds)     |
| time_compacting   | INTEGER          | Compaction time                 |
| time_archived     | INTEGER          | Archived time                   |

Indexes: `session_project_idx`, `session_parent_idx`, `session_workspace_idx`

Note: In many current DBs, `message` uses composite index `message_session_time_created_id_idx`, and `part` uses `part_message_id_id_idx`. Names can differ by version.

## `message` table

| Field        | Type             | Description                            |
| ------------ | ---------------- | -------------------------------------- |
| id           | TEXT PRIMARY KEY | Message ID                             |
| session_id   | TEXT NOT NULL    | Linked session                         |
| time_created | INTEGER          | Created time                           |
| time_updated | INTEGER          | Updated time                           |
| data         | TEXT (JSON)      | Message payload (`role`, `parts`, etc) |

Indexes: `message_session_time_created_id_idx` (`session_id + time_created + id`)

Note: Older migrations may show names like `message_session_idx`; trust `.indexes message` from the live DB.

## `part` table

| Field        | Type             | Description                                |
| ------------ | ---------------- | ------------------------------------------ |
| id           | TEXT PRIMARY KEY | Part ID                                    |
| message_id   | TEXT NOT NULL    | Linked message                             |
| session_id   | TEXT NOT NULL    | Linked session                             |
| time_created | INTEGER          | Created time                               |
| time_updated | INTEGER          | Updated time                               |
| data         | TEXT (JSON)      | Part payload (`tool_use`, `text`, etc)     |

Indexes: `part_message_id_id_idx` (`message_id + id`), `part_session_idx`

Note: Older migrations may use names like `part_message_idx`; trust `.indexes part` from the live DB.

## `project` table

| Field            | Type             | Description                               |
| ---------------- | ---------------- | ----------------------------------------- |
| id               | TEXT PRIMARY KEY | Project ID (= git worktree UUID)          |
| worktree         | TEXT NOT NULL    | Git worktree path                         |
| vcs              | TEXT             | Version control system                    |
| name             | TEXT             | Project name                              |
| icon_url         | TEXT             | Project icon URL                          |
| icon_color       | TEXT             | Project icon color                        |
| time_created     | INTEGER          | Created time                              |
| time_updated     | INTEGER          | Updated time                              |
| time_initialized | INTEGER          | Initialized time                          |
| sandboxes        | TEXT (JSON)      | Sandbox list                              |
| commands         | TEXT (JSON)      | Custom commands                           |
