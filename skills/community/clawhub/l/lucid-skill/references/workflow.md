# Workflow Guide

Detailed multi-step workflows for common lucid-skill scenarios.

## Table of Contents

- [First-Time Setup](#first-time-setup)
- [Returning Session](#returning-session)
- [Answering Data Questions](#answering-data-questions)
- [Multi-Source Analysis](#multi-source-analysis)

---

## First-Time Setup

Complete workflow for connecting data and building the semantic layer.

### Step 1: Connect Data

```bash
lucid-skill connect csv /path/to/data.csv
# or
lucid-skill connect excel /path/to/report.xlsx --sheets Sales,Customers
# or
lucid-skill connect mysql --host localhost --database mydb --username root --password pass
```

### Step 2: Verify Connection

```bash
lucid-skill overview    # Confirm sources appear
lucid-skill tables      # Check table names and row counts
```

### Step 3: Explore Schema

```bash
lucid-skill describe <table>   # Column types + sample data
lucid-skill profile <table>    # Statistical overview (null rates, distributions)
```

### Step 4: Build Semantic Layer

```bash
lucid-skill init-semantic      # Export raw schemas
```

Analyze the output, then infer business meanings for each column:

- What does this column represent in business terms?
- What role does it play? (id, dimension, measure, timestamp, attribute)
- How do tables relate to each other?
- What metrics are commonly computed?

Compose the semantic JSON (see [json-schema.md](json-schema.md)) and apply:

```bash
echo '{"tables":[...]}' | lucid-skill update-semantic -
```

### Step 5: Verify Semantics

```bash
lucid-skill search "test query"   # Should return meaningful results
lucid-skill domains               # Should show discovered business domains
```

---

## Returning Session

Previous connections auto-restore. No need to reconnect.

```bash
lucid-skill overview                    # 1. Check existing state
lucid-skill search "用户的问题"          # 2. Find relevant tables
lucid-skill query "SELECT ..."          # 3. Execute and return
```

If `overview` shows empty results, the data directory may have been cleared. Re-connect as in first-time setup.

---

## Answering Data Questions

Recommended flow when a user asks a data question:

### Simple Questions (single table)

```bash
lucid-skill search "月度销售额"          # Find the table
# Use suggestedMetricSqls from the response
lucid-skill query "SELECT month, SUM(amount) FROM sales GROUP BY month"
```

### Complex Questions (multi-table JOIN)

```bash
lucid-skill search "每个客户的订单金额"   # Find relevant tables
lucid-skill join-paths orders customers  # Get JOIN condition
lucid-skill query "SELECT c.name, SUM(o.amount) FROM orders o JOIN customers c ON o.customer_id = c.id GROUP BY c.name"
```

### Exploratory Questions

When the user's question is vague:

1. `lucid-skill domains` — show business domains to help narrow scope
2. `lucid-skill search "broad keywords"` — explore what's available
3. Present findings and ask the user to clarify
4. Then proceed with the specific query

---

## Multi-Source Analysis

Connect multiple sources and query across them:

```bash
lucid-skill connect csv /data/orders.csv
lucid-skill connect csv /data/customers.csv
lucid-skill connect postgres --host db.example.com --database analytics --username ro --password pass
```

After connecting, all tables from all sources are available for querying and JOINing. Use `join-paths` to discover cross-source relationships.

**Note**: Cross-source JOINs work because lucid-skill loads file-based sources into a local query engine. Database sources are queried directly.
