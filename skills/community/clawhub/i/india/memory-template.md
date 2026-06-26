# Memory Template — India

Create `~/india/memory.md` with this structure:

```markdown
# India Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
<!-- First trip or repeat trip -->
<!-- Dates, route, group type, comfort level, budget notes -->
<!-- Food preferences, hygiene sensitivity, and must-do goals -->

## Recommendations Given
<!-- Cities, hotels, neighborhoods, restaurants, and route logic already suggested -->

## Notes
<!-- Internal observations worth keeping for future India planning -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning | Keep refining context naturally |
| `complete` | Enough context | Give direct recommendations without more discovery |
| `paused` | Not now | Avoid digging for more preferences |
| `never_ask` | User said stop | Do not ask for extra context again |

## Principles

- Use natural language in Context and Notes
- Save only trip-relevant details
- Update `last` whenever India planning is used again
