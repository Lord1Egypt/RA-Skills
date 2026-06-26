# Property Graph Schema Designer - Quick Reference

Modular structure for the **property-graph-schema-designer** skill - designs Neo4j-style property graph schemas.

## 📁 Structure

```
property-graph-schema-designer/
│
├── SKILL.md                    # Skill definition & overview
│
├── references/                 # Technical guidance
│   └── schema-patterns.md      # Property graph design patterns
│
├── examples/                   # Domain examples
│   └── example-schemas.md      # University, E-Commerce, Social Network
│
└── scripts/                    # Utility scripts
    └── schema_builder.py       # SchemaBuilder implementation
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand Neo4j schema design
2. **Learn:** `references/schema-patterns.md` - Design patterns
3. **See:** `examples/example-schemas.md` - Real domain schemas

### For Implementation

1. Use `scripts/schema_builder.py` for building schemas
2. Supports: Node labels, relationships, properties, constraints, indexes
3. Generates: Cypher DDL statements, schema summaries

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, overview, use cases |
| `schema-patterns.md` | Neo4j design patterns & best practices |
| `example-schemas.md` | 3 domain schemas (University, E-Commerce, Social) |
| `schema_builder.py` | Python SchemaBuilder class |

## ⚡ Key Features

✓ Node label definition  
✓ Relationship type definition  
✓ Property management (types, constraints, indexes)  
✓ Constraint generation  
✓ Index recommendations  
✓ Cypher DDL output  
✓ Schema statistics  

## 🔗 Usage Example

```python
from scripts.schema_builder import SchemaBuilder, PropertyType

# Create schema
builder = SchemaBuilder("University")

# Add nodes
builder.add_property_to_node("Student", "student_id", PropertyType.STRING, unique=True)
builder.add_property_to_node("Student", "name", PropertyType.STRING, indexed=True)

# Add relationships
builder.add_relationship("Student", "ENROLLED_IN", "Course")

# View schema
builder.print_schema()

# Get statistics
stats = builder.get_schema_summary()
print(stats)
```

## 📖 See Also

- Skill Definition: `SKILL.md`
- Schema Patterns: `references/schema-patterns.md`
- Domain Examples: `examples/example-schemas.md`
- Implementation: `scripts/schema_builder.py`

---

**Lean, focused modular structure - only core functionality for Neo4j schema design.**

