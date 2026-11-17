---
name: kwdb-schema-design
description: |
  Design KWDB schemas and generate DDL for relational, time-series, and mixed workloads.
  Covers: CREATE/ALTER/DROP TABLE, INDEX, VIEW, constraints, partitioning, retention, tags.
  Trigger keywords: KWDB, schema, table, index, time-series, sensor, IoT, metrics,
  TAGS, PRIMARY TAGS, RETENTIONS, primary key, foreign key, DDL.
  NOT for: DML queries, deployment, backup, performance tuning.
version: 0.4.1
---

<EXTREMELY-IMPORTANT>
**ALWAYS invoke this skill via the Skill tool before designing any KWDB schema.**

This applies even when:
- Reference file contents appear in conversation context (from previous reads)
- Session was restored from a compacted conversation
- You believe you already know the KWDB syntax

**Reading reference files directly ≠ Skill invocation.** The Skill tool triggers the
complete workflow (classify → gather requirements → design → DDL → validate) and
ensures guardrails are followed. Skip this step = skip the workflow.
</EXTREMELY-IMPORTANT>

## Tiered Reference Architecture

**Tier 1 (Always Read)** - Core rules, scope, and examples:
- `references/key-rules.md` - Decision tree and core rules
- `references/disambiguation.md` - Clarifying questions
- `references/_scope.md` - Skill boundaries (IN/OUT of scope)
- `references/_examples.md` - Complete dialogue examples
- `references/_contributing.md` - How to add new references
- `references/_sections.md` - Tier definitions and categories

**Tier 2 (High-Frequency DDL)** - Read when designing tables/indexes/constraints:
- `references/table-ddl-ref.md` - CREATE/ALTER/DROP TABLE
- `references/index-ddl-ref.md` - CREATE/DROP INDEX
- `references/constraint-ref.md` - CHECK, UNIQUE, FOREIGN KEY

**Tier 3 (Medium-Frequency DDL)** - Read when needed:
- `references/view-ref.md` - Views and Materialized Views
- `references/sequence-ref.md` - Sequences and auto-increment
- `references/partitioning-ref.md` - LIST, RANGE, HASH partitioning
- `references/retention-ref.md` - Time-series retention policies

**Tier 4 (Low-Frequency DDL)** - Only when explicitly requested:
- `references/trigger-ref.md` - Triggers
- `references/procedure-ref.md` - Stored procedures and functions
- `references/database-ref.md` - Database and schema operations
- `references/privilege-ref.md` - User, role, and permission management

## When to Activate

**Should trigger (explicit KWDB):**
- "design a KWDB schema"
- "write KWDB DDL"
- "create a table/index/view in KWDB"
- "KWDB schema for ..."
- "KWDB CREATE TABLE"

**Should trigger (implicit - schema keywords):**
- "create table" / "design table" / "table structure"
- "add column" / "modify column" / "alter table"
- "create index" / "add index" / "drop index"
- "primary key" / "foreign key" / "constraints"
- "schema design" / "database schema"

**Should trigger (time-series keywords):**
- "sensor data" / "IoT" / "metrics" / "readings"
- "time-series" / "time series" / "timestamp data"
- "TAGS" / "PRIMARY TAGS" / "RETENTIONS"
- "device data" / "monitoring data" / "logs"

**Should trigger (relational keywords):**
- "users/orders/products" + "schema/table"
- "entity" + "table"
- "foreign key relationship"

**Should trigger (financial/trading keywords):**
- "高频交易" / "HFT" / "行情" / "tick data"
- "订单簿" / "order book" / "K线" / "kline"
- "VWAP" / "成交量" / "价差" / "深度"
- "stock" / "futures" / "期权" / "证券"

**Should NOT trigger:**
- "SELECT ..." / "INSERT ..." / "UPDATE ..." (DML queries)
- "how to query" / "optimize query" (query optimization)
- Deployment, troubleshooting, migration questions
- Backup/restore operations
- "explain analyze" / "slow query" (performance tuning)
- User/permission management (unless explicitly requested)

## Supported DDL Operations

| Category | Operations |
|----------|------------|
| Tables | CREATE TABLE, ALTER TABLE, DROP TABLE |
| Indexes | CREATE INDEX, ALTER INDEX, DROP INDEX |
| Constraints | PRIMARY KEY, UNIQUE, CHECK, FOREIGN KEY |
| Views | CREATE VIEW, DROP VIEW |
| Materialized Views | CREATE MATERIALIZED VIEW, REFRESH, DROP |
| Sequences | CREATE SEQUENCE, nextval(), setval() |
| Time-Series | Tags, Primary Tags, Retention |
| Partitioning | LIST, RANGE, HASH (relational), HASHPOINT (time-series) |

## Workflow

### Step 1: Classify Workload Type

```
Request → RELATIONAL / TIME-SERIES / MIXED
```

Ask if unclear. **Never skip this step.**

### Step 2: Gather Requirements

Use `disambiguation.md` to ask:
- What data fields are needed
- Primary key strategy
- Query patterns (filter, group, join)
- For time-series: retention needs

### Step 3: Design Schema

Apply rules from `key-rules.md` and relevant tier-2/3 references:
- Choose correct column types
- Design primary keys
- Add indexes only when needed
- For time-series: design tags and retention

### Step 4: Generate DDL

Output minimal, executable DDL:
- Use correct KWDB syntax
- Include NOT NULL where appropriate
- Add comments for clarity

### Step 5: Validate

Include validation step:
- `SHOW CREATE TABLE` to verify syntax
- `SHOW COLUMNS` to verify structure
- `SHOW INDEX` to verify indexes

## Output Format

```markdown
## Intent
[Brief description of what the schema does]

## Workload Type
[relational / time-series / mixed]

## Assumptions
[Any assumptions made - retention, primary key strategy, etc.]

## Design
[Table structure with column types and rationale]

## DDL
```sql
-- minimal executable DDL
```

## Validation
[How to verify the DDL works]
```

## Guardrails

1. **Never output DDL before classifying workload type**
2. **Never assume retention without stating it** (time-series)
3. **Never create speculative indexes** (label as optional)
4. **Prefer minimal schema** over comprehensive
5. **State all assumptions** when information is incomplete
6. **Validate DDL** before finishing
7. **FK columns must be indexed**
8. **Use appropriate types** (DECIMAL for money, not FLOAT)

## Error Handling

- If requirements unclear: ask clarifying questions first
- If DDL might be wrong: suggest validation steps
- If feature not supported: explain KWDB limitation
- If ambiguous request: classify workload type first
