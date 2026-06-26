# Neo4j Integration - Quick Reference

Connect to **Neo4j graph databases** and execute **Cypher queries** for storing, querying, and managing knowledge graph data with the property graph model.

## 📁 Structure

```
neo4j-integration/
│
├── SKILL.md                         # Skill definition & overview
│
├── references/                      # Technical guidance
│   └── neo4j-patterns.md            # Cypher patterns & best practices
│
├── examples/                        # Domain examples
│   └── neo4j-examples.md            # Real-world Neo4j implementations
│
└── scripts/                         # Utility scripts
    └── neo4j_connector.py           # Neo4jConnector implementation
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand Neo4j integration fundamentals
2. **Learn:** `references/neo4j-patterns.md` - Cypher patterns and queries
3. **See:** `examples/neo4j-examples.md` - Real-world graph examples

### For Implementation

1. Use `scripts/neo4j_connector.py` for Neo4j database operations
2. Supports: Connection management, Cypher execution, transactions, indexes
3. Features: Query execution, node/relationship creation, bulk operations, result mapping

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, overview, use cases |
| `neo4j-patterns.md` | Cypher query patterns & best practices |
| `neo4j-examples.md` | Business, scientific, social network examples |
| `neo4j_connector.py` | Python Neo4jConnector class |

## ⚡ Key Features

✓ Connection pooling and session management  
✓ Execute Cypher queries with parameters  
✓ Create nodes with labels and properties  
✓ Create relationships between nodes  
✓ Bulk import data from CSV or JSON  
✓ Transaction support with rollback  
✓ Index creation and management  
✓ Query result mapping to Python objects  
✓ Connection health checks  
✓ Error handling and retry logic  

## 🔗 Usage Example

```python
from scripts.neo4j_connector import Neo4jConnector

# Create connector
connector = Neo4jConnector(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="password"
)

# Execute query
results = connector.execute_query(
    "MATCH (p:Person) WHERE p.age > $age RETURN p.name, p.age",
    {"age": 30}
)

# Create node
connector.create_node(
    label="Person",
    properties={"name": "Alice", "age": 30}
)

# Create relationship
connector.create_relationship(
    start_node_id="alice",
    end_node_id="bob",
    relationship_type="KNOWS"
)

# Close connection
connector.close()
```

## 📖 See Also

- Skill Definition: `SKILL.md`
- Cypher Patterns: `references/neo4j-patterns.md`
- Examples: `examples/neo4j-examples.md`
- Implementation: `scripts/neo4j_connector.py`

---

**Lean, focused modular structure - only core functionality for Neo4j database operations.**


