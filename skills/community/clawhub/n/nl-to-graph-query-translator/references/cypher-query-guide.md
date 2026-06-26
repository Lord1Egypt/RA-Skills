# Cypher Query Guide

## Overview

Cypher is a declarative query language designed for Neo4j and other property graph databases. It uses ASCII-art syntax to represent graph patterns, making queries intuitive and readable.

## Basic Syntax

### Pattern Matching

Nodes are represented with parentheses:
```cypher
(n)          -- any node
(n:Person)   -- node with label Person
(n:Person {name: "Alice"})  -- node with label and properties
```

Relationships are represented with brackets:
```cypher
(a)--(b)           -- undirected relationship
(a)-->(b)          -- directed relationship
(a)-[:KNOWS]->(b)  -- directed relationship with type
(a)-[r:KNOWS]->(b) -- store relationship in variable r
```

### Basic Queries

#### Find a Node
```cypher
MATCH (p:Person {name: "Alice"})
RETURN p
```

#### Find Relationships
```cypher
MATCH (p:Person {name: "Alice"})-[:WORKS_AT]->(company:Company)
RETURN p, company
```

#### Multi-Step Traversal
```cypher
MATCH (p:Person)-[:WORKS_AT]->(company:Company)-[:LOCATED_IN]->(city:City)
RETURN p, company, city
```

#### Variable-Length Paths
```cypher
-- Find paths up to 3 hops away
MATCH (alice:Person {name: "Alice"})-[*1..3]-(connected)
RETURN connected

-- Find any path length
MATCH (alice:Person {name: "Alice"})-[*]-(connected)
RETURN connected
```

## Common Clauses

### MATCH
Specifies the pattern to search for:
```cypher
MATCH (n:Person)
```

### WHERE
Filters results:
```cypher
MATCH (n:Person)
WHERE n.age > 30
RETURN n
```

### RETURN
Specifies what to return:
```cypher
MATCH (n:Person)
RETURN n, n.name, n.age
```

### ORDER BY
Sorts results:
```cypher
MATCH (n:Person)
RETURN n
ORDER BY n.name ASC
```

### LIMIT
Limits result count:
```cypher
MATCH (n:Person)
RETURN n
LIMIT 10
```

### SKIP
Skips results:
```cypher
MATCH (n:Person)
RETURN n
SKIP 5
LIMIT 10
```

## Aggregation Functions

### COUNT
```cypher
MATCH (p:Person)-[:WORKS_AT]->(company:Company)
RETURN company.name, COUNT(p) as employee_count
```

### COLLECT
```cypher
MATCH (p:Person)-[:WORKS_AT]->(company:Company)
RETURN company.name, COLLECT(p.name) as employees
```

### SUM, AVG, MIN, MAX
```cypher
MATCH (p:Person)
RETURN AVG(p.salary), MAX(p.salary), MIN(p.salary)
```

## Creating and Updating Data

### CREATE
```cypher
CREATE (p:Person {name: "Bob", age: 30})
```

### CREATE with Relationships
```cypher
CREATE (p:Person {name: "Bob"})-[:WORKS_AT]->(c:Company {name: "Tech Corp"})
```

### MERGE
Creates or updates (idempotent):
```cypher
MERGE (p:Person {name: "Alice"})
ON CREATE SET p.created = datetime()
ON MATCH SET p.updated = datetime()
```

### SET
Updates properties:
```cypher
MATCH (p:Person {name: "Alice"})
SET p.age = 35
```

### DELETE
```cypher
MATCH (p:Person {name: "Alice"})-[r:KNOWS]-(friend)
DELETE r
```

## Advanced Patterns

### Optional Relationships
```cypher
MATCH (p:Person)
OPTIONAL MATCH (p)-[:KNOWS]->(friend:Person)
RETURN p.name, friend.name
```

### Conditional Returns
```cypher
MATCH (p:Person)
RETURN p.name, 
       CASE 
         WHEN p.age > 30 THEN "Senior"
         WHEN p.age > 20 THEN "Mid"
         ELSE "Junior"
       END as category
```

### WITH Clause (Sub-queries)
```cypher
MATCH (p:Person)-[:WORKS_AT]->(company:Company)
WITH company, COUNT(p) as count
WHERE count > 10
RETURN company.name, count
```

## Performance Tips

1. **Use labels**: Always specify node labels when possible
   ```cypher
   -- Fast
   MATCH (p:Person {name: "Alice"})
   
   -- Slow
   MATCH (p {name: "Alice"})
   ```

2. **Index on frequently searched properties**:
   ```cypher
   CREATE INDEX ON :Person(name)
   ```

3. **Limit result sets**:
   ```cypher
   MATCH (p:Person)
   RETURN p
   LIMIT 50
   ```

4. **Use OPTIONAL MATCH instead of LEFT JOIN patterns**:
   ```cypher
   MATCH (p:Person)
   OPTIONAL MATCH (p)-[:KNOWS]->(friend)
   RETURN p, friend
   ```

5. **Profile queries**:
   ```cypher
   PROFILE MATCH (p:Person)-[:WORKS_AT]->(c:Company)
   RETURN p, c
   ```

## Best Practices

✓ Use consistent casing for labels and relationship types (SCREAMING_SNAKE_CASE)  
✓ Always specify direction when relationships have semantic meaning  
✓ Use parameters for dynamic values  
✓ Test queries on sample data first  
✓ Monitor query performance with PROFILE  
✓ Keep path lengths reasonable (usually < 3 hops)  

## Common Mistakes

✗ Forgetting relationship direction  
✗ Mixing relationship types in complex patterns  
✗ Using variables you don't return  
✗ Not filtering early enough in the MATCH clause  

## See Also

- [Neo4j Documentation](https://neo4j.com/docs/cypher-manual/)
- [Cypher Refcard](https://neo4j.com/docs/cypher-refcard/current/)

