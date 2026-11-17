---
name: neo4j
description: "Use for Neo4j install, Cypher, schema design, and graph ops."
version: 1.2.0
author: Maxwell McClure
license: MIT-0
metadata:
  hermes:
    tags: [neo4j, graph-database, cypher, knowledge-graph, database]
    requires:
      anyBins: [python3]
---

# Neo4j — install, model, query, operate

Server graph DB (Bolt protocol, Cypher). Current line is calendar-versioned (2026.10.x); 5.26.x is the LTS line. Versions move — confirm current on https://neo4j.com/deployment-center before pinning.

## When to Use

- Setting up or connecting to a Neo4j instance (desktop, server, or cloud).
- Designing a property-graph schema from a domain description.
- Writing, debugging, or optimizing Cypher queries.
- Bulk-loading data or backing up / restoring a graph DB.
- A task needs graph structure (entity-relationship) where SQLite is too flat.

Not for: embedded single-process graph analytics with no server wanted — see LadybugDB (ex-Kuzu, `pip install ladybug`) as the alternative.

## 1. Install (desktop-first)

**Windows — Neo4j Desktop (recommended for dev):**
```powershell
winget install -e --id Neo4j.Neo4jDesktop
```
- Bundles its own JDK (no separate Java install) and includes a free **Enterprise Edition developer license** — APOC, GDS and Bloom are available in Desktop instances.
- Create an instance in the UI; on first start it **generates the initial password** and shows it once. Record it.
- Instance settings UI: choose version (e.g. 2026.10.x) and memory.

**Windows — headless zip (no GUI):**
1. Download the *Windows Executable (zip)* from the Neo4j Deployment Center. Requires **JDK 21** on PATH (Java 25 supported from Neo4j 2025.10+); Neo4j Desktop is the easier route when Java isn't installed.
2. Extract, set `setx NEO4J_HOME "C:\neo4j\neo4j-<version>"` (data/conf live under it; relocate via `server.directories.*` for easy upgrades).
3. Before first start: `%NEO4J_HOME%\bin\neo4j-admin dbms set-initial-password <password>` — without it the default `neo4j` password is enforced with a mandatory change at first login.
4. Start: `%NEO4J_HOME%\bin\neo4j console` (foreground), or as a service (persists across reboots): `neo4j windows-service install` then `neo4j start`. The service runs as LocalSystem via `bin\tools\prunsrv-amd64.exe`, SC name `neo4j`, defaults to AUTO_START — verify with `sc query neo4j` / `sc qc neo4j`. Service install needs admin: from a non-elevated shell, trigger UAC once with `powershell Start-Process <install.bat> -Verb RunAs` (have the .bat log to a file, then poll it; the user clicks Yes once). A PowerShell module ships in the zip (`Import-Module $env:NEO4J_HOME\bin\Neo4j-Management.psd1` → `Invoke-Neo4j console`).

**Linux/macOS:** package managers, Docker (`neo4j/neo4j` image), or zip; same `neo4j-admin`/`cypher-shell` tools. Min hardware: 2 GB RAM for personal use.

**Default ports:** Bolt `7687` (drivers), HTTP `7474` (Neo4j Browser at http://localhost:7474). Verify against the URL Desktop prints for the instance.

**Smoke test after install:**
```python
import neo4j
d = neo4j.GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "<password>"))
print(d.execute_query("RETURN 1 AS ok")[0][0]["ok"])  # → 1
d.close()
```

## 2. Python driver

- Install **`pip install neo4j`** (6.x, pure Python — works on any recent CPython). **Never `neo4j-driver`**: that package name is deprecated and frozen at 5.28.8.
- Connection schemes: `bolt://` unencrypted (fine for localhost), `neo4j://` routing (recommended default), `neo4j+s://` TLS, `neo4j+ssc://` self-signed cert.
- Driver 6.x API: `execute_query` manages session + transaction + retries for you:
```python
import neo4j

with neo4j.GraphDatabase.driver("neo4j://localhost:7687",
                                auth=("neo4j", "<password>")) as driver:
    records, summary, keys = driver.execute_query(
        "MATCH (p:Person {name: $name}) RETURN p.name AS name",
        name="Alice", database_="neo4j")
    for r in records:
        print(r.data())          # dict per row
    print(summary.counters)     # nodes_created, relationships_created, ...
```
- 6.x gotchas (most harvested code predates 6.0):
  - No implicit close — use `with` or call `driver.close()`.
  - `element_id` (str) replaces the int `id` on nodes/relationships.
  - The `trust=` config option is gone — use `trusted_certificates=` / `ssl_context=`. Do NOT copy `trust: "TRUST_ALL_CERTIFICATES"` patterns from old skills; pin real certs.
  - `Session` API: `execute_read()` / `execute_write()` (the old `read_transaction`/`write_transaction` are removed).
- `result_transformer_=neo4j.Result.to_df` returns a pandas DataFrame directly.
- **Performance (official driver manual, current):**
  - Always pass `database_="neo4j"` — omitting it adds a round-trip per query to resolve the default DB.
  - `execute_query` is EAGER: it fetches ALL records before returning. For large result sets use `execute_read`/`execute_write` and iterate the `Result` (never `list()` it) — lazy streaming bounds client+server memory.
  - Choose transaction granularity deliberately: 1 txn per query (safest, auto-retry) → 1 txn per N queries (balanced) → auto-commit `session.run()` loop (fastest, no retries).
  - `pip install neo4j-rust-ext` (verified 2026-11-16, 6.4.1.0): installs `neo4j\_rust.*.pyd` INTO the `neo4j` package — auto-activated, no code changes; official claim 3–10× faster (measured ~1000 qps on localhost round-trips).
- **`cypher-shell`** ships with the install (`%NEO4J_HOME%\bin\cypher-shell -u neo4j -p <pw> "<query>"`) — use it for one-off ops queries instead of writing scripts.

## 3. Schema design (D3)

Checklist, in order: identify entities → PascalCase node labels → identify relationships (verbs) → SCREAMING_SNAKE_CASE relationship types with explicit direction → extract properties (snake_case, typed) → unique constraints on identifiers → indexes for query properties → emit Cypher DDL.

Best practices: prefer directional relationships; keep nodes focused (no over-nesting); avoid redundant relationships; plan against the actual query patterns before modeling; document the schema.

**DDL (5.x+ syntax):**
```cypher
// Unique constraint (auto-creates the backing index — prefer over plain index)
CREATE CONSTRAINT person_email AS (p:Person) ASSERT p.email IS UNIQUE;
// Range index (default for scalar properties)
CREATE INDEX person_name FOR (p:Person) ON (p.name);
// Full-text index for text search
CREATE FULLTEXT INDEX post_fts FOR (p:Post) ON EACH [p.title, p.body];
// Label existence constraint
CREATE CONSTRAINT person_exists AS (p:Person) EXISTS;
// Inspect
SHOW INDEXES;   SHOW CONSTRAINTS;
```

**Index strategy taxonomy** (which index a query needs): unique constraint on identifiers (auto-index + enforces) → single-property range index for equality/range filters → multi-property (composite) for queries that always filter the same combination → full-text for lexical text → vector for similarity. Start traversals from the most selective constrained node and push attribute filters early (in MATCH/WHERE, not after expansion).

## 4. Schema discovery (before querying an unknown DB)

Run these first, and cache the result in-session — guessing labels wastes round-trips:
```cypher
CALL db.labels();
CALL db.relationshipTypes();
CALL db.propertyKeys();
CALL db.schema.visualization();        // one shot: labels, rels, sample props
MATCH (n:Person) RETURN n LIMIT 1;     // sample per important label
MATCH ()-[r:WORKS_AT]->() RETURN type(r), keys(r) LIMIT 1;
```
If labels are ambiguous (e.g. “customer” → `Customer` or `Client`), ask before querying.

**2026.x metadata surface:** the `SHOW` family is primary — `SHOW INDEXES` (rich YIELD: state, populationPercent, indexProvider, readCount, createStatement), `SHOW CONSTRAINTS`, `SHOW PROCEDURES`, `SHOW FUNCTIONS`, `SHOW SETTINGS`. `dbms.procedures`/`dbms.functions`/`dbms.settings`/`dbms.metrics` are REMOVED on 2026.x (`dbms.procedures` → ProcedureNotFound, verified on 2026.10.2). `db.labels()`/`db.relationshipTypes()`/`db.propertyKeys()`/`db.schema.visualization()` still work.

## 5. Cypher patterns (the traps)

- **MERGE matches the FULL pattern** — `MERGE (a)-[:KNOWS]->(b)` creates duplicates when the relationship is missing. Upsert nodes separately, then MERGE the relationship; use `ON CREATE SET` / `ON MATCH SET` (without them nothing updates on match). For simple node upsert: `MERGE (n:User {id: $id})` behind a unique constraint.
- **No index on a filtered property = full label scan.** Always index properties used in WHERE; unique constraints double as indexes.
- **Unbounded `[*]` explodes on connected graphs** — always bound: `[*1..5]`. `[*0..]` includes the start node (usually unintended). `shortestPath()` returns ONE path; `allShortestPaths()` returns all. Rel-property filters inside a path scan-then-filter — consider a model change.
- **Two disconnected patterns = cartesian product**: `MATCH (a:User), (b:Product)` is rows × rows. Connect them or split with WITH; `PROFILE` shows a `CartesianProduct` operator when it happens.
- **WITH resets scope** — only variables in the WITH carry forward. Aggregation forces WITH: `MATCH (u:User) WITH u.country AS c, count(*) AS n`. Filtering after aggregation needs a second WITH. Pagination: `WITH n ORDER BY n.created SKIP 10 LIMIT 10`.
- **NULLs from OPTIONAL MATCH propagate silently** — `WHERE` after OPTIONAL MATCH filters the row out; use `COALESCE()`. `count(NULL)` is 0 (useful for “did they review anything?”). Property access on NULL never errors — silent data loss.
- **Direction matters**: `(a)-[:KNOWS]-(b)` matches both ways (query only); creation requires a direction. Wrong direction = empty results, no error.
- **Batching**: large creates in one transaction exhaust the heap — `UNWIND $rows AS r CREATE (n:Node {id: r.id})`, chunk with `CALL {} IN TRANSACTIONS OF 1000 ROWS`, or `apoc.periodic.iterate()` for complex batch logic with progress. Delete in bounded chunks: `MATCH (n:Old) WITH n LIMIT 10000 DETACH DELETE n` in a loop.
- **Always parameterize** (`$param`), never string-concatenate — injection protection plus plan caching. List params for IN: `WHERE n.id IN $ids`.
- **Shape (official query-tuning guidance):** return only the properties you need (not whole nodes); aggregate early; `DISTINCT`/`LIMIT` early to cut row flow. Query options prefix: `CYPHER planner=cost` (default) vs `planner=dp` (exhaustive, slower planning); `CYPHER replan=force EXPLAIN <q>` forces off-peak replanning of an expensive query (EXPLAIN plans without executing); `replan=skip` avoids planning latency spikes at peak.
- **LOAD CSV from `file://`** requires the file in the server's `import/` directory plus a server restart — for agent-driven loads prefer `UNWIND` from the driver (or `apoc.loadCSV` where APOC is available).
- **Subqueries (Cypher 25, accepted by default on 2026.x)**: `CALL { ... }` runs an ISOLATED subquery — outer variables do NOT flow in; pass them with `WITH` inside (`MATCH (n) CALL { WITH n RETURN count(n) AS c } RETURN ...`). A bare root subquery `CALL { RETURN 1 AS x } RETURN x` is valid. Both Cypher 5 and 25 parse on 2025–2026 (`dbms.components()` → `versions: [5, 25]`); Cypher 5 apps need no changes.

## 6. Query guardrails

- Every generated query gets a `LIMIT` (default 100) and label restrictions — no bare `MATCH (n)` full-scan.
- Classify intent first: entity lookup, relationship exploration, path discovery, subgraph pattern, aggregation, metadata. Paths: bound depth (default ≤3).
- Write operations (CREATE/DELETE/SET/REMOVE/MERGE/DROP/LOAD) require explicit user authorization; reads do not.
- Mask sensitive properties in output (password, token, secret, ssn) — scan before returning.
- On failure, classify: connection (is the server up?), auth, syntax (show the query), semantic (check schema cache for real labels/props), timeout (add LIMIT/indexes), permissions.
- Verify server version when in doubt: `CALL dbms.components() YIELD versions`.

## 7. Operations

**Backup / restore (5.x+):**
```powershell
# OFFLINE: stop the DB first
neo4j-admin database dump <db> --to-path <dir>          # dump (also dump `system` DB)
neo4j-admin database load <db> --from-path <dir> --overwrite-destination=true   # replace existing
```
Online full backups are Enterprise (`neo4j-admin database backup`); Desktop's EE dev license includes them. Never practice restore on the only copy of the data.

**Users/auth:** `CREATE USER <name> SET PASSWORD '<pw>';` then grant roles (`READER`, `WRITE`); least privilege for app users — the `neo4j` user is admin.

**Monitoring:** 2026.x removed `dbms.metrics` — use `dbms.queryJmx`, `dbms.listConnections`, or the Prometheus endpoint at `http://localhost:9404/metrics` (enable in conf if absent). Query plan: `EXPLAIN` (cheap) before `PROFILE` (executes and times).

**Analytics:** APOC (`apoc.*`) and GDS (`gds.pageRank.stream`, `gds.betweenness`, ...) are available in Desktop instances via the EE dev license. **Verified on 2026.10.2 Community: ZERO `apoc.*`/`gds.*` procedures are registered even with the jars on disk (`labs/`, `products/`)** — never generate apoc/gds calls against a Community instance (ProcedureNotFound at runtime). GDS operates on projected graphs (`gds.graph.project`) — read its API docs before running; it is memory-hungry.

## 8. Work discipline

1. Identify the database (name, URI, owner) and what is authorized — reads, writes, or schema changes. State it.
2. Query read-only by default; never escalate after a read-only error.
3. Batch writes inside one explicit transaction; without it each statement commits separately — inspect partial state before retrying.
4. **Read back and report what you wrote** — properties, direction, identity — not just counts. The reported checks must be the ones actually run.
5. Close drivers; check result summaries (`summary.counters`) after every write.

## 9. Vector & full-text search (2026.x)

Full syntax + verified gotchas (CREATE with `WITH` filter properties, `SEARCH` clause, legacy `db.index.*`, background build states): **`references/vector-search.md`**. The two must-knows: search indexes are NOT used automatically (query with `SEARCH`), and in-index vector filter props must be declared `WITH [...]` at creation time.

## 10. 2026.x operations (memory, import, upgrades, maintenance)

Full reference (memory sizing rules incl. vectors-in-OS-memory, offline `import full`, upgrade policy, routine maintenance incl. the Community defrag path, logs, timeout posture): **`references/ops-2026.md`**. Quick facts: `db.transaction.timeout` ships disabled (0s) — set a positive default (e.g., 10s) so runaway queries can't hang the server; `database copy` (defrag) is Enterprise-only — Community reclaims space via offline dump → load.

## Pitfalls

- `neo4j-driver` on PyPI is the deprecated alias — install `neo4j`.
- The curl HTTP `tx/commit` endpoint was removed in Neo4j 5 — use the driver or cypher-shell.
- Don't harvest `trust: TRUST_ALL_CERTIFICATES` from pre-6.0 code; driver 6.x removed `trust`.
- Neo4j 5.x+ constraint syntax is `CREATE CONSTRAINT ... AS (n:Label) ASSERT ...` — old `CREATE CONSTRAINT x ON :Label(prop)` is 4.x and fails.
- Desktop-generated passwords are shown once — if lost, reset via Desktop UI or `neo4j-admin server dbms set-initial-password` on a fresh data dir (or `SET PASSWORD` as admin).
- `neo4j stop` does not see a console-mode instance (no pid file in `run/`) — it reports "not running" while the port stays bound. Kill the console process to free the port; a hard kill is safe on an empty/WAL db (WAL replays on next start).
- `dbms.components()` yields `versions` (plural, a list), not `version`.
- A script that crashes AFTER a write has committed leaves the rows behind; rerunning it duplicates data (counters from the new run will not show the old rows). Verify or clean up the DB before rerunning a failed write script.
- `summary.counters` is an attribute object (`summary.counters.nodes_created`), not a dict — `dict(summary.counters)` raises TypeError.
- 2026.x removed `dbms.procedures`/`dbms.functions`/`dbms.settings`/`dbms.metrics`/`dbms.system` — use `SHOW PROCEDURES` / `SHOW FUNCTIONS` / `SHOW SETTINGS`. Don't trust 5.x-era ops snippets.
- Search indexes are never used implicitly — a vector/full-text index only helps a query that uses `SEARCH` (or the deprecated `db.index.*` procedures).
- In-index vector filter props must be declared with `WITH [...]` at `CREATE VECTOR INDEX` time or the query fails `PropertyNotFound`.
- Driver `execute_query` takes exactly ONE statement per call — separate statements, never `;`-joined.
- `CREATE INDEX ON :Label(prop)` is 4.x syntax — invalid on 5.x+ (use `CREATE INDEX name FOR (n:Label) ON (n.prop)`).

## Sourcing

Cypher trap catalogue: @ivangdavila/neo4j @v1.0.0 (MIT-0). Schemes, batching, error classes: @fisa712/neo4j-integration @v1.0.0 (corrected: dropped fabricated `cypher-dsl-python` package, `TRUST_ALL_CERTIFICATES`, 4.x index names). Schema checklist: @fisa712/property-graph-schema-designer @v1.0.0. Discovery + guardrails: @jeffrao/neo4j-cypher-query-analyze @v1.0.0 (driver-based, not curl; dropped shipped .env and path residue). Work discipline: @ricardodpalmeida/ladybug-opencypher-updated @v1.1.6 (genericized from embedded LadybugDB to server Neo4j). Install (winget/zip/service, ports, set-initial-password) and ops (dump/load, users, metrics) written from neo4j.com docs, verified 2026-11-16. All candidates passed harvest triage 2026-11-16 (evidence: harvest candidates.txt, local scratch). Run-2 gap-fill (2026-11-16): vector/SEARCH syntax + 2026.x ops (memory, offline import, upgrades, logs, SHOW family, apoc/gds gating) verified LIVE on 2026.10.2 and against neo4j.com Cypher Manual / Operations Manual / Upgrade & Migration Guide (evidence: gap-harvest candidates.txt, local scratch). Index-strategy taxonomy + selective-entry rule: @fisa712/graph-query-optimization-assistant @v1.0.0 (corrected: 4.x DDL rewritten to 5.x+, fabricated benchmarks and dead tool recs — py2neo — dropped). Nodes/edges CSV intermediate format: @fisa712/csv-graph-loader-generator @v1.0.0. Run-3 best-practices pass (2026-11-16, user-approved): driver performance rules (database_ param, eager vs lazy, txn granularity), memory rules (initial=max, explicit sizes, vector-in-OS-memory, memory-recommendation, per-DB plan cache), maintenance ops (check/report/validate-config, Community defrag = dump+load, backup rules), transaction-timeout default, query shaping + CYPHER planner/replan options — all from current neo4j.com docs (Python driver manual, Operations Manual, Cypher Manual) verified LIVE on 2026.10.2; neo4j-rust-ext installed and benchmarked (~1000 qps).
