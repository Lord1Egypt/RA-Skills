---
name: graph_constraint_generator
title: Knowledge Graph Constraint Generator
description: Generate structural, semantic, and property constraints for knowledge graph schemas including RDF/OWL ontologies and property graph models.
category: graph-modeling
tags:
  - knowledge-graph
  - schema-constraints
  - rdf
  - owl
  - neo4j
  - shacl
  - data-integrity
  - graph-modeling
  - developer-tools
version: 1.0.0
author: community
license: MIT
---

# Knowledge Graph Constraint Generator

**Generate constraints for knowledge graph schemas to enforce data integrity.**

This skill automatically creates structural, semantic, and property constraints suitable for RDF/OWL ontologies and Neo4j property graphs.

## Quick Start

### Use When
- Designing constraints for graph schemas
- Enforcing graph integrity rules
- Generating SHACL validation rules
- Creating Neo4j database constraints
- Defining property requirements
- Establishing data governance

### Inputs
- Graph schema definitions
- Entity models
- Relationship types
- Property specifications
- Cardinality requirements
- Integrity rules

### Outputs
- Unique constraints
- Required property constraints
- Relationship constraints
- Cardinality rules
- SHACL shapes
- Cypher constraint statements

## Example

**Input Schema:**
```
Student: student_id (unique), name (required), email
Course: course_code (unique), title (required), credits
Relationship: (Student)-[:ENROLLED_IN]->(Course)
```

**Generated Constraints:**
```
Unique:
  Student.student_id UNIQUE
  Course.course_code UNIQUE

Required:
  Student.name (min 1)
  Course.title (min 1)

Relationships:
  (Student)-[:ENROLLED_IN]->(Course) [min 1]
```

## Constraint Types

### 1. Unique Constraints
Ensure properties uniquely identify nodes
```cypher
CREATE CONSTRAINT student_id_unique ON (s:Student) REQUIRE s.student_id IS UNIQUE
```

### 2. Required Property Constraints
Define mandatory properties
```
Student.name IS REQUIRED
Course.title IS REQUIRED
```

### 3. Relationship Constraints
Define allowed graph connections
```
(Student)-[:ENROLLED_IN]->(Course)
(Professor)-[:TEACHES]->(Course)
```

### 4. Cardinality Constraints
Define relationship occurrence limits
```
Student → ENROLLED_IN → Course (minimum: 1)
Professor → TEACHES → Course (maximum: 10)
```

### 5. Domain/Range Constraints (RDF/OWL)
Define semantic relationship constraints
```turtle
:writes rdfs:domain :Researcher ;
        rdfs:range :Paper .
```

### 6. Data Type Constraints
Ensure property values match types
```
student_id: String
credits: Integer
gpa: Float
```

## Execution Steps

1. **Analyze Schema** – Extract entities, relationships, properties
2. **Identify Keys** – Find unique identifiers
3. **Determine Required** – Identify mandatory properties
4. **Analyze Relationships** – Extract connection patterns
5. **Calculate Cardinality** – Determine relationship bounds
6. **Generate Constraints** – Create constraint definitions
7. **Format Output** – Output as SHACL, Cypher, or RDF

## Output Formats

### Neo4j Cypher
```cypher
CREATE CONSTRAINT student_id_unique ON (s:Student) REQUIRE s.student_id IS UNIQUE
CREATE INDEX ON (s:Student)(name)
```

### SHACL Shapes
```turtle
:StudentShape a sh:NodeShape ;
  sh:targetClass :Student ;
  sh:property [
    sh:path :student_id ;
    sh:minCount 1 ;
    sh:maxCount 1
  ] .
```

### RDF/OWL
```turtle
:writes rdfs:domain :Researcher ;
        rdfs:range :Paper ;
        rdf:type owl:ObjectProperty .
```

## Recommended Libraries

- **RDF/OWL:** rdflib, pyshacl, owlready2
- **Property Graph:** neo4j, py2neo, networkx
- **Data Validation:** pydantic, jsonschema

## Best Practices

✓ Define unique identifiers early  
✓ Avoid overly restrictive constraints  
✓ Keep domain/range rules clear  
✓ Validate data frequently  
✓ Combine database and semantic constraints  
✓ Document constraint reasoning  
✓ Test constraints before production  

## References

See [constraint-patterns.md](references/constraint-patterns.md) for constraint design patterns and [example-constraints.md](examples/example-constraints.md) for domain constraint examples.

---

**Version:** 1.0.0
