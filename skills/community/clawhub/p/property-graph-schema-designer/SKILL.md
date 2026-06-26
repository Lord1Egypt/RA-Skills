---
name: property_graph_schema_designer
title: Property Graph Schema Designer (Neo4j Style)
description: Design property graph schemas for knowledge graph systems using Neo4j-style node labels, relationships, and properties based on domain descriptions or developer requirements.
category: graph-modeling
tags:
  - knowledge-graph
  - property-graph
  - neo4j
  - graph-schema
  - graph-modeling
  - cypher
  - developer-tools
version: 1.0.0
author: community
license: MIT
---

# Property Graph Schema Designer

**Design Neo4j-style property graph schemas from domain descriptions.**

This skill translates domain models, requirements, and entity descriptions into structured property graph schemas with node labels, relationships, properties, and constraints.

## Quick Start

### Use When
- Designing property graph schemas for Neo4j
- Converting domain documentation → graph models
- Creating graph database data models
- Modeling entities and relationships
- Bootstrapping graph projects

### Inputs
- Domain descriptions
- System architecture docs
- Entity relationship diagrams
- Relational schemas
- JSON/API schemas
- Business rules

### Outputs
- Node labels (e.g., Student, Course)
- Relationship types (e.g., ENROLLED_IN, TEACHES)
- Node properties with types
- Relationship properties
- Index recommendations
- Constraint suggestions
- Cypher implementation templates

## Example

**Input:**
```
A university has students, professors, courses, and departments.
Students enroll in courses. Professors teach courses.
Departments manage professors and courses.
```

**Output:**
```
Node Labels:
- Student (properties: student_id, name, email, enrollment_year)
- Professor (properties: professor_id, name, research_area)
- Course (properties: course_id, title, credits)
- Department (properties: dept_id, name, budget)

Relationships:
- (Student)-[:ENROLLED_IN {semester}]->(Course)
- (Professor)-[:TEACHES {semester}]->(Course)
- (Department)-[:MANAGES]->(Course)
- (Department)-[:EMPLOYS]->(Professor)

Constraints:
- CREATE CONSTRAINT student_id UNIQUE on Student.student_id
- CREATE CONSTRAINT course_id UNIQUE on Course.course_id
- CREATE INDEX on Professor.name
```

## Execution Steps

1. **Identify Entities** – Extract nouns/concepts from domain text
2. **Map to Node Labels** – Determine PascalCase labels
3. **Identify Relationships** – Extract verbs and connections
4. **Map Relationship Types** – Determine SCREAMING_SNAKE_CASE types
5. **Extract Properties** – Identify node & relationship attributes
6. **Suggest Constraints** – Recommend unique constraints
7. **Suggest Indexes** – Recommend indexes for queries
8. **Generate Cypher** – Output implementation templates

## Schema Components

### Node Labels
```
PascalCase naming
Examples: Student, Professor, Course, Department
```

### Relationship Types
```
SCREAMING_SNAKE_CASE naming
Directional: A-[TYPE]->B
Examples: ENROLLED_IN, TEACHES, MANAGES
```

### Properties
```
Node properties: camelCase (student_id, name, email)
Relationship properties: camelCase (semester, grade)
Include types: String, Integer, Date, Float
```

### Constraints & Indexes
```
Unique constraints on identifiers
Indexes on frequently queried properties
Recommended indexes for relationships
```

## Recommended Libraries

- **Drivers:** neo4j, py2neo
- **Graph modeling:** networkx
- **Visualization:** pyvis, graphviz
- **Data:** pandas

## Best Practices

✓ Use clear, consistent naming (PascalCase, SCREAMING_SNAKE_CASE, camelCase)  
✓ Avoid redundant relationships  
✓ Prefer directional relationships  
✓ Use unique constraints on identifiers  
✓ Index frequently queried properties  
✓ Keep nodes focused, avoid over-nesting  
✓ Separate schema concerns from instance data  
✓ Plan for query patterns upfront  

## References

See [schema-patterns.md](references/schema-patterns.md) for property graph design patterns and [example-schemas.md](examples/example-schemas.md) for domain schema examples.

---

**Version:** 1.0.0
