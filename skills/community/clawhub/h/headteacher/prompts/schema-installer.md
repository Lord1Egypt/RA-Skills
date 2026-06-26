# Schema Installer

Use this prompt whenever you need to explain or apply the standard headteacher schema.

## Source of truth

The schema source of truth is:

- [references/schema-manifest.md](../references/schema-manifest.md)
- `python3 tools/schema_planner.py --backend <backend> --format <format>`

## Rules

- always start from the unified semantic model
- do not invent backend-specific tables or fields without checking the schema manifest
- if the backend is not fully implemented, emit a mapping plan and limitations instead of pretending to install it

## Typical commands

Feishu summary:

```bash
python3 tools/schema_planner.py --backend feishu_base --format markdown
```

Notion summary:

```bash
python3 tools/schema_planner.py --backend notion --format markdown
```

Obsidian summary:

```bash
python3 tools/schema_planner.py --backend obsidian --format markdown
```
