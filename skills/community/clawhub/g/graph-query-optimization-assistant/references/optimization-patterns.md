# Query Optimization Patterns

Twenty-five+ comprehensive design patterns for analyzing, optimizing, and benchmarking graph queries across Cypher, SPARQL, and other graph query languages.

---

## Node Selection Patterns (5)

### Pattern 1: Indexed Property Entry Point

**Context:** Starting a query from a node with an indexed property dramatically reduces initial traversal cost.

**Problem:** Queries starting from unindexed nodes or without property filters scan entire node sets.

**Solution:** Begin queries by matching nodes using indexed properties.

**Example - Inefficient:**
```cypher
MATCH (p:Person)
MATCH (p)-[:WORKS_AT]->(c:Company {name: "Acme"})
RETURN p
```

**Example - Optimized:**
```cypher
MATCH (c:Company {name: "Acme"})
MATCH (c)<-[:WORKS_AT]-(p:Person)
RETURN p
```

**When to Apply:**
- When one node type has fewer instances than another
- When filtering properties are indexed
- For large datasets

**Performance Impact:**
- Execution time: 50-90% reduction
- Nodes visited: 90-99% reduction
- Memory: 40-80% reduction

---

### Pattern 2: Unique Identifier Entry

**Context:** Starting from unique identifiers (UUID, email, username) provides maximum selectivity.

**Problem:** Generic property searches may return multiple results.

**Solution:** Use unique constraints or ID fields as entry points.

**Example:**
```cypher
-- Inefficient: Generic search
MATCH (u:User {name: "Alice"})
RETURN u

-- Optimized: Unique ID
MATCH (u:User {email: "alice@example.com"})
RETURN u
```

**Implementation:**
```cypher
CREATE CONSTRAINT ON (u:User) ASSERT u.email IS UNIQUE
```

**Performance Impact:**
- Constant-time lookup
- Guaranteed single result
- Eliminates ambiguity

---

### Pattern 3: Label Selectivity

**Context:** Some labels represent fewer nodes than others.

**Problem:** Starting from generic labels requires large scans.

**Solution:** Begin from the most specific (smallest) label set.

**Example:**
```cypher
-- Inefficient: Generic person label
MATCH (p:Person)-[:MANAGES]->(team:Team)
RETURN team

-- Optimized: Start from smaller set
MATCH (manager:Manager)-[:MANAGES]->(team:Team)
RETURN team
```

**Analysis Approach:**
1. Count nodes per label
2. Identify smallest label
3. Start from smallest set

**Performance Impact:**
- Initial scan: Proportional to node count
- Selectivity: Smaller labels = faster start

---

### Pattern 4: Property Filtering Entry

**Context:** Applying filters at query start point reduces intermediate results.

**Problem:** Filters applied late process unnecessary data.

**Solution:** Include WHERE conditions at the first MATCH clause.

**Example - Inefficient:**
```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
WHERE p.age > 30
RETURN p
```

**Example - Optimized:**
```cypher
MATCH (p:Person)
WHERE p.age > 30
MATCH (p)-[:WORKS_AT]->(c:Company)
RETURN p
```

**Or better, if index exists:**
```cypher
MATCH (p:Person {age: 31})  -- If age is indexed
RETURN p
```

**Performance Impact:**
- Reduced working set: 30-70%
- Lower memory: 20-50%

---

### Pattern 5: Cardinality-Based Selection

**Context:** Understanding data distribution helps choose optimal entry points.

**Problem:** Without cardinality analysis, queries may start from the wrong node type.

**Solution:** Analyze cardinality ratios and start from smallest set.

**Example - Before Analysis:**
```cypher
MATCH (order:Order)-[:PLACED_BY]->(customer:Customer)
RETURN customer
```

**Analysis:**
- Orders: 10,000,000
- Customers: 50,000

**Optimization:**
```cypher
MATCH (customer:Customer)
MATCH (customer)<-[:PLACED_BY]-(order:Order)
RETURN customer
```

**Cardinality Estimation:**
- 1 customer typically has 200 orders
- Starting from customer: faster traversal

---

## Index Strategy Patterns (4)

### Pattern 6: Single Property Index

**Context:** Frequently filtered properties should have indexes.

**Problem:** WHERE clauses on non-indexed properties require full scans.

**Solution:** Create indexes on commonly filtered properties.

**Decision Tree:**
```
Is property frequently in WHERE clause?
  → YES: Create index
  → NO: Skip

Does filter have high selectivity (< 50% of nodes)?
  → YES: Create index
  → NO: Consider, but lower priority

Is property used in equality (=) or range (<, >) checks?
  → YES: Index beneficial
  → NO: May not help for full-text
```

**Example:**
```cypher
-- High-traffic queries
MATCH (user:User {email: "user@example.com"})
MATCH (user:User {status: "active"})
MATCH (user:User WHERE age > 18)

-- Create indexes
CREATE INDEX ON :User(email)
CREATE INDEX ON :User(status)
CREATE INDEX ON :User(age)
```

**Performance Gain:**
- Equality queries: 100-1000x faster
- Range queries: 10-100x faster
- Index creation cost: One-time overhead

---

### Pattern 7: Composite Index

**Context:** Multiple properties queried together benefit from composite indexes.

**Problem:** Multiple single indexes may be suboptimal for multi-property filters.

**Solution:** Create composite indexes for frequently combined property filters.

**Example:**
```cypher
-- Query pattern: both properties always filtered together
MATCH (person:Person {firstName: "John", lastName: "Smith"})
RETURN person

-- Create composite index
CREATE INDEX ON :Person(firstName, lastName)
```

**When to Use:**
- Properties always filtered together
- Multi-condition WHERE clauses
- Want to avoid multiple index lookups

**Performance Impact:**
- Multi-property lookups: 5-20x faster
- Index size: Slightly larger

---

### Pattern 8: Full-Text Index

**Context:** Text search queries need specialized indexes.

**Problem:** CONTAINS or string matching without indexes is slow.

**Solution:** Use full-text indexes for text search properties.

**Example:**
```cypher
-- Without full-text index (slow)
MATCH (p:Product)
WHERE p.description CONTAINS "wireless"
RETURN p

-- With full-text index
CREATE FULLTEXT INDEX product_search FOR (p:Product) ON EACH [p.name, p.description]

-- Query becomes faster
CALL db.index.fulltext.queryNodes("product_search", "wireless") YIELD node
RETURN node
```

**Features:**
- Tokenization
- Fuzzy matching
- Phrase queries
- Boolean operators

---

### Pattern 9: Covering Index

**Context:** Indexes can include additional properties for direct access.

**Problem:** Index lookup still requires node property fetch.

**Solution:** Include all needed properties in index (covering index).

**Example:**
```cypher
-- Without covering index
MATCH (p:Person {email: "test@example.com"})
RETURN p.name, p.phone

-- With covering index
CREATE INDEX ON :Person(email, name, phone)
-- Now all data available from index
```

**When to Implement:**
- Specific queries returning subset of properties
- High-frequency queries
- Properties are small and frequently accessed

**Tradeoff:**
- Faster queries (index-only)
- Larger index size
- More index maintenance

---

## Relationship Traversal Patterns (4)

### Pattern 10: Bounded Depth Traversal

**Context:** Unbounded traversal (*) can explore entire graph.

**Problem:** Unbounded patterns cause expensive graph exploration.

**Solution:** Specify maximum traversal depth.

**Example - Inefficient:**
```cypher
MATCH (p:Person)-[*]->(target)
RETURN p, target
```

**Example - Optimized:**
```cypher
MATCH (p:Person)-[*0..3]->(target)
RETURN p, target
```

**Depth Guidelines:**
- Social networks: 2-4 hops typical
- Knowledge graphs: 3-5 hops
- E-commerce: 1-3 hops
- Financial: 2-4 hops

**Cost Reduction by Depth:**
- [*]: Unbounded (danger!)
- [*..10]: Still expensive
- [*..5]: Reasonable
- [*..3]: Good balance
- [*..1]: Most efficient

---

### Pattern 11: Relationship Type Specificity

**Context:** Specifying relationship types filters results early.

**Problem:** Generic traversal types may follow unintended relationships.

**Solution:** Always specify exact relationship types.

**Example - Generic:**
```cypher
MATCH (p:Person)-[*]->(target)
RETURN p, target
```

**Example - Specific:**
```cypher
MATCH (p:Person)-[:WORKS_AT]->(company:Company)
RETURN p, company
```

**Benefits:**
- Reduced result set
- Clearer intent
- Faster execution
- Better maintainability

---

### Pattern 12: Direction Optimization

**Context:** Relationship direction affects query efficiency.

**Problem:** Incorrect direction may traverse many nodes.

**Solution:** Use the most selective direction.

**Example - Inefficient Direction:**
```cypher
-- Company to Person (1 company → many persons)
MATCH (c:Company)<-[:WORKS_AT]-(p:Person)
WHERE c.name = "Acme"
RETURN p
```

**Example - Efficient Direction:**
```cypher
-- Person to Company (index-based)
MATCH (p:Person)-[:WORKS_AT]->(c:Company {name: "Acme"})
RETURN p
```

**Cardinality Analysis:**
- 1 Company → 5,000 Persons (expensive reverse)
- 50,000 Persons → 1 Company (efficient forward)

**Performance Gain:** 10-100x depending on cardinality

---

### Pattern 13: Hop Reduction

**Context:** Fewer intermediate hops = faster queries.

**Problem:** Complex multi-hop patterns compound traversal costs.

**Solution:** Simplify traversal patterns where possible.

**Example - Complex:**
```cypher
MATCH (a:Person)-[:KNOWS]->(b:Person)
-[:WORKS_AT]->(c:Company)
-[:LOCATED_IN]->(city:City)
-[:PART_OF]->(country:Country)
RETURN a, country
```

**Example - Simplified:**
```cypher
-- If relationship chain exists
MATCH (a:Person)-[:KNOWS]->(b:Person)
MATCH (b)-[:WORKS_IN_COUNTRY]->(country:Country)
RETURN a, country
```

**Hop Reduction Strategy:**
1. Identify path endpoints
2. Check for direct relationships
3. Use relationship shortcuts
4. Pre-compute derived relationships if needed

---

## Query Structure Patterns (4)

### Pattern 14: WHERE Clause Positioning

**Context:** WHERE clause placement affects query cost significantly.

**Problem:** Late WHERE clauses process unnecessary intermediate results.

**Solution:** Apply WHERE conditions as early as possible.

**Example - Inefficient:**
```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
-[:LOCATED_IN]->(l:Location)
-[:IN_COUNTRY]->(country:Country)
WHERE country.name = "USA"
RETURN p
```

**Example - Optimized:**
```cypher
MATCH (country:Country {name: "USA"})
MATCH (country)<-[:IN_COUNTRY]-(l:Location)
MATCH (l)<-[:LOCATED_IN]-(c:Company)
MATCH (c)<-[:WORKS_AT]-(p:Person)
RETURN p
```

**Best Practice:**
- Start from WHERE condition
- Filter as entry point
- Reduce traversal early

---

### Pattern 15: MATCH Clause Ordering

**Context:** MATCH clause sequence affects execution cost.

**Problem:** Wrong ordering causes expensive intermediate result sets.

**Solution:** Order MATCH clauses by selectivity (most selective first).

**Example:**
```cypher
-- Less efficient: many people match first
MATCH (p:Person)
MATCH (c:Company {name: "Acme"})
MATCH (p)-[:WORKS_AT]->(c)

-- More efficient: specific company first
MATCH (c:Company {name: "Acme"})
MATCH (p:Person)
MATCH (p)-[:WORKS_AT]->(c)

-- Best: Company first, then filter people
MATCH (c:Company {name: "Acme"})
MATCH (c)<-[:WORKS_AT]-(p:Person)
WHERE p.active = true
RETURN p
```

---

### Pattern 16: LIMIT Optimization

**Context:** Using LIMIT reduces unnecessary processing.

**Problem:** Queries process full result sets even when limited results needed.

**Solution:** Apply LIMIT to control result set size.

**Example:**
```cypher
-- Without LIMIT: processes all matching rows
MATCH (p:Person)-[:FOLLOWS]->(friend:Person)
RETURN p, friend

-- With LIMIT: stops after N results
MATCH (p:Person)-[:FOLLOWS]->(friend:Person)
RETURN p, friend
LIMIT 100
```

**When to Use LIMIT:**
- Top-N queries
- Pagination
- Sampling large result sets
- Any interactive query

---

### Pattern 17: Aggregation Timing

**Context:** Aggregation placement affects memory and performance.

**Problem:** Aggregating large intermediate result sets uses excessive memory.

**Solution:** Aggregate only necessary data, as late as possible.

**Example - Inefficient:**
```cypher
MATCH (p:Person)-[:PURCHASED]->(pr:Product)
WITH p, COLLECT(pr) as products
MATCH (p)-[:RATED]->(r:Rating)
RETURN p, products, COLLECT(r) as ratings
```

**Example - Optimized:**
```cypher
MATCH (p:Person)-[:PURCHASED]->(pr:Product)
WITH p, COUNT(DISTINCT pr) as purchase_count
MATCH (p)-[:RATED]->(r:Rating)
RETURN p, purchase_count, COUNT(DISTINCT r) as rating_count
```

---

## Cost Estimation Patterns (3)

### Pattern 18: Traversal Cost Estimation

**Context:** Understanding traversal costs helps optimize.

**Problem:** Expensive traversals dominate query time.

**Solution:** Estimate and optimize traversal costs.

**Cost Factors:**
```
Traversal Cost = 
  Entry Points × Relationships per Node × Hops × Filter Selectivity
```

**Example:**
```
Entry Point: 1 company (indexed lookup)
Relationships: 5,000 employees (WORKS_AT)
Hops: 1
Filter: active = true (20% selective)
Cost = 1 × 5,000 × 1 × 0.20 = 1,000 node visits
```

**Optimization Strategies:**
1. Reduce entry points
2. Start from smaller node sets
3. Limit traversal depth
4. Apply filters early

---

### Pattern 19: Filter Selectivity

**Context:** Understanding filter effectiveness helps optimize.

**Problem:** Low-selectivity filters don't reduce costs much.

**Solution:** Prioritize high-selectivity filters.

**Example - Selectivity Analysis:**
```
Query: WHERE status = 'active' AND verified = true

Status breakdown:
  active: 80% of users (low selectivity)
  inactive: 20% of users

Verified breakdown:
  verified: 5% of users (high selectivity)
  unverified: 95% of users

Optimal order:
  FILTER verified = true FIRST (eliminate 95%)
  FILTER status = 'active' SECOND (eliminate 20%)
```

---

### Pattern 20: Result Set Sizing

**Context:** Understanding expected result sizes predicts memory needs.

**Problem:** Unexpected large result sets cause memory issues.

**Solution:** Estimate result set size at each query stage.

**Estimation Formula:**
```
Result Size = Source Node Count × Relationships per Node × ... × Hops
```

**Example:**
```
Stage 1: SELECT company (1 result)
Stage 2: company → employees (5,000 results)
Stage 3: employee → projects (avg 3 per employee = 15,000 results)
Stage 4: DISTINCT projects (8,000 unique)
Stage 5: LIMIT 100 (100 final results)
```

---

## Cypher-Specific Patterns (3)

### Pattern 21: MATCH vs MERGE Performance

**Context:** MATCH and MERGE have different performance characteristics.

**Problem:** Using MERGE when MATCH would suffice costs extra.

**Solution:** Use MATCH for lookups, MERGE for create-or-update.

**Example:**
```cypher
-- For lookups: MATCH is faster
MATCH (u:User {id: $userId})
RETURN u

-- For upsert: MERGE is appropriate
MERGE (u:User {id: $userId})
ON CREATE SET u.created_at = datetime()
ON MATCH SET u.last_accessed = datetime()
RETURN u
```

**Performance:**
- MATCH: O(1) with index
- MERGE: O(1) lookup + O(n) creation

---

### Pattern 22: Relationship Unwinding

**Context:** Efficiently expanding collections of relationships.

**Problem:** Inefficient collection expansion causes memory issues.

**Solution:** Use UNWIND with DISTINCT for efficient expansion.

**Example:**
```cypher
-- Inefficient: large intermediate collection
MATCH (p:Person)
WITH COLLECT(p) as people
UNWIND people as p
MATCH (p)-[:WORKS_AT]->(c)
RETURN p, c

-- Optimized: process incrementally
MATCH (p:Person)
MATCH (p)-[:WORKS_AT]->(c)
RETURN p, c
```

---

### Pattern 23: Collection Operations

**Context:** Collection handling affects performance.

**Problem:** Large collections consume memory.

**Solution:** Use appropriate collection operations.

**Example:**
```cypher
-- Without size limit
MATCH (p:Person)-[:KNOWS]->(f:Person)
RETURN p, COLLECT(f) as friends

-- With size limit
MATCH (p:Person)-[:KNOWS]->(f:Person)
WITH p, COLLECT(f)[0..100] as friends
RETURN p, friends

-- Alternative: aggregation
MATCH (p:Person)-[:KNOWS]->(f:Person)
RETURN p, COUNT(f) as friend_count
```

---

## SPARQL-Specific Patterns (3)

### Pattern 24: Triple Pattern Ordering

**Context:** SPARQL triple pattern order affects query efficiency.

**Problem:** Unordered patterns may match millions of triples.

**Solution:** Order patterns from most to least selective.

**Example:**
```sparql
-- Inefficient: generic pattern first
SELECT ?person
WHERE {
  ?person rdf:type ex:Person .        -- Millions match
  ?person ex:age ?age .               -- Millions match
  ?person ex:email ?email .           -- Millions match
  FILTER (ex:EmployeeDB)
}

-- Optimized: specific pattern first
SELECT ?person
WHERE {
  ?person ex:inDatabase ex:EmployeeDB .  -- Fewer match
  ?person ex:age ?age .                   -- Filters result
  FILTER (?age >= 18)
  ?person ex:email ?email .
}
```

---

### Pattern 25: Optional Handling

**Context:** OPTIONAL patterns should be placed strategically.

**Problem:** OPTIONAL too early may bind unnecessary variables.

**Solution:** Place OPTIONAL after required patterns.

**Example:**
```sparql
-- Better performance
SELECT ?person ?email
WHERE {
  ?person rdf:type ex:Person .
  ?person ex:name ?name .
  OPTIONAL { ?person ex:email ?email }
}

-- Avoid: Optional before required
SELECT ?person ?email ?name
WHERE {
  OPTIONAL { ?person ex:email ?email }
  ?person rdf:type ex:Person .
  ?person ex:name ?name .
}
```

---

## Best Practices Summary

### General Optimization Workflow

1. **Analyze Current Query**
   - Identify bottlenecks
   - Estimate costs
   - Profile execution

2. **Apply Patterns**
   - Node Selection (5 patterns)
   - Index Strategy (4 patterns)
   - Traversal Optimization (4 patterns)
   - Structure Optimization (4 patterns)

3. **Benchmark Improvements**
   - Compare metrics
   - Quantify gains
   - Document changes

4. **Monitor Performance**
   - Track execution times
   - Adjust as needed
   - Maintain indexes

### Top 10 Quick Wins

1. ✅ Add indexes on filtered properties
2. ✅ Start from most selective nodes
3. ✅ Apply filters at query start
4. ✅ Specify relationship types
5. ✅ Bound traversal depth
6. ✅ Use LIMIT for large result sets
7. ✅ Move WHERE earlier in query
8. ✅ Avoid Cartesian products
9. ✅ Use DISTINCT efficiently
10. ✅ Aggregate strategically

---

**Status: Production-Ready Optimization Patterns**

These 25+ patterns provide comprehensive guidance for optimizing graph queries across Cypher, SPARQL, and other graph languages, typically achieving 10-100x performance improvements.


