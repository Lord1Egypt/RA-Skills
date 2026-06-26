# Graph Schema Validation - Quick Reference

Modular structure for the **graph-schema-validation** skill - validates graph schemas and data against defined constraints.

## 📁 Structure

```
graph-schema-validation/
│
├── SKILL.md                    # Skill definition & overview
│
├── references/                 # Technical guidance
│   └── validation-patterns.md  # Validation patterns & best practices
│
├── examples/                   # Domain examples
│   └── example-validations.md  # University, E-Commerce, RDF, Social
│
└── scripts/                    # Utility scripts
    └── schema_validator.py     # SchemaValidator implementation
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand schema validation
2. **Learn:** `references/validation-patterns.md` - Validation patterns
3. **See:** `examples/example-validations.md` - Real validation examples

### For Implementation

1. Use `scripts/schema_validator.py` for building validators
2. Supports: Rules, constraints, violation detection, reporting
3. Generates: Validation reports with suggestions

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, overview, use cases |
| `validation-patterns.md` | Validation patterns & best practices |
| `example-validations.md` | 4 domain validation examples |
| `schema_validator.py` | Python SchemaValidator class |

## ⚡ Key Features

✓ Required property validation  
✓ Unique constraint enforcement  
✓ Cardinality constraint checking  
✓ Enum value validation  
✓ Relationship validation  
✓ Graph integrity checking  
✓ Detailed violation reporting  
✓ Suggestions for fixes  

## 🔗 Usage Example

```python
from scripts.schema_validator import SchemaValidator, ViolationType

# Create validator
validator = SchemaValidator("University")

# Add rules
validator.add_required_property("Student", "student_id")
validator.add_unique_constraint("Student", "student_id")
validator.add_enum_constraint("Course", "status", ["Active", "Inactive"])

# Load and validate data
data = [
    {"id": "S001", "label": "Student", "student_id": "001", "name": "Alice"},
    {"id": "S002", "label": "Student", "name": "Bob"},  # Missing student_id!
]
validator.load_data(data)
validator.validate()

# Get report
validator.print_report()
```

## 📖 See Also

- Skill Definition: `SKILL.md`
- Validation Patterns: `references/validation-patterns.md`
- Examples: `examples/example-validations.md`
- Implementation: `scripts/schema_validator.py`

---

**Lean, focused modular structure - only core functionality for graph schema validation.**

