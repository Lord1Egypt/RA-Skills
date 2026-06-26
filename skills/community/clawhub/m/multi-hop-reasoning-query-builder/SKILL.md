---
name: multi-hop-reasoning-query-builder
description: Generate graph queries that perform multi-hop traversal and reasoning across relationships in graph databases and knowledge graphs.
metadata:
  {"openclaw":{"emoji":"🔗","homepage":"https://clawhub.com"}}
---

# Multi-Hop Reasoning Query Builder

Construct graph queries that explore indirect relationships through multiple hops in a graph.

This skill helps developers generate queries that traverse several relationships to discover hidden connections and complex patterns within graph datasets.

Multi-hop reasoning is commonly used in:

- knowledge graph exploration
- recommendation systems
- fraud detection
- supply chain analysis
- social network analysis

The skill produces queries that traverse multiple edges to identify connections between entities.

---

## 📋 Quick Start

### When To Use This Skill

Use this skill when a user wants to:

- build multi-hop graph queries
- explore indirect relationships
- perform reasoning across graph paths
- discover connections through several relationships
- construct path traversal queries
- find hidden patterns across hops
- analyze relationship chains

### Example Requests

- "Find friends of friends of Alice."
- "Find suppliers connected to a company within three hops."
- "Discover customers linked through purchase chains."
- "Find entities connected to a node within multiple relationships."
- "Show me the path from Product A to Product B."
- "Find all paths between two companies."

---

## 🎯 What This Skill Produces

The skill generates graph queries capable of:

- **Multi-hop traversal** - Traverse multiple relationship hops
- **Path discovery** - Find paths between entities
- **Indirect relationship detection** - Discover hidden connections
- **Graph reasoning queries** - Complex reasoning patterns
- **Variable-length path exploration** - Flexible traversal patterns
- **Performance-optimized queries** - Efficient multi-hop queries

Outputs include:

- Cypher traversal queries
- SPARQL property path queries
- Graph path exploration queries
- Parameterized multi-hop templates

---

## 🔍 Multi-Hop Query Types

### 1. Fixed Depth Multi-Hop

**Pattern:** Traverse exactly N relationships

**Cypher:**
```cypher
MATCH (start:$startLabel {id: $startId})-[:$relType*2]->(target)
RETURN target
```

**Example - Friends of Friends:**
```cypher
MATCH (alice:Person {name:"Alice"})-[:FOLLOWS*2]->(fof:Person)
RETURN fof
```

**Use Cases:**
- Exactly 2 hops from Alice
- Precise distance queries
- Specific relationship chain discovery

---

### 2. Variable Depth Multi-Hop

**Pattern:** Traverse between MIN and MAX relationships

**Cypher:**
```cypher
MATCH (start:$startLabel {id: $startId})-[:$relType*1..$maxHops]->(target)
RETURN target
LIMIT $limit
```

**Example - Up to 3 Hops:**
```cypher
MATCH (company:Company {id:"C123"})-[:SUPPLIES*1..3]->(supplier)
RETURN supplier
LIMIT 50
```

**Use Cases:**
- Within N hops
- Range-based discovery
- Flexible connection finding

---

### 3. Path Discovery

**Pattern:** Return actual path structures

**Cypher:**
```cypher
MATCH path = (start:$startLabel)-[*1..$maxHops]-(target:$targetLabel)
RETURN path, LENGTH(path) as hops
LIMIT $limit
```

**Example - Path from Alice to Bob:**
```cypher
MATCH path = (alice:Person {name:"Alice"})-[*1..4]-(bob:Person {name:"Bob"})
RETURN path, LENGTH(path) as hops
LIMIT 10
```

**Returns:** Full traversal paths showing relationships

---

### 4. Filtered Multi-Hop

**Pattern:** Multi-hop with relationship type filtering

**Cypher:**
```cypher
MATCH (start:$startLabel)-[:$relType*1..$hops]->(target:$targetLabel)
WHERE start.id = $startId AND target.$property = $value
RETURN target
LIMIT $limit
```

**Example - Specific Relationship Chain:**
```cypher
MATCH (source:Person)-[:KNOWS|:WORKS_WITH*1..3]->(target:Person)
WHERE source.name = "Alice" AND target.active = true
RETURN target
LIMIT 25
```

---

### 5. Undirected Multi-Hop

**Pattern:** Follow relationships in any direction

**Cypher:**
```cypher
MATCH (start:$startLabel)-[:$relType*1..$maxHops]-(target)
RETURN target
```

**Example - Undirected Network:**
```cypher
MATCH (node:Entity)-[*1..3]-(connected)
RETURN connected
LIMIT 100
```

---

### 6. SPARQL Property Paths

**Pattern:** SPARQL+ operator for one or more hops

**SPARQL:**
```sparql
SELECT ?target
WHERE {
  ?start ex:$property+ ?target .
}
```

**Example - Property Path:**
```sparql
PREFIX ex: <http://example.org/>
SELECT ?person
WHERE {
  :Alice ex:knows+ ?person .
}
```

---

### 7. Aggregated Multi-Hop

**Pattern:** Multi-hop with aggregation

**Cypher:**
```cypher
MATCH (start:$startLabel)-[:$relType*1..$hops]->(target)
RETURN target, COUNT(*) as path_count
GROUP BY target
ORDER BY path_count DESC
```

**Example - Count Paths:**
```cypher
MATCH (alice:Person {name:"Alice"})-[:FOLLOWS*1..3]->(person)
RETURN person, COUNT(*) as num_paths
GROUP BY person
ORDER BY num_paths DESC
LIMIT 10
```

---

### 8. Conditional Multi-Hop

**Pattern:** Multi-hop with WHERE conditions

**Cypher:**
```cypher
MATCH path = (start:$startLabel)-[:$relType*1..$hops]->(target)
WHERE ALL(n in nodes(path) WHERE n.$property <> $excludeValue)
RETURN target
```

**Example - Avoid Specific Nodes:**
```cypher
MATCH path = (alice:Person {name:"Alice"})-[:KNOWS*1..3]->(person)
WHERE ALL(n in nodes(path) WHERE n.status = "active")
RETURN person
LIMIT 50
```

---

## 📊 Multi-Hop Complexity

**Hop Depth Impact:**

```
Depth 1: O(n)
  ├─ 1 hop from start node
  └─ Direct relationships only

Depth 2: O(n²)
  ├─ 2 hops from start node
  └─ Friends of friends

Depth 3: O(n³)
  ├─ 3 hops from start node
  └─ Can be expensive

Depth 4+: O(n^4+) ⚠️ EXPENSIVE
  ├─ Exponential growth
  └─ Use only with filtering/limits
```

**Performance Guidelines:**
- Keep depth ≤ 3 for open queries
- Use depth ≤ 4 with strong filters
- Avoid depth > 4 without restrictions
- Always include LIMIT clause

---

## 🏢 Real-World Examples

### Social Network: Friends of Friends
```cypher
MATCH (user:User {id: $userId})-[:FOLLOWS*2]->(fof:User)
WHERE NOT (user)-[:FOLLOWS]->(fof)
RETURN DISTINCT fof
LIMIT 50
```

### E-Commerce: Product Recommendations
```cypher
MATCH (customer:Customer {id: $customerId})-[:PURCHASED*1..2]->(recommended:Product)
RETURN recommended, COUNT(*) as relevance
GROUP BY recommended
ORDER BY relevance DESC
LIMIT 10
```

### Supply Chain: Supplier Network
```cypher
MATCH (company:Company {name: $companyName})-[:SUPPLIES*1..3]->(supplier:Company)
RETURN supplier, COUNT(*) as connections
GROUP BY supplier
ORDER BY connections DESC
LIMIT 20
```

---

## ✅ Best Practices

When building multi-hop queries:

1. **Limit Traversal Depth**
   - Depth ≤ 3 for unrestricted queries
   - Depth ≤ 4 with heavy filtering
   - Always bound depth

2. **Restrict Relationship Types**
   - Specify exact relationships
   - Avoid wildcard traversal
   - Filter by direction

3. **Use Result Limits**
   - Always include LIMIT clause
   - Prevents memory issues
   - Controls response size

4. **Start from Specific Nodes**
   - Use indexed properties for entry
   - Filter by specific IDs/properties
   - Avoid full scans

5. **Filter Within Paths**
   - Use WHERE with ALL/ANY
   - Exclude specific nodes
   - Filter by node properties

6. **Apply Indexes**
   - Index starting node properties
   - Index relationship types
   - Index filter properties

7. **Test Performance**
   - Profile with real data
   - Monitor execution time
   - Optimize entry points

8. **Document Assumptions**
   - Expected path lengths
   - Relationship cardinality
   - Performance characteristics

---

## 🔗 Integration with Other Skills

This skill integrates with:

- **graph-query-debugging-tool** - Debug multi-hop queries
- **graph-query-optimization-assistant** - Optimize multi-hop patterns
- **graph-template-query-generator** - Generate multi-hop templates
- **nl-to-graph-query-translator** - Translate natural language to multi-hop
- **graph-schema-validation** - Validate multi-hop against schema

---

## 📋 Output Formats

The skill returns:

### 1. Multi-Hop Query
Executable Cypher or SPARQL query with specified hop depth.

### 2. Path Query
Returns relationship paths showing traversal chains.

### 3. Parameterized Template
Reusable template with hop parameters.

### 4. Complexity Analysis
Performance metrics and recommendations.

---

## 💡 Reasoning Patterns

### Pattern 1: Find Connections
Discover all entities within N hops.

```cypher
MATCH (start)-[:RELATIONSHIP*1..$n]->(end)
RETURN end
```

### Pattern 2: Find Paths
Return actual paths showing relationship chains.

```cypher
MATCH path = (start)-[*1..$n]-(end)
RETURN path
```

### Pattern 3: Count Paths
Count number of different paths.

```cypher
MATCH (start)-[:REL*1..$n]->(end)
RETURN end, COUNT(*) as paths
```

### Pattern 4: Shortest Path
Find shortest connection.

```cypher
MATCH path = shortestPath((start)-[*]-(end))
RETURN path
```

### Pattern 5: Circular Detection
Find cycles in relationships.

```cypher
MATCH path = (start)-[:REL*2..]->(start)
RETURN path
```

---

## 📖 Summary

This skill generates multi-hop graph queries that traverse multiple relationships to uncover indirect connections and hidden patterns in graph datasets.

It enables developers to perform advanced graph reasoning using Cypher or SPARQL for social networks, recommendation systems, fraud detection, and knowledge graph exploration.

---

**Status: Enterprise-Grade Multi-Hop Reasoning**

Comprehensive multi-hop query generation and reasoning system for professional knowledge graph development.
