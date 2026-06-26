# Ontology-Based Inference Helper - Quick Reference

Apply semantic ontology rules to knowledge graphs to infer new relationships, class memberships, and properties from explicit ontology definitions.

## 📁 Structure

```
ontology-based-inference-helper/
│
├── SKILL.md                         # Skill definition & overview
│
├── references/                      # Technical guidance
│   └── ontology-patterns.md         # Inference patterns & strategies
│
├── examples/                        # Domain examples
│   └── ontology-examples.md         # Real-world ontology applications
│
└── scripts/                         # Utility scripts
    └── ontology_inference_engine.py # OntologyInferenceEngine implementation
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand ontology-based inference fundamentals
2. **Learn:** `references/ontology-patterns.md` - Inference patterns and strategies
3. **See:** `examples/ontology-examples.md` - Real-world ontology examples

### For Implementation

1. Use `scripts/ontology_inference_engine.py` for ontology reasoning
2. Supports: Ontology parsing, rule-based inference, semantic reasoning
3. Features: Class hierarchies, property inheritance, domain/range inference

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, use cases, concepts |
| `ontology-patterns.md` | Inference patterns, reasoning strategies, optimization |
| `ontology-examples.md` | Business, scientific, semantic web examples |
| `ontology_inference_engine.py` | Python OntologyInferenceEngine class |

## ⚡ Key Features

✓ Support for RDF/OWL ontology standards  
✓ Subclass hierarchy inference  
✓ Property domain and range inference  
✓ Property inheritance rules  
✓ Symmetric and inverse property handling  
✓ Transitive property closure  
✓ Class membership inference  
✓ Semantic consistency checking  
✓ Rule caching for performance  
✓ Batch materialization  

## 🧠 Ontology Concepts

### Class Hierarchy
Hierarchical organization of concepts with inheritance.

```
Vehicle (root class)
  ├── Car (subclass)
  │   └── ElectricCar
  └── Truck (subclass)
```

### Property Inheritance
Properties inherited through class hierarchies.

```
Vehicle.hasOwner → Car.hasOwner (inherited)
Vehicle.hasColor → Car.hasColor (inherited)
```

### Domain and Range
Type constraints on property usage.

```
hasOwner domain: Vehicle
hasOwner range: Person
```

### Transitive Properties
Properties that propagate through chains.

```
partOf transitive: A partOf B, B partOf C → A partOf C
```

## 🔗 Usage Example

```python
from scripts.ontology_inference_engine import OntologyInferenceEngine, OntologyConfig

# Create inference engine
config = OntologyConfig(
    ontology_data={
        "classes": {
            "Vehicle": {"parent": None},
            "Car": {"parent": "Vehicle"},
            "ElectricCar": {"parent": "Car"}
        },
        "properties": {
            "hasOwner": {"domain": "Vehicle", "range": "Person"},
            "hasColor": {"domain": "Vehicle", "range": "String"}
        },
        "individuals": {
            "Tesla": {"type": "ElectricCar"}
        }
    }
)

engine = OntologyInferenceEngine(config)

# Apply inference rules
inferred = engine.apply_inference()

# Get inferred class memberships
classes = engine.get_inferred_classes("Tesla")
print(f"Tesla is a: {classes}")
# Output: Tesla is a: [ElectricCar, Car, Vehicle]
```

## 🧬 Key Concepts

### Explicit Knowledge
Facts explicitly stated in the ontology or graph.

### Implicit Knowledge
Facts that can be inferred from ontology rules.

### Class Membership
Which classes an individual belongs to (can be inferred from hierarchies).

### Property Inheritance
Properties inherited by subclasses from parent classes.

### Semantic Consistency
Ensuring inferred facts don't violate ontology constraints.

## 📖 See Also

- Skill Definition: `SKILL.md`
- Ontology Patterns: `references/ontology-patterns.md`
- Examples: `examples/ontology-examples.md`
- Implementation: `scripts/ontology_inference_engine.py`

---

**Production-ready modular structure - complete ontology reasoning toolkit for knowledge graphs.**


