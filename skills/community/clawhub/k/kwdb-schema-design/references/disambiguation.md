---
title: Requirement Disambiguation Questions
tier: 1
tags: [core, clarifying-questions, requirements, disambiguation, workload-type, time-series-questions, relational-questions]
---

# Disambiguation

Ask these questions to clarify requirements before DDL.

## Must Clarify (Critical)

### Q1: Workload Type

"Is this time-series data (sensors, metrics, events) or business entity data (users, orders, products)?"

- **Time-series**: Sensor readings, metrics, logs with timestamp
- **Relational**: Users, orders, products, standard CRUD
- **Mixed**: Both

### Q2: What's the Data?

"What fields/columns do you need? Can you give a sample record?"

## Time-Series Questions

| Question | Why |
|----------|-----|
| Timestamp precision? (ms/μs/ns) | Millisecond(3) default. Microsecond(6) for high-frequency data. Nanosecond(9) for scientific instruments. |
| What's the primary tag? (device_id, sensor_id) | Used for grouping/querying |
| How long to retain data? | Sets RETENTIONS |
| Common tag filters? | Candidate for tag indexes |

## Relational Questions

| Question | Why |
|----------|-----|
| Primary key strategy? | UUID, INT, or natural key |
| Foreign key relationships? | Design constraints |
| UPDATE/DELETE frequency? | Affects indexing |
| Common filter columns? | Candidate for indexes |

## Mixed Questions

| Question | Why |
|----------|-----|
| Entity + measurements in same table? | Determines schema structure |
| Common query pattern? | "Readings with device info" vs "Readings only" |

## Assumption Template

When incomplete, state assumptions:

```
Assuming:
- Workload: [relational/time-series/mixed]
- Primary key: [specified or "INT8 DEFAULT unique_rowid()"]
- Retention: [specified or "permanent unless specified"]

Please confirm.
```

## Quick Decision

| If user mentions... | Choose... |
|---------------------|-----------|
| sensors, metrics, logs, readings | TIME-SERIES |
| users, orders, products, inventory | RELATIONAL |
| both entity + measurements | MIXED |
