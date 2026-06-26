---
name: graph-query-optimization-assistant
description: Analyze graph queries and suggest optimizations to improve performance, reduce execution time, and ensure efficient traversal in graph databases.
metadata:
  {"openclaw":{"emoji":"⚡","homepage":"https://clawhub.com"}}
---

# Query Optimization Assistant

Analyze graph queries and recommend performance optimizations.

This skill helps developers improve the performance of graph database queries by identifying inefficiencies and suggesting optimized query patterns.

It evaluates queries written in languages such as Cypher or SPARQL and provides recommendations that reduce query cost, improve traversal efficiency, and minimize unnecessary graph scans.

---

## 📋 Quick Start

### When To Use This Skill

Use this skill when a user wants to:

- optimize graph queries for performance
- improve query execution time
- reduce query execution cost
- analyze query performance bottlenecks
- get index recommendations
- understand query traversal efficiency
- benchmark query alternatives
- tune Cypher or SPARQL queries

### Example Requests

- "Optimize this Cypher query."
- "Why is this SPARQL query slow?"
- "What indexes should I create?"
- "Suggest improvements for this graph query."
- "Help me tune this Neo4j query for performance."
- "Compare these two query approaches."

---

## 🎯 What This Skill Produces

The optimization assistant analyzes queries and provides:

- **Optimized Query Versions** - Rewritten queries with performance improvements
- **Index Recommendations** - Specific index creation suggestions
- **Cost Estimates** - Predicted performance metrics
- **Traversal Improvements** - Better graph navigation strategies
- **Performance Explanations** - Detailed reasoning for recommendations
- **Benchmark Comparisons** - Side-by-side performance metrics
- **Cardinality Analysis** - Expected result set sizes at each step

---

## 🔍 Optimization Pattern Categories

### 1. Node Selection Patterns (Entry Point Optimization)

Efficient queries start from the most selective nodes to minimize graph traversal.

**Patterns:**
- **Indexed Property Entry** - Start from node with indexed property
- **Unique Identifier Entry** - Use ID or unique constraints
- **Label Selectivity** - Choose most restrictive label
- **Property Filtering Entry** - Apply filters at entry point
- **Cardinality-Based Selection** - Start from smallest node set

**Example Inefficient:**
```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
WHERE c.name = "Acme"
RETURN p
```

**Example Optimized:**
```cypher
MATCH (c:Company {name: "Acme"})
MATCH (c)<-[:WORKS_AT]-(p:Person)
RETURN p
```

---

### 2. Index Strategy Patterns

Strategic index creation dramatically improves query performance.

**Patterns:**
- **Single Property Index** - Index frequently filtered properties
- **Composite Index** - Multi-property indexes for complex filters
- **Full-Text Index** - For text search and filtering
- **Covering Index** - Include all needed properties in index

**Recommendations:**
```cypher
-- Create single property index
CREATE INDEX ON :Company(name)

-- Create composite index
CREATE INDEX ON :Person(firstName, lastName)

-- Create full-text index for search
CREATE FULLTEXT INDEX person_search FOR (p:Person) ON EACH [p.name, p.email]
```

---

### 3. Relationship Traversal Patterns

Optimize how relationships are traversed.

**Patterns:**
- **Bounded Depth** - Limit traversal depth instead of unbounded
- **Relationship Type Specificity** - Specify relationship types
- **Direction Optimization** - Use correct relationship direction
- **Hop Reduction** - Minimize intermediate hops

**Example Inefficient:**
```cypher
MATCH (p:Person)-[*]->(target)
RETURN p, target
```

**Example Optimized:**
```cypher
MATCH (p:Person)-[*1..3]->(target:Company)
RETURN p, target
```

---

### 4. Query Structure Patterns

Organize query clauses for maximum efficiency.

**Patterns:**
- **WHERE Clause Positioning** - Apply filters early in query
- **MATCH Clause Ordering** - Order for maximum selectivity
- **LIMIT Optimization** - Use LIMIT to reduce result processing
- **Aggregation Timing** - Aggregate at the right query stage

**Example Inefficient:**
```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN p, c
LIMIT 100
```

**Example Optimized:**
```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN p, c
LIMIT 100
```

---

### 5. Cost Estimation Patterns

Understand and estimate query costs.

**Patterns:**
- **Traversal Cost** - Estimated cost of relationship traversal
- **Filter Selectivity** - How much data filtering removes
- **Result Set Sizing** - Expected number of results at each step
- **Cardinality Analysis** - Understanding data volume at each stage

**Cost Analysis Formula:**
```
Total Cost = Entry Point Cost + Traversal Cost + Filter Cost + Result Processing Cost
```

---

### 6. Cypher-Specific Patterns

Optimization techniques specific to Cypher/Neo4j.

**Patterns:**
- **MATCH vs MERGE** - Understanding performance differences
- **Relationship Unwinding** - Efficient collection expansion
- **Collection Operations** - Optimizing aggregation and collection handling
- **Node/Relationship Expansion** - Efficient expansion strategies

---

### 7. SPARQL-Specific Patterns

Optimization techniques for SPARQL/RDF.

**Patterns:**
- **Triple Pattern Ordering** - Order patterns for selectivity
- **OPTIONAL Placement** - Optimize optional clause placement
- **FILTER Positioning** - Apply filters at optimal points
- **PREFIX Efficiency** - Namespace handling optimization

---

## 💡 Optimization Strategy Workflow

When optimizing a graph query:

### Step 1: Analyze Current Query
- Identify entry points
- Analyze traversal patterns
- Estimate current cost
- Identify bottlenecks

### Step 2: Identify Inefficiencies
- Check for unbounded traversals
- Find late-stage filters
- Identify missing indexes
- Analyze cardinality issues

### Step 3: Generate Recommendations
- Suggest index creation
- Recommend query restructuring
- Propose alternative patterns
- Estimate performance improvements

### Step 4: Estimate Performance Impact
- Calculate cost reduction
- Estimate execution time improvement
- Quantify result set reduction
- Compare optimization strategies

### Step 5: Provide Optimized Query
- Rewrite for maximum performance
- Document changes
- Explain performance benefits
- Include implementation steps

---

## 📊 Performance Metrics & Benchmarking

### Key Metrics

**Execution Time:** Time required to execute query
- Units: milliseconds (ms)
- Benchmark: Compare original vs optimized

**Memory Usage:** Memory required during execution
- Units: megabytes (MB)
- Optimization: Reduce through cardinality reduction

**Node Visits:** Number of nodes examined during traversal
- Lower is better
- Optimization: Use selective entry points

**Relationship Traversals:** Number of relationships examined
- Lower is better
- Optimization: Specify relationship types, bound depth

**Index Usage:** Whether indexes are utilized
- Optimization: Create indexes on filtered properties

### Benchmark Comparison Format

```
Query Performance Comparison
═══════════════════════════════════════════════════════

Original Query:
  Execution Time: 5,432 ms
  Nodes Visited: 1,200,000
  Memory: 256 MB
  Cost Score: 8.5/10

Optimized Query:
  Execution Time: 245 ms
  Nodes Visited: 45,000
  Memory: 64 MB
  Cost Score: 2.1/10

Improvement:
  Speed: 22.1x faster (5,187 ms saved)
  Efficiency: 96.3% fewer nodes visited
  Memory: 75% reduction
```

---

## 🔗 Example Query Analysis

### Example 1: Product Recommendation Query (E-Commerce)

**Original Query:**
```cypher
MATCH (customer:Customer)-[:PURCHASED]->(p1:Product)
MATCH (p1)<-[:PURCHASED]-(other:Customer)
MATCH (other)-[:PURCHASED]->(recommended:Product)
WHERE recommended.price < 100
RETURN recommended
LIMIT 10
```

**Issues Identified:**
- Filter applied late in query
- Missing indexes on price property
- Unbounded traversal through customers

**Optimized Query:**
```cypher
MATCH (customer:Customer {id: $customerId})
MATCH (customer)-[:PURCHASED]->(p1:Product)
MATCH (p1)<-[:PURCHASED]-(other:Customer)
MATCH (other)-[:PURCHASED]->(recommended:Product {active: true})
WHERE recommended.price < 100
RETURN recommended
LIMIT 10
```

**Recommendations:**
1. Create index: `CREATE INDEX ON :Product(price)`
2. Create index: `CREATE INDEX ON :Customer(id)`
3. Add status filter at entry point
4. Use parameterized queries

**Performance Impact:**
- Execution time: 8,342 ms → 320 ms (26x faster)
- Nodes visited: 2,500,000 → 18,000 (99.3% reduction)

---

### Example 2: Friend-of-Friend Query (Social Network)

**Original Query:**
```sparql
SELECT ?friend
WHERE {
  ?user foaf:knows ?connection .
  ?connection foaf:knows ?friend .
}
```

**Issues Identified:**
- Unbounded traversal pattern
- May return very large result sets
- No filtering on result quality

**Optimized Query:**
```sparql
SELECT ?friend (COUNT(?connection) as ?mutual_friends)
WHERE {
  ?user foaf:knows ?connection .
  ?connection foaf:knows ?friend .
  FILTER (?user != ?friend)
  FILTER NOT EXISTS { ?user foaf:knows ?friend }
}
GROUP BY ?friend
ORDER BY DESC(?mutual_friends)
LIMIT 20
```

**Recommendations:**
1. Add mutual friend counting for ranking
2. Exclude self and existing connections
3. Limit results to prevent overwhelming result set
4. Use GROUP BY for aggregation

**Performance Impact:**
- Result set: Unlimited → 20 results (controlled)
- Relevance: Ranked by mutual connections
- Query cost: Reduced through aggregation

---

## 📈 Index Optimization Strategy

### When to Create Indexes

**Single Property Index:**
- Frequently used in WHERE clauses
- Used in equality checks
- Used for OPTIONAL MATCH

**Composite Index:**
- Multiple properties always filtered together
- Improve AND conditions in WHERE

**Full-Text Index:**
- Text search queries
- CONTAINS operations
- Prefix matching

### Index Examples

```cypher
-- Basic single property index
CREATE INDEX ON :Person(email)

-- Composite index for multiple properties
CREATE NAMED INDEX person_name_age FOR (p:Person) ON (p.firstName, p.lastName)

-- Full-text index for searching
CREATE FULLTEXT INDEX person_search FOR (p:Person) ON EACH [p.name, p.bio]

-- Unique constraint (also acts as index)
CREATE CONSTRAINT ON (u:User) ASSERT u.email IS UNIQUE
```

---

## ✅ Best Practices

When optimizing graph queries:

1. **Start from Selective Nodes** - Begin queries at most restrictive entry points
2. **Use Indexed Properties** - Filter on properties with indexes
3. **Avoid Unbounded Traversals** - Use bounded patterns like `[*1..3]`
4. **Apply Filters Early** - Move WHERE conditions near relevant MATCH
5. **Limit Result Sets** - Use LIMIT to prevent memory issues
6. **Specify Relationship Types** - Always specify relationships; avoid wildcard types
7. **Create Strategic Indexes** - Index properties used in WHERE clauses
8. **Analyze Query Plans** - Use EXPLAIN to understand execution
9. **Test with Real Data** - Benchmark against production-scale data
10. **Monitor Performance** - Continuously profile and optimize queries

---

## 🔗 Integration with Other Skills

This skill integrates with:

- **graph-query-debugging-tool** - Debug queries before optimization
- **graph-schema-validation** - Use schema for optimization recommendations
- **graph-template-query-generator** - Generate optimized query templates
- **multi-hop-reasoning-query-builder** - Optimize complex multi-hop patterns
- **nl-to-graph-query-translator** - Ensure translated queries are optimized

---

## 📚 Recommended Libraries

### Python
- `py2neo` - Neo4j driver with performance metrics
- `rdf-lib` - RDF query optimization utilities
- `graphistry` - Query visualization and optimization
- `numba` - JIT compilation for cost analysis

### Tools
- **Neo4j Browser** - EXPLAIN and PROFILE commands
- **Cypher Planner** - Query plan analysis
- **SPARQL Query Optimizer** - RDF optimization tools

---

## 📖 Summary

This skill improves the performance of graph database queries by analyzing query structure and suggesting optimized patterns.

It helps developers write faster, more efficient Cypher and SPARQL queries that scale effectively with large graph datasets through strategic index recommendations, intelligent query restructuring, and comprehensive performance analysis.

---

**Status: Enterprise-Grade Query Optimization Tool**

Comprehensive performance analysis, index optimization, and query acceleration for professional knowledge graph development.
