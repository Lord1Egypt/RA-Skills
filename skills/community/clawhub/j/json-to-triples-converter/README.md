# JSON to Triples Converter - Quick Reference

Modular structure for the **json-to-triples-converter** skill - converts JSON documents into RDF triples and graph-ready structures.

## 📁 Structure

```
json_to_triples_converter/
│
├── SKILL.md                         # Skill definition & overview
│
├── references/                      # Technical guidance
│   └── conversion-patterns.md       # JSON-to-triples conversion patterns
│
├── examples/                        # Domain examples
│   └── example-conversions.md       # Real JSON-to-triple examples
│
└── scripts/                         # Utility scripts
    └── json_converter.py            # JSONTriplesConverter implementation
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand JSON-to-triples conversion
2. **Learn:** `references/conversion-patterns.md` - Conversion patterns
3. **See:** `examples/example-conversions.md` - Real examples

### For Implementation

1. Use `scripts/json_converter.py` for converting JSON to triples
2. Supports: RDF Turtle, N-Triples, JSON-LD, Graph JSON
3. Generates: Semantic triples, linked data, knowledge graphs

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, overview, use cases |
| `conversion-patterns.md` | JSON-to-triples conversion patterns & best practices |
| `example-conversions.md` | Real-world JSON conversion examples |
| `json_converter.py` | Python JSONTriplesConverter class |

## ⚡ Key Features

✓ Multiple JSON-to-triple conversion strategies  
✓ Entity detection and relationship inference  
✓ Namespace and URI management  
✓ Multiple output formats (RDF Turtle, N-Triples, JSON-LD, Graph JSON)  
✓ Nested object flattening  
✓ Entity deduplication  
✓ Schema.org vocabulary mapping  
✓ Custom mapping rule support  
✓ Data type and literal inference  
✓ Batch conversion support  

## 🔗 Usage Example

```python
from scripts.json_converter import JSONTriplesConverter

# Create converter
converter = JSONTriplesConverter(
    base_namespace="http://example.org/",
    output_format="turtle"
)

# Define mapping rules
converter.add_entity_mapping("person", "Person")
converter.add_entity_mapping("company", "Organization")

# Convert JSON to triples
json_data = {
    "person": {
        "name": "Alice",
        "age": 30,
        "company": "Acme"
    }
}

triples = converter.convert(json_data)
output = converter.to_turtle()
print(output)
```

## 📖 See Also

- Skill Definition: `SKILL.md`
- Conversion Patterns: `references/conversion-patterns.md`
- Examples: `examples/example-conversions.md`
- Implementation: `scripts/json_converter.py`

---

**Lean, focused modular structure - only core functionality for JSON to triples conversion.**


