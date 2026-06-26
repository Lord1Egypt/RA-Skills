---
name: neo4j_integration
title: Neo4j Integration
description: Connect to Neo4j graph databases and execute Cypher queries for storing, querying, and managing knowledge graph data using the property graph model. Full support for transactions, indexes, bulk operations, and result mapping.
category: integrations
tags:
  - knowledge-graph
  - neo4j
  - graph-database
  - cypher
  - integration
  - graph-query
  - database-driver
  - property-graph
  - transactions
  - indexes
  - bulk-import
  - query-optimization
version: 1.0.0
author: community
license: MIT
metadata:
  {"openclaw":{"emoji":"🔗","homepage":"https://clawhub.com"}}
---

# Neo4j Integration

**Connect to Neo4j graph databases and execute Cypher queries for efficient knowledge graph management.**

This skill enables seamless interaction with **Neo4j graph databases** using the official Python driver. It provides connection management, query execution, transaction support, and result mapping for the property graph model.

## Quick Start

### Use When
- Working with Neo4j-backed knowledge graphs
- Executing Cypher queries on graph data
- Creating or updating nodes and relationships
- Importing graph data into Neo4j
- Querying graph structures with complex patterns
- Managing graph database transactions
- Creating indexes for performance optimization
- Building production graph applications

### Inputs
- Neo4j connection credentials (URI, username, password)
- Cypher queries with optional parameters
- Node/relationship definitions
- Bulk data for import
- Transaction context

### Outputs
- Query results (nodes, relationships, properties)
- Execution statistics and metrics
- Success/failure status
- Record counts and performance data

## Connection & Authentication

### Supported Protocols

```
bolt://        - Unencrypted connection
neo4j://       - Standard connection (recommended)
neo4j+s://     - TLS-encrypted connection
neo4j+ssc://   - Self-signed certificate
```

### Connection Configuration

```python
config = {
    "uri": "neo4j://localhost:7687",
    "username": "neo4j",
    "password": "secure_password",
    "encrypted": True,
    "trust": "TRUST_ALL_CERTIFICATES"
}
```

### Connection Pool

- Default pool size: 50 connections
- Configurable connection limits
- Automatic connection recycling
- Health checks for stale connections

## Property Graph Model

Neo4j uses a **property graph model** with three core elements:

### 1. Nodes
Represent entities with labels and properties.

```cypher
CREATE (p:Person {name: "Alice", age: 30, email: "alice@example.com"})
CREATE (c:Company {name: "TechCorp", industry: "Technology"})
```

Properties:
- Name: String identifier
- Properties: Key-value pairs
- Labels: Type classification (Person, Company, etc.)

### 2. Relationships
Connect nodes with typed, directed edges and properties.

```cypher
CREATE (a:Person)-[:WORKS_AT {since: 2020}]->(c:Company)
CREATE (a:Person)-[:KNOWS {strength: 0.8}]->(b:Person)
```

Characteristics:
- Direction: Start node → End node
- Type: Uppercase name (WORKS_AT, KNOWS, etc.)
- Properties: Optional metadata
- Can be traversed in both directions with `<-`

### 3. Properties
Attributes on nodes and relationships.

```
String: "text value"
Integer: 42
Float: 3.14
Boolean: true/false
DateTime: timestamp
List: [1, 2, 3]
```

## Core Cypher Query Patterns

### MATCH - Find Data
```cypher
MATCH (p:Person) WHERE p.age > 30 RETURN p.name, p.age
```

### CREATE - Add Data
```cypher
CREATE (p:Person {name: "Bob", age: 25}) RETURN p
```

### MERGE - Create or Update
```cypher
MERGE (p:Person {name: "Alice"}) SET p.age = 31 RETURN p
```

### MATCH + CREATE - Add Relationships
```cypher
MATCH (a:Person {name: "Alice"}), (b:Person {name: "Bob"})
CREATE (a)-[:KNOWS]->(b) RETURN a, b
```

### DELETE - Remove Data
```cypher
MATCH (p:Person {name: "Old Person"}) DELETE p
```

### RETURN + ORDER BY + LIMIT
```cypher
MATCH (p:Person) RETURN p ORDER BY p.age DESC LIMIT 10
```

## Advanced Query Features

### Aggregations
```cypher
MATCH (p:Person) RETURN COUNT(p), AVG(p.age), MAX(p.age)
```

### Collection Functions
```cypher
MATCH (p:Person)-[:KNOWS]->(friends:Person)
RETURN p.name, COLLECT(friends.name) AS friend_list
```

### Conditional Logic
```cypher
MATCH (p:Person) 
RETURN p.name, CASE WHEN p.age > 30 THEN "Senior" ELSE "Junior" END AS level
```

### Path Queries
```cypher
MATCH path = (a:Person)-[:KNOWS*1..3]->(b:Person)
WHERE a.name = "Alice" AND b.name = "Bob"
RETURN path, LENGTH(path) AS hops
```

### Graph Algorithms
```cypher
MATCH (n:Person) WHERE exists(n.pagerank) RETURN n ORDER BY n.pagerank DESC
```

## Transaction Management

### Simple Transaction
```cypher
BEGIN
CREATE (p:Person {name: "Alice"})
CREATE (c:Company {name: "TechCorp"})
COMMIT
```

### Rollback on Error
```cypher
BEGIN
CREATE (p:Person {name: "Alice"})
ROLLBACK
```

### Properties
- Atomicity: All-or-nothing execution
- Consistency: Graph constraints maintained
- Isolation: ACID compliance
- Durability: Persistent storage

## Indexes & Performance

### Create Index
```cypher
CREATE INDEX person_name FOR (p:Person) ON (p.name)
CREATE INDEX company_id FOR (c:Company) ON (c.id)
```

### Index Types
- **Range Index** - Efficient for range queries
- **Full-text Index** - Text search capability
- **Lookup Index** - Universal index
- **Unique Index** - Constraint enforcement

### Query Optimization
1. **Use indexes on filtered properties** - WHERE clauses
2. **Avoid cartesian products** - Join on common properties
3. **Limit result sets** - Use LIMIT clause
4. **Batch imports** - Load data in chunks
5. **Profile queries** - EXPLAIN/PROFILE for analysis

## Bulk Operations

### Import CSV
```cypher
LOAD CSV WITH HEADERS FROM "file:///data.csv" AS row
CREATE (p:Person {name: row.name, age: toInteger(row.age)})
```

### Batch Create
```cypher
UNWIND $nodes AS node
CREATE (n {id: node.id, name: node.name})
```

### Batch Update
```cypher
UNWIND $updates AS update
MATCH (p:Person {id: update.id})
SET p.age = update.age
```

## Result Mapping

### Simple Results
```cypher
MATCH (p:Person) RETURN p.name, p.age
```

Maps to:
```python
[
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25}
]
```

### Node Results
```cypher
MATCH (p:Person) RETURN p
```

Maps to Python Node objects with:
- id: Node internal ID
- labels: List of labels
- properties: Dict of properties

### Relationship Results
```cypher
MATCH (a)-[r]->(b) RETURN r
```

Maps to Relationship objects with:
- id: Relationship internal ID
- type: Relationship type
- properties: Dict of properties
- start_node_id: Source node ID
- end_node_id: Target node ID

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Connection refused | Neo4j not running | Start Neo4j server |
| Authentication failed | Wrong credentials | Verify username/password |
| Syntax error | Invalid Cypher | Check query syntax |
| Constraint violation | Duplicate/invalid data | Check constraints |
| Timeout | Query too slow | Add indexes, optimize query |
| Out of memory | Too much data | Batch operations, paginate |

### Retry Logic
- Connection failures: Automatic retry with exponential backoff
- Transient errors: Configurable retry attempts
- Circuit breaker: Fail fast on persistent failures

## Best Practices

✓ **Use parameterized queries** - Prevent injection attacks  
✓ **Create appropriate indexes** - Improve query performance  
✓ **Batch large imports** - Avoid memory exhaustion  
✓ **Use transactions** - Ensure data consistency  
✓ **Profile queries** - Identify performance bottlenecks  
✓ **Close connections** - Prevent resource leaks  
✓ **Limit result sets** - Avoid network overhead  
✓ **Normalize node names** - Prevent duplicate nodes  
✓ **Document schemas** - Maintain data governance  
✓ **Monitor database** - Track performance metrics  

## Integration Points

This skill integrates with:

- **GraphQL Graph Mapping** - Expose Neo4j via GraphQL
- **Graph Query Optimization** - Optimize Cypher queries
- **Schema Validation** - Validate graph structure
- **CSV Graph Loader** - Import CSV to Neo4j
- **Constraint Generator** - Define database constraints
- **REST API Wrapper** - Expose Neo4j as REST API

## Recommended Libraries

### Neo4j Python Driver
- `neo4j` - Official driver (4.x/5.x)
- `neomodel` - Python ORM for Neo4j
- `py2neo` - Pythonic interface

### Query Building
- `cypher-dsl-python` - Build Cypher programmatically
- `ipython-cypher` - Jupyter integration

### Data Processing
- `pandas` - Data frame operations
- `polars` - Efficient data loading
- `networkx` - Graph analysis

### Visualization
- `graphistry` - Interactive graph visualization
- `pyvis` - Network visualization
- `neovis.js` - Neo4j visualization

## Related Skills

- **RDF Triple Store Integration** - Alternative graph database
- **TigerGraph Connector** - Distributed graph platform
- **JanusGraph Connector** - Scalable graph database
- **GraphQL Graph Mapping** - API layer on Neo4j
- **Graph Query Optimization** - Improve query performance

---

**Version:** 1.0.0
