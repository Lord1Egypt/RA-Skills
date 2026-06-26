# Multi-Hop Queries

This document demonstrates complex path traversal queries that traverse multiple relationships or nodes.

## Two-Hop Queries

### Example 1: Find Friends of Friends

**Natural Language:**
```
Find all people who are friends of Alice's friends
```

**Cypher:**
```cypher
MATCH (alice:Person {name: "Alice"})-[:KNOWS]->(friend:Person)-[:KNOWS]->(friend_of_friend:Person)
WHERE friend_of_friend <> alice
RETURN DISTINCT friend_of_friend
```

**SPARQL:**
```sparql
SELECT DISTINCT ?friend_of_friend
WHERE {
  ex:Alice foaf:knows ?friend .
  ?friend foaf:knows ?friend_of_friend .
  FILTER (?friend_of_friend != ex:Alice)
}
```

---

### Example 2: Find Indirect Company Connections

**Natural Language:**
```
Show companies where people who work with Alice also work
```

**Cypher:**
```cypher
MATCH (alice:Person {name: "Alice"})-[:WORKS_WITH]->(colleague:Person)-[:WORKS_AT]->(company:Company)
RETURN DISTINCT company
```

**SPARQL:**
```sparql
SELECT DISTINCT ?company
WHERE {
  ex:Alice ex:works_with ?colleague .
  ?colleague ex:works_at ?company .
}
```

---

### Example 3: Find Suppliers' Suppliers

**Natural Language:**
```
Find all suppliers of our suppliers
```

**Cypher:**
```cypher
MATCH (our_company:Company {name: "Our Company"})-[:BUYS_FROM]->(supplier:Company)-[:BUYS_FROM]->(supplier_of_supplier:Company)
RETURN DISTINCT supplier_of_supplier
```

**SPARQL:**
```sparql
SELECT DISTINCT ?supplier_of_supplier
WHERE {
  ex:OurCompany ex:buys_from ?supplier .
  ?supplier ex:buys_from ?supplier_of_supplier .
}
```

---

## Variable-Length Paths

### Example 4: Find Nodes Within N Hops

**Natural Language:**
```
Find all people connected to Alice within 2 relationships
```

**Cypher:**
```cypher
MATCH (alice:Person {name: "Alice"})-[*1..2]-(connected:Person)
RETURN DISTINCT connected
```

**SPARQL (using Property Paths):**
```sparql
SELECT DISTINCT ?connected
WHERE {
  ex:Alice (foaf:knows|^foaf:knows)/
           (foaf:knows|^foaf:knows)? ?connected .
}
```

---

### Example 5: Find Any Path

**Natural Language:**
```
Find all people connected to Alice through any relationship chain
```

**Cypher:**
```cypher
MATCH (alice:Person {name: "Alice"})-[*]-(anyone:Person)
RETURN DISTINCT anyone
LIMIT 100
```

**SPARQL:**
```sparql
SELECT DISTINCT ?anyone
WHERE {
  ex:Alice (foaf:knows|foaf:worksWith)* ?anyone .
}
LIMIT 100
```

**Note:** Limit recommended to prevent expensive queries.

---

### Example 6: Find Nodes At Exact Distance

**Natural Language:**
```
Find people exactly 3 relationships away from Alice
```

**Cypher:**
```cypher
MATCH (alice:Person {name: "Alice"})-[*3]-(distant:Person)
RETURN DISTINCT distant
```

**SPARQL:**
```sparql
SELECT DISTINCT ?distant
WHERE {
  ex:Alice (foaf:knows|foaf:worksWith)/(foaf:knows|foaf:worksWith)/(foaf:knows|foaf:worksWith) ?distant .
}
```

---

## Shortest Path Queries

### Example 7: Find Shortest Path Between Two People

**Natural Language:**
```
How are Alice and Bob connected?
```

**Cypher:**
```cypher
MATCH path = shortestPath((alice:Person {name: "Alice"})-[*]-(bob:Person {name: "Bob"}))
RETURN path
```

**Output:**
```
Alice -[KNOWS]-> Charlie -[WORKS_WITH]-> Bob
```

---

### Example 8: Find All Shortest Paths

**Natural Language:**
```
Show all shortest paths between Alice and Bob
```

**Cypher:**
```cypher
MATCH (alice:Person {name: "Alice"}), (bob:Person {name: "Bob"})
MATCH paths = allShortestPaths((alice)-[*]-(bob))
RETURN paths
LIMIT 10
```

---

## Complex Multi-Hop Scenarios

### Example 9: Multi-Level Management Hierarchy

**Natural Language:**
```
Show all employees under Alice's management (direct and indirect)
```

**Cypher:**
```cypher
MATCH (alice:Person {name: "Alice"})-[:MANAGES*]->(subordinate:Person)
RETURN subordinate, 
       length(relationships) as levels_down
```

**SPARQL:**
```sparql
SELECT ?subordinate
WHERE {
  ex:Alice ex:manages+ ?subordinate .
}
```

---

### Example 10: Cross-Company Connections

**Natural Language:**
```
Find employees at Company A who know employees at Company B
```

**Cypher:**
```cypher
MATCH (emp_a:Employee)-[:WORKS_AT]->(comp_a:Company {name: "Company A"})
MATCH (emp_b:Employee)-[:WORKS_AT]->(comp_b:Company {name: "Company B"})
MATCH (emp_a)-[:KNOWS]-(emp_b)
RETURN emp_a, emp_b
```

**SPARQL:**
```sparql
SELECT ?emp_a ?emp_b
WHERE {
  ?emp_a rdf:type ex:Employee .
  ?emp_a ex:works_at ex:CompanyA .
  
  ?emp_b rdf:type ex:Employee .
  ?emp_b ex:works_at ex:CompanyB .
  
  { ?emp_a foaf:knows ?emp_b . }
  UNION
  { ?emp_b foaf:knows ?emp_a . }
}
```

---

## Path Analysis Queries

### Example 11: Count Hops in a Path

**Natural Language:**
```
Show how many steps it takes to get from Alice to Bob
```

**Cypher:**
```cypher
MATCH path = shortestPath((alice:Person {name: "Alice"})-[*]-(bob:Person {name: "Bob"}))
RETURN length(path) as hops
```

---

### Example 12: Show Path Details

**Natural Language:**
```
Find the path from Alice to Bob and show each intermediate person
```

**Cypher:**
```cypher
MATCH path = shortestPath((alice:Person {name: "Alice"})-[*]-(bob:Person {name: "Bob"}))
RETURN [node in nodes(path) | node.name] as path_nodes,
       [rel in relationships(path) | type(rel)] as path_relationships
```

**Output:**
```
path_nodes: ["Alice", "Charlie", "David", "Bob"]
path_relationships: ["KNOWS", "WORKS_WITH", "MANAGES"]
```

---

### Example 13: Find Strongly Connected Communities

**Natural Language:**
```
Find groups of people who all know each other
```

**Cypher:**
```cypher
MATCH (p1:Person)-[:KNOWS]->(p2:Person)-[:KNOWS]->(p3:Person)-[:KNOWS]->(p1)
RETURN p1, p2, p3
```

---

## Aggregation Over Paths

### Example 14: Count Connections Per Person

**Natural Language:**
```
Show each person and how many other people they're connected to within 3 hops
```

**Cypher:**
```cypher
MATCH (p:Person)-[*1..3]-(connected:Person)
RETURN p.name, 
       COUNT(DISTINCT connected) as connection_count
GROUP BY p.name
ORDER BY connection_count DESC
```

---

### Example 15: Find Popular Intermediaries

**Natural Language:**
```
Find people who appear most often as bridges between others
```

**Cypher:**
```cypher
MATCH (p1:Person)-[:KNOWS]-(bridge:Person)-[:KNOWS]-(p2:Person)
WHERE p1 <> p2
RETURN bridge.name, 
       COUNT(DISTINCT p1) + COUNT(DISTINCT p2) as bridge_count
GROUP BY bridge.name
ORDER BY bridge_count DESC
LIMIT 10
```

---

## Performance Tips for Multi-Hop Queries

1. **Limit path length** — Restrict to reasonable depths
   ```cypher
   -- Good: Limited to 3 hops
   MATCH (a)-[*1..3]-(b)
   
   -- Bad: Unbounded path search
   MATCH (a)-[*]-(b)
   ```

2. **Use specific relationship types**
   ```cypher
   -- Better: Specific types
   MATCH (a)-[:KNOWS|:WORKS_WITH]-(b)
   
   -- Slower: Any relationship
   MATCH (a)-[*]-(b)
   ```

3. **Add filters early**
   ```cypher
   -- Better: Filter source node
   MATCH (alice:Person {name: "Alice"})-[*]-(b)
   
   -- Worse: No label on source
   MATCH (n {name: "Alice"})-[*]-(b)
   ```

4. **Use LIMIT to prevent expensive queries**
   ```cypher
   MATCH (a)-[*]-(b)
   RETURN b
   LIMIT 100  -- Always limit for unbounded searches
   ```

---

## Common Multi-Hop Mistakes

### Mistake 1: Duplicate Results

❌ **Wrong:**
```cypher
MATCH (a:Person {name: "Alice"})-[*2]-(c:Person)
RETURN c
-- Returns Alice twice: Alice->B->Alice
```

✅ **Right:**
```cypher
MATCH (a:Person {name: "Alice"})-[*2]-(c:Person)
WHERE a <> c
RETURN DISTINCT c
```

---

### Mistake 2: Unbounded Search on Large Graph

❌ **Wrong:**
```cypher
MATCH (a:Person)-[*]-(b:Person)
RETURN a, b
-- May timeout on large graphs
```

✅ **Right:**
```cypher
MATCH (a:Person)-[*1..5]-(b:Person)
RETURN a, b
LIMIT 1000
```

---

### Mistake 3: Not Excluding Start Node

❌ **Wrong:**
```cypher
MATCH (alice:Person {name: "Alice"})-[*]-(others:Person)
RETURN others
-- May return Alice herself
```

✅ **Right:**
```cypher
MATCH (alice:Person {name: "Alice"})-[*]-(others:Person)
WHERE alice <> others
RETURN others
```

---

## Summary

Multi-hop queries enable:
- ✅ Finding indirect connections
- ✅ Path analysis and shortest paths
- ✅ Community detection
- ✅ Network analysis
- ✅ Hierarchical traversals

For parameterized versions of these queries, see [Parameterized Queries](parameterized-queries.md).

