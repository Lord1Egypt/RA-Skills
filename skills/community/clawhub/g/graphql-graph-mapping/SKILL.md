---
name: graphql_graph_mapping
title: GraphQL Graph Mapping
description: Map GraphQL queries and schemas to underlying graph database operations, enabling applications to access knowledge graph data through GraphQL APIs. Translates GraphQL schemas/queries to Cypher, Gremlin, SPARQL, and resolves results back to GraphQL response format.
category: integrations
tags:
  - knowledge-graph
  - graphql
  - api
  - graph-mapping
  - cypher
  - gremlin
  - sparql
  - neo4j
  - integration
  - query-translation
  - schema-mapping
  - developer-tools
version: 1.0.0
author: community
license: MIT
metadata:
  {"openclaw":{"emoji":"🔗","homepage":"https://clawhub.com"}}
---

# GraphQL Graph Mapping

**Bridge GraphQL APIs and graph databases by translating GraphQL schemas and queries into graph database operations.**

This skill enables seamless integration between **GraphQL APIs** and **graph databases** by translating GraphQL queries into native database queries (Cypher, Gremlin, SPARQL) and mapping results back to GraphQL response format. It allows developers to expose graph data through a clean GraphQL API layer.

## Quick Start

### Use When
- Building a GraphQL API for a knowledge graph
- Mapping GraphQL schemas to graph database schemas
- Translating GraphQL queries to database-specific queries
- Exposing graph relationships as API fields
- Integrating graph data into frontend applications
- Creating query resolvers for graph-backed APIs
- Optimizing nested graph traversals from GraphQL

### Inputs
- GraphQL schema (types, fields, relationships)
- GraphQL query or mutation
- Graph database type (Neo4j, TigerGraph, JanusGraph, RDF store)
- Mapping configuration (optional)
- Query execution context (variables, arguments)

### Outputs
- Translated database queries (Cypher, Gremlin, SPARQL)
- Resolved query results
- GraphQL response format (JSON)
- Query execution plan
- Performance metrics

## GraphQL-to-Graph Mapping Concepts

### Type Mapping

GraphQL types map naturally to graph entities:

| GraphQL Concept | Graph Concept | Example |
|---|---|---|
| Object Type | Node Type/Label | `type Person` → `:Person` label |
| Field | Node Property | `name: String` → `Person.name` |
| Relationship Field | Edge/Relationship | `friends: [Person]` → `KNOWS` relationship |
| ID Field | Node Identifier | `id: ID!` → Node unique identifier |
| Query Root | Graph Traversal Entry | Query field returns starting nodes |
| Nested Fields | Graph Traversal | Nested fields resolve relationships |

### Query Translation Strategy

GraphQL queries are translated to graph database queries following a systematic process:

#### Step 1: Parse GraphQL Query
```graphql
{
  person(id: "alice") {
    name
    age
    knows {
      name
    }
  }
}
```

#### Step 2: Map Root Query to Graph Traversal
- `person(id: "alice")` → Find Person node with id="alice"

#### Step 3: Resolve Fields to Properties
- `name` → Person.name property
- `age` → Person.age property

#### Step 4: Resolve Relationships
- `knows` → KNOWS relationship to other Person nodes

#### Step 5: Generate Target Query

**Cypher (Neo4j):**
```cypher
MATCH (p:Person {id: "alice"})
RETURN p.name, p.age,
       [(p)-[:KNOWS]->(f:Person) | {name: f.name}] AS knows
```

**Gremlin (JanusGraph, TigerGraph):**
```gremlin
g.V().has("Person","id","alice")
  .project("name","age","knows")
  .by("name")
  .by("age")
  .by(out("KNOWS").has("Person"))
```

**SPARQL (RDF):**
```sparql
SELECT ?name ?age ?friendName
WHERE {
  ex:alice ex:name ?name ;
           ex:age ?age ;
           ex:knows ?friend .
  ?friend ex:name ?friendName .
}
```

#### Step 6: Execute and Map Results

## Supported Query Patterns

### 1. Simple Field Selection
```graphql
{
  person(id: "alice") {
    name
    email
  }
}
```
Maps to: SELECT statement with specific properties

### 2. Filtered Queries
```graphql
{
  people(where: {age: {gt: 30}}) {
    name
    age
  }
}
```
Maps to: WHERE clauses with comparison operators

### 3. Nested Relationships
```graphql
{
  person(id: "alice") {
    name
    worksAt {
      name
      industry
      employees {
        name
      }
    }
  }
}
```
Maps to: Multi-hop graph traversals

### 4. Multiple Root Queries
```graphql
{
  alice: person(id: "alice") { name }
  bob: person(id: "bob") { name }
}
```
Maps to: Multiple graph traversals with aliases

### 5. List Queries with Pagination
```graphql
{
  people(first: 10, after: "cursor123") {
    nodes {
      name
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```
Maps to: LIMIT and OFFSET clauses

### 6. Aggregation Queries
```graphql
{
  personStats {
    count
    averageAge
    byDepartment {
      department
      count
    }
  }
}
```
Maps to: AGGREGATION and GROUP BY operations

## Database-Specific Translation

### Neo4j Cypher

**GraphQL:**
```graphql
{
  person(id: "alice") {
    name
    friends {
      name
    }
  }
}
```

**Cypher Output:**
```cypher
MATCH (p:Person {id: "alice"})-[:KNOWS]->(f:Person)
RETURN p.name, collect(f.name) AS friends
```

Features:
- Label matching for node types
- Property filtering for query arguments
- MATCH clauses for relationships
- RETURN projections for field selection
- Collection aggregation for list fields

### Gremlin (JanusGraph, TigerGraph)

**Gremlin Output:**
```gremlin
g.V().has("Person","id","alice")
  .project("name","friends")
  .by("name")
  .by(out("KNOWS").has("Person").values("name").fold())
```

Features:
- Vertex property filters
- Vertex traversal with has() filters
- Edge label traversal
- Property value extraction
- Aggregation with fold()

### SPARQL (RDF Triple Stores)

**SPARQL Output:**
```sparql
PREFIX ex: <http://example.org/>

SELECT ?name ?friendName
WHERE {
  ex:alice ex:name ?name ;
           ex:knows ?friend .
  ?friend ex:name ?friendName .
}
```

Features:
- Subject-predicate-object triple pattern
- Optional filters
- Named graph support
- SPARQL aggregation functions

## GraphQL Schema Requirements

### Node Type Definition
```graphql
type Person {
  id: ID!                    # Unique identifier
  name: String!              # Property
  age: Int                   # Property
  email: String              # Property
  knows: [Person]            # Relationship
  worksAt: Company           # Relationship
  posts: [Post]              # Relationship
}
```

Maps to graph:
- `Person` → Node label/type
- `id` → Node identifier property
- `name, age, email` → Node properties
- `knows, worksAt, posts` → Outgoing relationships

### Relationship Field Definition
```graphql
type Person {
  knows(first: Int, after: String): PersonConnection!
}

type PersonConnection {
  nodes: [Person!]!
  pageInfo: PageInfo!
}
```

Maps to:
- Relationship with pagination support
- Forward cursor navigation
- Results in graph relationships

## Query Resolution Process

### 1. Schema Analysis
- Parse GraphQL schema
- Map types to graph labels
- Identify relationships between types
- Extract property definitions

### 2. Query Parsing
- Parse incoming GraphQL query
- Validate fields against schema
- Extract arguments and filters
- Build query AST

### 3. Query Translation
- Translate root query to graph traversal start
- Resolve nested fields to relationship traversals
- Apply filters and arguments
- Add projections for selected fields

### 4. Optimization
- Reorder traversals for efficiency
- Combine filters when possible
- Limit traversal depth
- Add query hints/indexes

### 5. Execution
- Execute generated query on graph database
- Handle errors and timeouts
- Stream large result sets
- Cache common queries

### 6. Result Mapping
- Transform graph results to GraphQL shape
- Handle null values and missing relationships
- Apply field aliases
- Format connection/pageInfo for pagination

## Performance Considerations

### Query Depth Limiting
Prevent expensive deep traversals:
```
Default max depth: 5 levels
Configurable per schema
```

### Query Complexity Scoring
```
Simple field: 1 point
Relationship traversal: 2 points
List field: multiplied by max items
Max allowed: 100-1000 points
```

### Index Usage
- Create indexes on frequently filtered properties
- Index relationship types
- Index node labels

### Result Caching
- Cache frequently queried patterns
- Invalidate on data updates
- Implement cache layers

## Error Handling

### Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| Field not found | Property doesn't exist | Add property to graph schema |
| Invalid relationship | Relationship type mismatch | Update schema mapping |
| Query timeout | Expensive traversal | Add depth limit or filter |
| Missing node | ID doesn't exist | Return null or error |
| Type mismatch | Field type differs | Coerce or validate types |

### Validation

- Validate GraphQL query against schema
- Check field existence in graph schema
- Verify argument types
- Ensure relationship types exist

## Best Practices

✓ **Use stable, meaningful identifiers** - Base IDs on unique properties  
✓ **Implement query depth limits** - Prevent expensive traversals  
✓ **Cache schema metadata** - Avoid re-parsing  
✓ **Validate queries early** - Fail fast on invalid queries  
✓ **Index frequently filtered fields** - Improve query performance  
✓ **Document schema mappings** - Keep API contract clear  
✓ **Test edge cases** - Handle null relationships gracefully  
✓ **Monitor query performance** - Track slow queries  
✓ **Implement query complexity scoring** - Prevent abuse  
✓ **Version your GraphQL schema** - Support schema evolution  

## Integration Points

This skill integrates with:

- **Neo4j Integration** - Execute Cypher queries
- **Graph Query Optimization** - Optimize generated queries
- **Query Caching** - Cache frequent patterns
- **Schema Validation** - Validate schema mappings
- **REST API Wrapper** - Expose GraphQL as REST
- **Monitoring Tools** - Track query performance

## Recommended Libraries

### GraphQL Processing
- `graphql-core` - GraphQL query parsing and validation
- `graphene` - Python GraphQL framework
- `strawberry` - Modern Python GraphQL

### Neo4j Integration
- `neo4j` - Official Neo4j driver
- `neo4j-graphql` - GraphQL to Cypher translation
- `neomodel` - Python ORM for Neo4j

### Query Building
- `pyparsing` - Query string parsing
- `sqlalchemy` - Query builder patterns
- `sqlglot` - SQL/Graph query translation

### Validation
- `pydantic` - Data validation
- `jsonschema` - JSON schema validation
- `marshmallow` - Schema validation

## Related Skills

- **Neo4j Integration** - Neo4j-specific features
- **REST API Wrapper Generator** - Expose graphs via REST
- **Graph Query Optimization** - Optimize queries
- **Graph Schema Validation** - Validate schemas
- **Query Template Generator** - Generate common patterns

---

**Version:** 1.0.0
