# Mapping DSL Builder - Quick Reference

Modular structure for the **mapping-dsl-builder** skill - generates declarative mapping rules that transform structured data into graph entities using a domain-specific language.

## 📁 Structure

```
mapping-dsl-builder/
│
├── SKILL.md                         # Skill definition & overview
│
├── references/                      # Technical guidance
│   └── mapping-patterns.md          # DSL mapping design patterns
│
├── examples/                        # Domain examples
│   └── example-mappings.md          # Real mapping examples
│
└── scripts/                         # Utility scripts
    └── dsl_builder.py               # MappingDSLBuilder implementation
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand mapping DSL generation
2. **Learn:** `references/mapping-patterns.md` - Mapping patterns
3. **See:** `examples/example-mappings.md` - Real examples

### For Implementation

1. Use `scripts/dsl_builder.py` for creating mapping specifications
2. Supports: Database, CSV, JSON, API sources
3. Generates: Mapping DSL, R2RML, YAML, Property Graph mappings

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, overview, use cases |
| `mapping-patterns.md` | DSL mapping patterns & best practices |
| `example-mappings.md` | Real-world mapping examples |
| `dsl_builder.py` | Python MappingDSLBuilder class |

## ⚡ Key Features

✓ Multiple data source support (DB, CSV, JSON, API)  
✓ Entity mapping and identification  
✓ Property and relationship mapping  
✓ Multiple output formats (Custom DSL, R2RML, YAML)  
✓ URI template generation  
✓ Declarative transformation rules  
✓ Reusable mapping configurations  
✓ Schema analysis and inference  
✓ Data type handling  
✓ Foreign key relationship detection  

## 🔗 Usage Example

```python
from scripts.dsl_builder import MappingDSLBuilder

# Create builder
builder = MappingDSLBuilder(name="employee_mapping")

# Define source
builder.set_source(source_type="database", table="employee")

# Define entity mapping
builder.add_entity_mapping(
    entity_type="Person",
    id_column="id"
)

# Define properties
builder.add_property_mapping("name", "name")
builder.add_property_mapping("email", "email_address")

# Define relationships
builder.add_relationship_mapping(
    relationship_name="WORKS_AT",
    target_table="company",
    foreign_key="company_id"
)

# Generate mapping
mapping_dsl = builder.to_dsl()
mapping_r2rml = builder.to_r2rml()
mapping_yaml = builder.to_yaml()
```

## 📖 See Also

- Skill Definition: `SKILL.md`
- Mapping Patterns: `references/mapping-patterns.md`
- Examples: `examples/example-mappings.md`
- Implementation: `scripts/dsl_builder.py`

---

**Lean, focused modular structure - only core functionality for mapping DSL generation.**


