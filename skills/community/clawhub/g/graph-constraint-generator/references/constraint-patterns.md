# Constraint Generation Patterns

This guide provides patterns for generating graph constraints from schema definitions.

## Unique Constraint Patterns

### Property-Based Uniqueness

```
Pattern: Identifier properties must be unique

Neo4j:
CREATE CONSTRAINT student_id_unique ON (s:Student) REQUIRE s.student_id IS UNIQUE
CREATE CONSTRAINT email_unique ON (u:User) REQUIRE u.email IS UNIQUE

SHACL:
sh:property [
  sh:path :student_id ;
  sh:minCount 1 ;
  sh:maxCount 1
] .

When to use:
✓ Business identifiers (employee_id, student_id)
✓ External references (ISBN, SKU)
✓ Login credentials (email, username)
```

### Compound Unique Constraints

```
Pattern: Multiple properties form unique key

Neo4j:
CREATE CONSTRAINT unique_course ON (c:Course) REQUIRE (c.code, c.year) IS UNIQUE

SHACL:
sh:property [
  sh:path :code ;
  sh:minCount 1
] ;
sh:property [
  sh:path :year ;
  sh:minCount 1
] .
```

---

## Required Property Patterns

### Simple Required Property

```
Pattern: Property must exist on all nodes

Neo4j:
MATCH (s:Student)
WHERE s.name IS NULL
RETURN s  -- Should return empty

SHACL:
sh:property [
  sh:path :name ;
  sh:minCount 1 ;
  sh:datatype xsd:string
] .

When to use:
✓ Core business attributes (name, title)
✓ Identifying information
✓ Mandatory classifications
```

### Conditional Required Properties

```
Pattern: Property required based on condition

SHACL:
:StudentShape sh:property [
  sh:path :enrollment_date ;
  sh:minCount 1
] ;
sh:property [
  sh:path :graduation_date ;
  sh:minCount 0  -- Optional
] .
```

---

## Relationship Constraint Patterns

### Valid Relationship Types

```
Pattern: Define allowed relationship types

Neo4j Query:
MATCH (a)-[r]->(b)
WHERE type(r) NOT IN ["ENROLLED_IN", "TEACHES", "MANAGES"]
RETURN r  -- Should be empty

Constraint Specification:
(Student)-[:ENROLLED_IN]->(Course)
(Professor)-[:TEACHES]->(Course)
(Department)-[:MANAGES]->(Course)
```

### Relationship Direction

```
Pattern: Enforce correct relationship direction

Invalid:
(Course)-[:ENROLLED_IN]->(Student)

Valid:
(Student)-[:ENROLLED_IN]->(Course)

Validation Query:
MATCH (a:Course)-[:ENROLLED_IN]->(b:Student)
RETURN a, b  -- Should be empty
```

### Source/Target Type Constraints

```
Pattern: Ensure relationships connect correct types

SHACL:
:StudentShape sh:property [
  sh:path :enrolledIn ;
  sh:class :Course ;
  sh:nodeKind sh:IRI
] .

This ensures: (Student)-[:enrolledIn]-(Course)
```

---

## Cardinality Constraint Patterns

### Minimum Cardinality

```
Pattern: At least N relationships required

Neo4j:
MATCH (s:Student)
WHERE NOT (s)-[:ENROLLED_IN]->()
RETURN s  -- Should be empty if min >= 1

SHACL:
sh:property [
  sh:path :enrolledIn ;
  sh:minCount 1  -- At least one enrollment
] .

Example:
- Student must enroll in at least 1 course
- Course must have at least 1 professor
```

### Maximum Cardinality

```
Pattern: At most N relationships allowed

Neo4j:
MATCH (p:Professor)-[:TEACHES]->(c:Course)
WITH p, COUNT(c) as course_count
WHERE course_count > 5
RETURN p, course_count  -- Should be empty if max <= 5

SHACL:
sh:property [
  sh:path :teaches ;
  sh:maxCount 5  -- Maximum 5 courses
] .

Example:
- Professor can teach at most 5 courses
- Student can enroll in at most 10 courses
```

### Exact Cardinality

```
Pattern: Exactly N relationships required

SHACL:
sh:property [
  sh:path :hasMajor ;
  sh:minCount 1 ;
  sh:maxCount 1  -- Exactly 1 major
] .

Example:
- Person has exactly 1 primary contact
- Employee in exactly 1 department
```

---

## Domain/Range Constraint Patterns

### RDF/OWL Domain Constraints

```
Pattern: Restrict relationship source

RDF:
:teaches rdfs:domain :Professor ;
         rdfs:range :Course .

SHACL:
:ProfessorShape sh:property [
  sh:path :teaches ;
  sh:nodeKind sh:IRI
] .

Effect: Only Professor can TEACH
```

### RDF/OWL Range Constraints

```
Pattern: Restrict relationship target

RDF:
:enrolledIn rdfs:domain :Student ;
            rdfs:range :Course .

Effect: Can only enroll IN a Course
```

---

## Data Type Constraint Patterns

### Simple Type Constraints

```
Pattern: Property has specific data type

SHACL:
sh:property [
  sh:path :name ;
  sh:datatype xsd:string
] ;
sh:property [
  sh:path :age ;
  sh:datatype xsd:integer
] ;
sh:property [
  sh:path :gpa ;
  sh:datatype xsd:decimal
] .
```

### Value Range Constraints

```
Pattern: Property values within range

SHACL:
sh:property [
  sh:path :age ;
  sh:datatype xsd:integer ;
  sh:minInclusive 0 ;
  sh:maxInclusive 150
] ;
sh:property [
  sh:path :gpa ;
  sh:datatype xsd:decimal ;
  sh:minInclusive 0.0 ;
  sh:maxInclusive 4.0
] .
```

### Pattern Matching Constraints

```
Pattern: Property value matches pattern

SHACL:
sh:property [
  sh:path :email ;
  sh:datatype xsd:string ;
  sh:pattern "^[^@]+@[^@]+\\.[^@]+$"
] ;
sh:property [
  sh:path :studentId ;
  sh:pattern "^S[0-9]{4}$"  -- Format: S0001, S0002, etc.
] .
```

---

## Common Constraint Issues

| Issue | Detection | Solution |
|-------|-----------|----------|
| Over-constrained | Properties missing frequently | Relax constraints |
| Under-constrained | Invalid data passes | Add constraints |
| Conflicting | Mutually exclusive rules | Review and fix |
| Missing keys | Duplicate identifiers | Add unique constraints |
| Orphan nodes | Nodes with no relationships | Add cardinality |

---

## Best Practices

✓ Define unique identifiers early  
✓ Start with minimal constraints, add as needed  
✓ Keep domain/range rules clear  
✓ Document constraint rationale  
✓ Test constraints with real data  
✓ Avoid circular dependencies  
✓ Version constraint schemas  
✓ Monitor constraint violations  

---

See [example-constraints.md](../examples/example-constraints.md) for complete constraint generation examples.

