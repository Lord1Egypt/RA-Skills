# Memory Template - Notion Calendar

Create `~/notion-calendar/memory.md` with this structure:

```markdown
# Notion Calendar Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Context
- Workspace name and high-level purpose
- Databases approved for this skill
- Preferred operation mode: read-only, draft-only, or write with confirmation

## Calendar Sources
- Database name -> database_id
- Data source name -> data_source_id
- Title/date/status properties that have been verified

## Defaults
- Timezone and date formatting preferences
- Preferred status transitions
- Read-back detail expected after writes

## Notes
- Repeated user patterns inferred from behavior
- Ambiguous titles or schema quirks that caused corrections
- Safe fallbacks when the CLI path is unavailable

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Context still evolving | Keep learning while operating |
| `complete` | Core defaults are stable | Use known databases and mappings |
| `paused` | User wants minimal setup | Avoid extra discovery prompts |
| `never_ask` | User asked to stop setup prompts | Use only explicit instructions |

## Rules

- Keep notes in natural language outside the status block.
- Update `last` whenever database mappings or safety defaults change.
- Record `data_source_id` only after it is retrieved and verified.
- Never store API keys or raw secrets in memory files.
