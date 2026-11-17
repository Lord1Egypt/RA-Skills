# Ladybug workflow patterns

Use these checks for Neo4j adaptation and unexpected Cypher results; signatures and examples are in [API reference](api-reference.md).

## Engine upgrades

Follow the official [migration procedure](https://docs.ladybugdb.com/migrate/) on a consistent recoverable copy. Renaming a package import or file suffix does not migrate the database. Runtime setup is in the [API reference](api-reference.md#runtime-setup).

## New graph: schema, load, query

1. Choose one label per node/relationship table, node primary keys, relation direction and multiplicity.
2. Create tables with `CREATE NODE TABLE` / `CREATE REL TABLE`; use `IF NOT EXISTS` where appropriate.
3. Load CSV, Parquet or dataframe data with `COPY ... FROM` / `LOAD FROM`, or insert through Cypher.
4. Anchor queries with labels and selective predicates. Verify inserted properties and declared multiplicity, not only counts.

## Unexpected paths or counts

- Ladybug permits repeated edges in a pattern. Use `is_trail()` / `is_acyclic()` when required ([Neo4j differences](https://docs.ladybugdb.com/cypher/difference/)).
- Inspect explicit traversal bounds and the implicit maximum of 30. Bound dense traversals and use `LIMIT` where it preserves the intended answer.
- Use `SHORTEST` for one shortest path, `ALL SHORTEST` for all ties; see [MATCH](https://docs.ladybugdb.com/cypher/query-clauses/match/).
- Disconnected `MATCH (a:User), (b:Product)` multiplies rows; connect patterns or use `WITH`. Only variables listed in `WITH` remain in scope; stage aggregations explicitly.
- `MERGE` matches the full pattern. Inspect identity before using it to deduplicate.
- Verify typed and parallel relationships with distinct evidence IDs between the same endpoints; counts alone miss lost identity, direction or properties.

## Unsupported Neo4j syntax

| Topic | Ladybug alternative |
|-------|---------------------|
| `CREATE` / `MERGE` | Prefer explicit labels; otherwise schema inference may apply. |
| `FINISH` | Unsupported; use a suitable `RETURN`, such as `COUNT(*)`. |
| `FOREACH` | Use `UNWIND`. |
| `REMOVE` | Use `SET n.prop = NULL`. |
| `SET n += map` | Assign each property explicitly. |
| `USE` graph | One graph per database file; select the correct database connection. |
| `(n:Person WHERE ...)` | Move predicates to `MATCH (n:Person) WHERE ...`. |
| `WHERE n:Person` | Use `MATCH (n:Person)` or `WHERE label(n) = 'Person'`. |
| `SHOW ...` | Check documented `CALL` procedures, e.g. `show_functions()` / `SHOW_INDEXES()`. |

For subqueries, see [`EXISTS` and `COUNT`](https://docs.ladybugdb.com/cypher/subquery/). On unknown functions/procedures, check [CALL](https://docs.ladybugdb.com/cypher/query-clauses/call/) for the installed build's names and signatures.

## Full-text search

Check the loaded FTS extension, node-table `STRING` properties and exact table/index arguments. Use the [FTS procedures](api-reference.md#call--fts-procedures); extension setup must be in scope and engine-compatible.

## Execution failures

| Failure | Action |
|---------|--------|
| Missing database | Report it; create only with authorized `--write --create`. |
| Read-only mutation | Correct the query or use the approved write route; never add `--write` just to suppress the error. |
| Lock conflict | Find the owning process. Use its API or an authorized maintenance window; do not delete lock/WAL files or stop it unilaterally. |
| Slow query | Inspect selectivity, disconnected patterns and bounds. Preview limits do not limit engine execution. |
| Failed write batch | Without an explicit transaction, earlier statements may have committed. Inspect state before retrying. |
| Python import works, execution fails | Run `check_env.py --smoke`; check matching native libraries/platform dependencies. Do not change the engine version automatically. |
