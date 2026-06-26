# Graph Schema Validation Patterns

This guide provides patterns for validating graph schemas and data.

## Property Validation Patterns

### Required Properties

```
Pattern: Ensure required properties exist

RDF/OWL:
:StudentShape sh:property [
  sh:path :student_id ;
  sh:minCount 1
] .

Property Graph Check:
MATCH (s:Student)
WHERE s.student_id IS NULL
RETURN s
```

### Unique Constraints

```
Pattern: Enforce uniqueness

RDF/OWL:
sh:property [
  sh:path :email ;
  sh:uniqueLang false ;
  sh:maxCount 1
] .

Property Graph:
CREATE CONSTRAINT email_unique 
ON (u:User) REQUIRE u.email IS UNIQUE;
```

### Data Type Validation

```
Pattern: Verify property types

RDF/OWL:
sh:property [
  sh:path :age ;
  sh:datatype xsd:integer ;
  sh:minInclusive 0 ;
  sh:maxInclusive 150
] .

Property Graph Check:
def validate_age(node):
  if not isinstance(node.age, int):
    return False
  return 0 <= node.age <= 150
```

### Property Value Constraints

```
Pattern: Restrict property values

RDF/OWL:
sh:property [
  sh:path :status ;
  sh:in (ex:Active ex:Inactive ex:Pending)
] .

Property Graph Check:
VALID_STATUSES = ["Active", "Inactive", "Pending"]
MATCH (e:Entity)
WHERE e.status NOT IN VALID_STATUSES
RETURN e
```

---

## Relationship Validation Patterns

### Relationship Type Validation

```
Pattern: Check relationship types follow schema

RDF/OWL:
:StudentShape sh:property [
  sh:path ex:enrolledIn ;
  sh:class ex:Course ;
  sh:nodeKind sh:IRI
] .

Property Graph:
MATCH (s:Student)-[r]->(t)
WHERE NOT (t:Course)
RETURN r
```

### Cardinality Constraints

```
Pattern: Min/Max relationship counts

RDF/OWL:
sh:property [
  sh:path ex:teaches ;
  sh:minCount 1 ;
  sh:maxCount 10
] .

Property Graph:
MATCH (p:Professor)-[:TEACHES]->(c:Course)
WITH p, COUNT(c) as course_count
WHERE course_count < 1 OR course_count > 10
RETURN p, course_count
```

### Relationship Direction

```
Pattern: Validate relationship direction

Invalid:
(Course)-[:ENROLLED_IN]->(Student)  # Wrong direction

Valid:
(Student)-[:ENROLLED_IN]->(Course)  # Correct direction

Validation:
MATCH (a:Course)-[:ENROLLED_IN]->(b:Student)
RETURN a, b  # Should be empty
```

---

## Graph Integrity Patterns

### Orphan Node Detection

```
Pattern: Find nodes with no relationships

Cypher:
MATCH (n)
WHERE NOT (n)--()
RETURN n

Issue: Isolated nodes may indicate missing data
Solution: Either connect or remove orphan nodes
```

### Broken Reference Detection

```
Pattern: Find nodes referencing non-existent targets

Cypher:
MATCH (s:Student)-[:ENROLLED_IN]->(c)
WHERE NOT (c:Course)
RETURN s, c

Issue: Student enrolled in non-course entity
Solution: Verify or fix relationship target
```

### Duplicate Identifier Detection

```
Pattern: Find duplicate unique properties

Cypher:
MATCH (n:Student)
WITH n.student_id, COUNT(*) as cnt
WHERE cnt > 1
RETURN n.student_id, cnt

Issue: Multiple nodes with same identifier
Solution: Merge or delete duplicates
```

### Circular Relationships

```
Pattern: Detect unwanted cycles

Cypher:
MATCH path = (n:Department)-[:MANAGES*]->(n)
RETURN path

Use Case: Avoid circular management chains
```

---

## Schema Conformance Patterns

### Label Validation

```
Pattern: Check all nodes have required labels

Cypher:
MATCH (n)
WHERE NOT (n:Person OR n:Course OR n:Department)
RETURN n

Issue: Unexpected node types
Solution: Verify or correct labels
```

### Property Name Consistency

```
Pattern: Enforce naming conventions

Check:
- camelCase for properties: firstName, student_id
- PascalCase for labels: Student, Course
- SCREAMING_SNAKE_CASE for relationships: ENROLLED_IN

Validation:
def validate_property_naming(prop_name):
  return prop_name[0].islower()
```

### Schema Version Mismatch

```
Pattern: Detect data conforming to old schema

Check:
- Removed properties still in use
- Deprecated relationships present
- Old naming conventions
- Obsolete constraints

Solution:
- Update data to new schema
- Run migration scripts
- Document changes
```

---

## Common Validation Issues

| Issue | Detection | Solution |
|-------|-----------|----------|
| Missing required property | WHERE prop IS NULL | Add missing property |
| Duplicate identifier | GROUP BY + HAVING COUNT > 1 | Merge or remove duplicates |
| Invalid relationship type | WHERE type NOT IN allowed_types | Fix relationship type |
| Orphan node | WHERE NOT (n)--() | Connect or remove |
| Broken reference | Check target exists | Update or delete edge |
| Wrong cardinality | COUNT(*) < min OR > max | Add/remove relationships |
| Type mismatch | typeof(prop) != expected | Convert or replace value |

---

## Validation Report Format

```
VALIDATION REPORT
=================

Dataset: university_graph
Schema: university_schema.ttl
Validation Date: 2026-03-08

SUMMARY
-------
Total Nodes: 1,250
Total Relationships: 3,420
Violations Found: 15
Conformance: 98.8%

VIOLATIONS
----------
1. Missing Required Property (5 occurrences)
   - Node: Student(S042)
   - Property: student_id
   - Suggestion: Add missing student_id

2. Invalid Relationship Target (3 occurrences)
   - Relationship: (Student)-[:ENROLLED_IN]->(Unknown)
   - Expected: Course
   - Suggestion: Fix relationship target

3. Duplicate Identifier (2 occurrences)
   - Property: course_code
   - Value: "CS101" (appears 2 times)
   - Suggestion: Merge courses or rename one

4. Orphan Node (5 occurrences)
   - Nodes: [Professor(P125), Department(D018), ...]
   - Suggestion: Connect or remove orphan nodes

RECOMMENDATIONS
---------------
✓ Fix 15 violations before production deployment
✓ Establish regular validation schedule
✓ Document all constraint exceptions
✓ Review and update schema as needed
```

---

## Best Practices

✓ Validate frequently during development  
✓ Test with representative data samples  
✓ Document all constraints & exceptions  
✓ Enforce constraints at database level  
✓ Create validation test suites  
✓ Review violation reports carefully  
✓ Plan migrations for schema changes  
✓ Maintain validation logs  

---

See [example-validations.md](../examples/example-validations.md) for complete validation examples.

