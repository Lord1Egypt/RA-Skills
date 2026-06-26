# KG Schema from Text - Quick Reference

Modular structure for the **kg-schema-from-text** skill - generates graph schemas from domain documentation.

## 📁 Structure

```
kg-schema-from-text/
│
├── SKILL.md                    # Skill definition & overview
│
├── references/                 # Technical guidance
│   └── extraction-patterns.md  # Entity/relationship extraction patterns
│
├── examples/                   # Domain examples
│   └── example-schemas.md      # University, E-commerce, Healthcare, Social Network
│
└── scripts/                    # Utility scripts
    └── schema_extractor.py     # Schema extraction implementation
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand what the skill does
2. **Learn:** `references/extraction-patterns.md` - How to extract schema elements
3. **See:** `examples/example-schemas.md` - Real domain examples

### For Implementation

1. Use `scripts/schema_extractor.py` as reference implementation
2. Supports: Entity extraction, relationship extraction, property extraction
3. Generates: Cypher statements, RDF/Turtle output

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, overview, use cases |
| `extraction-patterns.md` | Extraction patterns & normalization rules |
| `example-schemas.md` | 4 domain examples (University, E-commerce, Healthcare, Social) |
| `schema_extractor.py` | Python implementation for schema extraction |

## ⚡ Key Features

✓ Entity extraction from text  
✓ Relationship extraction and direction  
✓ Property identification  
✓ Schema normalization  
✓ Output in Cypher & RDF/Turtle formats  

## 🔗 Usage Example

```python
from scripts.schema_extractor import SchemaExtractor

text = """
A library contains books and members.
Members borrow books. Librarians manage members and books.
"""

extractor = SchemaExtractor()
schema = extractor.extract_schema(text)

print(schema)
# Generates: entities, relationships, properties
```

## 📖 See Also

- Skill Definition: `SKILL.md`
- Extraction Patterns: `references/extraction-patterns.md`
- Domain Examples: `examples/example-schemas.md`
- Implementation: `scripts/schema_extractor.py`

---

**Lean, focused modular structure - only core functionality needed for this skill.**

