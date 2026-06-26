# Multi-Hop Reasoning Examples
Real-world multi-hop query examples across multiple domains showing path discovery, reasoning patterns, and complex relationship traversal.
---
## 1. Social Network Domain: Friends-of-Friends Discovery (Cypher)
### Scenario: Friend Recommendation System
**Business Goal:** Recommend new friends based on shared connections
### Query 1: Direct Friends of Friends
**Purpose:** Find friends-of-friends (exactly 2 hops)
```cypher
MATCH (user:User {username: $username})-[:FOLLOWS*2]->(fof:User)
WHERE NOT (user)-[:FOLLOWS]->(fof)
RETURN DISTINCT fof.username, fof.follower_count
ORDER BY fof.follower_count DESC
LIMIT 20
```
**Result:** New potential friends exactly 2 hops away
---
## 2. E-Commerce Domain: Product Recommendation (Cypher)
### Scenario: Recommendation Engine
**Business Goal:** Recommend products based on customer purchase chains
### Query: Products Through Purchase Network
**Purpose:** Find products frequently connected through other customers' purchases
```cypher
MATCH (customer:Customer {id: $customerId})-[:PURCHASED]->(p1:Product)
-[:PURCHASED_BY]-(otherCustomer:Customer)
-[:PURCHASED]->(recommended:Product)
WHERE recommended.id <> p1.id 
      AND recommended.price < $maxPrice
      AND recommended.availability = "in_stock"
RETURN DISTINCT recommended.id, recommended.name, recommended.price,
       COUNT(DISTINCT otherCustomer) as recommendation_strength
GROUP BY recommended.id, recommended.name, recommended.price
ORDER BY recommendation_strength DESC
LIMIT 15
```
---
## 3. Supply Chain Domain: Supplier Network Analysis (Cypher)
### Scenario: Supply Chain Risk Assessment
**Business Goal:** Identify supplier dependencies and risks
### Query: Multi-Level Supplier Discovery
**Purpose:** Find all suppliers within supply chain
```cypher
MATCH (manufacturer:Company {name: $manufacturerName})
-[:SUPPLIES_TO*1..3]->(supplier:Company)
RETURN supplier.name, supplier.country, supplier.financial_rating,
       LENGTH(path) as supply_distance
ORDER BY supply_distance, supplier.financial_rating DESC
LIMIT 100
```
---
## 4. Fraud Detection Domain: Transaction Chains (Cypher)
### Scenario: Money Laundering Detection
**Business Goal:** Detect suspicious transaction patterns
### Query: Multi-Hop Transaction Chains
**Purpose:** Find unusual transaction paths
```cypher
MATCH path = (account1:Account {id: $accountId})
-[:TRANSFER*2..5]->(account2:Account)
WHERE account1.id <> account2.id
      AND ALL(n in nodes(path) WHERE n.verification_status = "low")
      AND ALL(r in relationships(path) WHERE r.amount > $largeAmount)
RETURN [n in nodes(path) | n.id] as account_chain,
       [r in relationships(path) | r.amount] as amounts,
       SUM([r in relationships(path) | r.amount]) as total_transferred,
       LENGTH(path) as hops,
       "HIGH_RISK" as fraud_score
LIMIT 20
```
---
## 5. Knowledge Graph Domain: Entity Reasoning (SPARQL)
### Scenario: Academic Collaboration Network
**Business Goal:** Discover research collaboration paths
### Query: Multi-Hop Collaboration Discovery
**Purpose:** Find research connections through publications
```sparql
PREFIX ex: <http://example.org/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
SELECT ?researcher ?papers ?distance
WHERE {
  :Alice ex:collaboratesWith+ ?researcher .
  ?researcher dc:wrote ?paper .
  ?paper ex:citationCount ?citations .
  FILTER (?citations > 10)
}
ORDER BY DESC(?citations)
LIMIT 50
```
---
## 6. Healthcare Domain: Patient Network Analysis (Cypher)
### Scenario: Disease Outbreak Tracking
**Business Goal:** Track disease transmission paths
### Query: Multi-Hop Contact Tracing
**Purpose:** Find contacts and contact-of-contacts
```cypher
MATCH path = (patient:Patient {id: $patientId})
-[:HAD_CONTACT_WITH*1..3]->(exposed:Patient)
WHERE patient.diagnosis = $disease
      AND ALL(n in nodes(path) WHERE n.quarantine_status = "pending")
RETURN DISTINCT exposed.id, exposed.last_location,
       [n in nodes(path) | n.id] as contact_chain,
       LENGTH(path) as exposure_distance,
       CASE 
         WHEN exposure_distance = 1 THEN "DIRECT_CONTACT"
         WHEN exposure_distance = 2 THEN "SECONDARY_CONTACT"
         ELSE "TERTIARY_CONTACT"
       END as contact_type
ORDER BY exposure_distance
LIMIT 200
```
---
## 7. Knowledge Management Domain: Document Relationships (Cypher)
### Scenario: Information Discovery
**Business Goal:** Find related documents through citation chains
### Query: Document Citation Paths
**Purpose:** Trace knowledge lineage
```cypher
MATCH path = (doc1:Document {id: $sourceDocId})
-[:CITES*1..4]->(doc2:Document)
-[:WRITTEN_BY]->(author:Author)
WHERE ALL(r in relationships(path) WHERE r.publication_year >= 2020)
RETURN [n in nodes(path) | CASE WHEN n:Document THEN n.title ELSE n.name END] as path_info,
       doc2.title as destination_doc,
       author.name as destination_author,
       COUNT(*) as num_paths
GROUP BY doc2.id, doc2.title, author.name
ORDER BY num_paths DESC
LIMIT 25
```
---
## 8. Financial Network: Transaction Routing (Cypher)
### Scenario: Inter-bank Settlement Analysis
**Business Goal:** Understand fund flows through banking network
### Query: Multi-Bank Settlement Paths
**Purpose:** Find routing paths for settlement
```cypher
MATCH path = (bank1:Bank {swift: $bank1Swift})
-[:SETTLES_THROUGH*1..3]->(bank2:Bank {swift: $bank2Swift})
WHERE ALL(n in nodes(path) WHERE n.operational = true)
RETURN [n in nodes(path) | n.name] as settlement_path,
       [r in relationships(path) | r.delay_time_hours] as delays,
       SUM([r in relationships(path) | r.settlement_fee]) as total_fee,
       LENGTH(path) as intermediaries,
       MIN([r in relationships(path) | r.delay_time_hours]) as min_delay
ORDER BY total_fee ASC, LENGTH(path) ASC
LIMIT 10
```
---
## Performance Guidelines
Keep depth ≤ 3 for unrestricted queries  
Use depth ≤ 4 with strong filters  
Always include LIMIT clause  
Index starting node properties  
Use specific relationship types  
---
**8 comprehensive multi-hop examples across diverse domains showing practical applications.**
