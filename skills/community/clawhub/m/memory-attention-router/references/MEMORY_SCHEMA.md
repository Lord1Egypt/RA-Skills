# Memory Schema

## Main table: `memories`

| Column                  | Type    | Meaning                                                       |
| ----------------------- | ------- | ------------------------------------------------------------- |
| `id`                    | TEXT PK | Stable memory ID                                              |
| `memory_type`           | TEXT    | `episode`, `summary`, `reflection`, `procedure`, `preference` |
| `abstraction_level`     | INTEGER | 0 raw, 1 session, 2 task, 3 long-term                         |
| `role_scope`            | TEXT    | `planner`, `executor`, `critic`, `responder`, `global`        |
| `session_id`            | TEXT    | Session scope                                                 |
| `task_id`               | TEXT    | Task scope                                                    |
| `title`                 | TEXT    | Short title                                                   |
| `summary`               | TEXT    | Main reusable text                                            |
| `details_json`          | TEXT    | Structured details                                            |
| `keywords_json`         | TEXT    | Search keywords                                               |
| `tags_json`             | TEXT    | Tags                                                          |
| `source_refs_json`      | TEXT    | References to turns, tools, or external evidence              |
| `importance`            | REAL    | 0.0 to 1.0                                                    |
| `confidence`            | REAL    | 0.0 to 1.0                                                    |
| `success_score`         | REAL    | 0.0 to 1.0                                                    |
| `recency_ts`            | TEXT    | When the memory became relevant                               |
| `valid_from_ts`         | TEXT    | Optional validity start                                       |
| `valid_to_ts`           | TEXT    | Optional validity end                                         |
| `is_active`             | INTEGER | 1 active, 0 inactive                                          |
| `replaced_by_memory_id` | TEXT    | Forward pointer to the active replacement                     |
| `retired_reason`        | TEXT    | Why the memory was retired                                    |
| `created_at`            | TEXT    | Created timestamp                                             |
| `updated_at`            | TEXT    | Updated timestamp                                             |

## Edge table: `memory_edges`

| Column           | Type    | Meaning                                                         |
| ---------------- | ------- | --------------------------------------------------------------- |
| `id`             | TEXT PK | Edge ID                                                         |
| `from_memory_id` | TEXT    | Source                                                          |
| `to_memory_id`   | TEXT    | Target                                                          |
| `edge_type`      | TEXT    | `similar`, `supports`, `contradicts`, `extends`, `derived_from` |
| `weight`         | REAL    | 0.0 to 1.0                                                      |
| `created_at`     | TEXT    | Created timestamp                                               |

## Working packet table: `working_memory_packets`

Stores the final routed packet for inspection and debugging.

## JSON conventions

### `details_json`

Free-form object. Suggested keys:

- `tool_name`
- `tool_input`
- `tool_output`
- `error`
- `notes`
- `result`
- `next_action`
- `user_preference_type`

### `source_refs_json`

Suggested values:

- turn IDs
- message IDs
- external URLs
- tool run IDs
- task run IDs

## Example add payload

```json
{
  "memory_type": "procedure",
  "abstraction_level": 2,
  "role_scope": "planner",
  "session_id": "sess_001",
  "task_id": "task_skill_build",
  "title": "Build the OpenClaw skill in the workspace first",
  "summary": "Start with a workspace-level skill folder so testing overrides bundled or shared copies.",
  "details": {
    "why": "Workspace precedence makes iteration easier."
  },
  "keywords": ["openclaw", "skill", "workspace"],
  "tags": ["procedure", "openclaw"],
  "source_refs": ["manual-note"],
  "importance": 0.86,
  "confidence": 0.9,
  "success_score": 0.85
}
```

## Example add payload with replacement

```json
{
  "memory_type": "procedure",
  "title": "Validated OpenClaw workflow",
  "summary": "Use a workspace-level skill folder before iterating on prompts so testing targets the active copy.",
  "replaces_memory_id": "mem_old_001"
}
```

## Example refresh payload

```json
{
  "stale_memory_ids": ["mem_old_001"],
  "replacement_memory_id": "mem_new_002",
  "refresh_reason": "New tool behavior changed after upgrade."
}
```
