# Graph Rule Engine Builder - Quick Reference

Create rule-based reasoning systems for knowledge graphs that infer new relationships and facts from existing data using declarative logic rules.

## 📁 Structure

```
graph-rule-engine-builder/
│
├── SKILL.md                         # Skill definition & overview
│
├── references/                      # Technical guidance
│   └── graph-rule-patterns.md       # Rule patterns & strategies
│
├── examples/                        # Domain examples
│   └── graph-rule-examples.md       # Real-world rule applications
│
└── scripts/                         # Utility scripts
    └── graph_rule_engine.py         # GraphRuleEngine implementation
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand rule-based reasoning fundamentals
2. **Learn:** `references/graph-rule-patterns.md` - Rule patterns and execution strategies
3. **See:** `examples/graph-rule-examples.md` - Real-world rule applications

### For Implementation

1. Use `scripts/graph_rule_engine.py` for rule execution
2. Supports: Rule definition, pattern matching, inference, validation
3. Features: Multiple rule types, constraint checking, materialization strategies

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, use cases, concepts |
| `graph-rule-patterns.md` | Rule patterns, execution strategies, optimization |
| `graph-rule-examples.md` | Business rules, fraud detection, recommendation rules |
| `graph_rule_engine.py` | Python GraphRuleEngine class |

## ⚡ Key Features

✓ Define inference rules with IF-THEN logic  
✓ Match graph patterns for rule conditions  
✓ Derive new relationships automatically  
✓ Support multiple rule types (derivation, constraint, aggregation)  
✓ Constraint-based filtering and validation  
✓ Forward and backward chaining  
✓ Cycle detection and prevention  
✓ Rule optimization and scheduling  
✓ Materialization and persistence  
✓ Rule conflict resolution  

## 🧠 Rule Engine Concepts

### Inference Rule
An IF-THEN rule that derives new facts from existing patterns.

```
IF (Person)-[WORKS_AT]->(Company)
   AND (Person)-[WORKS_AT]->(Company)
THEN (Person)-[COLLEAGUE_OF]->(Person)
```

### Derivation Rule
Creates new relationships based on patterns.

```
IF (A)-[BORN_IN]->(City)
   AND (City)-[LOCATED_IN]->(Country)
THEN (A)-[BORN_IN_COUNTRY]->(Country)
```

### Constraint Rule
Validates data and flags violations.

```
IF (Account)-[TRANSFERRED]->(Account)
   AND (Account)-[TRANSFERRED]->(Account)
   AND (Account)-[TRANSFERRED]->(Account)
THEN Flag(FraudRing)
```

### Aggregation Rule
Computes metrics from graph patterns.

```
IF aggregate(count((Person)-[WORKS_AT]->(Company)))
THEN Company.employee_count = count
```

## 🔗 Usage Example

```python
from scripts.graph_rule_engine import GraphRuleEngine, RuleConfig, Rule

# Create rule engine
config = RuleConfig(
    graph_data={
        "nodes": {"Alice": {}, "Bob": {"role": "Manager"}, "TechCorp": {}},
        "edges": [
            {"source": "Alice", "target": "TechCorp", "type": "works_at"},
            {"source": "Bob", "target": "TechCorp", "type": "works_at"}
        ]
    }
)

engine = GraphRuleEngine(config)

# Define and add rules
colleague_rule = Rule(
    name="colleague_inference",
    condition="(a)-[WORKS_AT]->(c)<-[WORKS_AT]-(b)",
    inference="(a)-[COLLEAGUE_OF]->(b)",
    rule_type="derivation"
)

engine.add_rule(colleague_rule)

# Execute rules
results = engine.execute_rules()
print(f"Inferred {len(results['inferred_edges'])} new relationships")

# Get inferred facts
inferred = engine.get_inferred_facts()
for fact in inferred:
    print(f"  {fact['source']} --{fact['type']}--> {fact['target']}")
```

## 📖 See Also

- Skill Definition: `SKILL.md`
- Rule Patterns: `references/graph-rule-patterns.md`
- Examples: `examples/graph-rule-examples.md`
- Implementation: `scripts/graph_rule_engine.py`

---

**Production-ready modular structure - complete rule-based reasoning toolkit for knowledge graphs.**


