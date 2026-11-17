# Memory Template — GraphQL

Create `~/Clawic/data/graphql/memory.md` with this structure:

```markdown
# GraphQL Memory

## Status
status: ongoing
last: YYYY-MM-DD

## Context
<!-- Their graph: server library, schema size, schema-first or code-first -->
<!-- Datastore and ORM, deployment target, federated or single schema -->
<!-- Client surfaces and how fast each one can be redeployed -->

## Pain Points
<!-- Failures they have already hit: N+1, nulled branches, cache not updating, limits -->

## Preferences
<!-- Conventions agreed: naming, pagination shape, error style -->
<!-- Limits calibrated from their traffic: depth, alias, token, complexity, timeouts -->
<!-- SDL only vs SDL plus resolver code; explanation depth -->
<!-- How proactively to surface hardening and breaking-change warnings -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning |
|-------|---------|
| `ongoing` | Still learning their schema and stack |
| `complete` | Know their graph and conventions well |
