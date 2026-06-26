# Multi-Hop Reasoning Query Builder - Quick Reference
Modular structure for the **multi-hop-reasoning-query-builder** skill - construct advanced graph queries that traverse multiple relationship hops to discover indirect connections and hidden patterns.
## 📁 Structure
```
multi-hop-reasoning-query-builder/
│
├── SKILL.md                         # Skill definition & overview
│
├── references/                      # Technical guidance
│   └── multi-hop-patterns.md        # Multi-hop reasoning design patterns
│
├── examples/                        # Domain examples
│   └── multi-hop-examples.md        # 8 domain examples
│
└── scripts/                         # Utility scripts
    ├── multi_hop_query_builder.py   # MultiHopQueryBuilder implementation
    └── path_reasoner.py             # Path reasoning engine
```
## 🎯 Quick Start
### For Using This Skill
1. **Read:** `SKILL.md` - Understand multi-hop reasoning concepts
2. **Learn:** `references/multi-hop-patterns.md` - Reasoning patterns
3. **See:** `examples/multi-hop-examples.md` - Real multi-hop examples
### For Implementation
1. Use `scripts/multi_hop_query_builder.py` for building queries
2. Supports: Cypher and SPARQL multi-hop queries
3. Provides: 8+ hop reasoning patterns
4. Generates: Path queries and traversal queries
## 📚 Files
| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, overview, use cases |
| `multi-hop-patterns.md` | Multi-hop reasoning patterns & best practices |
| `multi-hop-examples.md` | Business, Social, Supply Chain, Fraud, Knowledge Graph examples |
| `multi_hop_query_builder.py` | Python MultiHopQueryBuilder class |
| `path_reasoner.py` | Path reasoning and analysis engine |
## ⚡ Key Features
✓ Cypher multi-hop query generation  
✓ SPARQL property path generation  
✓ Variable-length path traversal  
✓ Bounded depth reasoning  
✓ Path discovery  
✓ Relationship filtering  
✓ Multi-hop optimization  
✓ Performance analysis  
✓ Pattern-based reasoning  
✓ Schema-aware query construction  
## 🔗 Usage Example
```python
from scripts.multi_hop_query_builder import MultiHopQueryBuilder, QueryType
# Create builder
builder = MultiHopQueryBuilder()
# Build friends-of-friends query
query = builder.build_query(
    start_label="Person",
    start_id_property="name",
    start_id_value="Alice",
    relationship_type="FOLLOWS",
    num_hops=2,
    target_label="Person",
    language=QueryType.CYPHER
)
print(f"Query: {query.query}")
print(f"Hops: {query.num_hops}")
```
## 📖 See Also
- Skill Definition: `SKILL.md`
- Multi-Hop Patterns: `references/multi-hop-patterns.md`
- Examples: `examples/multi-hop-examples.md`
- Implementation: `scripts/multi_hop_query_builder.py`
- Path Reasoning: `scripts/path_reasoner.py`
---
**Modular structure - comprehensive multi-hop reasoning for advanced graph exploration.**
