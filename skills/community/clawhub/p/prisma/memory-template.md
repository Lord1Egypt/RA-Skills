# Memory Template — Prisma

Create `~/Clawic/data/prisma/memory.md` with this structure:

```markdown
# Prisma Memory

## Status
status: ongoing
last: YYYY-MM-DD

## Context
<!-- Provider and version, hosting target, pooler -->
<!-- Schema scale: models, largest tables, multi-tenancy shape -->
<!-- Migration workflow and who applies migrations -->

## Pain Points
<!-- Failures already hit: pool exhaustion, failed migration, N+1, drift -->

## Preferences
<!-- Raw SQL allowed or not; migrations applied vs reviewed -->
<!-- Explanation depth: schema only vs schema plus reasoning -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning |
|-------|---------|
| `ongoing` | Still learning their schema and topology |
| `complete` | Know their stack and workflow well |
