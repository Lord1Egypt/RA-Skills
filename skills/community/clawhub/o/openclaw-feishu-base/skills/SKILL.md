---
name: openclaw-feishu-base
description: Use when the user needs Feishu Base / Lark Bitable operations via the feishu_base tool, including table lookup, schema inspection, field creation, and record writes.
---

# OpenClaw Feishu Base Plugin Skill

Prefer the runtime tool:

- `feishu_base`

Key supported actions include:

- `resolve_link`
- `discover_tables`
- `find_table`
- `list_tables`
- `create_table`
- `create_field`
- `rename_field`
- `update_field`
- `get_table`
- `query_records`
- `create_records`
- `update_records`
- `upsert_records`

When `feishu_base` is exposed, use it before falling back to lower-level bundled Feishu bitable tools.
