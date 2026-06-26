---
name: ladybug-opencypher
description: |
  Runs openCypher against Ladybug DB with schema-first DDL, Python sync/async execution, CALL procedures,
  full-text search (CREATE_FTS_INDEX / QUERY_FTS_INDEX), and Neo4j divergence notes.
  Use when: (1) Writing or debugging Ladybug Cypher, real_ladybug, or .lbug databases,
  (2) COPY/LOAD import or structured property graphs,
  (3) Comparing or migrating queries from Neo4j-style Cypher,
  (4) FTS extension setup or CALL catalog procedures.
  NOT for: generic graph theory without Ladybug / openCypher execution context.
metadata:
  {
    "openclaw":
      {
        "emoji": "🐞",
        "requires": { "anyBins": ["python3", "python"] },
        "primaryEnv": null,
      },
  }
---

# Ladybug openCypher

Ladybug follows [openCypher](https://opencypher.org/) where possible. **Schema, DDL, some clauses, and MATCH semantics differ** from Neo4j. Overview: [Differences between Ladybug and Neo4j](https://docs.ladybugdb.com/cypher/difference/). DDL: [Create table](https://docs.ladybugdb.com/cypher/data-definition/create-table/).

Ladybug is **embedded (in-process)** — no server URI; open a file path or **`:memory:`** via `real_ladybug`.

## Core principles

1. **Schema first** — node and relationship tables must exist before insert. One label per node/rel table; every node table needs a **primary key**.
2. **Walk vs trail** — patterns use **walk** semantics (edges may repeat). Use **`is_trail()`** / **`is_acyclic()`** when you need Neo4j-like trail checks.
3. **Variable-length paths** — require an upper bound for termination; if omitted, default upper bound is **30**.
4. **Catalog** — prefer **`CALL procedure(...)`** instead of Neo4j `SHOW …` for many introspection tasks.

## Execute from Python (quick start)

Import **`real_ladybug`** (Ladybug Python bindings). Full docs: [Python API](https://docs.ladybugdb.com/client-apis/python/), [generated reference](https://api-docs.ladybugdb.com/python).

```python
import real_ladybug as lb

db = lb.Database("path/to/db.lbug")
conn = lb.Connection(db)
rows = conn.execute("""
    MATCH (a:User)-[f:Follows]->(b:User)
    RETURN a.name, b.name, f.since;
""")
for row in rows:
    print(row)
```

- **`conn.execute` / `await conn.execute`** per statement unless the API documents batching.
- **Multiple statements** (semicolon-separated) return a **list** of results; a single statement returns one result.
- **`COPY` / `LOAD FROM`** paths resolve relative to the process CWD unless absolute.

For async, result helpers, UDFs, and Parquet/DataFrame import — see [references/api-reference.md](references/api-reference.md).

## Schema snippet (DDL)

```cypher
CREATE NODE TABLE User(name STRING PRIMARY KEY, age INT64);
CREATE NODE TABLE City(name STRING PRIMARY KEY, population INT64);
CREATE REL TABLE Follows(FROM User TO User, since INT64);
CREATE REL TABLE LivesIn(FROM User TO City, MANY_ONE);
```

Optional **`IF NOT EXISTS`**. Multiplicity: `MANY_ONE`, `ONE_MANY`, `MANY_MANY`, `ONE_ONE`. **`CREATE NODE TABLE AS` / `CREATE REL TABLE AS`** — infer schema from `LOAD FROM` or `MATCH … RETURN`.

## Import

- **`COPY NodeTable FROM "file.csv"`** (Parquet and other formats per [Import data](https://docs.ladybugdb.com/import/)).
- Neo4j’s `LOAD CSV FROM` → **`LOAD FROM`** in Ladybug.
- In Python: **`LOAD FROM df`** / **`COPY Table FROM df`** for Pandas/Polars/Arrow without an intermediate file.

## Full-text search (FTS)

Load the FTS [extension](https://docs.ladybugdb.com/extensions/) first. Index **STRING** columns on node tables only; query with **`CALL QUERY_FTS_INDEX`**; list with **`CALL SHOW_INDEXES() RETURN *`**. Full procedure signatures: [references/api-reference.md](references/api-reference.md).

## When results differ from Neo4j

Use the checklist and clause table in [references/workflow-patterns.md](references/workflow-patterns.md): walk vs trail, variable-length defaults, unsupported clauses (`FOREACH`, `REMOVE`, `FINISH`, `SET +=`, …), and **`CALL`** vs `SHOW`.

## Utility scripts

Bundled helpers (optional — require `real_ladybug` on `PYTHONPATH`):

- **`scripts/run_cypher.py`** — run a Cypher string or `.cypher` file against a `.lbug` path.
- **`scripts/check_env.py`** — verify `import real_ladybug` and print basic info.

## Additional resources

- Detailed Python API, FTS `CALL` syntax, and DDL/import tables: [references/api-reference.md](references/api-reference.md)
- Debugging workflows, Neo4j comparison table, query habits: [references/workflow-patterns.md](references/workflow-patterns.md)

## Doc links

- [Ladybug vs Neo4j](https://docs.ladybugdb.com/cypher/difference/)
- [DDL / create table](https://docs.ladybugdb.com/cypher/data-definition/create-table/)
- [Import data](https://docs.ladybugdb.com/import/)
- [Full-text search](https://docs.ladybugdb.com/extensions/full-text-search/)
- [MATCH](https://docs.ladybugdb.com/cypher/query-clauses/match)
- [CALL / functions](https://docs.ladybugdb.com/cypher/query-clauses/call)
