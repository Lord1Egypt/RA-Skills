# Neo4j Integration - Examples

Real-world examples demonstrating Neo4j usage across multiple domains.

---

## Example 1: Social Network Graph

Build and query a social network with users, friendships, and interactions.

### Schema

```cypher
CREATE (alice:User {id: "user_alice", name: "Alice", email: "alice@example.com", joined: 2020})
CREATE (bob:User {id: "user_bob", name: "Bob", email: "bob@example.com", joined: 2019})
CREATE (carol:User {id: "user_carol", name: "Carol", email: "carol@example.com", joined: 2021})

CREATE (alice)-[:FOLLOWS {since: 2022}]->(bob)
CREATE (bob)-[:FOLLOWS {since: 2022}]->(alice)
CREATE (alice)-[:FOLLOWS {since: 2023}]->(carol)
```

### Common Queries

**Find mutual friends:**
```cypher
MATCH (a:User {name: "Alice"})-[:FOLLOWS]->(f:User)<-[:FOLLOWS]-(a)
RETURN f.name AS mutual_friend
```

**Find friends of friends:**
```cypher
MATCH (a:User {name: "Alice"})-[:FOLLOWS]->()-[:FOLLOWS]->(friend:User)
WHERE friend.id <> a.id
RETURN DISTINCT friend.name
```

**Social distance between two users:**
```cypher
MATCH (a:User {name: "Alice"}), (b:User {name: "Bob"})
MATCH path = shortestPath((a)-[:FOLLOWS*]-(b))
RETURN LENGTH(path) AS distance
```

**Find influencers (most followed):**
```cypher
MATCH (u:User)<-[:FOLLOWS]-(followers:User)
RETURN u.name, COUNT(followers) AS follower_count
ORDER BY follower_count DESC
LIMIT 10
```

---

## Example 2: E-Commerce Product Network

Manage products, categories, suppliers, and customer interactions.

### Schema

```cypher
CREATE (laptop:Product {id: "prod_001", name: "Laptop Pro", price: 1299.99, stock: 50})
CREATE (mouse:Product {id: "prod_002", name: "Wireless Mouse", price: 29.99, stock: 200})

CREATE (electronics:Category {id: "cat_elec", name: "Electronics"})
CREATE (peripherals:Category {id: "cat_peri", name: "Peripherals"})

CREATE (supplier:Supplier {id: "supp_001", name: "TechCorp Inc"})

CREATE (customer:Customer {id: "cust_001", name: "John Doe"})

CREATE (laptop)-[:IN_CATEGORY]->(electronics)
CREATE (mouse)-[:IN_CATEGORY]->(peripherals)
CREATE (laptop)-[:SUPPLIED_BY]->(supplier)
CREATE (customer)-[:PURCHASED {quantity: 1, date: "2024-01-15"}]->(laptop)
```

### Common Queries

**Products in category:**
```cypher
MATCH (p:Product)-[:IN_CATEGORY]->(c:Category {name: "Electronics"})
RETURN p.name, p.price
ORDER BY p.price DESC
```

**Customer purchase history:**
```cypher
MATCH (c:Customer {name: "John Doe"})-[r:PURCHASED]->(p:Product)
RETURN p.name, r.quantity, r.date
ORDER BY r.date DESC
```

**Product recommendations (customers who bought similar items):**
```cypher
MATCH (c:Customer)-[:PURCHASED]->(p:Product)<-[:PURCHASED]-(other:Customer)
WHERE c.name = "John Doe" AND other.name <> c.name
MATCH (other)-[:PURCHASED]->(rec:Product)
WHERE NOT (c)-[:PURCHASED]->(rec)
RETURN DISTINCT rec.name, COUNT(*) AS rec_count
ORDER BY rec_count DESC
```

**Supplier relationships:**
```cypher
MATCH (s:Supplier {name: "TechCorp Inc"})<-[:SUPPLIED_BY]-(p:Product)
RETURN s.name, COUNT(p) AS product_count, SUM(p.stock) AS total_stock
```

---

## Example 3: Knowledge Base / Documentation Network

Create a documentation system with topics, relationships, and dependencies.

### Schema

```cypher
CREATE (python:Topic {id: "topic_py", name: "Python", level: "beginner"})
CREATE (functions:Topic {id: "topic_func", name: "Functions", level: "beginner"})
CREATE (oop:Topic {id: "topic_oop", name: "Object-Oriented Programming", level: "intermediate"})
CREATE (fastapi:Topic {id: "topic_fa", name: "FastAPI", level: "advanced"})

CREATE (python)-[:PREREQUISITE_FOR]->(functions)
CREATE (functions)-[:PREREQUISITE_FOR]->(oop)
CREATE (python)-[:PREREQUISITE_FOR]->(fastapi)
CREATE (oop)-[:PREREQUISITE_FOR]->(fastapi)

CREATE (doc:Document {id: "doc_001", title: "Python Basics", topic_id: "topic_py"})
CREATE (doc2:Document {id: "doc_002", title: "Functions Guide", topic_id: "topic_func"})

CREATE (doc)-[:COVERS]->(python)
CREATE (doc2)-[:COVERS]->(functions)
```

### Common Queries

**Learning path from Python to FastAPI:**
```cypher
MATCH (start:Topic {name: "Python"}), (end:Topic {name: "FastAPI"})
MATCH path = shortestPath((start)-[:PREREQUISITE_FOR*]->(end))
RETURN [node IN nodes(path) | node.name] AS learning_path
```

**All prerequisites for a topic:**
```cypher
MATCH (t:Topic {name: "FastAPI"})<-[:PREREQUISITE_FOR*]-(prereq:Topic)
RETURN DISTINCT prereq.name AS prerequisite
```

**Documentation by topic:**
```cypher
MATCH (doc:Document)-[:COVERS]->(t:Topic {name: "Python"})
RETURN doc.title, t.name
```

---

## Example 4: Organizational Hierarchy

Model company structure with employees, departments, and reporting relationships.

### Schema

```cypher
CREATE (ceo:Employee {id: "emp_001", name: "CEO", title: "Chief Executive Officer"})
CREATE (cto:Employee {id: "emp_002", name: "Alice Smith", title: "CTO"})
CREATE (dev_lead:Employee {id: "emp_003", name: "Bob Johnson", title: "Dev Lead"})
CREATE (dev:Employee {id: "emp_004", name: "Carol Davis", title: "Developer"})

CREATE (eng_dept:Department {id: "dept_eng", name: "Engineering"})

CREATE (ceo)-[:MANAGES {since: 2015}]->(cto)
CREATE (cto)-[:MANAGES {since: 2018}]->(dev_lead)
CREATE (dev_lead)-[:MANAGES {since: 2020}]->(dev)

CREATE (cto)-[:WORKS_IN]->(eng_dept)
CREATE (dev_lead)-[:WORKS_IN]->(eng_dept)
CREATE (dev)-[:WORKS_IN]->(eng_dept)
```

### Common Queries

**Organizational chart (management chain):**
```cypher
MATCH (emp:Employee {name: "CEO"})-[:MANAGES*]->(subordinate:Employee)
RETURN DISTINCT subordinate.name, subordinate.title
```

**Direct reports:**
```cypher
MATCH (manager:Employee {name: "Alice Smith"})-[:MANAGES]->(direct:Employee)
RETURN direct.name, direct.title
```

**Department members:**
```cypher
MATCH (dept:Department {name: "Engineering"})<-[:WORKS_IN]-(emp:Employee)
RETURN emp.name, emp.title
```

**Chain of command (path to CEO):**
```cypher
MATCH (emp:Employee {name: "Carol Davis"})<-[:MANAGES*]-(head:Employee)
RETURN head.name, COUNT(*) AS levels
```

---

## Example 5: Research Paper Citation Network

Build a research publication graph with papers, authors, and citations.

### Schema

```cypher
CREATE (paper1:Paper {id: "paper_001", title: "Graph Neural Networks", year: 2020})
CREATE (paper2:Paper {id: "paper_002", title: "Attention Mechanisms", year: 2017})
CREATE (paper3:Paper {id: "paper_003", title: "Transformer Architecture", year: 2017})

CREATE (alice:Author {id: "author_alice", name: "Alice Johnson"})
CREATE (bob:Author {id: "author_bob", name: "Bob Smith"})
CREATE (carol:Author {id: "author_carol", name: "Carol Wang"})

CREATE (ml:Field {id: "field_ml", name: "Machine Learning"})
CREATE (dl:Field {id: "field_dl", name: "Deep Learning"})

CREATE (alice)-[:WROTE {position: 1}]->(paper1)
CREATE (bob)-[:WROTE {position: 2}]->(paper1)
CREATE (bob)-[:WROTE {position: 1}]->(paper2)
CREATE (carol)-[:WROTE {position: 1}]->(paper3)

CREATE (paper1)-[:CITES {strength: 0.9}]->(paper2)
CREATE (paper1)-[:CITES {strength: 0.85}]->(paper3)
CREATE (paper2)-[:IN_FIELD]->(dl)
CREATE (paper3)-[:IN_FIELD]->(dl)
```

### Common Queries

**Citation graph (what papers cite a paper):**
```cypher
MATCH (paper:Paper {title: "Attention Mechanisms"})<-[:CITES]-(citing:Paper)
RETURN citing.title, citing.year
ORDER BY citing.year DESC
```

**Author collaborations:**
```cypher
MATCH (author:Author {name: "Bob Smith"})-[:WROTE]->(p:Paper)<-[:WROTE]-(collaborator:Author)
WHERE collaborator.name <> author.name
RETURN DISTINCT collaborator.name, COUNT(p) AS papers_together
```

**Papers by author with citations received:**
```cypher
MATCH (author:Author {name: "Alice Johnson"})-[:WROTE]->(paper:Paper)
MATCH (citing:Paper)-[:CITES]->(paper)
RETURN paper.title, COUNT(citing) AS citation_count
ORDER BY citation_count DESC
```

**Research trajectory (author papers by year):**
```cypher
MATCH (author:Author {name: "Bob Smith"})-[:WROTE]->(paper:Paper)
RETURN paper.year, COLLECT(paper.title) AS papers
ORDER BY paper.year
```

**Co-authorship network:**
```cypher
MATCH (a1:Author)-[:WROTE]->(paper:Paper)<-[:WROTE]-(a2:Author)
WHERE a1.name = "Alice Johnson" AND a1.id < a2.id
RETURN DISTINCT a2.name, COUNT(paper) AS collaborations
ORDER BY collaborations DESC
```

---

## Index Best Practices

For each example, create indexes on frequently queried properties:

### Social Network Indexes
```cypher
CREATE INDEX user_id FOR (u:User) ON (u.id)
CREATE INDEX user_name FOR (u:User) ON (u.name)
```

### E-Commerce Indexes
```cypher
CREATE INDEX product_id FOR (p:Product) ON (p.id)
CREATE INDEX product_price FOR (p:Product) ON (p.price)
CREATE INDEX customer_id FOR (c:Customer) ON (c.id)
```

### Knowledge Base Indexes
```cypher
CREATE INDEX topic_name FOR (t:Topic) ON (t.name)
CREATE INDEX doc_id FOR (d:Document) ON (d.id)
```

### Organizational Indexes
```cypher
CREATE INDEX emp_id FOR (e:Employee) ON (e.id)
CREATE INDEX dept_name FOR (d:Department) ON (d.name)
```

### Citation Network Indexes
```cypher
CREATE INDEX paper_id FOR (p:Paper) ON (p.id)
CREATE INDEX paper_year FOR (p:Paper) ON (p.year)
CREATE INDEX author_name FOR (a:Author) ON (a.name)
```

---

## Transaction Example

Safe data insertion with rollback capability:

```cypher
BEGIN
CREATE (p:Product {id: "new_prod", name: "New Product", price: 99.99})
CREATE (c:Category {id: "new_cat", name: "New Category"})
CREATE (p)-[:IN_CATEGORY]->(c)
COMMIT
```

---

## Bulk Import Example

Loading data from CSV:

```cypher
LOAD CSV WITH HEADERS FROM "file:///products.csv" AS row
CREATE (p:Product {
    id: row.product_id,
    name: row.product_name,
    price: toFloat(row.price),
    stock: toInteger(row.stock)
})
```

---


