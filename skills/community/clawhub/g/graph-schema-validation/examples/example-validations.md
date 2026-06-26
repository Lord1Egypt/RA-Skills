# Graph Validation Examples

Complete validation examples for different domains and use cases.

## Example 1: University Schema Validation

### Schema Definition

```
CONSTRAINTS:
- Student: student_id UNIQUE, name REQUIRED, email REQUIRED
- Professor: professor_id UNIQUE, name REQUIRED, research_area REQUIRED
- Course: course_code UNIQUE, title REQUIRED, credits INTEGER
- Department: dept_id UNIQUE, name REQUIRED

RELATIONSHIPS:
- (Student)-[:ENROLLED_IN]->(Course): Required
- (Professor)-[:TEACHES]->(Course): Required
- (Department)-[:MANAGES]->(Course): Required
- (Department)-[:EMPLOYS]->(Professor): Required
```

### Validation Rules

```cypher
-- Check for missing student_id
MATCH (s:Student)
WHERE s.student_id IS NULL
RETURN "VIOLATION: Missing student_id" as violation, COUNT(s) as count

-- Check for duplicate student IDs
MATCH (s:Student)
WITH s.student_id, COUNT(*) as cnt
WHERE cnt > 1 AND s.student_id IS NOT NULL
RETURN "VIOLATION: Duplicate student_id" as violation, COUNT(*) as count

-- Check for students not enrolled in any course
MATCH (s:Student)
WHERE NOT (s)-[:ENROLLED_IN]->()
RETURN "WARNING: Student not enrolled" as warning, s.student_id

-- Check for orphan courses
MATCH (c:Course)
WHERE NOT (c)<-[:ENROLLED_IN]-() AND NOT ()-[:TEACHES]->(c)
RETURN "WARNING: Orphan course" as warning, c.course_code

-- Check valid enrollment relationships
MATCH (s:Student)-[e:ENROLLED_IN]->(t)
WHERE NOT (t:Course)
RETURN "VIOLATION: Invalid enrollment target" as violation, COUNT(e) as count
```

### Validation Report

```
VALIDATION: University Schema
=============================

Violations Found: 3
Warnings: 5
Conformance: 96.2%

CRITICAL:
1. ✗ Missing student_id (2 students)
   Nodes: S042, S089
   Fix: Add student_id property

2. ✗ Duplicate course_code (1 occurrence)
   Value: "CS101" (appears in courses C042 and C115)
   Fix: Rename one course

3. ✗ Invalid relationship (1 enrollment)
   (Student S050)-[:ENROLLED_IN]->(Unknown)
   Fix: Correct course reference

WARNINGS:
1. ⚠ Orphan professors (2): P018, P025
   Fix: Assign to department or remove

2. ⚠ Unenrolled students (3): S001, S005, S012
   Fix: Verify enrollment status

Overall Status: REVIEW REQUIRED
Action: Fix critical violations before deployment
```

---

## Example 2: E-Commerce Schema Validation

### Schema Definition

```
CONSTRAINTS:
- Customer: customer_id UNIQUE, email UNIQUE, name REQUIRED
- Product: product_id UNIQUE, sku UNIQUE, price > 0
- Order: order_id UNIQUE, order_date DATE, total > 0
- OrderItem: quantity > 0, unit_price > 0

RELATIONSHIPS:
- (Customer)-[:PLACES]->(Order): Required
- (Order)-[:CONTAINS]->(OrderItem): Required
- (OrderItem)-[:OF_PRODUCT]->(Product): Required
- (Product)-[:BELONGS_TO]->(Category): Required
```

### Validation Rules

```cypher
-- Check for negative prices
MATCH (p:Product)
WHERE p.price <= 0
RETURN "VIOLATION: Invalid price" as violation, p.product_id, p.price

-- Check for duplicate emails
MATCH (c:Customer)
WITH c.email, COUNT(*) as cnt
WHERE cnt > 1 AND c.email IS NOT NULL
RETURN "VIOLATION: Duplicate email" as violation, c.email, cnt

-- Check for orders with no items
MATCH (o:Order)
WHERE NOT (o)-[:CONTAINS]->()
RETURN "WARNING: Empty order" as warning, o.order_id

-- Check for products in no category
MATCH (p:Product)
WHERE NOT (p)-[:BELONGS_TO]->()
RETURN "WARNING: Uncategorized product" as warning, p.product_id

-- Validate order totals
MATCH (o:Order)-[:CONTAINS]->(oi:OrderItem)-[:OF_PRODUCT]->(p:Product)
WITH o, SUM(oi.quantity * oi.unit_price) as calculated_total
WHERE calculated_total != o.total
RETURN "VIOLATION: Order total mismatch" as violation, o.order_id, calculated_total, o.total
```

### Validation Report

```
VALIDATION: E-Commerce Schema
==============================

Total Orders: 5,240
Total Items: 12,150
Violations Found: 2
Warnings: 8
Conformance: 99.9%

CRITICAL:
1. ✗ Invalid prices (2 products)
   Products: SKU-4521, SKU-7834
   Issue: Price <= 0
   Fix: Update prices

2. ✗ Order total mismatch (0 violations - OK)

WARNINGS:
1. ⚠ Empty orders (3): O004521, O005123, O006445
   Fix: Add items or cancel orders

2. ⚠ Uncategorized products (5)
   Fix: Assign to categories

Overall Status: REVIEW REQUIRED
Action: Fix warnings and investigate empty orders
```

---

## Example 3: RDF/OWL Ontology Validation

### SHACL Shapes Definition

```turtle
@prefix ex: <http://example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:ResearcherShape a sh:NodeShape ;
  sh:targetClass ex:Researcher ;
  sh:property [
    sh:path ex:name ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:maxCount 1
  ] ;
  sh:property [
    sh:path ex:email ;
    sh:datatype xsd:string ;
    sh:pattern "^[^@]+@[^@]+\\.[^@]+$"
  ] ;
  sh:property [
    sh:path ex:writes ;
    sh:class ex:Paper ;
    sh:minCount 0
  ] .

ex:PaperShape a sh:NodeShape ;
  sh:targetClass ex:Paper ;
  sh:property [
    sh:path ex:title ;
    sh:datatype xsd:string ;
    sh:minCount 1
  ] ;
  sh:property [
    sh:path ex:writtenBy ;
    sh:class ex:Researcher ;
    sh:minCount 1 ;
    sh:maxCount 10
  ] .
```

### Validation with PyShACL

```python
from pyshacl import validate
from rdflib import Graph

# Load data and shapes
data_graph = Graph().parse("research_data.ttl", format="turtle")
shapes_graph = Graph().parse("research_shapes.ttl", format="turtle")

# Validate
conforms, results_graph, results_text = validate(
    data_graph, 
    shacl_graph=shapes_graph
)

if conforms:
    print("✓ All data conforms to shapes")
else:
    print("✗ Violations found:")
    print(results_text)
```

### Validation Report

```
VALIDATION: Research Ontology (SHACL)
======================================

Violations Found: 4
Conforms: False

VIOLATION 1:
- Type: MinCount
- Focus: ex:researcher_42
- Property: ex:name
- Message: Minimum count is 1 but the value is 0

VIOLATION 2:
- Type: Pattern
- Focus: ex:researcher_15
- Property: ex:email
- Value: "invalid_email"
- Message: Email does not match pattern

VIOLATION 3:
- Type: ClassType
- Focus: ex:paper_108
- Property: ex:writtenBy
- Message: Value is not of class ex:Researcher

VIOLATION 4:
- Type: MaxCount
- Focus: ex:paper_56
- Property: ex:writtenBy
- Message: Maximum count is 10 but value is 12

RECOMMENDATIONS:
1. Add name to researcher_42
2. Fix email format for researcher_15
3. Verify author references in paper_108
4. Review/split authors for paper_56
```

---

## Example 4: Property Graph Data Quality Check

### Dataset: Social Network

```cypher
-- Overall Statistics
MATCH (n) RETURN COUNT(n) as total_nodes, 
       COUNT(DISTINCT labels(n)) as distinct_labels;

-- Check data completeness
MATCH (u:User)
RETURN 
  COUNT(u) as total_users,
  COUNT(CASE WHEN u.username IS NOT NULL THEN 1 END) as with_username,
  COUNT(CASE WHEN u.email IS NOT NULL THEN 1 END) as with_email,
  COUNT(CASE WHEN u.created_date IS NOT NULL THEN 1 END) as with_date;

-- Property Statistics
MATCH (n)
WITH DISTINCT keys(n) as props
UNWIND props as prop
RETURN prop, COUNT(*) as frequency
ORDER BY frequency DESC;

-- Relationship Validation
MATCH (a)-[r]->(b)
RETURN type(r) as rel_type,
       labels(a)[0] as source_type,
       labels(b)[0] as target_type,
       COUNT(r) as count;

-- Find Anomalies
MATCH (u:User)
WHERE u.email IS NULL OR 
      NOT u.username =~ '[a-zA-Z0-9_]+' OR
      u.joined_date > date.today()
RETURN u.username, u.email, u.joined_date
AS anomalies;
```

---

## Comparison Table

| Aspect | University | E-Commerce | Research | Social |
|--------|-----------|-----------|----------|--------|
| **Type** | Property Graph | Property Graph | RDF/OWL | Property Graph |
| **Nodes** | 1,250 | 5,240+ | 1,000+ | 50,000+ |
| **Constraints** | 4 | 5 | 8 | 3 |
| **Violations** | 3 | 2 | 4 | Varies |
| **Conformance** | 96.2% | 99.9% | 85% | 98% |

---

See [validation-patterns.md](../references/validation-patterns.md) for detailed validation patterns and best practices.

