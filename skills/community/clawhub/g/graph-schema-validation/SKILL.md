---
name: graph_schema_validation
title: Graph Schema Validation
description: Validate knowledge graph schemas and data against defined ontology, RDF/OWL, or property graph schema constraints.
category: graph-modeling
tags:
  - knowledge-graph
  - schema-validation
  - rdf
  - owl
  - property-graph
  - neo4j
  - data-validation
  - shacl
  - developer-tools
version: 1.0.0
author: community
license: MIT
---

# Graph Schema Validation

**Validate knowledge graph schemas and data against defined constraints.**

This skill ensures graph data conforms to schema definitions, ontology rules, and consistency requirements.

## Quick Start

### Use When
- Validating graph data before ingestion
- Testing schema correctness
- Enforcing ontology constraints
- Checking graph consistency
- Verifying RDF/OWL compliance
- Validating property graph models

### Inputs
- RDF datasets (Turtle, RDF/XML)
- OWL ontologies
- Property graph schemas
- Cypher structures
- Graph data files
- Graph exports

### Outputs
- Validation report
- Detected violations
- Suggested corrections
- Conformance status
- Constraint violations

## Example

**Input Schema:**
```
Student: student_id (UNIQUE), name, email
Course: course_code (UNIQUE), title, credits
Relationship: (Student)-[:ENROLLED_IN]->(Course)
```

**Input Data:**
```
(Student {name: "Alice"})              # INVALID: missing student_id
(Student {student_id: "S001", name: "Bob"})-[:ENROLLED_IN]->(Course)  # OK
```

**Validation Report:**
```
Violations: 1
- Node S002: Missing required property student_id
- Suggestion: Add student_id to Student node
```

## Validation Types

### 1. Schema Conformance
- Node labels match schema classes
- Relationships follow schema rules
- Property types are valid

### 2. Property Validation
- Required properties present
- Data types correct
- Property names consistent

### 3. Relationship Validation
- Relationships follow schema rules
- Direction correct
- Source/target types valid

### 4. Cardinality Constraints
- Minimum/maximum occurrences
- Uniqueness constraints
- Collection sizes

### 5. Graph Integrity
- No orphan nodes
- No broken references
- No duplicate identifiers
- Consistent relationships

## Schema Formats

### RDF/OWL (SHACL Shapes)
```turtle
:StudentShape a sh:NodeShape ;
  sh:targetClass :Student ;
  sh:property [
    sh:path :student_id ;
    sh:datatype xsd:string ;
    sh:minCount 1
  ] .
```

### Property Graph (Cypher Constraints)
```cypher
CREATE CONSTRAINT student_id_unique ON (s:Student) REQUIRE s.student_id IS UNIQUE
CREATE INDEX ON (s:Student)(name)
```

## Execution Steps

1. **Load Schema** – Load ontology, SHACL shapes, or schema definition
2. **Load Data** – Load graph data to validate
3. **Define Rules** – Specify validation constraints
4. **Execute Validation** – Check data against rules
5. **Generate Report** – Produce validation results
6. **Suggest Fixes** – Recommend corrections

## Recommended Libraries

- **RDF/OWL:** rdflib, pyshacl, owlready2
- **Property Graph:** neo4j, py2neo, networkx
- **Data Validation:** pydantic, jsonschema
- **Graph Analysis:** networkx

## Best Practices

✓ Validate before production deployment  
✓ Enforce constraints at database level  
✓ Use consistent property naming  
✓ Define validation rules early  
✓ Maintain validation tests  
✓ Document constraint rules  
✓ Review violation reports carefully  

## References

See [validation-patterns.md](references/validation-patterns.md) for validation strategies and [example-validations.md](examples/example-validations.md) for domain validation examples.

---

**Version:** 1.0.0
