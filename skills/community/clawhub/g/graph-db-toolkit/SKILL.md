---
name: graph-db-toolkit
description: Graph database toolkit for Neo4j and Cypher-based graph analytics. Use when working with knowledge graphs, relationship queries, graph traversal, Neo4j operations, social network analysis, recommendation systems, or any task requiring nodes, edges, and graph patterns. Triggers on phrases like "graph database", "Neo4j", "Cypher query", "knowledge graph", "graph traversal", "relationship analysis", "graph analytics".
---

# Graph Database Toolkit

Operations toolkit for graph databases with focus on Neo4j and Cypher.

## Quick Start

```python
from scripts.neo4j_client import Neo4jClient

client = Neo4jClient(uri="bolt://localhost:7687", user="neo4j", password="password")
client.create_node("Person", {"name": "Alice", "age": 30})
client.create_node("Person", {"name": "Bob", "age": 25})
client.create_relationship("Alice", "Person", "KNOWS", "Bob", "Person", {"since": 2020})
results = client.query("""
    MATCH (a:Person)-[r:KNOWS]->(b:Person)
    RETURN a.name, b.name, r.since
""")
```

## Scripts

- `scripts/neo4j_client.py` - Neo4j connection and CRUD operations
- `scripts/cypher_builder.py` - Cypher query builder utilities
- `scripts/graph_analytics.py` - Graph algorithms (centrality, paths, community)

## References

- `references/cypher_cheatsheet.md` - Common Cypher patterns
- `references/neo4j_patterns.md` - Neo4j design patterns
