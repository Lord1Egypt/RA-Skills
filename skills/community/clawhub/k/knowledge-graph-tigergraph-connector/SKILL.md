---
name: tigergraph_connector
description: Connect to TigerGraph distributed graph database to query, load, and manage large-scale knowledge graph data using GSQL and REST++ APIs
category: integrations
tags:
  - knowledge-graph
  - tigergraph
  - graph-database
  - gsql
  - graph-analytics
  - distributed-graph
  - real-time-analytics
  - graph-algorithms
  - integration
version: 1.0.0
author: kg-dev-skills
---

# TigerGraph Connector

## Purpose

This skill enables comprehensive interaction with **TigerGraph graph database** for storing, querying, analyzing, and managing large-scale knowledge graph data.

**TigerGraph** is a high-performance distributed graph database platform optimized for:
- Large-scale graph analytics
- Real-time graph processing
- Advanced graph algorithms
- Distributed graph computing
- Enterprise-grade reliability

### Key Capabilities
- Execute GSQL queries on TigerGraph instances
- Load vertices and edges via REST++ APIs
- Run built-in and custom graph algorithms
- Perform real-time graph analytics
- Manage graph schema and data
- Query result mapping to Python objects
- Batch data loading
- Performance optimization

---

## When To Use This Skill

Use this skill when:

- **Querying TigerGraph**: Executing GSQL queries and algorithms
- **Loading Data**: Inserting vertices and edges into graph
- **Graph Analytics**: Running PageRank, community detection, etc.
- **Large-Scale Graphs**: Processing enterprise-scale knowledge graphs
- **Real-Time Analysis**: Performing real-time graph computations
- **Pattern Matching**: Finding complex patterns in graph data

### Example Triggers

- "Execute this GSQL query"
- "Run PageRank algorithm"
- "Insert vertices into TigerGraph"
- "Find shortest path between nodes"
- "Detect communities in the graph"
- "Get graph statistics and metrics"

---

## Connection Configuration

### Connection Parameters

```json
{
  "host": "http://localhost",
  "restpp_port": 9000,
  "graph_name": "MyGraph",
  "api_token": "your-api-token",
  "timeout": 30,
  "retry_count": 3
}
```

### Configuration Details

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| host | string | required | TigerGraph server URL |
| restpp_port | integer | 9000 | REST++ API port |
| graph_name | string | required | Graph name to work with |
| api_token | string | required | Authentication token |
| timeout | integer | 30 | Request timeout in seconds |
| retry_count | integer | 3 | Number of retries |
| username | string | optional | Alternative authentication |
| password | string | optional | Alternative authentication |

### Authentication Methods
- API Token (preferred)
- Username/Password
- Custom headers

---

## Core Concepts

### GSQL (Graph Search Query Language)

- **Turing-Complete**: Supports complex computations
- **Pattern Matching**: Efficiently matches graph patterns
- **Algorithm Support**: Built-in library of graph algorithms
- **Vertex/Edge Access**: Direct access to graph structure
- **Aggregation**: Built-in aggregation functions

Example Query:
```gsql
CREATE QUERY getNeighbors(VERTEX<Person> person) FOR GRAPH MyGraph {
  Start = {person};
  Result = SELECT t
           FROM Start:s -(KNOWS:e)-> Person:t;
  PRINT Result;
}
```

### Graph Schema

#### Vertex Types
- Define entities in the graph
- Have properties (attributes)
- Can have primary keys
- Support custom data types

#### Edge Types
- Define relationships between vertices
- Support directional connections
- Have properties
- Can be undirected

#### Properties
- Store data on vertices/edges
- Multiple data types supported
- Can be indexed
- Support default values

### REST++ APIs

- HTTP-based interface
- JSON request/response format
- RESTful endpoint design
- Real-time data loading
- Query execution

---

## GSQL Query Patterns

### Basic Query Structure

```gsql
CREATE QUERY queryName(PARAMETERS) FOR GRAPH graphName {
  // Variable declarations
  // Pattern matching
  // Aggregations
  // Output
}
```

### Vertex Pattern Matching

#### Query Single Vertex Type
```gsql
Start = {Person.*};
Result = SELECT * FROM Start;
```

#### Query Multiple Vertex Types
```gsql
Start = {Person.* UNION Company.*};
Result = SELECT * FROM Start;
```

### Traversal Patterns

#### Single-Hop Traversal
```gsql
Result = SELECT t
         FROM Start:s -(KNOWS:e)-> Person:t;
```

#### Multi-Hop Traversal
```gsql
Result = SELECT t
         FROM Start:s -(KNOWS:e)-> Person:t -(WORKS_AT:e2)-> Company:c;
```

#### Variable-Length Traversal
```gsql
Result = SELECT t
         FROM Start:s -(KNOWS:e)->* Person:t;
```

### Aggregation Patterns

#### Count Aggregation
```gsql
Result = SELECT COUNT(DISTINCT t)
         FROM Start:s -(KNOWS:e)-> Person:t;
```

#### Property Aggregation
```gsql
Result = SELECT s.name, COUNT(DISTINCT t)
         FROM Start:s -(KNOWS:e)-> Person:t
         GROUP BY s.name;
```

### Filtering Patterns

#### Where Clause
```gsql
Result = SELECT *
         FROM Start
         WHERE age > 25 AND status == "active";
```

#### Having Clause
```gsql
Result = SELECT s.name, COUNT(DISTINCT t) as cnt
         FROM Start:s -(KNOWS:e)-> Person:t
         GROUP BY s.name
         HAVING cnt > 5;
```

---

## Data Loading Operations

### Insert Vertices

```json
{
  "vertices": {
    "Person": {
      "alice": {
        "name": "Alice",
        "age": 30,
        "email": "alice@example.com"
      },
      "bob": {
        "name": "Bob",
        "age": 25,
        "email": "bob@example.com"
      }
    }
  }
}
```

### Insert Edges

```json
{
  "edges": {
    "Person": {
      "alice": {
        "KNOWS": {
          "Person": {
            "bob": {
              "since": "2020-01-15"
            }
          }
        }
      }
    }
  }
}
```

### Batch Loading

#### CSV File Loading
```python
connector.load_from_csv(
    file_path="data.csv",
    vertex_type="Person",
    mapping={"name": "Name", "age": "Age"}
)
```

---

## Graph Algorithms

### Built-In Algorithms

#### PageRank
```gsql
RUN QUERY pagerank(max_iterations=100, damping_factor=0.85)
```

Measures vertex importance in the graph.

#### Shortest Path
```gsql
RUN QUERY shortest_path(source_vertex, target_vertex)
```

Finds shortest path between two vertices.

#### Community Detection
```gsql
RUN QUERY louvain_community(resolution=1.0)
```

Detects communities/clusters in graph.

#### Centrality Analysis
```gsql
RUN QUERY betweenness_centrality()
```

Measures vertex betweenness centrality.

### Custom Algorithms

Can be defined using GSQL for specific use cases.

---

## Query Execution Patterns

### Simple Query Execution

```python
result = connector.run_query(
    query_name="getNeighbors",
    parameters={"person": "Alice"}
)
```

### Query with Timeout

```python
result = connector.run_query(
    query_name="complexQuery",
    parameters={...},
    timeout=60
)
```

### Batch Query Execution

```python
results = connector.batch_query(
    queries=[
        {"name": "query1", "params": {...}},
        {"name": "query2", "params": {...}}
    ]
)
```

---

## Error Handling

### Common Error Scenarios

| Error | Cause | Solution |
|-------|-------|----------|
| Connection refused | Server not running | Start TigerGraph server |
| Unauthorized | Invalid token | Regenerate API token |
| Query not found | Query not installed | Install query definition |
| Timeout | Query too slow | Optimize query, increase timeout |
| Graph not found | Wrong graph name | Verify graph name |

### Error Handling Best Practices

1. **Validate Connections** - Check before operations
2. **Handle Retries** - Implement exponential backoff
3. **Log Errors** - Track all errors for debugging
4. **Graceful Degradation** - Handle partial failures
5. **Timeout Management** - Set appropriate timeouts

---

## Best Practices

### 1. Query Design
✅ Use installed queries for performance  
✅ Pre-compile queries instead of dynamic ones  
✅ Optimize pattern matching  
✅ Use appropriate graph traversal depth  
✅ Leverage built-in algorithms  

### 2. Data Loading
✅ Use batch loading for bulk data  
✅ Validate data before loading  
✅ Use atomic transactions  
✅ Monitor loading progress  
✅ Handle duplicates appropriately  

### 3. Performance
✅ Create indexes on frequently queried properties  
✅ Monitor query execution plans  
✅ Use result streaming for large datasets  
✅ Cache frequently accessed data  
✅ Distribute computation across nodes  

### 4. Schema Management
✅ Design schema for query patterns  
✅ Use appropriate data types  
✅ Maintain referential integrity  
✅ Document schema changes  
✅ Version schema updates  

### 5. Analytics
✅ Use built-in graph algorithms  
✅ Tune algorithm parameters  
✅ Monitor resource usage  
✅ Implement incremental updates  
✅ Cache algorithm results  

### 6. Scalability
✅ Partition data appropriately  
✅ Use distributed loading  
✅ Monitor cluster health  
✅ Balance load across nodes  
✅ Plan capacity growth  

### 7. Security
✅ Protect API tokens  
✅ Use HTTPS connections  
✅ Implement access control  
✅ Audit all operations  
✅ Encrypt sensitive data  

### 8. Maintenance
✅ Monitor database health  
✅ Regular backups  
✅ Update software regularly  
✅ Archive old data  
✅ Clean up temporary data  

---

## Integration with Related Skills

### Neo4j Integration
- Alternative property graph database
- Query language: Cypher vs GSQL
- Scale and deployment models differ

### JanusGraph Connector
- Distributed graph storage
- Different architecture and use cases
- Complementary strengths

### RDF Triple Store Integration
- Semantic web alternative
- Triple-based vs property graph
- Different query languages

### Graph Query Optimization
- Optimize GSQL query performance
- Analyze execution plans
- Performance tuning

### REST API Wrapper
- Expose TigerGraph via REST API
- Custom endpoint creation
- API documentation

---

## Libraries & Dependencies

### Core Libraries

| Library | Purpose |
|---------|---------|
| pyTigerGraph | Official Python SDK |
| requests | HTTP client |
| json | JSON handling |

### Installation

```bash
pip install pyTigerGraph requests
```

---

## Expected Benefits

Using this skill enables:

✅ **Performance** - High-speed graph processing at scale  
✅ **Analytics** - Advanced graph algorithms and analytics  
✅ **Scalability** - Enterprise-scale knowledge graph processing  
✅ **Real-Time** - Real-time graph computations  
✅ **Flexibility** - Support for complex graph patterns  
✅ **Reliability** - Enterprise-grade reliability and backup  
✅ **Integration** - Easy integration with applications  

---

## Quick Reference

### Connection & Query
```python
connector = TigerGraphConnector()
connector.connect(config)
result = connector.run_query("queryName", params)
connector.close()
```

### Common Operations
```python
# Insert vertices
connector.insert_vertices(vertex_type, vertices)

# Insert edges
connector.insert_edges(edge_type, edges)

# Run algorithm
connector.run_algorithm("pagerank", params)

# Get statistics
stats = connector.get_statistics()
```

### Data Loading
```python
connector.load_from_csv(file_path, vertex_type, mapping)
connector.batch_insert(vertices, edges)
```

---

## Related Skills

- **Neo4j Integration** - Property graph database using Cypher
- **JanusGraph Connector** - Distributed graph using Gremlin
- **RDF Triple Store Integration** - SPARQL for RDF
- **GraphQL Graph Mapping** - GraphQL API interface
- **Graph Query Optimization** - Query performance tuning
- **REST API Wrapper** - REST interface for graphs

---

## Resources

- [TigerGraph Official Documentation](https://docs.tigergraph.com/)
- [GSQL Reference](https://docs.tigergraph.com/gsql-ref/current/)
- [REST++ API Guide](https://docs.tigergraph.com/api/rest-api/)
- [Python pyTigerGraph](https://pytigergraph.github.io/intro/)

---

**Version:** 1.0.0  
**Last Updated:** April 12, 2026
