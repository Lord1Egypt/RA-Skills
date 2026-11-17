# Ladybug Python & Cypher API reference

Contents: [Runtime setup](#runtime-setup) · [OpenClaw installation](#openclaw-installation-checks) · [Python: sync](#python-sync) · [Python: async](#python-async) · [Result helpers](#result-helpers) · [Multiple statements & parameters](#multiple-statements--parameters) · [Python UDFs](#python-udfs) · [Schema (DDL) — extended](#schema-ddl--extended) · [Import & file scan](#import--file-scan) · [MATCH — variable length & shortest paths](#match--variable-length--shortest-paths) · [CALL — FTS procedures](#call--fts-procedures) · [Official links](#official-links)

Examples, FTS signatures and iterator details for [SKILL.md](../SKILL.md).

Baseline: **ladybug 0.21.2**, not legacy `real_ladybug`. File suffixes are conventions, not permission to rename or migrate existing databases.

## Runtime setup

Use the project environment. Existing shared location: `~/.local/share/ladybug-opencypher-updated/venv`; Windows uses `Scripts/python.exe`. For requested installation with `uv` available:

```sh
uv venv --python python3 --no-python-downloads ~/.local/share/ladybug-opencypher-updated/venv
uv pip install --python ~/.local/share/ladybug-opencypher-updated/venv/bin/python --only-binary :all: 'ladybug==0.21.2'
```

Alternatively, create a dedicated `python3 -m venv` and run its `python -m pip install -r <skill-dir>/requirements.txt`. Report missing prerequisites without altering system Python or changing the engine pin. Sources: [installation](https://docs.ladybugdb.com/installation/), [PyPI](https://pypi.org/project/ladybug/0.21.2/).

Use the same interpreter for installation and execution. `check_env.py` checks Python API/version only; `--smoke` also executes `RETURN 1` in memory, without opening user data. `--expect-version` selects a separately verified baseline, never an automatic upgrade.

For native-load failures, including missing Windows DLL dependencies, report the prerequisite and use matching official runtime libraries. Successful import alone does not prove engine execution.

---

## OpenClaw installation checks

Only when installation verification is requested, check intended agents with `openclaw skills info ladybug-opencypher-updated --agent <id> --json`: version, `eligible`, `disabled`, `blockedByAgentFilter`, `modelVisible`. Shared files do not override filters. Check Python execution separately; discovery alone is insufficient. Do not restart a Gateway merely to refresh skills.

## Python: sync

```python
import ladybug as lb

with lb.Database("path/to/db.lbdb", read_only=True) as db, lb.Connection(db) as conn:
    with conn.execute("MATCH (a:User)-[f:Follows]->(b:User) RETURN a.name, b.name, f.since LIMIT 20") as rows:
        for row in rows:
            print(row)
```

For read-only access to an existing file, use `lb.Database(path, read_only=True, buffer_pool_size=256 * 1024 * 1024)`. Use context managers or `finally` to close resources on failure too. Use the owning application API for live read-write databases; these standalone examples do not coordinate multiple processes.

## Python: async

Connection pool is managed on the async connection:

```python
import asyncio
import ladybug as lb

async def main():
    with lb.Database("path/to/db.lbdb", read_only=True) as db:
        with lb.AsyncConnection(db, max_concurrent_queries=4) as conn:
            with await conn.execute("MATCH (n:User) RETURN n.name LIMIT 10") as rows:
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

```python
result = conn.execute(
    "MATCH (p:Paper) WHERE p.id = $id RETURN p.id",
    parameters={"id": "paper-123"},
)
```

Values are parameterized; validate schema identifiers separately. Set a query timeout using `conn.set_query_timeout(30000)` (milliseconds). Multiple statements normally auto-commit separately. For an atomic write batch use `BEGIN TRANSACTION`, the statements, and `COMMIT`; use `ROLLBACK` on failure. See [transactions](https://docs.ladybugdb.com/cypher/transaction/).

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

- Use explicit traversal upper bounds; the engine defaults to **30** when omitted.
- **Shortest paths**: **`SHORTEST`** / **`ALL SHORTEST`** between Kleene star and bounds, e.g. `(n)-[r* SHORTEST 1..10]-(m)`. Use `SHORTEST` for one shortest path and `ALL SHORTEST` for all ties. [MATCH](https://docs.ladybugdb.com/cypher/query-clauses/match)

## CALL — FTS procedures

Install/load the [FTS extension](https://docs.ladybugdb.com/extensions/full-text-search/) before use.

Extension installation is separate from installing this skill. Only install extensions when authorized, using the official source compatible with the engine version. The bundled helpers do not install them. Run `CREATE_FTS_INDEX` as a standalone statement, not in a multi-statement block with other statements.

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
