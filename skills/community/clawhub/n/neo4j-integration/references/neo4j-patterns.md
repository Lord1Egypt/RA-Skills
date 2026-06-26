# Neo4j Integration - Design Patterns

Comprehensive patterns for Neo4j Cypher queries, database operations, and optimization strategies.

---

## 1. Basic CRUD Operations

### 1.1 CREATE - Add Nodes

**Pattern:** Create single node with labels and properties.

```cypher
CREATE (p:Person {id: 1, name: "Alice", age: 30})
RETURN p
```

**Pattern:** Create multiple nodes in one query.

```cypher
CREATE (a:Person {name: "Alice"}), (b:Person {name: "Bob"})
RETURN a, b
```

**Best Practice:**
- Use unique identifiers for nodes
- Set all required properties at creation
- Use meaningful labels

---

### 1.2 CREATE Relationships

**Pattern:** Connect two existing nodes with relationship.

```cypher
MATCH (a:Person {name: "Alice"}), (b:Person {name: "Bob"})
CREATE (a)-[:KNOWS {since: 2020}]->(b)
RETURN a, b
```

**Pattern:** Create relationship with properties.

```cypher
MATCH (emp:Employee {id: 1}), (dept:Department {id: 101})
CREATE (emp)-[:WORKS_IN {since: 2015}]->(dept)
RETURN emp, dept
```

---

### 1.3 READ - MATCH Patterns

**Pattern:** Simple node matching by property.

```cypher
MATCH (p:Person {name: "Alice"})
RETURN p
```

**Pattern:** Match with WHERE clause for complex conditions.

```cypher
MATCH (p:Person)
WHERE p.age > 30 AND p.active = true
RETURN p.name, p.age
```

**Pattern:** Match relationships and traverse.

```cypher
MATCH (a:Person)-[:KNOWS]->(b:Person)
RETURN a.name AS person1, b.name AS person2
```

---

### 1.4 UPDATE - SET Properties

**Pattern:** Update single property.

```cypher
MATCH (p:Person {name: "Alice"})
SET p.age = 31
RETURN p
```

**Pattern:** Update multiple properties.

```cypher
MATCH (p:Person {name: "Alice"})
SET p.age = 31, p.city = "New York"
RETURN p
```

**Pattern:** Increment numeric property.

```cypher
MATCH (p:Person {name: "Alice"})
SET p.age = p.age + 1
RETURN p.age
```

---

### 1.5 DELETE - Remove Data

**Pattern:** Delete nodes (must remove relationships first).

```cypher
MATCH (p:Person {name: "Alice"})
DETACH DELETE p
```

**Pattern:** Delete specific relationships.

```cypher
MATCH (a:Person)-[r:KNOWS]->(b:Person)
WHERE a.name = "Alice" AND b.name = "Bob"
DELETE r
```

---

### 1.6 MERGE - Create or Update

**Pattern:** Merge ensures single occurrence.

```cypher
MERGE (p:Person {name: "Alice"})
ON CREATE SET p.created = timestamp()
ON MATCH SET p.last_seen = timestamp()
RETURN p
```

**Pattern:** Merge with relationship creation.

```cypher
MERGE (a:Person {name: "Alice"})
MERGE (b:Person {name: "Bob"})
MERGE (a)-[:KNOWS]->(b)
```

---

## 2. Query Patterns

### 2.1 Filtering Patterns

**Pattern:** Exact match.

```cypher
MATCH (p:Person {name: "Alice"})
RETURN p
```

**Pattern:** Range query (greater than, less than).

```cypher
MATCH (p:Person)
WHERE p.age > 30 AND p.age < 50
RETURN p.name, p.age
```

**Pattern:** List membership.

```cypher
MATCH (p:Person)
WHERE p.status IN ["active", "pending"]
RETURN p.name, p.status
```

**Pattern:** String pattern matching.

```cypher
MATCH (p:Person)
WHERE p.name STARTS WITH "A" OR p.name CONTAINS "ice"
RETURN p.name
```

**Pattern:** Null checking.

```cypher
MATCH (p:Person)
WHERE p.email IS NULL
RETURN p.name
```

---

### 2.2 Relationship Traversal Patterns

**Pattern:** Single hop relationship.

```cypher
MATCH (a:Person)-[:KNOWS]->(b:Person)
RETURN a.name, b.name
```

**Pattern:** Variable-length relationship (path).

```cypher
MATCH (a:Person)-[:KNOWS*1..3]->(b:Person)
WHERE a.name = "Alice"
RETURN DISTINCT b.name
```

**Pattern:** Find all paths between two nodes.

```cypher
MATCH path = (a:Person {name: "Alice"})-[:KNOWS*]-(b:Person {name: "Bob"})
RETURN path, LENGTH(path) AS hops
```

**Pattern:** Bidirectional relationship.

```cypher
MATCH (a:Person)-[:KNOWS]-(b:Person)
WHERE a.name = "Alice"
RETURN b.name
```

---

### 2.3 Aggregation Patterns

**Pattern:** Count nodes.

```cypher
MATCH (p:Person)
RETURN COUNT(p) AS total_people
```

**Pattern:** Count distinct values.

```cypher
MATCH (p:Person)
RETURN COUNT(DISTINCT p.city) AS unique_cities
```

**Pattern:** Aggregate with GROUP BY.

```cypher
MATCH (emp:Employee)-[:WORKS_IN]->(dept:Department)
RETURN dept.name, COUNT(emp) AS employee_count
GROUP BY dept.name
```

**Pattern:** Math aggregations.

```cypher
MATCH (p:Person)
RETURN AVG(p.age) AS avg_age, MIN(p.age) AS min_age, MAX(p.age) AS max_age
```

---

### 2.4 Sorting and Limiting

**Pattern:** Order and limit.

```cypher
MATCH (p:Person)
RETURN p
ORDER BY p.age DESC
LIMIT 10
```

**Pattern:** Skip for pagination.

```cypher
MATCH (p:Person)
RETURN p
ORDER BY p.name
SKIP 20
LIMIT 10
```

---

### 2.5 Collection Patterns

**Pattern:** Collect into list.

```cypher
MATCH (dept:Department)<-[:WORKS_IN]-(emp:Employee)
RETURN dept.name, COLLECT(emp.name) AS employees
```

**Pattern:** Filter collection.

```cypher
MATCH (p:Person)
RETURN p.name, [friend IN p.friends WHERE friend.active] AS active_friends
```

**Pattern:** Flatten nested lists.

```cypher
MATCH (dept:Department)<-[:WORKS_IN]-(emp:Employee)-[:MANAGES]->(sub:Employee)
RETURN dept.name, COLLECT(DISTINCT sub.name) AS managed_employees
```

---

## 3. Relationship Patterns

### 3.1 One-to-Many

**Pattern:** Node with many relationships.

```cypher
MATCH (author:Author)-[:WROTE]->(books:Book)
RETURN author.name, COUNT(books) AS book_count
```

---

### 3.2 Many-to-Many

**Pattern:** Through relationship type.

```cypher
MATCH (author:Author)-[:WROTE]->(book:Book)<-[:LIKES]-(user:User)
RETURN author.name, user.name
```

---

### 3.3 Self-Referential

**Pattern:** Node related to same type.

```cypher
MATCH (emp:Employee)-[:REPORTS_TO]->(manager:Employee)
RETURN emp.name, manager.name
```

---

### 3.4 Hierarchical

**Pattern:** Tree-like structure.

```cypher
MATCH (root:Category)
WHERE NOT (root)<-[:PARENT_OF]-()
MATCH (root)-[:PARENT_OF*]->(child:Category)
RETURN root.name, collect(DISTINCT child.name)
```

---

## 4. Performance Patterns

### 4.1 Index Creation

**Pattern:** Create index on label and property.

```cypher
CREATE INDEX idx_person_name FOR (p:Person) ON (p.name)
```

**Pattern:** Create composite index.

```cypher
CREATE INDEX idx_person_age_city FOR (p:Person) ON (p.age, p.city)
```

**Pattern:** Create unique index (constraint).

```cypher
CREATE CONSTRAINT person_id FOR (p:Person) REQUIRE p.id IS UNIQUE
```

---

### 4.2 Query Optimization

**Pattern:** Use indexes in WHERE clause.

```cypher
MATCH (p:Person)
WHERE p.name = "Alice"  // Indexed, fast!
RETURN p
```

**Pattern:** Avoid cartesian products (use small set first).

```cypher
MATCH (small_set:SpecificLabel {id: 123})
MATCH (small_set)-[:RELATIONSHIP]->(large_set:CommonLabel)
RETURN large_set
```

**Pattern:** Push filters down.

```cypher
// Good: Filter early
MATCH (p:Person {status: "active"})
MATCH (p)-[:KNOWS]->(friends:Person)
RETURN friends

// Bad: Filter late
MATCH (p:Person)
MATCH (p)-[:KNOWS]->(friends:Person)
WHERE p.status = "active"
RETURN friends
```

---

### 4.3 Batching Patterns

**Pattern:** Create multiple nodes efficiently.

```cypher
UNWIND $nodes AS node
CREATE (n:Person {id: node.id, name: node.name})
```

**Pattern:** Batch update.

```cypher
UNWIND $updates AS update
MATCH (p:Person {id: update.id})
SET p.status = update.status
```

---

### 4.4 Caching Patterns

**Pattern:** Store computed results.

```cypher
MATCH (p:Person)
WITH p, COUNT(*) AS friend_count
SET p.cached_friend_count = friend_count
```

---

## 5. Transaction Patterns

### 5.1 Simple Transaction

```cypher
BEGIN
CREATE (p:Person {name: "Alice"})
CREATE (c:Company {name: "TechCorp"})
CREATE (p)-[:WORKS_AT]->(c)
COMMIT
```

---

### 5.2 Transaction with Error Handling

```cypher
BEGIN
CREATE (p:Person {id: 1, name: "Alice"})
CREATE (p2:Person {id: 1, name: "Bob"})  // Duplicate ID - will fail
ROLLBACK
```

---

## 6. Advanced Patterns

### 6.1 Conditional Creation (FOREACH)

```cypher
MATCH (emp:Employee)
FOREACH (bonusYear IN [2020, 2021, 2022] |
  CREATE (bonus:Bonus {year: bonusYear, amount: 5000})
  CREATE (emp)-[:RECEIVED]->(bonus)
)
```

---

### 6.2 Recursive Descent

```cypher
MATCH (root:Category)
MATCH (root)-[:PARENT_OF*0..]->(allCategories:Category)
RETURN root.name, allCategories.name
```

---

### 6.3 List Comprehension

```cypher
MATCH (author:Author)-[:WROTE]->(book:Book)
RETURN author.name, [book IN book WHERE book.rating > 4 | book.title]
```

---

### 6.4 Graph Projection

```cypher
MATCH (n)
WHERE NOT (n)-[:TEMPORARY]->()
RETURN {
  id: id(n),
  labels: labels(n),
  properties: properties(n)
} AS node_projection
```

---

## 7. Data Validation Patterns

### 7.1 Check Data Integrity

```cypher
MATCH (p:Person)
WHERE NOT exists(p.email)
RETURN p.name, "Missing email" AS issue
```

---

### 7.2 Detect Duplicates

```cypher
MATCH (p1:Person), (p2:Person)
WHERE p1.id = p2.id AND id(p1) < id(p2)
RETURN p1.name, p2.name, "Duplicate ID" AS issue
```

---

### 7.3 Orphaned Data

```cypher
MATCH (p:Person)
WHERE NOT (p)-[:WORKS_AT]->()
RETURN p.name, "No employment" AS issue
```

---

## 8. Visualization Patterns

### 8.1 Relationship Counts

```cypher
MATCH (a:Person)-[r]->(b:Person)
RETURN type(r) AS relationship_type, COUNT(r) AS count
ORDER BY count DESC
```

---

### 8.2 Network Density

```cypher
MATCH (p:Person)
WITH COUNT(p) AS total_people
MATCH (a:Person)-[:KNOWS]->(b:Person)
WITH total_people, COUNT(*) AS relationships
RETURN relationships / (total_people * (total_people - 1)) AS density
```

---

## 9. Import/Export Patterns

### 9.1 LOAD CSV

```cypher
LOAD CSV WITH HEADERS FROM "file:///data.csv" AS row
CREATE (p:Person {
  name: row.name,
  age: toInteger(row.age),
  email: row.email
})
```

---

### 9.2 APOC Export

```cypher
CALL apoc.export.json.all("export.json", {})
```

---

## 10. Testing & Validation Patterns

### 10.1 Data Validation Query

```cypher
MATCH (p:Person)
WITH p, [
  NOT exists(p.name),
  NOT exists(p.email),
  p.age < 0
] AS issues
WHERE true IN issues
RETURN p.id, issues
```

---

### 10.2 Count Verification

```cypher
MATCH (p:Person)
RETURN COUNT(p) AS person_count
UNION
MATCH (c:Company)
RETURN COUNT(c) AS company_count
```

---


