# Query Debugging Examples

Five comprehensive real-world domain examples showing query issues, debugging approaches, and corrected solutions.

---

## 1. Business Domain: Employee-Company Relationships (Cypher)

### Business Context

A Human Resources knowledge graph tracks employees, their work locations, departments, and reporting structures.

### Broken Query 1: Missing Relationship Type Name

**Query:**
```cypher
MATCH (e:Employee)-[:MANAGES]->(c:Colleague)
RETURN e.name, c.name
```

**Error Analysis:**
- Relationship type `MANAGES` is likely singular, but the standard convention uses plural
- The target type should be `Manager`, not `Colleague`
- No parenthesis mismatch, but semantic error exists

**Corrected Query:**
```cypher
MATCH (e:Employee)-[:MANAGES]->(manager:Employee)
RETURN e.name, manager.name
```

**Or if the relationship is actually:**
```cypher
MATCH (manager:Employee)-[:MANAGES]->(e:Employee)
RETURN manager.name, e.name
```

### Broken Query 2: Schema Mismatch with Property Filter

**Query:**
```cypher
MATCH (e:Employee {salary: ">100000"})-[:WORKS_AT]->(d:Dept)
RETURN e.name, d.name
```

**Error Analysis:**
- The string `">100000"` should be a numeric comparison in a WHERE clause
- Salary is a numeric property, not a string to match
- Comparison operators cannot be used in property filters

**Corrected Query:**
```cypher
MATCH (e:Employee)-[:WORKS_AT]->(d:Dept)
WHERE e.salary > 100000
RETURN e.name, d.name
```

### Broken Query 3: Multi-Hop with Incorrect Directions

**Query:**
```cypher
MATCH (c:Company)<-[:REPORTS_TO]-(e:Employee)<-[:WORKS_IN]-(d:Dept)
RETURN c, e, d
```

**Error Analysis:**
- Direction: Company should have employees, not employees pointing to company
- `WORKS_IN` should likely be `WORKS_AT` and direction should be forward
- The relationship chain has reversed directions

**Corrected Query:**
```cypher
MATCH (c:Company)<-[:WORKS_AT]-(e:Employee)-[:IN_DEPT]->(d:Dept)
RETURN c, e, d
```

### Debugging Workflow for "No Results"

**Original Complex Query:**
```cypher
MATCH (e:Employee {dept:"Sales"})-[:REPORTS_TO]->(mgr:Employee)
-[:WORKS_AT]->(loc:Location {city:"NYC"})
RETURN e.name, mgr.name, loc.name
```

**Step 1: Verify Employees Exist**
```cypher
MATCH (e:Employee)
RETURN DISTINCT e.dept
LIMIT 10
```

**Step 2: Check if Property is "dept" or "department"**
```cypher
MATCH (e:Employee)
RETURN keys(e)
LIMIT 1
```

**Step 3: Verify Relationship Exists**
```cypher
MATCH (e:Employee)-[r:REPORTS_TO]->(mgr:Employee)
RETURN COUNT(r)
```

**Step 4: Test Each Hop Separately**
```cypher
MATCH (e:Employee)-[:WORKS_AT]->(loc:Location)
WHERE loc.city = "NYC"
RETURN COUNT(e)
```

**Corrected Multi-Step Query:**
```cypher
MATCH (e:Employee {department:"Sales"})-[:REPORTS_TO]->(mgr:Employee)
MATCH (mgr)-[:WORKS_AT]->(loc:Location)
WHERE loc.city = "NYC"
RETURN e.name, mgr.name, loc.name
```

---

## 2. Scientific Domain: Research Papers (SPARQL)

### Academic Context

A semantic research knowledge graph tracks researchers, papers, institutions, and research areas using RDF/OWL.

### Broken Query 1: Missing Prefixes

**Query:**
```sparql
SELECT ?researcher ?paper
WHERE {
  ?researcher rdf:type Person .
  ?researcher authored ?paper .
  ?paper hasKeyword "machine learning" .
}
```

**Error Analysis:**
- `Person` and the properties lack namespace prefixes
- RDF requires full URIs for all resource references
- The query references undefined terms

**Corrected Query:**
```sparql
PREFIX ex: <http://example.org/academic/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX schema: <http://schema.org/>

SELECT ?researcher ?paper
WHERE {
  ?researcher rdf:type ex:Researcher .
  ?researcher ex:authored ?paper .
  ?paper ex:hasKeyword "machine learning" .
}
```

### Broken Query 2: Type Mismatch in Filter

**Query:**
```sparql
PREFIX ex: <http://example.org/academic/>

SELECT ?paper ?citationCount
WHERE {
  ?paper rdf:type ex:Paper .
  ?paper ex:citationCount ?count .
  FILTER (?count > "50")
}
```

**Error Analysis:**
- `citationCount` is an integer literal, not a string
- Comparison operators require type-compatible values
- String "50" cannot be reliably compared with numeric values

**Corrected Query:**
```sparql
PREFIX ex: <http://example.org/academic/>

SELECT ?paper ?citationCount
WHERE {
  ?paper rdf:type ex:Paper .
  ?paper ex:citationCount ?citationCount .
  FILTER (?citationCount > 50)
}
```

### Broken Query 3: Missing Optional Pattern

**Query:**
```sparql
PREFIX ex: <http://example.org/academic/>

SELECT ?researcher ?email
WHERE {
  ?researcher rdf:type ex:Researcher .
  ?researcher ex:email ?email .
}
```

**Problem:** 
- Not all researchers have email addresses
- Query returns incomplete results if emails are missing

**Issue-Aware Query:**
```sparql
PREFIX ex: <http://example.org/academic/>

SELECT ?researcher ?email
WHERE {
  ?researcher rdf:type ex:Researcher .
  OPTIONAL { ?researcher ex:email ?email }
}
```

### Broken Query 4: Missing Transitive Property Handling

**Query:**
```sparql
PREFIX ex: <http://example.org/academic/>

SELECT ?institute
WHERE {
  ?researcher ex:affiliatedWith ?institute .
  ?researcher ex:collaboratesWith ?colleague .
}
```

**Problem:**
- Doesn't capture indirect collaborations
- Transitive relationships require explicit handling

**Enhanced Query with Transitive Relationships:**
```sparql
PREFIX ex: <http://example.org/academic/>

SELECT ?researcher ?colleague ?institute
WHERE {
  ?researcher ex:affiliatedWith ?institute .
  ?researcher ex:collaboratesWith+ ?colleague .
}
```

### Debugging Workflow

**Complex Query Returning No Results:**
```sparql
PREFIX ex: <http://example.org/academic/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?name ?paperTitle ?year
WHERE {
  ?researcher foaf:name ?name .
  ?researcher ex:authored ?paper .
  ?paper ex:title ?paperTitle .
  ?paper ex:year ?year .
  FILTER (?year >= 2020)
}
```

**Step 1: Check Researcher Data Structure**
```sparql
PREFIX ex: <http://example.org/academic/>

SELECT ?p ?o
WHERE {
  ?s rdf:type ex:Researcher .
  ?s ?p ?o .
}
LIMIT 10
```

**Step 2: Verify Authored Relationship**
```sparql
PREFIX ex: <http://example.org/academic/>

SELECT (COUNT(?paper) as ?paperCount)
WHERE {
  ?researcher ex:authored ?paper .
}
```

**Step 3: Check Paper Properties**
```sparql
PREFIX ex: <http://example.org/academic/>

SELECT ?property (COUNT(DISTINCT ?value) as ?valueCount)
WHERE {
  ?paper rdf:type ex:Paper .
  ?paper ?property ?value .
}
GROUP BY ?property
```

**Corrected Query:**
```sparql
PREFIX ex: <http://example.org/academic/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?name ?paperTitle ?year
WHERE {
  ?researcher foaf:name ?name .
  ?researcher ex:authoredPaper ?paper .
  ?paper dc:title ?paperTitle .
  ?paper ex:publicationYear ?year .
  FILTER (?year >= 2020)
}
```

---

## 3. E-Commerce Domain: Complex Multi-Hop Queries (Cypher)

### E-Commerce Context

An e-commerce platform tracks customers, orders, products, sellers, and shipping information.

### Broken Query: Missing Parentheses

**Query:**
```cypher
MATCH (c:Customer {id:"C123"})-[:PLACED]->(o:Order
-[:CONTAINS]->(p:Product)-[:SOLD_BY]->(s:Seller)
RETURN c.name, p.name, s.name
```

**Error:**
- Missing closing parenthesis after Order node
- Query cannot be parsed

**Corrected Query:**
```cypher
MATCH (c:Customer {id:"C123"})-[:PLACED]->(o:Order)
-[:CONTAINS]->(p:Product)-[:SOLD_BY]->(s:Seller)
RETURN c.name, p.name, s.name
```

### Broken Query: Relationship Direction

**Query:**
```cypher
MATCH (s:Seller)<-[:SOLD_BY]-(p:Product)<-[:CONTAINS]-(o:Order)
WHERE o.totalAmount > 1000
RETURN s.name, COUNT(p) as productCount
```

**Issue:**
- Directions are reversed; should track from Customer through Order to Product to Seller
- Grouping without GROUP BY returns unexpected results

**Corrected Query:**
```cypher
MATCH (c:Customer)-[:PLACED]->(o:Order)-[:CONTAINS]->(p:Product)-[:SOLD_BY]->(s:Seller)
WHERE o.totalAmount > 1000
RETURN s.name, COUNT(DISTINCT p) as productCount
GROUP BY s.name
```

### Broken Query: Cartesian Product

**Query:**
```cypher
MATCH (c:Customer), (p:Product)
WHERE c.country = "USA"
RETURN c.name, p.name
```

**Issue:**
- Creates Cartesian product of all US customers with all products
- Likely millions of result rows

**Corrected Query:**
```cypher
MATCH (c:Customer {country:"USA"})-[:PLACED]->(o:Order)-[:CONTAINS]->(p:Product)
RETURN c.name, p.name
```

### Debugging Workflow: Orders for Customers with High-Value Purchases

**Complex Query Returning Unexpected Results:**
```cypher
MATCH (c:Customer {premium:true})-[:PLACED]->(o:Order)
-[:CONTAINS]->(p:Product)
-[:HAS_INVENTORY]->(inv:Inventory)
WHERE p.price > 500 AND inv.stock > 0 AND o.status = "completed"
RETURN c.name, p.name, p.price
LIMIT 100
```

**Step 1: Verify Premium Customers Exist**
```cypher
MATCH (c:Customer)
RETURN DISTINCT c.premium
```

**Step 2: Check Customer-Order Relationships**
```cypher
MATCH (c:Customer {premium:true})-[r:PLACED]->(o:Order)
RETURN COUNT(r)
```

**Step 3: Verify Order Structure**
```cypher
MATCH (o:Order)
RETURN keys(o)
LIMIT 1
```

**Step 4: Test Each Filter**
```cypher
MATCH (c:Customer {premium:true})-[:PLACED]->(o:Order)
WHERE o.status = "completed"
RETURN COUNT(o)
```

**Corrected Query with Filters Applied Early:**
```cypher
MATCH (c:Customer {premium:true})
WHERE c.status = "active"
MATCH (c)-[:PLACED]->(o:Order)
WHERE o.status = "completed" AND o.createdDate > date("2024-01-01")
MATCH (o)-[:CONTAINS]->(p:Product)
WHERE p.price > 500
RETURN c.name, p.name, p.price, o.createdDate
ORDER BY o.createdDate DESC
LIMIT 100
```

---

## 4. Real Estate Domain: Schema Mismatch Detection (Cypher)

### Real Estate Context

A property management knowledge graph tracks properties, owners, tenants, mortgages, and locations.

### Broken Query 1: Non-Existent Property Labels

**Query:**
```cypher
MATCH (p:PropertyListing {status:"available"})-[:LOCATED_IN]->(c:City)
WHERE p.monthlyCost < 2000
RETURN p, c
```

**Issue:**
- The node label is `PropertyListing`, but schema uses `Property`
- Property references `monthlyCost`, but actual property is `monthlyRent`

**Schema Validation:**
```cypher
-- Check available labels
CALL db.labels()
YIELD label RETURN label

-- Check Property properties
MATCH (p:Property)
RETURN keys(p)
LIMIT 1
```

**Corrected Query:**
```cypher
MATCH (p:Property {status:"available"})-[:LOCATED_IN]->(c:City)
WHERE p.monthlyRent < 2000
RETURN p, c
```

### Broken Query 2: Incorrect Relationship Between Types

**Query:**
```cypher
MATCH (owner:Owner)-[:RENTS]->(property:Property)-[:MANAGES]->(mortgage:Mortgage)
RETURN owner, property, mortgage
```

**Issue:**
- Owners don't directly MANAGE mortgages
- Relationships: Owner -> Property -> (owned by Bank through) Mortgage
- Correct: Bank -[:HOLDS_MORTGAGE]-> Property

**Corrected Query:**
```cypher
MATCH (owner:Owner)-[:OWNS]->(property:Property)
MATCH (bank:Bank)-[:HOLDS_MORTGAGE]->(property)
RETURN owner, property, bank
```

### Broken Query 3: Missing Required Intermediates

**Query:**
```cypher
MATCH (owner:Owner)-[:MANAGES]->(tenant:Tenant)
RETURN owner, tenant
```

**Issue:**
- Owners don't directly manage tenants
- Tenants are managed through Properties they rent
- Relationship chain: Owner -> Property -> Tenant

**Corrected Query:**
```cypher
MATCH (owner:Owner)-[:OWNS]->(property:Property)-[:RENTED_BY]->(tenant:Tenant)
RETURN owner, property, tenant
```

---

## 5. Social Network Domain: Performance Issue Detection (Cypher)

### Social Network Context

A social media knowledge graph tracks users, posts, comments, friendships, and engagement metrics.

### Performance Issue 1: Inefficient Filter Placement

**Inefficient Query:**
```cypher
MATCH (user:User)-[:POSTED]->(post:Post)
-[:HAS_COMMENT]->(comment:Comment)-[:BY]->(commenter:User)
WHERE commenter.followerCount > 10000
RETURN COUNT(comment)
```

**Problem:**
- Filters applied after all relationship matching
- Processes millions of posts and comments before filtering

**Optimized Query:**
```cypher
MATCH (influencer:User)
WHERE influencer.followerCount > 10000
MATCH (influencer)<-[:BY]-(comment:Comment)
-[:HAS_COMMENT]-(post:Post)-[:POSTED]-(user:User)
RETURN COUNT(comment)
```

### Performance Issue 2: Cartesian Product

**Problematic Query:**
```cypher
MATCH (user:User), (friend:User)
WHERE user.country = "USA" AND friend.country = "USA"
RETURN user.name, friend.name
```

**Issue:**
- Creates Cartesian product of all US users (potentially millions × millions)

**Corrected Query:**
```cypher
MATCH (user:User {country:"USA"})-[:FRIENDS_WITH]-(friend:User)
RETURN user.name, friend.name
```

### Performance Issue 3: Missing Index

**Query That Runs Slowly:**
```cypher
MATCH (user:User {email:"alice@example.com"})
RETURN user
```

**Suggestion:**
```cypher
CREATE INDEX ON :User(email)
```

**Verification:**
```cypher
-- Check indexes
CALL db.indexes()
```

### Complex Query with Performance Issues

**Original Complex Query:**
```cypher
MATCH (user:User {verified:true})-[:POSTED]->(post:Post)
WHERE post.createdDate > datetime("2024-01-01T00:00:00Z")
MATCH (post)-[:HAS_COMMENT]-(comment:Comment)
MATCH (comment)-[:BY]-(commenter:User)
WHERE commenter.verified = true
MATCH (commenter)-[:FRIENDS_WITH]-(friend:User)
WHERE friend.followerCount > 1000
RETURN DISTINCT user.name, COUNT(comment) as commentCount
```

**Performance Analysis:**
- Multiple unoptimized MATCH clauses
- Late filtering
- DISTINCT on large result set
- Missing indexes

**Optimized Query:**
```cypher
MATCH (user:User {verified:true})
MATCH (user)-[:POSTED]->(post:Post)
WHERE post.createdDate > datetime("2024-01-01T00:00:00Z")
MATCH (post)-[:HAS_COMMENT]-(comment:Comment)-[:BY]-(commenter:User {verified:true})
WITH user, commenter, COUNT(comment) as commentCount
MATCH (commenter)-[:FRIENDS_WITH]-(friend:User)
WHERE friend.followerCount > 1000
RETURN user.name, commenter.name, commentCount
LIMIT 1000
```

**Index Recommendations:**
```cypher
CREATE INDEX ON :User(verified)
CREATE INDEX ON :Post(createdDate)
CREATE INDEX ON :User(followerCount)
CREATE INDEX ON :User(email)
```

---

## Summary

These five examples demonstrate:

1. **Business Domain (Cypher)** - Relationship naming conventions, property filters, multi-hop directions
2. **Scientific Domain (SPARQL)** - Namespace prefixes, type handling, optional patterns, transitive relationships
3. **E-Commerce (Cypher)** - Syntax errors, direction reversals, Cartesian products
4. **Real Estate (Cypher)** - Label mismatches, relationship chain validation, schema awareness
5. **Social Network (Cypher)** - Filter placement, index optimization, performance tuning

Each demonstrates debugging strategies from simple fixes to complex optimization scenarios.


