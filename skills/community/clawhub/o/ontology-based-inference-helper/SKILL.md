---
name: ontology_based_inference_helper
title: Ontology-Based Inference Helper
description: Apply semantic ontology rules to knowledge graphs to infer new relationships, class memberships, and properties from explicit ontology definitions. Supports RDF/OWL standards, class hierarchies, property inheritance, and domain/range constraints.
category: reasoning
tags:
  - knowledge-graph
  - reasoning
  - ontology
  - inference
  - semantic-web
  - rdf
  - owl
  - class-hierarchy
  - property-inheritance
  - domain-range
version: 1.0.0
author: community
license: MIT
metadata:
  {"openclaw":{"emoji":"🧬","homepage":"https://clawhub.com"}}
---

# Ontology-Based Inference Helper

**Apply semantic ontology rules to knowledge graphs to infer new relationships and facts from explicit definitions.**

This skill enables comprehensive ontology reasoning by applying RDF/OWL-based inference rules that automatically expand knowledge graphs through class hierarchies, property inheritance, and semantic constraints.

## Quick Start

### Use When
- Working with RDF/OWL ontologies
- Inferring class memberships from hierarchies
- Applying property inheritance rules
- Expanding knowledge graphs semantically
- Validating semantic consistency
- Deriving implicit relationships
- Building semantic web applications
- Materializing ontology inferences

### Inputs
- Ontology definitions (classes, properties, constraints)
- Graph individuals (instances)
- Inference rule types to apply
- Optional: Domain-specific ontology (RDFS, OWL)

### Outputs
- Inferred class memberships
- Derived relationships
- Expanded property assignments
- Semantic consistency results
- Materialized triple sets

## Ontology Concepts

### Class Hierarchy
Hierarchical organization of concepts with subclass relationships.

```
Thing (root)
  ├── PhysicalObject
  │   ├── Vehicle
  │   │   ├── Car
  │   │   │   └── ElectricCar
  │   │   └── Truck
  │   └── Animal
  │       ├── Mammal
  │       └── Bird
  └── AbstractConcept
```

Properties: Inheritance, specialization, polymorphism

### Class Membership
Individuals are instances of classes; inheritance propagates membership.

```
tesla:Individual
  type: ElectricCar
  (inherited) type: Car
  (inherited) type: Vehicle
  (inherited) type: PhysicalObject
  (inherited) type: Thing
```

### Property Definitions
Properties have domain (source class) and range (target type).

```
Property: hasOwner
  domain: Vehicle      # hasOwner applies to Vehicles
  range: Person        # hasOwner points to Person
  inverse: owns        # owns is inverse of hasOwner

Property: hasColor
  domain: PhysicalObject
  range: Color
```

### Property Inheritance
Subclasses inherit property definitions from parent classes.

```
Vehicle.hasOwner → Car.hasOwner (inherited)
Vehicle.hasColor → ElectricCar.hasColor (inherited)
```

### Inverse Properties
Properties with inverse relationships (e.g., hasOwner ↔ owns).

```
A hasOwner B  ⇒  B owns A (by inverse property)
married_to inverse married_to  ⇒  A married_to B  ⇒  B married_to A
```

### Transitive Properties
Properties where chaining implies relationship.

```
transitiveProperty: partOf
  A partOf B ∧ B partOf C  ⇒  A partOf C

transitiveProperty: locatedIn
  Paris locatedIn France ∧ France locatedIn Europe  ⇒  Paris locatedIn Europe
```

## Ontology Inference Rules

### Rule 1: Subclass Membership Inference

If X is instance of A and A is subclass of B, then X is instance of B.

```
IF
  X instance_of A
  A subclass_of B
THEN
  X instance_of B
```

Example:
```
tesla instance_of Car
Car subclass_of Vehicle
⇒ tesla instance_of Vehicle
```

**Application:** Materializing full class hierarchy for each individual

---

### Rule 2: Property Domain Inference

If property P has domain D and P is used with subject S, then S is instance of D.

```
IF
  property P has domain D
  S P O
THEN
  S instance_of D
```

Example:
```
hasOwner domain Vehicle
john_car hasOwner jane
⇒ john_car instance_of Vehicle
```

---

### Rule 3: Property Range Inference

If property P has range R and P is used with object O, then O is instance of R.

```
IF
  property P has range R
  S P O
THEN
  O instance_of R
```

Example:
```
hasOwner range Person
john_car hasOwner jane
⇒ jane instance_of Person
```

---

### Rule 4: Property Inheritance

If property P belongs to class A, and B is subclass of A, then property P belongs to B.

```
IF
  class A has property P
  B subclass_of A
THEN
  class B has property P
```

---

### Rule 5: Subproperty Inference

If property P is subproperty of Q and (S P O), then (S Q O).

```
IF
  P subproperty_of Q
  S P O
THEN
  S Q O
```

Example:
```
son subproperty_of child
alice son bob
⇒ alice child bob
```

---

### Rule 6: Inverse Property Inference

If property P is inverse of Q and (S P O), then (O Q S).

```
IF
  P inverse_of Q
  S P O
THEN
  O Q S
```

Example:
```
hasOwner inverse_of owns
vehicle hasOwner person
⇒ person owns vehicle
```

---

### Rule 7: Symmetric Property Inference

If property P is symmetric and (S P O), then (O P S).

```
IF
  P is symmetric
  S P O
THEN
  O P S
```

Example:
```
knows symmetric
alice knows bob
⇒ bob knows alice
```

---

### Rule 8: Transitive Property Closure

If property P is transitive and (S P M) and (M P O), then (S P O).

```
IF
  P is transitive
  S P M
  M P O
THEN
  S P O
```

Example:
```
ancestor transitive
alice ancestor bob
bob ancestor charlie
⇒ alice ancestor charlie
```

---

## Inference Strategies

### Forward Chaining Materialization
Eagerly apply all inference rules to derive complete closure.

```
Algorithm:
1. Load ontology and individuals
2. Apply rules iteratively until fixpoint
3. Store all inferred facts
4. Index for fast querying
```

**Pros:** Complete, fast queries  
**Cons:** Storage cost, upfront computation  
**Best For:** OLAP, offline reasoning

---

### Backward Chaining Resolution
Query-driven inference - derive facts only when queried.

```
Algorithm:
1. Receive query for fact
2. Check explicit facts
3. If not found, apply rules backward
4. Return proof or empty
```

**Pros:** Storage efficient, on-demand  
**Cons:** Query latency, repeated computation  
**Best For:** OLTP, large graphs

---

### Hybrid Approach
Combine materialization for common facts with backward chaining for rare ones.

```
Materialize: Subclass membership, property domain/range
Backward chain: Transitive closure, complex paths
```

---

## Ontology Standards Support

### RDF (Resource Description Framework)
- Triple model: (subject, predicate, object)
- Namespace support
- URI-based identifiers

### RDFS (RDF Schema)
- Class and property definitions
- Subclass/subproperty relationships
- Domain and range constraints

### OWL (Web Ontology Language)
- Richer semantics than RDFS
- Class restrictions and logical operators
- Advanced property characteristics (transitive, symmetric, inverse)

### Property Graph Extensions
- Ontology support on property graphs
- Type systems and hierarchies
- Custom property constraints

## Semantic Consistency

### Type Checking
Verify property domain/range constraints.

```
hasOwner domain Vehicle
john_car hasOwner "red"  ← Type violation! "red" is not Person
```

### Hierarchy Validation
Ensure no contradictory subclass relationships.

```
A subclass_of B
B subclass_of C
NOT (C subclass_of A)  ← Would create cycle
```

### Constraint Satisfaction
Enforce cardinality, uniqueness, and other constraints.

```
hasOwner cardinality 1  ← Each vehicle has exactly one owner
```

## Error Handling

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Infinite loops | Cyclic properties | Detect cycles, limit depth |
| Memory overflow | Too many inferences | Selective materialization |
| Type violations | Domain/range mismatches | Validation, filtering |
| Inconsistencies | Contradictory rules | Detect, flag, or resolve |
| Performance degradation | Expensive transitive closure | Caching, incremental updates |
| Missing inferences | Incomplete ontology | Augment definitions |

## Best Practices

✓ **Define ontologies clearly** - Use consistent naming and structure  
✓ **Minimize cyclic dependencies** - Design acyclic hierarchies  
✓ **Choose inference strategy wisely** - Match to query patterns  
✓ **Cache inference results** - Reuse computed closures  
✓ **Validate ontology consistency** - Check before inference  
✓ **Handle inverse properties carefully** - Avoid redundant storage  
✓ **Document semantic assumptions** - Clarify rule semantics  
✓ **Monitor inference performance** - Track computation time  
✓ **Version ontologies** - Enable evolution and rollback  
✓ **Test with sample data** - Validate inference correctness  

## Advanced Features

### Custom Inference Rules
Define domain-specific reasoning beyond OWL.

### Fuzzy Inference
Support uncertain or probabilistic reasoning.

### Temporal Ontologies
Time-aware class hierarchies and properties.

### Cross-Ontology Reasoning
Align and reason over multiple ontologies.

### Ontology Alignment
Map concepts between different ontologies.

### Explanation Generation
Provide derivation traces and proof chains.

## Integration Points

This skill integrates with:

- **Graph Rule Engine Builder** - Define custom inference rules
- **Causal Chain Analyzer** - Understand inference chains
- **Graph Path Reasoning Analyzer** - Analyze derivation paths
- **Transitive Closure Generator** - Compute transitive closure
- **Multi-Hop Reasoning Query Builder** - Build complex queries

## Recommended Libraries

### Ontology Tools
- `rdflib` - RDF/OWL support
- `owlready2` - OWL ontology reasoning
- `pysparql` - SPARQL endpoint

### Reasoning Engines
- `Hermit` - OWL reasoner
- `Pellet` - Description logic reasoner
- `Jena` - Semantic web framework

### Graph Processing
- `networkx` - Graph algorithms
- `neo4j` - Graph database
- `virtuoso` - RDF triple store

### Semantic Standards
- `rdflib-jsonld` - JSON-LD support
- `pyshacl` - SHACL validation

## Related Skills

- **Graph Rule Engine Builder** - Define custom rules
- **Transitive Closure Generator** - Compute closure
- **Causal Chain Analyzer** - Analyze implications
- **Graph Path Reasoning Analyzer** - Find paths
- **Multi-Hop Reasoning Query Builder** - Complex queries

---

**Version:** 1.0.0
