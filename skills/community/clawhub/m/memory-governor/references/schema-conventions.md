# Schema Conventions

## Goal

让关键 target class 不只“人能看懂”，也能被轻量工具稳定读取和校验。

这是弱约束，不是重数据库模式。

## Format

推荐在 markdown 文件顶部使用 TOML frontmatter：

```toml
+++
target_class = "proactive_state"
schema_version = "0.1"
updated_at = "2026-03-31T00:00:00Z"
+++
```

原因：

- markdown 仍然可读
- TOML frontmatter 可被标准库稳定解析
- 不要求宿主切到 JSON-only 或数据库存储

## Common Required Keys

所有结构化 target 文件都推荐至少有：

- `target_class`
- `schema_version`
- `updated_at`

## Target-Specific Keys

### `proactive_state`

推荐键：

- `target_class = "proactive_state"`
- `schema_version`
- `updated_at`
- `state_mode = "combined"` or `"split-slice"`
- `current_objective`
- `current_blocker`
- `next_move`

如果是 split adapter：

- current-task slice 仍然应携带这些 canonical current-state keys
- durable boundary slice 可以补充宿主自己的结构，但不应替代 current-task truth

### `working_buffer`

推荐键：

- `target_class = "working_buffer"`
- `schema_version`
- `updated_at`
- `task_ref`
- `buffer_status = "active" | "stale" | "cleared"`

### `reusable_lessons`

推荐键：

- `target_class = "reusable_lessons"`
- `schema_version`
- `updated_at`
- `scope = "global" | "domain" | "project"`

## Required Sections

为了让正文也保持可扫描，推荐这些 heading：

### `proactive_state`

- `## Current Task State`
- `## Durable Boundaries`

### `working_buffer`

- `## Breadcrumbs`

### `reusable_lessons`

- `## Lessons`

## Validation Philosophy

不要把 validator 做成重型编排器。

它只应该检查：

- frontmatter 是否存在
- 必填键是否存在
- enum 值是否合法
- 关键 heading 是否存在

它不应试图替代人类判断“这条经验值不值得记”。
