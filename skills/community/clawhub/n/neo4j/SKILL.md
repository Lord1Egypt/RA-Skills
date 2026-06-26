---
name: Neo4j
description: Write Cypher queries with proper patterns for merging, traversal, and performance.
metadata: {"clawdbot":{"emoji":"🕸️","requires":{"anyBins":["cypher-shell","neo4j"]},"os":["linux","darwin","win32"]}}
---

## MERGE Trap

- `MERGE` matches the FULL pattern—`MERGE (a)-[:KNOWS]->(b)` creates duplicates if relationship missing
- Safe upsert: merge nodes separately, then merge relationship
- Use `ON CREATE SET` and `ON MATCH SET` for conditional properties—without these, nothing updates on match
- For simple node upsert: `MERGE (n:User {id: $id})` with unique constraint on id

## Indexes

- No index on property = full label scan—always index properties used in WHERE
- Unique constraint auto-creates index—prefer constraint over plain index when applicable
- Check plan with `EXPLAIN` before production—look for "NodeByLabelScan" without filter pushdown
- Text search needs full-text index: `CREATE FULLTEXT INDEX FOR (n:Post) ON EACH [n.title, n.body]`

## Variable-Length Paths

- Unbounded `[*]` explodes on connected graphs—always set upper bound `[*1..5]`
- `[*0..]` includes start node—usually unintended, start from `[*1..]`
- `shortestPath()` returns one path only—use `allShortestPaths()` for all equally short paths
- Filter inside path is expensive: `[r:KNOWS* WHERE r.active]` scans then filters—consider data model change

## Cartesian Product

- Two disconnected patterns multiply: `MATCH (a:User), (b:Product)` returns rows × rows
- Connect patterns or split with WITH—unintended cartesian kills performance
- Same variable in two patterns = implicit join, no cartesian
- `PROFILE` query shows "CartesianProduct" operator when it happens

## WITH Scope Reset

- Only variables in WITH carry forward—`MATCH (a)--(b) WITH a` loses `b`
- Aggregation forces WITH: `MATCH (u:User) WITH u.country AS c, count(*) AS n`
- Common mistake: filtering after aggregation requires second WITH
- Pagination: `WITH n ORDER BY n.created SKIP 10 LIMIT 10`

## NULL Propagation

- `OPTIONAL MATCH` returns NULL for missing patterns—NULLs propagate through expressions
- `WHERE` after OPTIONAL MATCH filters out NULLs—use `COALESCE()` to preserve rows
- `count(NULL)` returns 0—useful: `OPTIONAL MATCH (u)-[:REVIEWED]->(p) RETURN count(p)`
- Property access on NULL throws no error, returns NULL—silent data loss

## Direction

- Query direction ignored with no arrow: `(a)-[:KNOWS]-(b)` matches both ways
- Creation requires direction—must pick one, can't create undirected
- Wrong direction = empty results—if relationship is `(a)-[:OWNS]->(b)`, query `(b)-[:OWNS]->(a)` finds nothing

## Batch Operations

- Large creates in single transaction exhaust heap—use `CALL {} IN TRANSACTIONS OF 1000 ROWS`
- `UNWIND $list AS item CREATE (n:Node {id: item.id})` for batch inserts
- `apoc.periodic.iterate()` for complex batch logic with progress
- Delete in batches: `MATCH (n:Old) WITH n LIMIT 10000 DETACH DELETE n` in loop

## Parameter Injection

- Always use parameters `$param` not string concatenation—prevents Cypher injection
- Parameters also enable query plan caching—literal values recompile each time
- Pass as map: `{param: value}` in driver, `:param {param: value}` in browser
- List parameter for IN: `WHERE n.id IN $ids`
