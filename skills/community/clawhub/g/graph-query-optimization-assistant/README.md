# Graph Query Optimization Assistant - Quick Reference

Modular structure for the **graph-query-optimization-assistant** skill - analyze and optimize Cypher and SPARQL queries for maximum performance with intelligent index recommendations and traversal optimization.

## 📁 Structure

```
graph-query-optimization-assistant/
│
├── SKILL.md                         # Skill definition & overview
│
├── references/                      # Technical guidance
│   └── optimization-patterns.md     # Query optimization design patterns
│
├── examples/                        # Domain examples
│   └── optimization-examples.md     # E-Commerce, Social, Scientific, etc.
│
└── scripts/                         # Utility scripts
    ├── query_optimizer.py           # QueryOptimizer implementation
    └── performance_benchmarking.py  # Performance analysis tools
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand query optimization concepts
2. **Learn:** `references/optimization-patterns.md` - Optimization strategies
3. **See:** `examples/optimization-examples.md` - Real optimization examples

### For Implementation

1. Use `scripts/query_optimizer.py` for analyzing queries
2. Supports: Cypher and SPARQL query optimization
3. Provides: Index recommendations, cost analysis, optimization suggestions
4. Generates: Performance reports and improvement estimates

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, overview, use cases |
| `optimization-patterns.md` | Query optimization patterns & best practices |
| `optimization-examples.md` | E-Commerce, Social, Scientific, Knowledge, Finance, Healthcare examples |
| `query_optimizer.py` | Python QueryOptimizer class |
| `performance_benchmarking.py` | Performance benchmarking tools |

## ⚡ Key Features

✓ Cypher query optimization analysis  
✓ SPARQL query optimization analysis  
✓ Automatic language detection  
✓ Index recommendation engine  
✓ Cost estimation and analysis  
✓ Traversal optimization suggestions  
✓ Node selection strategy recommendations  
✓ Performance metrics and comparisons  
✓ Cardinality analysis  
✓ Query simplification suggestions  

## 🔗 Usage Example

```python
from scripts.query_optimizer import QueryOptimizer, QueryType

# Create optimizer
optimizer = QueryOptimizer()

# Define schema for better analysis
optimizer.add_node_type("Person", properties={"id": "indexed", "name": "string", "age": "integer"})
optimizer.add_node_type("Company", properties={"id": "indexed", "name": "string", "industry": "string"})
optimizer.add_relationship_type("WORKS_AT", "Person", "Company")

# Analyze a Cypher query
query = """
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
WHERE c.industry = "Tech"
RETURN p
"""

result = optimizer.analyze_query(query, QueryType.CYPHER)

print(f"Cost Estimate: {result.estimated_cost}")
print(f"Optimization Count: {len(result.suggestions)}")

for suggestion in result.suggestions:
    print(f"- {suggestion.title}: {suggestion.description}")
    print(f"  Impact: {suggestion.performance_impact}")

print(f"\nOptimized Query:\n{result.optimized_query}")
```

## 📖 See Also

- Skill Definition: `SKILL.md`
- Optimization Patterns: `references/optimization-patterns.md`
- Examples: `examples/optimization-examples.md`
- Implementation: `scripts/query_optimizer.py`
- Benchmarking: `scripts/performance_benchmarking.py`

---

**Focused modular structure - comprehensive query optimization and performance analysis across graph query languages.**


