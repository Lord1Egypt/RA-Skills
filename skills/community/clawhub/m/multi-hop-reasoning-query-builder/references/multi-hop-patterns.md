# Multi-Hop Reasoning Patterns
Twenty+ comprehensive design patterns for multi-hop query generation, covering systematic approaches to building efficient, performant graph reasoning queries.
---
## Fixed Depth Patterns (3)
### Pattern 1: Exactly N Hops
**Context:** Need exact hop distance traversal.
**Template:**
```cypher
MATCH (start:$label {id: $id})-[:$rel*$n]->(target)
RETURN target
```
**When to Use:** Friends of friends (exactly 2), exact distance requirements
---
### Pattern 2: Single Starting Condition
**Context:** Begin from specific starting point.
**Template:**
```cypher
MATCH (start:$label)-[:$rel*$n]->(target:$targetLabel)
WHERE start.$filter = $value
RETURN target
```
---
### Pattern 3: Fixed Depth with Count
**Context:** Count destinations at exact distance.
**Template:**
```cypher
MATCH (start)-[:$rel*$n]->(target)
RETURN target, COUNT(*) as num_paths
GROUP BY target
ORDER BY num_paths DESC
```
---
## Variable Depth Patterns (4)
### Pattern 4: Bounded Range Traversal
**Context:** Find connections within distance range.
**Template:**
```cypher
MATCH (start:$label)-[:$rel*$min..$max]->(target)
WHERE start.id = $id
RETURN DISTINCT target
LIMIT $limit
```
---
### Pattern 5: Variable Depth with Entry Point
**Context:** Optimize entry point for traversal.
**Template:**
```cypher
MATCH (start:$startLabel {$property: $value})
MATCH (start)-[:$rel*1..$maxHops]->(target:$targetLabel)
RETURN DISTINCT target
LIMIT $limit
```
---
### Pattern 6: Multi-Relationship Variable Hops
**Context:** Traverse multiple relationship types.
**Template:**
```cypher
MATCH (start)-[:$rel1|:$rel2|:$rel3*1..$hops]->(target)
WHERE start.id = $id
RETURN target
LIMIT $limit
```
---
### Pattern 7: Undirected Variable Depth
**Context:** Follow relationships both directions.
**Template:**
```cypher
MATCH (start)-[:$rel*1..$hops]-(target)
WHERE start.id = $id
RETURN DISTINCT target
LIMIT $limit
```
---
## Path Discovery Patterns (4)
### Pattern 8: Path Query with Length
**Context:** Return actual paths, not just destinations.
**Template:**
```cypher
MATCH path = (start:$label)-[*1..$maxHops]-(target)
WHERE start.id = $startId
RETURN path, LENGTH(path) as hops
ORDER BY hops
LIMIT $limit
```
---
### Pattern 9: Shortest Path
**Context:** Find minimal hop path.
**Template:**
```cypher
MATCH path = shortestPath((start)-[*]-(target))
WHERE start.id = $startId AND target.id = $targetId
RETURN path, LENGTH(path) as hops
```
---
### Pattern 10: All Paths Query
**Context:** Find all possible paths.
**Template:**
```cypher
MATCH path = (start)-[:$rel*1..$maxHops]-(target)
WHERE start.id = $startId AND target.id = $targetId
RETURN path, LENGTH(path) as hops
LIMIT $limit
```
---
### Pattern 11: Path Filtering
**Context:** Filter paths by node properties.
**Template:**
```cypher
MATCH path = (start)-[:$rel*1..$hops]->(target)
WHERE start.id = $id AND ALL(n in nodes(path) WHERE n.$property = $value)
RETURN path
```
---
## Relationship Type Patterns (3)
### Pattern 12: Specific Relationship Type
**Context:** Traverse only specific relationships.
**Template:**
```cypher
MATCH (start)-[:$specificRel*1..$hops]->(target)
RETURN target
```
---
### Pattern 13: Relationship Direction Control
**Context:** Control traversal direction explicitly.
**Template:**
```cypher
MATCH (start)-[:$rel*1..$hops]->(target)  -- Directed
RETURN target
```
---
### Pattern 14: Relationship Property Filtering
**Context:** Filter by relationship properties.
**Template:**
```cypher
MATCH (start)-[r:$rel*1..$hops]->(target)
WHERE ALL(rel in relationships(path) WHERE rel.$property > $value)
RETURN target
```
---
## Aggregation Patterns (3)
### Pattern 15: Multi-Hop Aggregation
**Context:** Aggregate results across multi-hop paths.
**Template:**
```cypher
MATCH (start)-[:$rel*1..$hops]->(target)
RETURN target, COUNT(*) as path_count
GROUP BY target
ORDER BY path_count DESC
LIMIT $limit
```
---
### Pattern 16: Path-Based Aggregation
**Context:** Aggregate path statistics.
**Template:**
```cypher
MATCH path = (start)-[:$rel*1..$hops]->(target)
RETURN target,
       COUNT(DISTINCT path) as unique_paths,
       AVG(LENGTH(path)) as avg_hops,
       MAX(LENGTH(path)) as max_hops
GROUP BY target
ORDER BY unique_paths DESC
```
---
### Pattern 17: Source Aggregation
**Context:** Count incoming multi-hop connections.
**Template:**
```cypher
MATCH (many)-[:$rel*1..$hops]->(target:$label {id: $id})
RETURN target.id, COUNT(DISTINCT many) as connection_count
ORDER BY connection_count DESC
```
---
## Filtering Patterns (3)
### Pattern 18: Node Property Filtering
**Context:** Filter nodes along path.
**Template:**
```cypher
MATCH (start)-[:$rel*1..$hops]->(target)
WHERE ANY(n in [start] + nodes(target) WHERE n.$property = $value)
RETURN target
```
---
### Pattern 19: Path Node ALL Filter
**Context:** All nodes in path must match condition.
**Template:**
```cypher
MATCH path = (start)-[:$rel*1..$hops]->(target)
WHERE ALL(n in nodes(path) WHERE n.$property <> $excludedValue)
RETURN path
```
---
### Pattern 20: Path Edge Filtering
**Context:** Filter relationships in path.
**Template:**
```cypher
MATCH path = (start)-[*1..$hops]-(target)
WHERE ALL(r in relationships(path) WHERE r.$property > $minValue)
RETURN path
```
---
## Optimization Patterns (3)
### Pattern 21: Dual Entry Point Optimization
**Context:** Query from both ends for shorter paths.
**Template:**
```cypher
MATCH path1 = (start)-[:$rel*1..2]->(middle)
MATCH path2 = (middle)-[:$rel*1..2]->(target)
WHERE start.id = $startId AND target.id = $targetId
RETURN path1 + path2 as full_path, LENGTH(path1) + LENGTH(path2) as hops
```
---
### Pattern 22: Indexed Starting Point
**Context:** Use indexes to optimize entry.
**Best Practice:**
```cypher
CREATE INDEX ON :Person(id)
MATCH (start:Person {id: $id})
MATCH (start)-[:FOLLOWS*1..3]->(target)
```
---
### Pattern 23: Result Limitation Strategy
**Context:** Control memory usage with LIMIT.
**Template:**
```cypher
MATCH (start)-[:$rel*1..$hops]->(target)
WHERE start.id = $id
RETURN target
LIMIT $pageSize
```
---
## Advanced Patterns (3)
### Pattern 24: Cycle Detection
**Context:** Find cycles in relationship graphs.
**Template:**
```cypher
MATCH path = (start)-[:$rel*2..]->(start)
WHERE start.id = $id
RETURN path, LENGTH(path) as cycle_length
```
---
### Pattern 25: Multi-Start Multi-Hop
**Context:** Query from multiple starting points.
**Template:**
```cypher
MATCH (start:$label)
WHERE start.id IN [$id1, $id2, $id3]
MATCH (start)-[:$rel*1..$hops]->(target)
RETURN start.id as source, target, COUNT(*) as shared_connections
GROUP BY source, target
```
---
### Pattern 26: Conditional Hop Depth
**Context:** Dynamic hop depth based on conditions.
**Usage:**
```python
max_hops = 2 if condition_1 else 4
query = f"MATCH (start)-[:$rel*1..{max_hops}]->(target) RETURN target"
```
---
## Best Practices Summary
✅ Depth 1: O(n) - Always safe, very fast
✅ Depth 2: O(n²) - Safe, reasonable performance
✅ Depth 3: O(n³) - Use with caution, add filters
✅ Depth 4: O(n⁴) - Add strong filters, LIMIT
⚠️ Depth 5+: O(n⁵+) - Avoid, use alternative queries
---
**26+ production-ready multi-hop patterns for graph query generation.**
