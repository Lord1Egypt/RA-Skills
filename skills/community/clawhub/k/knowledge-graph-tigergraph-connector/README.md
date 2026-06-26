# TigerGraph Connector

> Connect to TigerGraph to query, load, and manage large-scale knowledge graphs using GSQL and REST++ APIs

## Directory Structure

```
tigergraph-connector/
├── README.md                      (This file - Quick reference)
├── SKILL.md                       (Skill definition with examples & best practices)
├── examples/
│   └── tigergraph-examples.md     (5 complete production examples)
├── references/
│   └── tigergraph-patterns.md     (30+ design patterns for GSQL)
└── scripts/
    └── tigergraph_connector.py    (Production-ready Python implementation)
```

## Quick Start

### Installation

```bash
pip install pyTigerGraph
```

### Basic Connection

```python
from tigergraph_connector import TigerGraphConnector, ConnectionConfig

# Configure connection
config = ConnectionConfig(
    host="http://localhost",
    restpp_port=9000,
    graph_name="MyGraph",
    api_token="your-api-token"
)

# Create connector
connector = TigerGraphConnector()
connector.connect(config)

# Execute GSQL query
result = connector.run_query("getNeighbors", {"person": "Alice"})
print(result.records)

# Cleanup
connector.close()
```

## Features

✅ **Connection Management**
- REST++ API connectivity
- Token-based authentication
- Graph switching
- Connection pooling

✅ **GSQL Query Execution**
- Execute pre-installed queries
- Dynamic query parameters
- Result mapping to Python objects
- Error handling and status tracking

✅ **Data Loading**
- Vertex insertion
- Edge insertion
- Batch loading support
- Atomic transactions

✅ **Graph Algorithms**
- PageRank calculation
- Shortest path finding
- Community detection
- Centrality analysis
- Pattern matching

✅ **Schema Management**
- Create and manage graph schemas
- Define vertex and edge types
- Property management
- Index management

✅ **Advanced Features**
- Real-time graph analytics
- Distributed processing
- Statistics collection
- Performance monitoring

## Key Concepts

### GSQL (Graph Search Query Language)
- Turing-complete graph query language
- Designed specifically for graph databases
- Efficient graph pattern matching
- Built-in graph algorithm library

### Vertices and Edges
- Vertices: Nodes in the graph with properties
- Edges: Connections between vertices
- Both support custom properties
- Types define structure

### Graph Schema
- Defines vertex types and edge types
- Specifies allowed connections
- Property definitions
- Indexes for performance

### Queries
- Installed queries: Pre-compiled and optimized
- Dynamic queries: Run-time execution
- Built-in algorithms: Community detection, PageRank, etc.

### REST++ APIs
- HTTP protocol for communication
- JSON request/response format
- RESTful endpoint design
- Standard HTTP status codes

## File Descriptions

| File | Purpose | Size |
|------|---------|------|
| README.md | Quick reference and getting started | This file |
| SKILL.md | Complete skill definition | 350+ lines |
| examples/tigergraph-examples.md | 5 production domain examples | 500+ lines |
| references/tigergraph-patterns.md | 30+ design patterns | 450+ lines |
| scripts/tigergraph_connector.py | Production Python implementation | 500+ lines |

## Common Use Cases

### 1. Social Graph Analytics
Real-time analysis of social networks with community detection

### 2. Recommendation Engines
Personalized recommendations using graph traversal

### 3. Fraud Detection
Pattern-based fraud detection across transaction networks

### 4. Supply Chain Management
Track and optimize supply chain relationships

### 5. Knowledge Graph Management
Large-scale knowledge base with semantic relationships

## Integration Points

This skill integrates with:
- **Neo4j Integration** - Property graph alternative
- **JanusGraph Connector** - Distributed graph alternative
- **RDF Triple Store Integration** - Semantic web
- **Graph Query Optimization** - Performance tuning
- **REST API Wrapper** - API exposure
- **CSV Graph Loader** - Data import

## Quick Examples

### Run Query with Parameters
```python
result = connector.run_query(
    "getNeighbors",
    {"person": "Alice", "max_depth": 2}
)
```

### Insert Vertices
```python
connector.insert_vertices(
    vertex_type="Person",
    vertices=[
        {"id": "alice", "name": "Alice", "age": 30},
        {"id": "bob", "name": "Bob", "age": 25}
    ]
)
```

### Insert Edges
```python
connector.insert_edges(
    edge_type="KNOWS",
    edges=[
        {"from_vertex": "alice", "to_vertex": "bob", "since": "2020-01-15"}
    ]
)
```

### Run Graph Algorithm
```python
result = connector.run_algorithm(
    "pagerank",
    {"max_iterations": 100}
)
```

### Get Graph Statistics
```python
stats = connector.get_statistics()
print(f"Vertices: {stats['vertex_count']}")
print(f"Edges: {stats['edge_count']}")
```

## Performance Tips

1. **Use Installed Queries** - Pre-compiled queries are faster
2. **Batch Loading** - Load data in batches for efficiency
3. **Indexes** - Create indexes on frequently queried properties
4. **Query Optimization** - Analyze query execution plans
5. **Graph Algorithms** - Use built-in algorithms when possible
6. **Caching** - Cache frequently accessed data

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Verify host, port, and credentials |
| Query not found | Install query before running |
| Authentication fails | Check API token validity |
| Timeout errors | Increase timeout, optimize query |
| Out of memory | Reduce query scope, enable streaming |

## Related Documentation

- See **SKILL.md** for complete skill definition
- See **examples/tigergraph-examples.md** for detailed examples
- See **references/tigergraph-patterns.md** for design patterns
- See **scripts/tigergraph_connector.py** for implementation details

## Next Steps

1. Review the SKILL.md for comprehensive documentation
2. Check examples/tigergraph-examples.md for your use case
3. Look at references/tigergraph-patterns.md for design patterns
4. Use scripts/tigergraph_connector.py as reference implementation

---

**Status:** ✅ Production Ready | **Version:** 1.0.0 | **Last Updated:** April 12, 2026

