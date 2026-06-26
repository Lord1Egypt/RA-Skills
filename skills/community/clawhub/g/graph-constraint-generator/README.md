# Graph Constraint Generator - Quick Reference

Modular structure for the **graph-constraint-generator** skill - generates constraints for knowledge graph schemas.

## 📁 Structure

```
graph-constraint-generator/
│
├── SKILL.md                    # Skill definition & overview
│
├── references/                 # Technical guidance
│   └── constraint-patterns.md  # Constraint design patterns
│
├── examples/                   # Domain examples
│   └── example-constraints.md  # University, E-Commerce, RDF, Social
│
└── scripts/                    # Utility scripts
    └── constraint_generator.py # ConstraintGenerator implementation
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand constraint generation
2. **Learn:** `references/constraint-patterns.md` - Design patterns
3. **See:** `examples/example-constraints.md` - Real constraint examples

### For Implementation

1. Use `scripts/constraint_generator.py` for generating constraints
2. Supports: Unique, required, cardinality, domain/range constraints
3. Generates: Cypher DDL, SHACL shapes, validation queries

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, overview, use cases |
| `constraint-patterns.md` | Constraint generation patterns & best practices |
| `example-constraints.md` | 4 domain constraint examples |
| `constraint_generator.py` | Python ConstraintGenerator class |

## ⚡ Key Features

✓ Unique constraint generation  
✓ Required property constraints  
✓ Cardinality constraint definition  
✓ Domain/range constraints  
✓ Cypher constraint output  
✓ SHACL shape generation  
✓ Validation query generation  

## 🔗 Usage Example

```python
from scripts.constraint_generator import ConstraintGenerator

# Create generator
gen = ConstraintGenerator("University")

# Add labels
gen.add_label("Student")
gen.add_label("Course")

# Add constraints
gen.add_unique_constraint("Student", "student_id")
gen.add_required_property("Student", "name")
gen.add_cardinality_constraint("Student", "ENROLLED_IN", "Course", 
                               min_count=1, max_count=10)

# Print and generate
gen.print_constraints()
cypher = gen.generate_cypher_constraints()
shacl = gen.generate_shacl_shapes()
```

## 📖 See Also

- Skill Definition: `SKILL.md`
- Constraint Patterns: `references/constraint-patterns.md`
- Examples: `examples/example-constraints.md`
- Implementation: `scripts/constraint_generator.py`

---

**Lean, focused modular structure - only core functionality for constraint generation.**

