# Graph Template Query Generator - Quick Reference

Modular structure for the **graph-template-query-generator** skill - generate reusable parameterized query templates for common graph database operations across Cypher and SPARQL.

## 📁 Structure

```
graph-template-query-generator/
│
├── SKILL.md                         # Skill definition & overview
│
├── references/                      # Technical guidance
│   └── template-patterns.md         # Query template design patterns
│
├── examples/                        # Domain examples
│   └── template-examples.md         # Real-world template examples
│
└── scripts/                         # Utility scripts
    ├── query_template_generator.py  # QueryTemplateGenerator implementation
    └── template_registry.py         # Template storage and retrieval
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand query template concepts
2. **Learn:** `references/template-patterns.md` - Template design patterns
3. **See:** `examples/template-examples.md` - Real template examples

### For Implementation

1. Use `scripts/query_template_generator.py` to generate templates
2. Supports: Cypher and SPARQL templates
3. Provides: 8+ template categories
4. Generates: Parameterized, reusable queries

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, overview, use cases |
| `template-patterns.md` | Query template design patterns & best practices |
| `template-examples.md` | Business, Scientific, E-Commerce, Social examples |
| `query_template_generator.py` | Python QueryTemplateGenerator class |
| `template_registry.py` | Template storage and management |

## ⚡ Key Features

✓ Cypher query template generation  
✓ SPARQL query template generation  
✓ 8+ template categories  
✓ Automatic parameterization  
✓ Parameter validation  
✓ Template customization  
✓ Multi-language support  
✓ Real-world pattern library  
✓ Query explanation generation  
✓ Template registry/caching  

## 🔗 Usage Example

```python
from scripts.query_template_generator import QueryTemplateGenerator, QueryType

# Create generator
generator = QueryTemplateGenerator()

# Generate node lookup template
template = generator.generate_template(
    goal="find_node",
    label="Person",
    properties=["name", "email"],
    language=QueryType.CYPHER
)

print(f"Template: {template.query}")
print(f"Parameters: {template.parameters}")
print(f"Usage: {template.usage_example}")

# Generate relationship traversal template
rel_template = generator.generate_template(
    goal="find_relationships",
    source_label="Person",
    rel_type="WORKS_AT",
    target_label="Company",
    language=QueryType.CYPHER
)

print(f"\nRelationship Template: {rel_template.query}")
```

## 📖 See Also

- Skill Definition: `SKILL.md`
- Template Patterns: `references/template-patterns.md`
- Examples: `examples/template-examples.md`
- Implementation: `scripts/query_template_generator.py`
- Registry: `scripts/template_registry.py`

---

**Modular structure - comprehensive query template generation for graph database operations.**

