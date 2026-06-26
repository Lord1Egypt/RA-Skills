# Graph Query Debugging Tool - Quick Reference

Modular structure for the **graph-query-debugging-tool** skill - diagnose and fix errors in Cypher and SPARQL queries with comprehensive error analysis and corrected query suggestions.

## 📁 Structure

```
graph-query-debugging-tool/
│
├── SKILL.md                         # Skill definition & overview
│
├── references/                      # Technical guidance
│   └── debugging-patterns.md         # Query debugging design patterns
│
├── examples/                        # Domain examples
│   └── query-debugging-examples.md  # Cypher, SPARQL, and complex query examples
│
└── scripts/                         # Utility scripts
    └── query_debugger.py            # QueryDebugger implementation
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand query debugging concepts
2. **Learn:** `references/debugging-patterns.md` - Debugging patterns and strategies
3. **See:** `examples/query-debugging-examples.md` - Real query examples and fixes

### For Implementation

1. Use `scripts/query_debugger.py` for debugging queries
2. Supports: Cypher and SPARQL query analysis
3. Detects: Syntax errors, schema mismatches, relationship issues, performance problems
4. Provides: Error explanations, corrected queries, debugging suggestions

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, overview, use cases |
| `debugging-patterns.md` | Query debugging patterns & best practices |
| `query-debugging-examples.md` | Business, Scientific, E-Commerce, Real Estate, Social examples |
| `query_debugger.py` | Python QueryDebugger class |

## ⚡ Key Features

✓ Syntax error detection for Cypher and SPARQL  
✓ Schema validation and mismatch detection  
✓ Relationship type and direction validation  
✓ Query traversal pattern analysis  
✓ Performance issue identification  
✓ Corrected query suggestions  
✓ Step-by-step debugging guidance  
✓ Multi-language query support  
✓ Comprehensive error categorization  
✓ Query plan analysis  

## 🔗 Usage Example

```python
from scripts.query_debugger import QueryDebugger, QueryType

# Create debugger
debugger = QueryDebugger()

# Define schema (optional but recommended)
debugger.add_schema_element("Node", "Person", 
                           properties=["name", "age", "email"])
debugger.add_schema_element("Node", "Company", 
                           properties=["name", "industry"])
debugger.add_schema_element("Relationship", "WORKS_AT", 
                           source="Person", target="Company")

# Debug a Cypher query
query = "MATCH (p:Person)-[:WORKS_AT]->(c:Company RETURN p"
result = debugger.analyze_query(query, QueryType.CYPHER)

print(f"Errors found: {len(result.errors)}")
for error in result.errors:
    print(f"- {error.category}: {error.message}")
    print(f"  Suggestion: {error.suggestion}")

print(f"\nCorrected query:\n{result.corrected_query}")
```

## 📖 See Also

- Skill Definition: `SKILL.md`
- Debugging Patterns: `references/debugging-patterns.md`
- Examples: `examples/query-debugging-examples.md`
- Implementation: `scripts/query_debugger.py`

---

**Lean, focused modular structure - comprehensive query analysis and debugging across multiple graph query languages.**


