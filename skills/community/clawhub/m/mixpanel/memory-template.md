# Memory Template — Mixpanel

Create `~/mixpanel/memory.md` with this structure:

```markdown
# Mixpanel Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Project
<!-- Product context learned from conversations -->

## Key Events
<!-- Events the user tracks and cares about -->

## Saved Queries
<!-- Queries they run frequently -->

## Insights
<!-- Notable findings from analysis -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning their setup | Gather context from queries |
| `complete` | Know their product well | Focus on analysis |
| `paused` | User said "not now" | Work with what you have |

## Key Principles

- Learn events from actual queries, not by asking for lists
- Save interesting insights for future reference
- Track which queries are useful to suggest similar ones
- Never store credentials in memory — use env vars only
