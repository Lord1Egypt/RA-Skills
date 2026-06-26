# Property Graph Schema Design Patterns

This guide provides patterns for designing Neo4j-style property graph schemas from domain descriptions.

## Node Label Patterns

### Entity as Node

Represent core business entities as node labels:

```
Domain: "A library contains books"
Node Label: Book

Domain: "Customers place orders"
Node Labels: Customer, Order
```

### Naming Convention

```
✓ PascalCase: Student, ResearchPaper, OrderItem
✗ snake_case: student, research_paper
✗ camelCase: student, researchPaper
✗ UPPERCASE: STUDENT, RESEARCHPAPER
```

### Avoiding Over-Nesting

❌ **Wrong** - Too many details in node labels:
```
StudentEnrolledInCourseInDepartment
UniversityStudentProfile
```

✅ **Right** - Clear, focused labels:
```
Student
Course
Department
```

---

## Relationship Type Patterns

### Common Relationship Verbs

| Verb | Relationship Type | Direction | Example |
|------|------------------|-----------|---------|
| enroll in | ENROLLED_IN | → | (Student)-[:ENROLLED_IN]->(Course) |
| teach | TEACHES | → | (Professor)-[:TEACHES]->(Course) |
| manage | MANAGES | → | (Department)-[:MANAGES]->(Course) |
| work in | WORKS_IN | → | (Person)-[:WORKS_IN]->(Department) |
| knows | KNOWS | ↔ | (Person)-[:KNOWS]-(Person) |
| owns | OWNS | → | (Person)-[:OWNS]->(Company) |
| created by | CREATED_BY | ← | (Product)-[:CREATED_BY]->(Person) |

### Naming Convention

```
✓ SCREAMING_SNAKE_CASE: ENROLLED_IN, TEACHES, MANAGES
✗ snake_case: enrolled_in, teaches
✗ camelCase: enrolledIn, teaches
✗ PascalCase: EnrolledIn, Teaches
```

### Relationship Direction

```
✓ Directional: (Student)-[:ENROLLED_IN]->(Course)
✗ Ambiguous: (Student)-[:RELATIONSHIP]-(Course)

Forward direction: Active verb
(Employee)-[:WORKS_AT]->(Company)

Reverse direction: Passive verb
(Company)-[:EMPLOYS]->(Employee)
```

---

## Property Patterns

### Node Properties

```
Naming: camelCase
Types: String, Integer, Date, Float, Boolean

✓ student_id: "S001"
✓ enrollment_date: date("2026-01-15")
✓ gpa: 3.85
✓ is_active: true

Property Placement:
- Always include identifier properties
- Include commonly queried fields
- Include domain-relevant attributes
```

### Relationship Properties

```
(Student)-[:ENROLLED_IN {semester: "Fall", grade: "A"}]->(Course)

When to use:
✓ Temporal info: enrollDate, grade
✓ Context: semester, score
✓ Metadata: status, priority

Avoid:
✗ Data that belongs on a node
✗ Redundant information
✗ Overly complex objects
```

---

## Constraint Patterns

### Unique Constraints

```cypher
-- Unique identifier for Student
CREATE CONSTRAINT student_id IF NOT EXISTS
FOR (s:Student)
REQUIRE s.student_id IS UNIQUE;

-- Unique email per user
CREATE CONSTRAINT user_email IF NOT EXISTS
FOR (u:User)
REQUIRE u.email IS UNIQUE;
```

### When to Use Unique Constraints

```
✓ Business identifiers: employee_id, student_id
✓ External references: ISBN, SKU
✓ Login credentials: email (often)
✓ Avoid duplicates critical to domain

✗ Natural names (too restrictive)
✗ Non-core attributes
```

---

## Index Patterns

### Frequently Queried Properties

```cypher
-- Index for common lookups
CREATE INDEX name_idx IF NOT EXISTS
FOR (p:Person)
ON (p.name);

-- Index for date ranges
CREATE INDEX created_date_idx IF NOT EXISTS
FOR (a:Article)
ON (a.created_date);
```

### When to Index

```
✓ Properties used in WHERE clauses
✓ Properties used in relationship matching
✓ High-cardinality properties
✓ Frequently accessed nodes

✗ Low-cardinality properties
✗ Rarely queried properties
✗ Small node sets
```

---

## Property Graph Patterns

### One-to-Many

```
Domain: "A department has many employees"

Schema:
(Department)-[:HAS_EMPLOYEE]->(Employee)
(Employee)-[:WORKS_IN]->(Department)

Cypher:
MATCH (d:Department)-[:HAS_EMPLOYEE]->(e:Employee)
RETURN d, e;
```

### Many-to-Many

```
Domain: "Students enroll in many courses"

Schema:
(Student)-[:ENROLLED_IN {semester}]->(Course)

Cypher:
MATCH (s:Student)-[:ENROLLED_IN]->(c:Course)
WHERE s.student_id = "S001"
RETURN c;
```

### Self-Referential

```
Domain: "Employees report to managers"

Schema:
(Employee)-[:REPORTS_TO]->(Employee)

Cypher:
MATCH (emp:Employee)-[:REPORTS_TO*1..]->(ceo:Employee)
WHERE ceo.title = "CEO"
RETURN emp;
```

### Intermediate Node (Reification)

```
Domain: "Orders contain products with quantities"

Schema Option 1 (Direct):
(Order)-[:CONTAINS {qty: 5}]->(Product)

Schema Option 2 (Intermediate Node):
(Order)-[:HAS_ITEM]->(OrderItem)-[:OF_PRODUCT]->(Product)
OrderItem has: quantity, price

Use intermediate when:
✓ Multiple relationships needed
✓ Rich metadata required
✓ Historical tracking needed
```

---

## Normalization Patterns

### Avoid Redundancy

❌ **Wrong** - Duplicated data:
```
(Student {name: "Alice", university_name: "MIT"})-
[:ENROLLED_IN]->
(Course {name: "CS101", university_name: "MIT"})
```

✅ **Right** - Single source of truth:
```
(University {name: "MIT"})-[:OFFERS]->(Course {name: "CS101"})
(Student {name: "Alice"})-[:ENROLLED_IN]->(Course)
(Student)-[:STUDIES_AT]->(University)
```

### Separate Concerns

```
✓ Metadata node: (Company {name, founded, industry})
✓ Relationship for context: (Person)-[:WORKS_AT {since}]->(Company)
✓ Derived info: Query-time calculations

✗ Embedding all data: (Person {company_name, ...})
✗ Storing computed values: (Person {company_info, ...})
```

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Node labels too specific | Use more general labels (Person vs Manager) |
| Relationship direction unclear | Always use active voice |
| Properties on node vs relationship | Properties on relationship if contextual |
| Missing constraints | Add UNIQUE on identifiers |
| No indexes on common queries | Index properties in WHERE clauses |
| Circular relationships | Document direction and use (→) |
| Ambiguous relationships | Be specific (MANAGES vs WORKS_WITH) |

---

## Best Practices Checklist

✓ Node labels are PascalCase  
✓ Relationship types are SCREAMING_SNAKE_CASE  
✓ Properties are camelCase  
✓ Relationships are directional (one-way arrow)  
✓ Unique constraints on identifiers  
✓ Indexes on frequently queried properties  
✓ No redundant data between nodes  
✓ Clear, focused node designs  
✓ Relationship properties for context  
✓ Self-explanatory schema  

---

See [example-schemas.md](../examples/example-schemas.md) for complete domain schema examples.

