---
name: graph_rule_engine_builder
title: Graph Rule Engine Builder
description: Create rule-based reasoning systems for knowledge graphs that infer new relationships and facts from existing data using declarative logic rules. Supports derivation, constraint, aggregation, and conditional rules with cycle detection.
category: reasoning
tags:
  - knowledge-graph
  - reasoning
  - rule-engine
  - inference
  - logic-programming
  - graph-reasoning
  - derivation-rules
  - constraint-checking
  - forward-chaining
  - backward-chaining
version: 1.0.0
author: community
license: MIT
metadata:
  {"openclaw":{"emoji":"🧩","homepage":"https://clawhub.com"}}
---

# Graph Rule Engine Builder

**Create rule-based reasoning systems for knowledge graphs that derive new relationships and facts from existing data.**

This skill enables comprehensive rule-based inference by defining declarative logic rules that automatically derive new knowledge, validate constraints, and apply business logic to graph data.

## Quick Start

### Use When
- Defining inference rules for knowledge graphs
- Deriving new relationships automatically
- Creating constraint-based validation
- Building semantic reasoning systems
- Implementing fraud detection rules
- Designing recommendation logic
- Applying business rules to graphs
- Materializing inferred facts

### Inputs
- Knowledge graph structure
- Rule definitions (patterns and inferences)
- Constraint specifications
- Execution parameters (forward/backward chaining, materialization)

### Outputs
- Inferred relationships and facts
- Constraint violations and alerts
- Aggregated metrics
- Materialized triple sets
- Rule execution statistics

## Rule Engine Concepts

### Inference Rule
Derives new facts from existing patterns using IF-THEN logic.

```
IF (Person)-[WORKS_AT]->(Company)
   AND (Person2)-[WORKS_AT]->(Company)
THEN (Person)-[COLLEAGUE_OF]->(Person2)
```

Properties: Declarative, deterministic, generates new knowledge

### Derivation Rule
Creates transitive or hierarchical relationships.

```
IF (A)-[BORN_IN]->(City)
   AND (City)-[LOCATED_IN]->(Country)
THEN (A)-[BORN_IN_COUNTRY]->(Country)
```

Use: Geographic inference, hierarchies, transitive closure

### Constraint Rule
Validates data and flags violations.

```
IF (Account)-[TRANSFERRED]->(Account)
   AND (Account)-[TRANSFERRED]->(Account)
   AND (Account)-[TRANSFERRED]->(Account)
THEN Flag(FraudRing, confidence=0.95)
```

Use: Fraud detection, compliance, data validation

### Aggregation Rule
Computes metrics from patterns.

```
IF aggregate(count((Employee)-[WORKS_AT]->(Company)))
THEN Company.employee_count = count
```

Use: Analytics, metrics, summarization

### Conditional Rule
Applies logic with conditions.

```
IF (Person)-[AGE]->(age)
   AND age > 65
THEN (Person)-[STATUS]->(Retired)
```

Use: Classification, segmentation, categorization

## Rule Execution Models

### Forward Chaining
Apply all rules to derive all possible inferences (data-driven).

```
1. Load graph data
2. Find all rule pattern matches
3. Apply THEN inferences
4. Repeat until fixpoint (no new inferences)
```

Best For: Complete materialization, data warehouse
Complexity: May be expensive for large graphs

### Backward Chaining
Query-driven inference - derive facts only when queried.

```
1. Receive query for fact (person)-[COLLEAGUE_OF]->(other)
2. Check if exists in graph
3. If not, try rules with COLLEAGUE_OF as consequence
4. Recursively check rule conditions
```

Best For: Lazy evaluation, query optimization
Complexity: Lower memory, higher query latency

### Hybrid Approach
Combine forward and backward chaining.

```
Forward chain core rules → Materialized facts
Backward chain on-demand rules → Query results
```

Best For: Balanced performance and completeness

## Rule Definition Syntax

### Basic Structure

```
Rule Name: colleague_inference
Type: derivation
Priority: 100

Condition (IF):
  MATCH (person1:Person)-[:WORKS_AT]->(company:Company)
  MATCH (person2:Person)-[:WORKS_AT]->(company:Company)
  WHERE person1 != person2

Inference (THEN):
  CREATE (person1)-[:COLLEAGUE_OF]->(person2)
  CREATE (person2)-[:COLLEAGUE_OF]->(person1)

Constraints:
  Cycle Detection: true
  Materialization: true
```

### Pattern Matching

Supported patterns:

```
(n)                              Single node
(n:Label)                        Node with label
(n {prop: value})                Node with property
(n)-[r]->(m)                     Relationship
(n)-[r:TYPE]->(m)                Typed relationship
(a)-[:TYPE*1..3]->(b)            Variable-length path
(a)-[:TYPE1|:TYPE2]->(b)         Multiple relationship types
```

### Constraints

```
WHERE conditions:
  n.property = value
  n.age > 21
  NOT exists(n)-[:EXCLUDES]->(m)
  size(n.tags) > 0
  
Aggregate conditions:
  count(nodes) > 10
  avg(property) < 50
  sum(values) = 100
```

## Rule Types & Implementations

### Type 1: Transitive Derivation
Extend relationships transitively.

```
IF (a)-[REL]->(b)
   AND (b)-[REL]->(c)
THEN (a)-[REL_TRANSITIVE]->(c)
```

Example: Manager chains, geographic nesting

### Type 2: Multi-Relationship Derivation
Combine multiple relationship types.

```
IF (a)-[BORN_IN]->(city)
   AND (city)-[LOCATED_IN]->(country)
   AND (country)-[PART_OF]->(region)
THEN (a)-[BORN_IN_REGION]->(region)
```

### Type 3: Property Computation
Derive properties from relationships.

```
IF (person)-[WORKS_AT]->(company)
   AND aggregate(count(person)) as count
THEN company.employee_count = count
```

### Type 4: Conditional Classification
Apply rules conditionally.

```
IF (person)-[AGE]->(age)
   WHERE age >= 65
THEN (person)-[LIFECYCLE_STAGE]->(Retired)

IF (person)-[AGE]->(age)
   WHERE age < 25
THEN (person)-[LIFECYCLE_STAGE]->(Junior)
```

### Type 5: Anomaly Detection
Flag patterns matching suspicious rules.

```
IF (account1)-[TRANSFERRED]->(account2)
   AND (account2)-[TRANSFERRED]->(account3)
   AND (account3)-[TRANSFERRED]->(account1)
   AND NOT EXISTS (account1)-[AUTHORIZED_TRANSFER]->(account3)
THEN Flag(TransferCycle, risk_level=HIGH)
```

## Cycle Detection & Prevention

### Circular Rule Detection
Detect rules that could cause infinite loops.

```
Rule A: IF X THEN Y
Rule B: IF Y THEN X
→ Circular dependency detected!
```

### Strategies

1. **Explicit Cycle Limit**: Stop after N iterations
2. **Fixpoint Detection**: Stop when no new inferences
3. **Recursive Depth Limit**: Maximum recursion depth
4. **Manual Cycle Prevention**: Annotate acyclic rules

## Rule Optimization

### Indexing
Create indexes on frequently matched properties.

```
Index on: Person.age, Company.name
Benefit: Faster pattern matching
```

### Rule Ordering
Execute high-impact, low-cost rules first.

```
Rule Priority:
1. Simple derivations (low cost, high impact)
2. Complex pattern matches (high cost)
3. Constraint checks (validation)
4. Aggregations (expensive computations)
```

### Incremental Inference
Update inferences only on data changes.

```
On Insert (person)-[WORKS_AT]->(company):
  → Check all rules with WORKS_AT pattern
  → Derive only affected consequences
  → Update materialized views
```

## Materialization Strategies

### Full Materialization
Compute and store all inferences.

```
Pros: Fast queries, explicit facts
Cons: Storage cost, update latency, staleness
```

### Lazy Materialization
Compute on-demand during queries.

```
Pros: Storage efficient, always current
Cons: Query latency, repeated computation
```

### Partial Materialization
Materialize important inferences, compute others on-demand.

```
Pros: Balanced approach
Implementation: Tier inferences by importance
```

## Rule Conflict Resolution

### Priority-Based
Rules with higher priority execute first.

```
Rule A (priority=100): (a)-[R]->(b) THEN (a)-[T]->(b)
Rule B (priority=50): (a)-[R]->(b) THEN (a)-[U]->(b)
→ Rule A executes first
```

### Specificity-Based
More specific patterns override general ones.

```
General: (a)-[REL]->(b) THEN ...
Specific: (a:Person)-[REL]->(b:Person) THEN ...
→ Specific rule wins for Person nodes
```

### Temporal-Based
Later rules override earlier ones.

```
v1: IF condition THEN inference1
v2: IF condition THEN inference2 (overrides v1)
```

## Error Handling

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Infinite loops | Circular rules | Enable cycle detection, set depth limit |
| Duplicate inferences | Multiple matching rules | Add constraints, use priorities |
| Memory overflow | Too many inferences | Lazy materialization, limit scope |
| Performance degradation | Complex patterns | Index optimization, rule reordering |
| Constraint violations | Invalid inferences | Add validation, pre-check rules |
| Stale materialized facts | Data changes not applied | Incremental updates, refresh triggers |

## Best Practices

✓ **Define rules clearly** - Use consistent patterns and naming  
✓ **Avoid circular dependencies** - Design acyclic rule sets  
✓ **Test rules thoroughly** - Validate inferences before materialization  
✓ **Use priorities wisely** - Order rules by cost and impact  
✓ **Index strategically** - Index frequently matched properties  
✓ **Consider materialization** - Choose strategy based on query patterns  
✓ **Document assumptions** - Clarify rule semantics and constraints  
✓ **Monitor performance** - Track rule execution times  
✓ **Version rules** - Allow rule evolution and rollback  
✓ **Validate inferred data** - Check quality before use  

## Advanced Features

### Rule Composition
Combine rules to build complex inference chains.

### Negation as Failure
Support negative conditions (NOT EXISTS).

### Rule Learning
Generate rules from examples or patterns.

### Temporal Rules
Rules that consider timestamps and time windows.

### Probabilistic Rules
Rules with confidence scores and uncertainty.

### Cross-Graph Rules
Apply rules spanning multiple graphs or sources.

## Integration Points

This skill integrates with:

- **Causal Chain Analyzer** - Understand causal rule implications
- **Graph Path Reasoning Analyzer** - Analyze derivation paths
- **Transitive Closure Generator** - Compute rule consequences
- **Graph Query Optimizer** - Optimize rule queries
- **Multi-Hop Reasoning Query Builder** - Build complex rule queries

## Recommended Libraries

### Rule Engines
- `Drools` - Java rule engine
- `Prolog` - Logic programming
- `Rete` - Rule matching algorithm
- `networkx` - Graph algorithms

### Pattern Matching
- `regex` - Pattern matching
- `pyparsing` - Grammar parsing
- `antlr4-python3-runtime` - Parser generator

### Inference
- `pyswip` - Python-Prolog integration
- `owlready2` - OWL ontology reasoning

### Graph Libraries
- `rdflib` - RDF/SPARQL
- `neo4j` - Neo4j driver

## Related Skills

- **Causal Chain Analyzer** - Analyze rule implications
- **Graph Path Reasoning Analyzer** - Find derivation paths
- **Transitive Closure Generator** - Compute closure
- **Ontology-Based Inference Helper** - Semantic rules
- **Multi-Hop Reasoning Query Builder** - Complex queries

---

**Version:** 1.0.0
