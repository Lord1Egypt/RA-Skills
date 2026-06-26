---
name: graph-query-debugging-tool
description: Diagnose errors in Cypher or SPARQL queries and suggest fixes for syntax issues, schema mismatches, and incorrect graph traversal patterns.
metadata:
  {"openclaw":{"emoji":"🛠️","homepage":"https://clawhub.com"}}
---

# Query Debugging Tool

Analyze graph queries, identify errors, and suggest fixes.

This skill helps developers debug graph database queries by detecting syntax errors, schema mismatches, incorrect relationship patterns, and logical mistakes.

It explains why a query fails or returns incorrect results and provides corrected query versions.

---

## 📋 Quick Start

### When To Use This Skill

Use this skill when a user wants to:

- debug Cypher queries
- debug SPARQL queries
- understand query errors
- fix incorrect graph traversal patterns
- diagnose why a query returns no results
- correct query syntax
- optimize poorly performing queries
- validate queries against a schema
- understand relationship traversal issues

### Example Requests

- "Why is this Cypher query failing?"
- "Fix this SPARQL query."
- "Debug this graph query."
- "Explain what is wrong with this query."
- "Does this query match my schema?"
- "Why does this query return no results?"
- "What relationships can I traverse from Person nodes?"

---

## 🎯 What This Skill Produces

The debugging tool provides:

- **Error Diagnosis** - Identifies syntax errors, schema mismatches, relationship issues
- **Corrected Query Versions** - Fixed versions of broken queries
- **Explanations** - Clear explanations of what went wrong and why
- **Debugging Steps** - Step-by-step guidance to isolate problems
- **Schema Validation** - Detection of schema mismatches
- **Relationship Analysis** - Validation of relationship types and directions
- **Performance Insights** - Identification of potential query performance issues
- **Alternative Queries** - Simplified or optimized query alternatives

---

## 🔍 Query Components & Error Categories

### Query Structure Elements

**Cypher Query Components:**
- Node patterns: `(n:Label {prop: value})`
- Relationship patterns: `-[r:TYPE]->`, `<-[r:TYPE]-`
- Clauses: MATCH, WHERE, RETURN, WITH, etc.
- Functions: count(), collect(), relationships(), etc.
- Aggregations: GROUP BY, ORDER BY, LIMIT

**SPARQL Query Components:**
- Triple patterns: `?s ?p ?o`
- Prefixes: `PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>`
- Variable bindings: `?variable`
- Filters: `FILTER (?var > 5)`
- Aggregates: GROUP BY, ORDER BY, LIMIT

### Error Categories

1. **Syntax Errors** - Malformed query structure
   - Missing parentheses or brackets
   - Incorrect clause ordering
   - Invalid operator usage
   - Missing periods or semicolons

2. **Schema Errors** - References to non-existent elements
   - Non-existent node labels
   - Non-existent relationship types
   - Non-existent properties
   - Type mismatches

3. **Relationship Errors** - Issues with relationship traversal
   - Incorrect relationship type
   - Wrong traversal direction
   - Non-existent relationship between nodes
   - Invalid relationship cardinality

4. **Logical Errors** - Query logic problems
   - Unreachable patterns
   - Contradictory conditions
   - Incorrect variable bindings
   - Missing result columns

5. **Performance Issues** - Queries that are inefficient
   - Missing indexes
   - Inefficient filter placement
   - Cartesian products
   - Unoptimized join patterns

---

## 🛠️ Debugging Strategy

When analyzing a query, the tool performs these validation steps:

### Step 1: Syntax Validation
- Parse query structure
- Verify parentheses and bracket matching
- Check clause ordering
- Validate operator usage
- Identify malformed expressions

### Step 2: Schema Validation
- Check node labels against schema
- Verify relationship types exist
- Validate property names
- Confirm property types
- Detect schema mismatches

### Step 3: Relationship Analysis
- Verify traversal directions
- Confirm relationship types
- Check source and target node labels
- Identify relationship cardinality issues
- Detect unreachable patterns

### Step 4: Query Logic Verification
- Analyze variable bindings
- Check return column validity
- Verify aggregation syntax
- Validate filter expressions
- Identify contradiction conditions

### Step 5: Performance Analysis
- Identify missing indexes
- Detect inefficient filters
- Find Cartesian products
- Analyze join patterns
- Suggest optimization strategies

---

## 📊 Syntax Error Examples

### Example 1: Missing Closing Parenthesis

**Broken Cypher query:**
```text
MATCH (p:Person)-[:WORKS_AT]->(c:Company
RETURN p
```

**Issue:** Missing closing parenthesis for Company node.

**Fixed query:**
```text
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN p
```

**Explanation:** All node patterns must be properly enclosed in parentheses. The query declares a Company node pattern but fails to close it before the RETURN clause.

---

### Example 2: Incorrect SPARQL Triple Syntax

**Broken SPARQL query:**
```text
SELECT ?person
WHERE {
  ?person rdf:type :Person
  ?person :worksAt :Acme .
}
```

**Issue:** Missing period between triple statements.

**Fixed query:**
```text
SELECT ?person
WHERE {
  ?person rdf:type :Person .
  ?person :worksAt :Acme .
}
```

**Explanation:** Each RDF triple in SPARQL must end with a period. The first triple is missing its terminating period, causing a syntax error.

---

### Example 3: Invalid Operator Usage

**Broken Cypher query:**
```text
MATCH (p:Person) 
WHERE p.age > "30"
RETURN p
```

**Issue:** Comparing numeric property with string literal.

**Fixed query:**
```text
MATCH (p:Person) 
WHERE p.age > 30
RETURN p
```

**Explanation:** The age property is numeric, so it should be compared with a numeric value, not a string. Type mismatches cause unexpected behavior.

---

## 🔗 Schema Mismatch Examples

### Example 1: Non-Existent Node Label

**Query:**
```text
MATCH (p:Employee)-[:WORKS_AT]->(c:Company)
RETURN p
```

**Problem:** The label `Employee` may not exist in the graph schema.

**Possible correction:**
```text
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN p
```

**Explanation:** Different graph schemas use different naming conventions. Common alternatives: Person, Actor, User, Individual. The debugging tool suggests schema-aligned labels.

---

### Example 2: Non-Existent Relationship Type

**Query:**
```text
MATCH (p:Person)-[:WORK_AT]->(c:Company)
RETURN p
```

**Issue:** Relationship type `WORK_AT` (singular) may be incorrect; `WORKS_AT` (plural) is more likely.

**Corrected query:**
```text
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN p
```

**Explanation:** Common naming pattern mismatches. The tool checks against known relationship patterns and suggests corrections based on schema definitions.

---

### Example 3: Non-Existent Property

**Query:**
```text
MATCH (p:Person) 
WHERE p.age > 30 
RETURN p.age, p.salary
```

**Problem:** The property `salary` may not exist on Person nodes.

**Debugging approach:**
```text
MATCH (p:Person)
RETURN keys(p)
LIMIT 5
```

**Explanation:** Use the `keys()` function to inspect actual properties on nodes before writing complex queries.

---

## ↔️ Relationship Traversal Examples

### Example 1: Incorrect Traversal Direction

**Query:**
```text
MATCH (c:Company)<-[:WORKS_AT]-(p:Person)
RETURN p
```

**Possible issue:** The relationship direction may be reversed. Should be `Person -[:WORKS_AT]-> Company`.

**Corrected query:**
```text
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN p
```

**Explanation:** Relationship direction matters. If the schema defines `WORKS_AT` as `Person -> Company`, the reverse direction produces no results.

---

### Example 2: Multi-Hop Relationship Issues

**Query:**
```text
MATCH (a:Person)-[:KNOWS]->(b:Person)-[:WORKS_AT]->(c:Company)
RETURN a, b, c
```

**Problem:** Relationship chain may be incomplete or require intermediate nodes.

**Debugging approach:**
```text
-- First, check the KNOWS relationship
MATCH (a:Person)-[:KNOWS]->(b:Person)
RETURN a, b
LIMIT 10

-- Then, check if Person nodes connect to Company
MATCH (b:Person)-[:WORKS_AT]->(c:Company)
RETURN b, c
LIMIT 10
```

**Explanation:** Break complex queries into intermediate steps to isolate where the chain breaks.

---

### Example 3: Non-Existent Relationship Between Types

**Query:**
```text
MATCH (p:Person)-[:LIKES]->(p2:Person)-[:MANUFACTURES]->(prod:Product)
RETURN p, prod
```

**Problem:** Person nodes may not have `MANUFACTURES` relationships; that relationship may only exist from Company to Product.

**Corrected query:**
```text
MATCH (p:Person)-[:WORKS_AT]->(c:Company)-[:MANUFACTURES]->(prod:Product)
RETURN p, prod
```

**Explanation:** Relationships often connect specific node types. The tool validates that relationship types connect compatible node labels.

---

## ❌ Query Returning No Results

### Scenario: Query Structure Is Valid But Returns Empty

**Example query:**
```text
MATCH (p:Person {name:"Alice"})-[:WORKS_AT]->(c:Company {name:"Google"})
RETURN p
```

**Possible issues:**

1. Alice does not work at Google
2. Company name differs in the dataset (e.g., "Google Inc.", "Alphabet")
3. Relationship type differs (e.g., `EMPLOYED_BY` instead of `WORKS_AT`)
4. Person or Company nodes don't exist with specified properties

### Debugging Approach

**Step 1: Check if Alice exists**
```text
MATCH (p:Person {name:"Alice"})
RETURN p
```

**Step 2: Check if Google exists**
```text
MATCH (c:Company {name:"Google"})
RETURN c
```

**Step 3: Check Alice's relationships**
```text
MATCH (p:Person {name:"Alice"})-[r]->(target)
RETURN r, target
```

**Step 4: Relax constraints progressively**
```text
MATCH (p:Person {name:"Alice"})-[:WORKS_AT]->(c:Company)
RETURN p, c
```

This reveals the actual relationships and targets connected to Alice, helping isolate the mismatch.

---

## 💬 SPARQL-Specific Examples

### Example 1: Missing Namespace Prefix

**Broken SPARQL query:**
```text
SELECT ?person
WHERE {
  ?person rdf:type Person
}
```

**Issue:** `Person` is referenced without a namespace prefix.

**Fixed query:**
```text
PREFIX ex: <http://example.org/>
SELECT ?person
WHERE {
  ?person rdf:type ex:Person
}
```

**Explanation:** RDF requires full URIs. Prefixes abbreviate long namespace URIs. Without a prefix, the term is interpreted as a bare string, not a resource URI.

---

### Example 2: Filter Expression Syntax

**Broken SPARQL query:**
```text
SELECT ?person
WHERE {
  ?person rdf:type ex:Person .
  ?person ex:age ?age .
  FILTER (?age > "30")
}
```

**Issue:** Type mismatch in filter; comparing numeric age with string "30".

**Fixed query:**
```text
PREFIX ex: <http://example.org/>
SELECT ?person
WHERE {
  ?person rdf:type ex:Person .
  ?person ex:age ?age .
  FILTER (?age > 30)
}
```

**Explanation:** SPARQL FILTER expressions require type-compatible comparisons. Numeric properties must be compared with numeric literals.

---

### Example 3: Optional Triple Patterns

**Query with potential issue:**
```text
SELECT ?person ?email
WHERE {
  ?person rdf:type ex:Person .
  ?person ex:email ?email .
}
```

**Problem:** If not all Person nodes have email, query returns incomplete results.

**Optimized query:**
```text
PREFIX ex: <http://example.org/>
SELECT ?person ?email
WHERE {
  ?person rdf:type ex:Person .
  OPTIONAL { ?person ex:email ?email }
}
```

**Explanation:** Use OPTIONAL to include results even when optional properties are missing.

---

## 📈 Performance Issue Patterns

### Issue 1: Inefficient Filter Placement

**Inefficient query:**
```text
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
WHERE p.age > 30
RETURN p
```

**Problem:** Filters are applied after relationship matching, processing all relationships first.

**Optimized query:**
```text
MATCH (p:Person) 
WHERE p.age > 30
MATCH (p)-[:WORKS_AT]->(c:Company)
RETURN p
```

**Explanation:** Apply filters early to reduce the working set before expensive relationship traversals.

---

### Issue 2: Cartesian Product

**Problematic query:**
```text
MATCH (p:Person), (c:Company)
RETURN p, c
```

**Problem:** Without relationship constraints, this creates a Cartesian product of all persons and companies.

**Corrected query:**
```text
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN p, c
```

**Explanation:** Always specify relationship patterns to limit the result set to relevant combinations.

---

### Issue 3: Missing Index

**Query that benefits from indexing:**
```text
MATCH (p:Person {email: "alice@example.com"})
RETURN p
```

**Suggestion:** Create an index on Person.email
```text
CREATE INDEX ON :Person(email)
```

**Explanation:** Indexes accelerate exact-match lookups. If frequently querying by specific properties, create indexes.

---

## 📋 Output Formats

The debugging tool provides multiple output formats:

### 1. Error Report

Human-readable breakdown of all issues:
```json
{
  "query": "...",
  "query_type": "cypher",
  "has_errors": true,
  "error_count": 2,
  "errors": [
    {
      "category": "syntax",
      "line": 1,
      "message": "Missing closing parenthesis",
      "position": 45,
      "suggestion": "Add ) after Company"
    },
    {
      "category": "schema",
      "message": "Relationship type WORK_AT not found",
      "suggestion": "Did you mean WORKS_AT?"
    }
  ]
}
```

### 2. Corrected Query

The debugged and corrected version of the query ready for execution.

### 3. Debugging Suggestions

Step-by-step guidance for manual debugging and investigation.

### 4. Schema Validation Report

Details on schema element validation results.

---

## 🏗️ Implementation Details

The debugging tool internally performs:

- **Syntax Validation** - Tokenization and parsing of query structure
- **Schema Awareness** - Checking against provided or learned schema
- **Relationship Validation** - Verifying relationship types and directions
- **Logical Query Analysis** - Analyzing query semantics and correctness
- **Step-by-step Query Breakdown** - Decomposing queries into understandable components
- **Pattern Matching** - Identifying common error patterns
- **Performance Analysis** - Identifying inefficiency patterns

---

## 📚 Libraries & Tools

### Recommended Libraries

**Python:**
- `lark` - Query parsing and tokenization
- `regex` - Pattern matching for query analysis
- `dataclasses-json` - Serialization of analysis results
- `jsonschema` - Schema validation for provided schemas

**JavaScript/Node.js:**
- `cypher-parser` - Cypher query parsing
- `sparql-parser` - SPARQL query parsing
- `json-schema-validator` - Schema validation

---

## ✅ Best Practices

When debugging graph queries:

1. **Test Query Components Separately** - Break complex queries into simpler parts; debug each independently
2. **Inspect Node Labels and Properties** - Use discovery queries to understand available data
3. **Verify Relationship Types and Directions** - Check that relationships connect expected node types
4. **Limit Result Sets While Debugging** - Use LIMIT clauses to reduce output volume during investigation
5. **Simplify Queries Before Expanding** - Start with basic patterns; add complexity incrementally
6. **Document Assumptions** - Clearly state assumptions about schema and data
7. **Use Schema Validation** - Provide schema definitions to enable comprehensive validation
8. **Version Query Patterns** - Save working query patterns for reuse
9. **Monitor Relationship Cardinality** - Understand how many relationships exist of each type
10. **Keep Debugging Queries Handy** - Maintain a library of diagnostic queries for common investigations
11. **Understand Query Execution Plans** - Examine execution plans to identify performance bottlenecks
12. **Profile Against Real Data** - Test queries against representative data volumes

---

## 🔗 Integration with Other Skills

This skill integrates with:

- **graph-query-optimization-assistant** - Optimize debugged queries further
- **graph-template-query-generator** - Generate query templates from corrected queries
- **nl-to-graph-query-translator** - Validate queries generated from natural language
- **graph-schema-validation** - Provide schema for comprehensive validation
- **multi-hop-reasoning-query-builder** - Debug complex multi-hop queries

---

## 📖 Summary

This skill helps developers diagnose and fix issues in graph queries across multiple query languages.

It detects syntax errors, schema mismatches, relationship traversal issues, and logical mistakes while providing corrected query versions and step-by-step debugging guidance. Whether working with Cypher, SPARQL, or other graph query languages, the debugging tool accelerates query development and troubleshooting.

---

**Status: Enterprise-Grade Query Debugging Tool**

Comprehensive error detection, schema validation, and query assistance for professional knowledge graph development.
