# Ladybug workflow patterns

Recipes and checklists for authoring Cypher and debugging Neo4j-style assumptions. Pair with [SKILL.md](../SKILL.md) and [api-reference.md](api-reference.md).

---

## Pattern 1: Greenfield graph (schema → load → query)

**Trigger**: New `.lbug` database or new labels/relationships.

**Steps**:

1. Design **one label per node table** and **one label per relationship table**; choose primary keys for every node table.
2. Run `CREATE NODE TABLE` / `CREATE REL TABLE` (optional `IF NOT EXISTS`).
3. Bulk load with **`COPY … FROM`** or **`LOAD FROM`**, or insert via Cypher per your workflow.
4. Anchor **`MATCH`** patterns with labels and selective predicates before wide scans.

**Outcome**: Inserts succeed and queries align with declared multiplicity (`MANY_ONE`, etc.).

---

## Pattern 2: “Wrong” paths or counts vs Neo4j

**Trigger**: Path cardinality, duplicates, or reachability differs from Neo4j.

**Steps**:

1. **Walk vs trail** — Ladybug allows repeated edges in a pattern; use **`is_trail()`** / **`is_acyclic()`** when you need trail or acyclic semantics ([difference doc](https://docs.ladybugdb.com/cypher/difference/)).
2. **Variable-length** — check implicit **upper bound 30** and explicit bounds on `*`.
3. **Shortest paths** — use **`SHORTEST`** / **`ALL SHORTEST`** syntax where appropriate ([MATCH](https://docs.ladybugdb.com/cypher/query-clauses/match)).

**Outcome**: Expected path behavior once semantics match the question being asked.

---

## Pattern 3: Unsupported Neo4j clauses

**Trigger**: Parser errors or surprising lack of effect.

**Checklist** — common mappings:

| Topic | Ladybug |
|--------|---------|
| `CREATE` / `MERGE` | Prefer explicit labels; label may be inferred from schema otherwise. |
| `FINISH` | Not supported — use `RETURN COUNT(*)` etc. |
| `FOREACH` | Not supported — use `UNWIND`. |
| `REMOVE` | Not supported — use `SET n.prop = NULL`. |
| `SET` | Only `n.prop = expr` per property; **map `+=` not supported** — set one by one. |
| `USE` graph | Not supported — **one graph per DB file**; open another `Database` for another graph. |
| `WHERE` inside patterns | Not supported — not `(n:Person WHERE n.name = 'x')`; use `MATCH (n:Person) WHERE …`. |
| Label filter in `WHERE` | Not `WHERE n:Person` — use `MATCH (n:Person)` or `WHERE label(n) = 'Person'`. |
| `SHOW …` | Often **`CALL`** (e.g. `CALL show_functions() RETURN *`, `CALL SHOW_INDEXES() RETURN *`). |

**Subqueries**: `EXISTS` and `COUNT` subqueries — see [Subqueries](https://docs.ladybugdb.com/cypher/subquery).

---

## Pattern 4: Full-text search errors

**Trigger**: FTS procedure fails or returns empty.

**Steps**:

1. Confirm the **FTS extension** is installed/loaded ([Extensions](https://docs.ladybugdb.com/extensions/)).
2. Index only **`STRING`** properties on **node** tables.
3. Verify index name/table match `CREATE_FTS_INDEX` / `QUERY_FTS_INDEX` arguments.
4. List indexes: **`CALL SHOW_INDEXES() RETURN *`**.

---

## Pattern 5: Catalog / introspection

**Trigger**: “Unknown function” or `SHOW` syntax errors.

**Action**: Switch to **`CALL`**-style procedures documented for your build ([CALL](https://docs.ladybugdb.com/cypher/query-clauses/call)); procedure names/casing may vary.

---

## Query authoring habits (Neo4j-style Cypher)

- **Anchor** with labels and selective predicates to limit scans.
- **Cartesian products** — disconnected `MATCH (a:User), (b:Product)` multiplies rows; connect patterns or use `WITH`.
- **`WITH` scope** — only listed variables continue; aggregations often need explicit `WITH`.
- **`MERGE`** matches the **full pattern** — same duplicate risk as Neo4j.
- **Dense graphs** — bound variable-length paths, explicit upper bounds, `LIMIT` where appropriate.

---

## Debug checklist: results “wrong” vs Neo4j

1. **Schema** — labels and rel types match `CREATE NODE TABLE` / `CREATE REL TABLE`.
2. **Walk vs trail** — duplicate edges in paths.
3. **Variable-length defaults** — implicit upper bound **30**.
4. **Unsupported clauses** — `FOREACH`, `REMOVE`, `FINISH`, property-pattern `WHERE`, `SET +=`.
5. **`SHOW` errors** → **`CALL …()`**.
6. **FTS** — extension loaded; **STRING** columns only.
