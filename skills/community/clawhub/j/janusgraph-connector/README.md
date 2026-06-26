# JanusGraph Connector

> Connect to JanusGraph for querying, managing, and analyzing distributed graph data using Gremlin

## Directory Structure

```
janusgraph-connector/
├── README.md                      (This file - Quick reference)
├── SKILL.md                       (Skill definition with examples & best practices)
├── examples/
│   └── janusgraph-examples.md     (5 complete production examples)
├── references/
│   └── janusgraph-patterns.md     (30+ design patterns for JanusGraph)
└── scripts/
    └── janusgraph_connector.py    (Production-ready Python implementation)
```

## Quick Start

### Installation

```bash
pip install gremlin-python
```

### Basic Connection

```python
from janusgraph_connector import JanusGraphConnector, ConnectionConfig

# Configure connection
config = ConnectionConfig(
    host="localhost",
    port=8182,
    protocol="ws",
    traversal_source="g"
)

# Create connector
connector = JanusGraphConnector()
connector.connect(config)

# Execute query
result = connector.execute_query("g.V().limit(5)")
print(result.records)

# Cleanup
connector.close()
```

## Features

✅ **Connection Management**
- Gremlin Server connectivity
- WebSocket protocol support
- Connection pooling
- Session management

✅ **Gremlin Query Execution**
- Execute traversal queries
- Parameter binding for safety
- Result mapping to Python objects
- Error handling and status tracking

✅ **Graph Operations**
- Create vertices (nodes)
- Create edges (relationships)
- Find vertices by label/properties
- Delete vertices and edges
- Update properties

✅ **Transaction Support**
- Begin/commit/rollback transactions
- ACID compliance
- Atomic operations
- Transaction status tracking

✅ **Index Management**
- Create composite indexes
- Create mixed indexes
- Performance optimization
- Index verification

✅ **Advanced Features**
- Batch operations
- Graph statistics
- Connection health checks
- Query result mapping

## Key Concepts

### Vertices (Nodes)
- Labeled entities in the graph
- Contain properties (key-value pairs)
- Examples: Person, Product, Location

### Edges (Relationships)
- Labeled connections between vertices
- Support properties
- Directional
- Examples: KNOWS, PURCHASED, LOCATED_IN

### Gremlin
- Graph traversal language (domain-specific language for TinkerPop)
- Supports filtering, traversal, aggregation
- Language-independent

### TinkerPop
- Apache framework for graph computing
- Abstraction layer for multiple graph databases
- Enables vendor independence

## File Descriptions

| File | Purpose | Size |
|------|---------|------|
| README.md | Quick reference and getting started | This file |
| SKILL.md | Complete skill definition | 350+ lines |
| examples/janusgraph-examples.md | 5 production domain examples | 500+ lines |
| references/janusgraph-patterns.md | 30+ design patterns | 450+ lines |
| scripts/janusgraph_connector.py | Production Python implementation | 500+ lines |

## Common Use Cases

### 1. Social Network Analysis
Query friend relationships, find mutual friends, analyze connection patterns

### 2. E-Commerce Knowledge Graph
Manage products, categories, suppliers, customer relationships

### 3. Knowledge Base
Organize topics, create learning paths, track prerequisites

### 4. Organizational Hierarchy
Model organizational structure, chain of command, department relationships

### 5. Research Network
Track papers, authors, citations, collaborations

## Integration Points

This skill integrates with:
- **Neo4j Integration** - Alternative property graph database
- **GraphQL Graph Mapping** - Expose JanusGraph via GraphQL API
- **Graph Query Optimization** - Optimize Gremlin queries
- **CSV Graph Loader** - Bulk import data
- **REST API Wrapper** - Expose as REST API

## Quick Examples

### Query all vertices of a type
```python
result = connector.execute_query("g.V().hasLabel('Person')")
```

### Find specific vertex
```python
result = connector.execute_query(
    "g.V().has('name', ?)",
    params=['Alice']
)
```

### Create a vertex
```python
result = connector.create_vertex(
    label='Person',
    properties={'name': 'Alice', 'age': 30}
)
```

### Create an edge
```python
result = connector.create_edge(
    from_id='v1',
    to_id='v2',
    label='KNOWS'
)
```

### Get statistics
```python
stats = connector.get_statistics()
print(stats)
```

## Performance Tips

1. **Use Indexes** - Create indexes on frequently filtered properties
2. **Limit Traversals** - Avoid unbounded graph traversals
3. **Batch Operations** - Use batch mode for bulk inserts
4. **Connection Pooling** - Reuse connections across requests
5. **Parameterized Queries** - Use parameter binding to prevent injection

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Verify JanusGraph server is running on correct host/port |
| Query timeout | Reduce traversal depth or add index on filtered properties |
| Memory errors | Limit result sets, use iterators instead of loading all |
| Transaction rollback | Check for conflicts, simplify transaction operations |

## Related Documentation

- See **SKILL.md** for complete skill definition
- See **examples/janusgraph-examples.md** for detailed domain examples
- See **references/janusgraph-patterns.md** for design patterns
- See **scripts/janusgraph_connector.py** for implementation details

## Next Steps

1. Review the SKILL.md for comprehensive documentation
2. Check examples/janusgraph-examples.md for your use case
3. Look at references/janusgraph-patterns.md for design patterns
4. Use scripts/janusgraph_connector.py as reference implementation

---

**Status:** ✅ Production Ready | **Version:** 1.0.0 | **Last Updated:** April 12, 2026

