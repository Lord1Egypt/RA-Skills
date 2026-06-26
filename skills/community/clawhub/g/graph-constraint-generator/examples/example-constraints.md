# Constraint Generation Examples

Complete constraint examples for different domains.

## Example 1: University Domain Constraints

### Schema Definition

```
Entities:
  Student: student_id (unique), name (required), email (unique)
  Professor: professor_id (unique), name (required)
  Course: course_code (unique), title (required), credits
  Department: dept_id (unique), name (required)

Relationships:
  (Student)-[:ENROLLED_IN]->(Course): min 1, max 10
  (Professor)-[:TEACHES]->(Course): min 1, max 5
  (Department)-[:MANAGES]->(Course): min 0, max unlimited
  (Department)-[:EMPLOYS]->(Professor): min 1
```

### Generated Neo4j Constraints

```cypher
-- Unique Constraints
CREATE CONSTRAINT student_id_unique ON (s:Student) REQUIRE s.student_id IS UNIQUE
CREATE CONSTRAINT professor_id_unique ON (p:Professor) REQUIRE p.professor_id IS UNIQUE
CREATE CONSTRAINT course_code_unique ON (c:Course) REQUIRE c.course_code IS UNIQUE
CREATE CONSTRAINT dept_id_unique ON (d:Department) REQUIRE d.dept_id IS UNIQUE
CREATE CONSTRAINT student_email_unique ON (s:Student) REQUIRE s.email IS UNIQUE

-- Indexes
CREATE INDEX ON (s:Student)(name)
CREATE INDEX ON (p:Professor)(name)
CREATE INDEX ON (c:Course)(title)
CREATE INDEX ON (d:Department)(name)

-- Validation Queries
MATCH (s:Student) WHERE s.name IS NULL RETURN s  -- Should be empty
MATCH (c:Course) WHERE c.title IS NULL RETURN c  -- Should be empty
MATCH (s:Student) WHERE NOT (s)-[:ENROLLED_IN]->() RETURN s  -- Check min enrollment
```

### Generated SHACL Shapes

```turtle
@prefix ex: <http://example.org/university#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:StudentShape a sh:NodeShape ;
  sh:targetClass ex:Student ;
  sh:property [
    sh:path ex:student_id ;
    sh:minCount 1 ;
    sh:maxCount 1
  ] ;
  sh:property [
    sh:path ex:name ;
    sh:datatype xsd:string ;
    sh:minCount 1
  ] ;
  sh:property [
    sh:path ex:email ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:pattern "^[^@]+@[^@]+\\.[^@]+$"
  ] ;
  sh:property [
    sh:path ex:enrolledIn ;
    sh:class ex:Course ;
    sh:minCount 1 ;
    sh:maxCount 10
  ] .

ex:ProfessorShape a sh:NodeShape ;
  sh:targetClass ex:Professor ;
  sh:property [
    sh:path ex:professor_id ;
    sh:minCount 1
  ] ;
  sh:property [
    sh:path ex:name ;
    sh:datatype xsd:string ;
    sh:minCount 1
  ] ;
  sh:property [
    sh:path ex:teaches ;
    sh:class ex:Course ;
    sh:minCount 1 ;
    sh:maxCount 5
  ] .
```

---

## Example 2: E-Commerce Domain Constraints

### Schema Definition

```
Entities:
  Customer: customer_id (unique), email (unique), name (required)
  Product: product_id (unique), sku (unique), price > 0
  Order: order_id (unique), total > 0
  Category: category_id (unique), name (required)

Relationships:
  (Customer)-[:PLACES]->(Order): min 0, max unlimited
  (Order)-[:CONTAINS]->(Product): min 1, max 1000
  (Product)-[:BELONGS_TO]->(Category): min 1, max 1
```

### Generated Neo4j Constraints

```cypher
-- Unique Constraints
CREATE CONSTRAINT customer_id_unique ON (c:Customer) REQUIRE c.customer_id IS UNIQUE
CREATE CONSTRAINT email_unique ON (c:Customer) REQUIRE c.email IS UNIQUE
CREATE CONSTRAINT product_id_unique ON (p:Product) REQUIRE p.product_id IS UNIQUE
CREATE CONSTRAINT sku_unique ON (p:Product) REQUIRE p.sku IS UNIQUE
CREATE CONSTRAINT order_id_unique ON (o:Order) REQUIRE o.order_id IS UNIQUE
CREATE CONSTRAINT category_id_unique ON (cat:Category) REQUIRE cat.category_id IS UNIQUE

-- Data Type Validation Queries
MATCH (p:Product) WHERE p.price <= 0 RETURN p  -- Should be empty
MATCH (o:Order) WHERE o.total <= 0 RETURN o  -- Should be empty
MATCH (c:Customer) WHERE c.name IS NULL RETURN c  -- Should be empty

-- Relationship Validation Queries
MATCH (p:Product) WHERE NOT (p)-[:BELONGS_TO]->() RETURN p  -- All products must have category
MATCH (o:Order) WHERE NOT (o)-[:CONTAINS]->() RETURN o  -- All orders must contain items
```

---

## Example 3: RDF/OWL Constraints

### SHACL Shapes

```turtle
@prefix ex: <http://example.org/research#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:ResearcherShape a sh:NodeShape ;
  sh:targetClass ex:Researcher ;
  sh:nodeKind sh:IRI ;
  sh:property [
    sh:path foaf:name ;
    sh:minCount 1 ;
    sh:datatype xsd:string
  ] ;
  sh:property [
    sh:path foaf:email ;
    sh:minCount 1 ;
    sh:pattern "^[^@]+@[^@]+\\.[^@]+$"
  ] ;
  sh:property [
    sh:path ex:writes ;
    sh:class ex:Paper ;
    sh:minCount 1
  ] .

ex:PaperShape a sh:NodeShape ;
  sh:targetClass ex:Paper ;
  sh:property [
    sh:path ex:title ;
    sh:minCount 1 ;
    sh:datatype xsd:string ;
    sh:minLength 5
  ] ;
  sh:property [
    sh:path ex:writtenBy ;
    sh:class ex:Researcher ;
    sh:minCount 1 ;
    sh:maxCount 10
  ] ;
  sh:property [
    sh:path ex:publicationYear ;
    sh:datatype xsd:gYear ;
    sh:minInclusive "2000"^^xsd:gYear
  ] .
```

---

## Example 4: Social Network Constraints

### Constraint Specification

```
User: user_id (unique), username (unique), email (unique)
Post: post_id (unique), content (required), created_date (required)
Comment: comment_id (unique), text (required)

Cardinality:
- User can FOLLOW many users
- User can CREATE many posts (no max)
- Post can HAVE_COMMENT many (no max)
- Comment has exactly 1 author (min 1, max 1)
```

### Generated Constraints

```cypher
-- Unique Constraints
CREATE CONSTRAINT user_id_unique ON (u:User) REQUIRE u.user_id IS UNIQUE
CREATE CONSTRAINT username_unique ON (u:User) REQUIRE u.username IS UNIQUE
CREATE CONSTRAINT email_unique ON (u:User) REQUIRE u.email IS UNIQUE
CREATE CONSTRAINT post_id_unique ON (p:Post) REQUIRE p.post_id IS UNIQUE
CREATE CONSTRAINT comment_id_unique ON (c:Comment) REQUIRE c.comment_id IS UNIQUE

-- Required Property Validation
MATCH (p:Post) WHERE p.content IS NULL OR p.created_date IS NULL RETURN p
MATCH (c:Comment) WHERE c.text IS NULL RETURN c

-- Relationship Validation
MATCH (c:Comment) WHERE NOT (c)<-[:AUTHORED_BY]-(u:User) RETURN c  -- All comments need author
```

### SHACL Format

```turtle
ex:UserShape a sh:NodeShape ;
  sh:targetClass ex:User ;
  sh:property [
    sh:path ex:follows ;
    sh:class ex:User
  ] .

ex:PostShape a sh:NodeShape ;
  sh:targetClass ex:Post ;
  sh:property [
    sh:path ex:content ;
    sh:minCount 1 ;
    sh:datatype xsd:string ;
    sh:minLength 1
  ] ;
  sh:property [
    sh:path ex:createdDate ;
    sh:minCount 1 ;
    sh:datatype xsd:dateTime
  ] .

ex:CommentShape a sh:NodeShape ;
  sh:targetClass ex:Comment ;
  sh:property [
    sh:path ex:text ;
    sh:minCount 1 ;
    sh:datatype xsd:string
  ] ;
  sh:property [
    sh:path ex:authoredBy ;
    sh:class ex:User ;
    sh:minCount 1 ;
    sh:maxCount 1
  ] .
```

---

## Constraint Comparison Table

| Domain | Unique | Required | Relationships | Cardinality | Type |
|--------|--------|----------|---------------|-------------|------|
| University | 4 | 3 | 4 | 4 constraints | Mixed |
| E-Commerce | 6 | 1 | 3 | 3 constraints | Mixed |
| Research | 0 | 3 | 2 | 3 constraints | SHACL |
| Social | 5 | 2 | 3 | 2 constraints | Cypher |

---

See [constraint-patterns.md](../references/constraint-patterns.md) for detailed constraint patterns and best practices.

