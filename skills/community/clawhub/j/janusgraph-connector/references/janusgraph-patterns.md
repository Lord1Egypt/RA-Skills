# JanusGraph Design Patterns

This document contains 30+ production-ready design patterns for common JanusGraph operations. Each pattern includes the Gremlin query, description, and use case.

---

## Table of Contents

1. [CRUD Operation Patterns](#crud-operation-patterns)
2. [Query Patterns](#query-patterns)
3. [Relationship Patterns](#relationship-patterns)
4. [Performance Patterns](#performance-patterns)
5. [Transaction Patterns](#transaction-patterns)
6. [Advanced Patterns](#advanced-patterns)
7. [Import/Export Patterns](#importexport-patterns)
8. [Testing & Validation Patterns](#testing--validation-patterns)

---

## CRUD Operation Patterns

### Pattern 1: Create a Simple Vertex

**Description:** Add a new vertex with label and properties

**Gremlin:**
```gremlin
g.addV("Person")
  .property("name", "Alice")
  .property("age", 30)
  .property("email", "alice@example.com")
```

**Use Case:** Creating a new entity (person, product, location, etc.)

**Python:**
```python
connector.create_vertex(
    label="Person",
    properties={
        "name": "Alice",
        "age": 30,
        "email": "alice@example.com"
    }
)
```

### Pattern 2: Create Vertex with ID

**Description:** Add a vertex with explicit ID (for linking with external systems)

**Gremlin:**
```gremlin
g.addV("Product")
  .property("id", "PROD-12345")
  .property("name", "Laptop")
  .property("price", 999.99)
```

**Use Case:** Syncing with external databases, maintaining external IDs

### Pattern 3: Create a Relationship Between Two Vertices

**Description:** Create an edge between two existing vertices

**Gremlin:**
```gremlin
g.V().has("name", "Alice")
  .addE("KNOWS")
  .to(g.V().has("name", "Bob"))
  .property("since", "2020-01-15")
```

**Use Case:** Creating connections, relationships, edges

**Python:**
```python
connector.create_edge(
    from_id=alice_id,
    to_id=bob_id,
    label="KNOWS",
    properties={"since": "2020-01-15"}
)
```

### Pattern 4: Read a Vertex by ID

**Description:** Query vertex by its unique ID

**Gremlin:**
```gremlin
g.V("12345").valueMap()
```

**Use Case:** Direct lookup when ID is known

**Python:**
```python
connector.execute_query("g.V(?).valueMap()", params=[vertex_id])
```

### Pattern 5: Read Vertices by Label

**Description:** Find all vertices of a specific type

**Gremlin:**
```gremlin
g.V().hasLabel("Person").valueMap()
```

**Use Case:** Get all instances of a type

**Python:**
```python
result = connector.execute_query("g.V().hasLabel('Person').valueMap()")
```

### Pattern 6: Update Vertex Properties

**Description:** Modify existing vertex properties

**Gremlin:**
```gremlin
g.V().has("name", "Alice")
  .property("age", 31)
  .property("updated_at", 1681305600)
```

**Use Case:** Updating entity information

**Python:**
```python
connector.execute_query(
    "g.V().has('name', ?).property('age', ?)",
    params=["Alice", 31]
)
```

### Pattern 7: Update Edge Properties

**Description:** Modify edge properties

**Gremlin:**
```gremlin
g.V().has("name", "Alice")
  .outE("KNOWS")
  .to(g.V().has("name", "Bob"))
  .property("weight", 0.95)
```

**Use Case:** Updating relationship metadata

### Pattern 8: Delete a Vertex

**Description:** Remove a vertex from the graph

**Gremlin:**
```gremlin
g.V().has("name", "Alice").drop()
```

**Use Case:** Removing entities

**Python:**
```python
connector.execute_query("g.V().has('name', ?).drop()", params=["Alice"])
```

### Pattern 9: Delete Multiple Vertices

**Description:** Remove vertices matching criteria

**Gremlin:**
```gremlin
g.V().hasLabel("Temporary").drop()
```

**Use Case:** Cleanup, batch deletion

### Pattern 10: Delete an Edge

**Description:** Remove a relationship between vertices

**Gremlin:**
```gremlin
g.V().has("name", "Alice")
  .outE("KNOWS")
  .where(inV().has("name", "Bob"))
  .drop()
```

**Use Case:** Removing relationships

---

## Query Patterns

### Pattern 11: Exact Property Match

**Description:** Find vertices with exact property value

**Gremlin:**
```gremlin
g.V().has("status", "active")
```

**Use Case:** Status filtering, exact searches

**Python:**
```python
connector.execute_query("g.V().has('status', 'active')")
```

### Pattern 12: Range Filter

**Description:** Find vertices within a range

**Gremlin:**
```gremlin
g.V().has("age", gt(25)).has("age", lt(65))
```

**Use Case:** Age ranges, price ranges, date ranges

**Operators:** `gt()`, `gte()`, `lt()`, `lte()`, `neq()`

### Pattern 13: Text Search Patterns

**Description:** Find vertices by text patterns

**Gremlin:**
```gremlin
g.V().has("email", endingWith("@example.com"))
g.V().has("name", startingWith("Al"))
g.V().has("description", containing("important"))
```

**Use Case:** Email domain filtering, name prefixes, keyword search

### Pattern 14: List/Set Membership

**Description:** Check if property is in a list

**Gremlin:**
```gremlin
g.V().has("status", within("active", "pending", "review"))
```

**Use Case:** Multiple status values, category filtering

### Pattern 15: NOT Patterns

**Description:** Exclude vertices matching criteria

**Gremlin:**
```gremlin
g.V().has("status", without("deleted", "archived"))
g.V().hasNot("phone")  // Missing property
g.V().where(neq(g.V().has("special")))  // Complex negation
```

**Use Case:** Excluding data, finding incomplete records

### Pattern 16: Single-Hop Traversal

**Description:** Get immediate neighbors

**Gremlin:**
```gremlin
g.V().has("name", "Alice").out("KNOWS")  // Outgoing
g.V().has("name", "Alice").in("FOLLOWS")  // Incoming
g.V().has("name", "Alice").both("KNOWS")  // Both directions
```

**Use Case:** Finding direct relationships

**Python:**
```python
result = connector.execute_query("g.V().has('name', 'Alice').out('KNOWS')")
```

### Pattern 17: Variable-Length Traversal

**Description:** Traverse multiple hops

**Gremlin:**
```gremlin
g.V().has("name", "Alice").repeat(out("KNOWS")).times(3)
```

**Use Case:** Network depth, multi-level relationships

### Pattern 18: Path Finding

**Description:** Find path between two vertices

**Gremlin:**
```gremlin
g.V().has("name", "Alice")
  .repeat(out("KNOWS"))
  .until(has("name", "Bob"))
  .path()
  .limit(1)
```

**Use Case:** Shortest path, navigation

### Pattern 19: Aggregation - Count

**Description:** Count vertices

**Gremlin:**
```gremlin
g.V().count()  // Total vertices
g.V().hasLabel("Person").count()  // Count by label
g.V().has("status", "active").count()  // Conditional count
```

**Use Case:** Statistics, validation

**Python:**
```python
result = connector.execute_query("g.V().hasLabel('Person').count()")
count = result.records[0] if result.records else 0
```

### Pattern 20: Group By

**Description:** Group and aggregate

**Gremlin:**
```gremlin
g.V().group().by("status")  // Group by property
g.V().group().by("label")  // Group by vertex label
g.V().groupCount().by("age")  // Count per group
```

**Use Case:** Category analysis, statistics

### Pattern 21: Statistics - Mean/Min/Max

**Description:** Calculate aggregate functions

**Gremlin:**
```gremlin
g.V().values("age").mean()
g.V().values("salary").max()
g.V().values("price").min()
```

**Use Case:** Analytics, reporting

### Pattern 22: Deduplication

**Description:** Remove duplicate results

**Gremlin:**
```gremlin
g.V().values("department").dedup()  // Unique departments
g.V().both().dedup()  // Unique neighbors
```

**Use Case:** Removing duplicates, unique values

### Pattern 23: Sorting

**Description:** Order results

**Gremlin:**
```gremlin
g.V().order().by("name")  // Ascending
g.V().order().by("age", desc)  // Descending
g.V().order().by(shuffled())  // Random
```

**Use Case:** Ranking, ordering results

### Pattern 24: Limit and Pagination

**Description:** Limit result set

**Gremlin:**
```gremlin
g.V().limit(10)  // First 10
g.V().skip(20).limit(10)  // Page 3 (assuming 10 per page)
g.V().tail(5)  // Last 5
```

**Use Case:** Pagination, sampling

---

## Relationship Patterns

### Pattern 25: One-to-Many Relationship

**Description:** One vertex connected to many others

**Gremlin:**
```gremlin
// Create
g.V().has("Department", "name", "Engineering")
  .addE("CONTAINS")
  .to(g.V().hasLabel("Employee"))

// Query
g.V().has("Department", "name", "Engineering")
  .out("CONTAINS")
  .values("name")
```

**Use Case:** Department-Employee, Category-Product

### Pattern 26: Many-to-Many Relationship

**Description:** Many vertices connected to many others

**Gremlin:**
```gremlin
// Students and Courses
g.V().has("Student", "name", "Alice")
  .addE("ENROLLED_IN")
  .to(g.V().has("Course", "code", "CS101"))

g.V().has("Course", "code", "CS101")
  .in("ENROLLED_IN")
  .values("name")
```

**Use Case:** Student-Course, Author-Paper, Product-Tag

### Pattern 27: Self-Referential Relationship

**Description:** Vertex related to others of same type

**Gremlin:**
```gremlin
// Employees managing other employees
g.V().has("name", "Bob").addE("MANAGES").to(g.V().has("name", "Alice"))

g.V().has("name", "Bob").out("MANAGES")  // Bob's direct reports
g.V().has("name", "Alice").in("MANAGES")  // Alice's manager
```

**Use Case:** Management hierarchy, follow relationships

### Pattern 28: Hierarchical Structure

**Description:** Tree-like relationships (parent-child)

**Gremlin:**
```gremlin
// Create hierarchy
g.V().has("Category", "name", "Electronics")
  .addE("PARENT_OF")
  .to(g.V().has("Category", "name", "Computers"))

// Find all parents
g.V().has("Category", "name", "Laptop")
  .repeat(out("PARENT_OF"))
  .until(not(out("PARENT_OF")))
  .values("name")

// Find all children
g.V().has("Category", "name", "Electronics")
  .repeat(in("PARENT_OF"))
  .until(not(in("PARENT_OF")))
  .values("name")
```

**Use Case:** Category hierarchies, org structure, file systems

### Pattern 29: Weighted Relationships

**Description:** Edges with strength/weight properties

**Gremlin:**
```gremlin
g.V().has("name", "Alice")
  .outE("KNOWS")
  .filter(has("confidence", gt(0.8)))
  .inV()
  .values("name")
```

**Use Case:** Trust networks, confidence scores, edge ranking

---

## Performance Patterns

### Pattern 30: Creating Indexes - Composite Index

**Description:** Fast exact-match lookups

**Gremlin:**
```gremlin
mgmt = graph.openManagement()
name = mgmt.getPropertyKey("name")
mgmt.buildIndex("PersonByName", Vertex.class)
  .addKey(name)
  .buildCompositeIndex()
mgmt.commit()
```

**Use Case:** Speed up has() filters on frequently searched properties

**Python:**
```python
connector.create_index(
    name="PersonByName",
    properties=["name"],
    index_type="composite"
)
```

### Pattern 31: Creating Indexes - Mixed Index

**Description:** Full-text search and range queries

**Gremlin:**
```gremlin
mgmt = graph.openManagement()
name = mgmt.getPropertyKey("name")
description = mgmt.getPropertyKey("description")
mgmt.buildIndex("PersonSearch", Vertex.class)
  .addKey(name, Mapping.TEXT.asParameter())
  .addKey(description, Mapping.TEXT.asParameter())
  .buildMixedIndex("search")
mgmt.commit()
```

**Use Case:** Text search on description fields

### Pattern 32: Batch Insert

**Description:** Efficient bulk data loading

**Gremlin:**
```gremlin
graph.tx().open()
for i in range(1000):
    g.addV("Person")
      .property("id", i)
      .property("name", f"Person{i}")
      .next()
graph.tx().commit()
```

**Use Case:** Initial data loading, data migration

**Python:**
```python
connector.batch_create_vertices([
    {"label": "Person", "properties": {"id": i, "name": f"Person{i}"}}
    for i in range(1000)
])
```

### Pattern 33: Query Optimization - Filter Early

**Description:** Apply filters at beginning of traversal

**Gremlin:**
```gremlin
// BAD: Traverses all, then filters
g.V().out("KNOWS").filter(has("age", gt(25)))

// GOOD: Filter before traversal
g.V().has("age", gt(25)).out("KNOWS")
```

**Use Case:** Performance optimization

### Pattern 34: Limit Results

**Description:** Prevent unbounded results

**Gremlin:**
```gremlin
g.V().repeat(out()).times(10).limit(100)
```

**Use Case:** Preventing memory overflow on large traversals

---

## Transaction Patterns

### Pattern 35: Simple Transaction

**Description:** Basic transaction with rollback

**Python:**
```python
try:
    connector.begin_transaction()
    
    connector.execute_query("g.addV('Person').property('name', 'Alice')")
    connector.execute_query("g.addV('Person').property('name', 'Bob')")
    
    connector.commit_transaction()
except Exception as e:
    connector.rollback_transaction()
    print(f"Error: {e}")
```

**Use Case:** Ensuring atomicity of operations

### Pattern 36: Transaction with Error Handling

**Description:** Complex transaction with validation

**Python:**
```python
max_retries = 3
retry_count = 0

while retry_count < max_retries:
    try:
        connector.begin_transaction()
        
        # Complex operations
        result1 = connector.execute_query("g.V().has('status', 'pending').limit(10)")
        
        if not result1.success:
            raise Exception("Query failed")
        
        # Update based on result
        connector.execute_query("g.V().has('status', 'pending').property('status', 'processing')")
        
        connector.commit_transaction()
        break
        
    except Exception as e:
        connector.rollback_transaction()
        retry_count += 1
        if retry_count >= max_retries:
            raise
```

**Use Case:** Handling conflicts and retries

---

## Advanced Patterns

### Pattern 37: Conditional Creation (FOREACH)

**Description:** Create vertices conditionally

**Gremlin:**
```gremlin
g.V().has("status", "active")
  .sideEffect { v ->
    if (v.property("verified").isPresent()) {
      // Vertex already verified
    } else {
      // Create verification vertex
      graph.addVertex("VertexLabel:Verification")
    }
  }
```

**Use Case:** Conditional graph updates

### Pattern 38: Recursive Traversal - Depth-First

**Description:** Deep graph traversal

**Gremlin:**
```gremlin
g.V().has("type", "root")
  .repeat(out("CHILD"))
  .until(not(out("CHILD")))
  .path()
```

**Use Case:** Tree traversal, category hierarchies

### Pattern 39: List Comprehension

**Description:** Collect properties into lists

**Gremlin:**
```gremlin
g.V().has("Department")
  .out("HAS_EMPLOYEE")
  .group()
  .by(select("department"))
  .by(select("name").fold())
```

**Use Case:** Grouping and aggregation

### Pattern 40: Graph Projection

**Description:** Create subgraph view

**Gremlin:**
```gremlin
g.V().has("importance", gt(0.7))
  .both("RELATED_TO")
  .has("importance", gt(0.7))
```

**Use Case:** Focusing on high-value nodes

### Pattern 41: Data Validation

**Description:** Query to validate data

**Gremlin:**
```gremlin
g.V().where(not(out("HAS_OWNER"))).values("id")
```

**Use Case:** Finding orphaned data

### Pattern 42: Recommendation Engine

**Description:** Collaborative filtering

**Gremlin:**
```gremlin
g.V().has("User", "id", "user123")
  .out("LIKES")
  .in("LIKES")
  .where(neq(g.V().has("id", "user123")))
  .out("LIKES")
  .dedup()
  .values("id")
```

**Use Case:** Product recommendations

---

## Import/Export Patterns

### Pattern 43: Load from CSV (Using APOC)

**Description:** Bulk import from CSV

**Gremlin:**
```gremlin
graph.io(graphson()).readGraph("data.graphson")
```

**Use Case:** Data migration, initialization

**Python:**
```python
import csv

vertices = []
with open('users.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        vertices.append({
            'label': 'Person',
            'properties': {'name': row['name'], 'email': row['email']}
        })

connector.batch_create_vertices(vertices)
```

### Pattern 44: Export to GraphSON

**Description:** Export graph structure

**Gremlin:**
```gremlin
graph.io(graphson()).writeGraph("export.graphson")
```

**Use Case:** Backup, sharing graph structure

---

## Testing & Validation Patterns

### Pattern 45: Count Verification

**Description:** Verify data correctness

**Gremlin:**
```gremlin
// Should have equal counts
g.V().hasLabel("Person").count()
g.V().in("HAS_EMPLOYEE").count()
```

**Use Case:** Data integrity checks

**Python:**
```python
def verify_referential_integrity():
    employees = connector.execute_query("g.V().hasLabel('Employee').count()").records[0]
    managed_by = connector.execute_query("g.V().in('MANAGES').count()").records[0]
    return employees == managed_by
```

### Pattern 46: Find Orphaned Data

**Description:** Locate invalid references

**Gremlin:**
```gremlin
g.V().where(not(out("REFERENCES")))  // Vertices with no outgoing refs
```

**Use Case:** Data cleanup

### Pattern 47: Statistics Query

**Description:** Get overall graph stats

**Gremlin:**
```gremlin
// Vertex count by label
g.V().groupCount().by(label())

// Edge count by label
g.E().groupCount().by(label())

// Property cardinality
g.V().values("name").dedup().count()
```

**Use Case:** Monitoring, reporting

---

## Summary

**30+ Patterns Covered:**
- ✅ 10 CRUD operations
- ✅ 14 Query patterns
- ✅ 5 Relationship patterns
- ✅ 5 Performance patterns
- ✅ 2 Transaction patterns
- ✅ 6 Advanced patterns
- ✅ 2 Import/Export patterns
- ✅ 3 Testing patterns

Each pattern includes:
- Clear description
- Gremlin query
- Use case
- Python implementation (where applicable)

---

**Last Updated:** April 12, 2026  
**JanusGraph Version:** 0.6.0+  
**Gremlin Version:** 3.6.0+

