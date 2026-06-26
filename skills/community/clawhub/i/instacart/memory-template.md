# Memory Template - Instacart

Create `~/instacart/memory.md` with this structure:

```markdown
# Instacart Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Activation
- When this should activate automatically
- Terms or situations that should not trigger it

## Environment
- Preferred surface: MCP, Developer Platform REST, or Connect
- Typical environment: development or production
- Approved write level and launch boundary

## Context
- Markets, postal codes, and country defaults
- Retailer preferences or exclusions
- Common request types: recipe page, shopping list, retailer lookup, launch review

## Notes
- Known-good payload patterns
- Retry or approval issues seen before
- Caching and attribution details worth remembering

---
Updated: YYYY-MM-DD
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning usage patterns | Gather context opportunistically |
| `complete` | Enough context to operate smoothly | Use stored defaults unless the task changes |
| `paused` | User does not want deeper setup now | Help with the immediate task and avoid extra intake |
| `never_ask` | User does not want this configured further | Stop asking setup-like follow-ups |

## Key Principles

- Keep secrets out of memory files
- Store boundaries, not credentials
- Prefer natural-language notes over rigid config
- Update `last` every time the skill is used
