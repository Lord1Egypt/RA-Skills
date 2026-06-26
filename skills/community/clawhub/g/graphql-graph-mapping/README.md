# GraphQL Graph Mapping - Quick Reference

Bridge **GraphQL APIs** and **graph databases** by translating GraphQL schemas and queries into graph database operations (Cypher, Gremlin, SPARQL).

## 📁 Structure

```
graphql-graph-mapping/
│
├── SKILL.md                         # Skill definition & overview
│
├── references/                      # Technical guidance
│   └── graphql-mapping-patterns.md  # GraphQL-to-graph mapping patterns
│
├── examples/                        # Domain examples
│   └── graphql-mapping-examples.md  # Real-world GraphQL → Graph examples
│
└── scripts/                         # Utility scripts
    └── graphql_mapper.py            # GraphQLGraphMapper implementation
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand GraphQL-to-graph mapping
2. **Learn:** `references/graphql-mapping-patterns.md` - Mapping strategies
3. **See:** `examples/graphql-mapping-examples.md` - Real GraphQL examples

### For Implementation

1. Use `scripts/graphql_mapper.py` for translating GraphQL to graph queries
2. Supports: Neo4j Cypher, Gremlin, SPARQL, and property graph JSON
3. Features: Schema parsing, query translation, result mapping, relationship resolution

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, overview, use cases |
| `graphql-mapping-patterns.md` | GraphQL-to-graph mapping patterns & strategies |
| `graphql-mapping-examples.md` | Real-world social network, e-commerce, knowledge graph examples |
| `graphql_mapper.py` | Python GraphQLGraphMapper class |

## ⚡ Key Features

✓ Parse GraphQL schemas and queries  
✓ Map GraphQL types to graph node types  
✓ Translate GraphQL queries to Cypher, Gremlin, SPARQL  
✓ Resolve nested relationships efficiently  
✓ Map query results back to GraphQL response format  
✓ Support for multiple graph database backends  
✓ Automatic field-to-property mapping  
✓ Query depth limiting for performance  
✓ Alias resolution and field selection  
✓ Argument and filter support  

## 🔗 Usage Example

```python
from scripts.graphql_mapper import GraphQLGraphMapper

# Create mapper
mapper = GraphQLGraphMapper(
    database_type="neo4j",
    graph_schema={
        "Person": {
            "properties": ["id", "name", "age"],
            "relationships": {
                "KNOWS": "Person",
                "WORKS_AT": "Company"
            }
        },
        "Company": {
            "properties": ["id", "name", "industry"]
        }
    }
)

# Parse GraphQL query
query = """
{
    person(id: "alice") {
        name
        age
        knows {
            name
        }
    }
}
"""

# Translate to Cypher
cypher = mapper.translate_to_cypher(query)
print(cypher)
# Output: MATCH (p:Person {id: "alice"}) RETURN p.name, p.age, ...

# Map results
results = execute_query(cypher)
graphql_response = mapper.map_results(results, query)
```

## 📖 See Also

- Skill Definition: `SKILL.md`
- Mapping Patterns: `references/graphql-mapping-patterns.md`
- Examples: `examples/graphql-mapping-examples.md`
- Implementation: `scripts/graphql_mapper.py`

---

**Lean, focused modular structure - only core functionality for GraphQL-to-graph mapping.**


