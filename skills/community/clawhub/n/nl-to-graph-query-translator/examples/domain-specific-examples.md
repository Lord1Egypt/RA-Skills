# Domain-Specific Examples

This document provides real-world examples across different business domains and use cases.

## HR and Employee Management Domain

### Example 1: Employee Directory

**Natural Language:**
```
Find all managers in the Engineering department
```

**Cypher:**
```cypher
MATCH (m:Manager)-[:MANAGES]->(e:Employee)-[:IN_DEPARTMENT]->(d:Department {name: "Engineering"})
RETURN DISTINCT m
```

---

### Example 2: Organizational Hierarchy

**Natural Language:**
```
Show the full reporting chain from an employee to the CEO
```

**Cypher:**
```cypher
MATCH path = (emp:Employee {name: "Bob"})-[:REPORTS_TO*0..]->(ceo:Employee {title: "CEO"})
RETURN [node in nodes(path) | node.name] as reporting_chain
```

---

### Example 3: Team Composition

**Natural Language:**
```
List all teams and the count of employees in each
```

**Cypher:**
```cypher
MATCH (t:Team)-[:HAS_MEMBER]->(e:Employee)
RETURN t.name as team_name, COUNT(e) as employee_count
GROUP BY t.name
ORDER BY employee_count DESC
```

---

### Example 4: Skill Matching

**Natural Language:**
```
Find employees with Python skills who work in the Backend team
```

**Cypher:**
```cypher
MATCH (e:Employee)-[:HAS_SKILL]->(s:Skill {name: "Python"}),
      (e)-[:WORKS_IN]->(t:Team {name: "Backend"})
RETURN e
```

---

## E-Commerce Domain

### Example 5: Product Recommendations

**Natural Language:**
```
Show products frequently bought together with iPhone
```

**Cypher:**
```cypher
MATCH (p1:Product {name: "iPhone"})<-[:PURCHASED]-(c:Customer)-[:PURCHASED]->(p2:Product)
WHERE p1 <> p2
RETURN p2.name, COUNT(*) as frequency
GROUP BY p2.name
ORDER BY frequency DESC
LIMIT 10
```

---

### Example 6: Customer Segmentation

**Natural Language:**
```
Find high-value customers who haven't purchased in the last 90 days
```

**Cypher:**
```cypher
MATCH (c:Customer)-[:PURCHASED]->(p:Product)
WITH c, SUM(p.price) as total_spent, MAX(datetime(p.purchase_date)) as last_purchase
WHERE total_spent > 1000 AND duration.between(last_purchase, datetime()).days > 90
RETURN c
```

---

### Example 7: Inventory Chain

**Natural Language:**
```
Show the supply chain from raw materials to final product
```

**Cypher:**
```cypher
MATCH path = (material:RawMaterial)-[:USED_IN*]->(product:Product)
RETURN path
```

---

## Social Network Domain

### Example 8: Friend Recommendations

**Natural Language:**
```
Find people you might know (friends of friends not yet connected)
```

**Cypher:**
```cypher
MATCH (user:User {name: "Alice"})-[:FOLLOWS]->(friend:User)-[:FOLLOWS]->(recommended:User)
WHERE NOT (user)-[:FOLLOWS]->(recommended) AND recommended <> user
RETURN DISTINCT recommended
LIMIT 20
```

---

### Example 9: Influencer Identification

**Natural Language:**
```
Find the most connected users (influencers) with at least 1000 followers
```

**Cypher:**
```cypher
MATCH (u:User)-[:FOLLOWED_BY]-(follower:User)
WITH u, COUNT(follower) as follower_count
WHERE follower_count > 1000
RETURN u.name, follower_count
ORDER BY follower_count DESC
```

---

### Example 10: Community Detection

**Natural Language:**
```
Find groups of users who frequently interact with each other
```

**Cypher:**
```cypher
MATCH (u1:User)-[:INTERACTS_WITH]-(u2:User)-[:INTERACTS_WITH]-(u3:User)-[:INTERACTS_WITH]-(u1)
RETURN DISTINCT u1, u2, u3
```

---

## Healthcare Domain

### Example 11: Patient Treatment History

**Natural Language:**
```
Show all treatments and medications for a patient
```

**Cypher:**
```cypher
MATCH (p:Patient {name: "John"})-[:RECEIVED]->(t:Treatment)-[:PRESCRIBES]->(m:Medication)
RETURN t.date as treatment_date, t.name as treatment, m.name as medication
ORDER BY t.date DESC
```

---

### Example 12: Drug Interaction Warnings

**Natural Language:**
```
Find medications that interact with Aspirin
```

**Cypher:**
```cypher
MATCH (aspirin:Medication {name: "Aspirin"})-[:INTERACTS_WITH]-(other:Medication)
RETURN other.name
```

---

### Example 13: Hospital Network Analysis

**Natural Language:**
```
Find which hospital has the most patient referrals
```

**Cypher:**
```cypher
MATCH (from_hospital:Hospital)<-[:REFERRED_FROM]-(p:Patient)-[:REFERRED_TO]->(to_hospital:Hospital)
RETURN from_hospital.name, to_hospital.name, COUNT(*) as referral_count
GROUP BY from_hospital.name, to_hospital.name
ORDER BY referral_count DESC
```

---

## Finance Domain

### Example 14: Transaction Networks

**Natural Language:**
```
Show all transactions between Alice and Bob, either direct or through intermediaries
```

**Cypher:**
```cypher
MATCH path = (alice:Account {holder: "Alice"})-[:SENT_TO|:RECEIVED_FROM*]-(bob:Account {holder: "Bob"})
RETURN path
```

---

### Example 15: Fraud Ring Detection

**Natural Language:**
```
Find groups of accounts that frequently transfer money to each other
```

**Cypher:**
```cypher
MATCH (a1:Account)-[:SENT_TO]-(a2:Account)-[:SENT_TO]-(a3:Account)-[:SENT_TO]-(a1)
RETURN a1, a2, a3
```

---

### Example 16: Credit Network

**Natural Language:**
```
Show credit lines and total credit exposure for a company
```

**Cypher:**
```cypher
MATCH (bank:Bank)-[:EXTENDED_CREDIT_TO]->(company:Company)
RETURN bank.name, SUM(credit_line.amount) as total_credit
GROUP BY bank.name
```

---

## Real Estate Domain

### Example 17: Property Network

**Natural Language:**
```
Find all properties owned by investors who also own commercial real estate
```

**Cypher:**
```cypher
MATCH (investor:Investor)-[:OWNS]->(commercial:Property {type: "Commercial"})
MATCH (investor)-[:OWNS]->(residential:Property {type: "Residential"})
RETURN investor.name, COUNT(residential) as residential_count, COUNT(commercial) as commercial_count
```

---

### Example 18: Neighborhood Connectivity

**Natural Language:**
```
Show all properties within 1km of a specific address that are for sale
```

**Cypher:**
```cypher
MATCH (ref_property:Property {address: "123 Main St"})-[:NEAR {distance_m: distance}]->(nearby:Property {status: "For Sale"})
WHERE distance < 1000
RETURN nearby
ORDER BY distance ASC
```

---

## Knowledge Management Domain

### Example 19: Topic Hierarchy

**Natural Language:**
```
Show the full taxonomy from a topic to its root
```

**Cypher:**
```cypher
MATCH path = (topic:Topic {name: "Machine Learning"})-[:SUBTOPIC_OF*0..]->(root:Topic)
WHERE NOT (root)-[:SUBTOPIC_OF]->()
RETURN [node in nodes(path) | node.name] as hierarchy
```

---

### Example 20: Expert Finding

**Natural Language:**
```
Find experts in a specific technology with active contributions this year
```

**Cypher:**
```cypher
MATCH (expert:Person)-[:EXPERT_IN]->(tech:Technology {name: "Kubernetes"}),
      (expert)-[:CONTRIBUTED]->(article:Article)
WHERE article.published_date.year = 2026
RETURN expert.name, COUNT(article) as contribution_count
```

---

## Manufacturing Domain

### Example 21: Supply Chain Optimization

**Natural Language:**
```
Find suppliers and their delivery times for a specific component
```

**Cypher:**
```cypher
MATCH (supplier:Supplier)-[delivery:SUPPLIES]->(component:Component {name: "CPU"})
RETURN supplier.name, delivery.delivery_time_days, delivery.price
ORDER BY delivery.delivery_time_days ASC
```

---

### Example 22: Quality Issues Tracking

**Natural Language:**
```
Show all defects reported for a product and their root causes
```

**Cypher:**
```cypher
MATCH (product:Product {name: "Model-X"})-[:HAS_DEFECT]->(defect:Defect)-[:CAUSED_BY]->(root_cause:RootCause)
RETURN defect.id, defect.date_reported, root_cause.description, COUNT(*) as frequency
GROUP BY defect.id, root_cause.description
ORDER BY frequency DESC
```

---

## Academic Domain

### Example 23: Degree Requirements

**Natural Language:**
```
Show all courses required for a Computer Science degree
```

**Cypher:**
```cypher
MATCH (degree:Degree {name: "Computer Science"})-[:REQUIRES*]->(course:Course)
RETURN course.code, course.name
ORDER BY course.code
```

---

### Example 24: Research Collaboration

**Natural Language:**
```
Find researchers who collaborated on papers in AI and have co-authors in common
```

**Cypher:**
```cypher
MATCH (r1:Researcher)-[:AUTHORED]->(paper1:Paper)-[:IN_FIELD]->(field:Field {name: "AI"}),
      (r2:Researcher)-[:AUTHORED]->(paper2:Paper)-[:IN_FIELD]->(field),
      (r1)-[:COLLABORATES_WITH]-(common:Researcher)-[:COLLABORATES_WITH]-(r2)
WHERE r1 <> r2
RETURN r1.name, r2.name, common.name
```

---

## Cross-Domain Patterns

### Example 25: Temporal Queries

**Natural Language:**
```
Find events that happened within a week of each other
```

**Cypher:**
```cypher
MATCH (e1:Event)-[:PRECEDES]->(e2:Event)
WHERE duration.between(e1.timestamp, e2.timestamp).days <= 7
RETURN e1.name, e2.name, duration.between(e1.timestamp, e2.timestamp).days as days_apart
```

---

### Example 26: Multi-Level Aggregation

**Natural Language:**
```
Show average metrics by department and then by company
```

**Cypher:**
```cypher
MATCH (e:Employee)-[:IN_DEPARTMENT]->(d:Department)-[:PART_OF]->(c:Company)
WITH c, d, AVG(e.salary) as avg_dept_salary
WITH c, AVG(avg_dept_salary) as avg_company_salary, COUNT(d) as dept_count
RETURN c.name, avg_company_salary, dept_count
ORDER BY avg_company_salary DESC
```

---

## Summary

These domain-specific examples demonstrate:
- ✅ Real-world business scenarios
- ✅ Complex multi-hop traversals
- ✅ Aggregations and analytics
- ✅ Temporal queries
- ✅ Domain-specific patterns

For more examples, combine techniques from:
- [Basic Translations](basic-translations.md)
- [Multi-Hop Queries](multi-hop-queries.md)
- [Parameterized Queries](parameterized-queries.md)

