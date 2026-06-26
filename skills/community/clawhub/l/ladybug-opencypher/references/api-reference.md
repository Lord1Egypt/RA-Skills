# Ladybug Python & Cypher API reference

Supplement to the main [SKILL.md](../SKILL.md). Use when you need full examples, FTS procedure arguments, or result-iterator details.

---

## Python: sync

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

## Python: async

Connection pool is managed on the async connection:

```python
import asyncio
import real_ladybug as lb

async def main():
    db = lb.Database("path/to/db.lbug")
    conn = lb.AsyncConnection(db, max_concurrent_queries=4)
    rows = await conn.execute("MATCH (n:User) RETURN n.name LIMIT 10")
    for row in rows:
        print(row)

asyncio.run(main())
```

## Result helpers

Per [Python API](https://docs.ladybugdb.com/client-apis/python/):

- `get_all()`, `get_n(n)`, `has_next()` / `get_next()`, `rows_as_dict()`
- **`get_as_df()`** (Pandas), plus Polars/Arrow as documented

## Multiple statements & parameters

- Semicolon-separated **multiple statements** → **list** of result objects; single statement → one result.
- Prefer **bound parameters** when the client supports them (security, plan reuse).

## Python UDFs

- `conn.create_function(name, callable, …)` — invoke the name inside Cypher
- `conn.remove_function(name)` — unregister

## Schema (DDL) — extended

```cypher
CREATE NODE TABLE User(name STRING PRIMARY KEY, age INT64);
CREATE NODE TABLE City(name STRING PRIMARY KEY, population INT64);
CREATE REL TABLE Follows(FROM User TO User, since INT64);
CREATE REL TABLE LivesIn(FROM User TO City, MANY_ONE);
```

- Primary key types: `STRING`, numeric, `DATE`, `BLOB`, or `SERIAL` ([SERIAL](https://docs.ladybugdb.com/cypher/data-types/#serial))
- Optional **`IF NOT EXISTS`** on `CREATE NODE TABLE` / `CREATE REL TABLE`
- **`CREATE NODE TABLE AS` / `CREATE REL TABLE AS`** — schema from `LOAD FROM` or `MATCH … RETURN`

## Import & file scan

| Mechanism | Notes |
|-----------|--------|
| `COPY NodeTable FROM "file.csv"` | Bulk load; variants for Parquet etc. ([Import](https://docs.ladybugdb.com/import/)) |
| `LOAD FROM` | Broader than Neo4j `LOAD CSV FROM` |
| `LOAD FROM df` / `COPY Table FROM df` | Pandas/Polars/Arrow in Python without intermediate files |

Paths in `COPY` / `LOAD FROM` are relative to the process working directory unless absolute.

## MATCH — variable length & shortest paths

- Variable-length rels need an **upper bound**; default max **30** if not specified.
- **Shortest paths**: **`SHORTEST`** / **`ALL SHORTEST`** between Kleene star and bounds, e.g. `(n)-[r* SHORTEST 1..10]-(m)`. Prefer `SHORTEST` when full path objects are not needed. [MATCH](https://docs.ladybugdb.com/cypher/query-clauses/match)

## CALL — FTS procedures

Install/load the [FTS extension](https://docs.ladybugdb.com/extensions/full-text-search/) before use.

**Create index** (node table `STRING` properties only):

```cypher
CALL CREATE_FTS_INDEX('Book', 'book_index', ['title', 'abstract'], stemmer := 'porter', stopwords := './stopwords.csv')
```

(`stopwords` optional; can be one-column table, CSV, or remote file with httpfs per docs.)

**Query (BM25):**

```cypher
CALL QUERY_FTS_INDEX('Book', 'book_index', 'quantum machine', conjunctive := false, TOP := 10) RETURN node, score ORDER BY score DESC
```

Optional tuning: `K`, `B`, `conjunctive`, `TOP`.

**Drop:**

```cypher
CALL DROP_FTS_INDEX('Book', 'book_index')
```

**List indexes:**

```cypher
CALL SHOW_INDEXES() RETURN *
```

Other catalog-style introspection: e.g. `CALL show_functions() RETURN *` — see [CALL](https://docs.ladybugdb.com/cypher/query-clauses/call); case may vary per procedure.

## Official links

- [Python API](https://docs.ladybugdb.com/client-apis/python/)
- [Generated Python reference](https://api-docs.ladybugdb.com/python)
- [Create table](https://docs.ladybugdb.com/cypher/data-definition/create-table/)
- [Import data](https://docs.ladybugdb.com/import/)
- [Extensions](https://docs.ladybugdb.com/extensions/)
