# Memory Template — PostgreSQL

Create `~/Clawic/data/pg/memory.md` with this structure:

```markdown
# PostgreSQL Memory

## Status
status: ongoing
last: YYYY-MM-DD

## Context
<!-- Their databases: version, provider, rough size, workload shape (OLTP/analytics/mixed) -->
<!-- Schema landmarks: the big tables, the partitioned ones, multi-tenant or not -->

## Constraints
<!-- Extensions unavailable, no-superuser, compliance rules, tables that cannot go offline -->

## Pain Points
<!-- Incidents and recurring problems they have raised -->

## Preferences
<!-- Migration tooling, run-DDL vs hand-back-SQL, plan detail wanted, review gates -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning |
|-------|---------|
| `ongoing` | Still learning their setup |
| `complete` | Know their schema and workflow well |
