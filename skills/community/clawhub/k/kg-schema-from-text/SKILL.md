---
name: kg_schema_from_text
title: Knowledge Graph Ontology & Schema Generation from Text
description: Generate a structured knowledge graph ontology or schema from unstructured or semi-structured text sources.
category: graph-modeling
tags:
  - knowledge-graph
  - ontology
  - schema
  - rdf
  - owl
  - graph-modeling
  - entity-extraction
  - developer-tools
version: 1.0.0
author: community
license: MIT
---

# Knowledge Graph Schema Generation from Text

**Automatically derive structured graph schemas from natural language documentation and domain descriptions.**

This skill converts textual descriptions into machine-readable graph models with entities, relationships, properties, and constraints.

## Quick Start

### Use When
- Converting domain documentation → ontology
- Bootstrapping a knowledge graph schema
- Designing initial RDF/OWL or Neo4j schemas
- Extracting schema from requirements or API docs

### Inputs
- Natural language domain descriptions
- Technical documentation
- Example records or datasets
- JSON/CSV structures

### Outputs
- Entity types (nodes/classes)
- Relationship types (edges/predicates)
- Properties & attributes
- Graph schema representation (Property Graph or RDF)

## Example

**Input:**
```
A university contains students, professors, courses, and departments.
Students enroll in courses. Professors teach courses.
Departments manage both courses and professors.
```

**Output:**
```
Entities: Student, Professor, Course, Department

Relationships:
- Student -> ENROLLED_IN -> Course
- Professor -> TEACHES -> Course
- Department -> MANAGES -> Course
- Department -> MANAGES -> Professor

Properties:
- Student: id, name, email, enrollment_date
- Course: id, title, credits, department
- Professor: id, name, department, specialization
- Department: id, name, budget
```

## Execution Steps

1. **Extract Entities** – Identify nouns/concepts from text
2. **Extract Relationships** – Identify verbs/connections
3. **Extract Properties** – Identify attributes and constraints
4. **Infer Structure** – Build graph patterns
5. **Generate Schema** – Output in target format (Property Graph or RDF)

## Schema Formats

### Property Graph (Neo4j, TigerGraph)
```
Nodes: Student, Professor, Course, Department
Relationships: ENROLLED_IN, TEACHES, MANAGES
Properties: Names, IDs, dates, descriptions
```

### RDF/OWL (Semantic Web)
```
Classes: Student, Professor, Course, Department
Properties: enrolledIn, teaches, manages
Attributes: name, id, description
```

## Recommended Libraries

- **NLP**: spaCy, transformers, nltk
- **Graph**: networkx, rdflib, pyvis, owlready2
- **Schema**: pydantic, dataclasses, jsonschema

## Best Practices

✓ Use clear, consistent entity names (PascalCase)  
✓ Normalize relationship directions  
✓ Extract domain-specific constraints  
✓ Separate schema from instance data  
✓ Follow knowledge graph modeling standards  

## References

See [extraction-patterns.md](references/extraction-patterns.md) for entity/relationship extraction guidelines and [example-schemas.md](examples/example-schemas.md) for domain examples.

---

**Version:** 1.0.0
