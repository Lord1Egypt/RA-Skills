# Query Debugging Patterns

Twenty+ design patterns for detecting, analyzing, and fixing common query issues in Cypher, SPARQL, and graph query languages.

---

## Syntax Error Detection Patterns

### Pattern 1: Unmatched Brackets/Parentheses

**Symptom:** Parser error on query execution

**Detection Rules:**
- Count opening and closing parentheses: `(` vs `)`
- Count opening and closing brackets: `[` vs `]`
- Count opening and closing braces: `{` vs `}`
- Verify proper nesting order

**Example Broken Query:**
```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company
RETURN p
```

**Detection:** Missing `)` after `Company`

**Fix:** Add closing parenthesis
```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN p
```

---

### Pattern 2: Missing Clause Periods/Semicolons

**Symptom:** SPARQL parser error

**Detection Rules:**
- In SPARQL, each triple pattern must end with a period `.`
- Identify consecutive triple patterns without period separation
- Check for missing semicolon at query end (some dialects)

**Example Broken Query:**
```sparql
SELECT ?person
WHERE {
  ?person rdf:type :Person
  ?person :worksAt :Company .
}
```

**Detection:** First triple pattern missing period after `:Person`

**Fix:** Add period separator
```sparql
SELECT ?person
WHERE {
  ?person rdf:type :Person .
  ?person :worksAt :Company .
}
```

---

### Pattern 3: Clause Ordering Violations

**Symptom:** Query parsing fails or behaves unexpectedly

**Detection Rules:**
- Cypher: MATCH/OPTIONAL MATCH → WHERE → RETURN/WITH
- SPARQL: PREFIX → SELECT/ASK → WHERE
- Identify clauses appearing in wrong order

**Example Broken Query:**
```cypher
RETURN p.name
MATCH (p:Person)
WHERE p.age > 30
```

**Detection:** RETURN appears before MATCH

**Fix:** Reorder clauses correctly
```cypher
MATCH (p:Person)
WHERE p.age > 30
RETURN p.name
```

---

### Pattern 4: Invalid Operator Usage

**Symptom:** Type error or unexpected results

**Detection Rules:**
- Comparison operators (`>`, `<`, `=`, `!=`) must connect compatible types
- Logical operators (AND, OR) must connect boolean expressions
- Pattern operators (`-[r]->`) must connect valid node patterns

**Example Broken Query:**
```cypher
WHERE p.age > "30"
```

**Detection:** Comparing integer property with string literal

**Fix:** Use numeric comparison
```cypher
WHERE p.age > 30
```

---

## Schema Validation Patterns

### Pattern 5: Non-Existent Node Labels

**Symptom:** Query returns no results or "label not found" error

**Detection Approach:**
1. Extract all node labels from query: `:Label1`, `:Label2`
2. Query schema for available labels
3. Compare query labels against schema
4. Suggest nearest matching labels using string similarity

**Example:**
```cypher
MATCH (e:Employee)-[:WORKS_AT]->(c:Company)
```

**Detection Schema Check:**
```cypher
CALL db.labels() YIELD label
WITH collect(label) as available_labels
RETURN available_labels
-- Returns: ["Person", "Company", "Department"] (no "Employee")
```

**Suggestion:** Did you mean `Person` instead of `Employee`?

**Corrected Query:**
```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
```

---

### Pattern 6: Non-Existent Relationship Types

**Symptom:** Query returns no results with valid node labels

**Detection Approach:**
1. Extract relationship types from query: `[:TYPE1]`, `[:TYPE2]`
2. Query schema for available relationship types
3. Compare against schema
4. Suggest similar relationship names

**Example:**
```cypher
MATCH (p:Person)-[:WORK_AT]->(c:Company)
```

**Detection Schema Check:**
```cypher
CALL db.relationshipTypes() YIELD relationshipType
-- Returns: ["WORKS_AT", "MANAGES", "LOCATED_AT"] (no "WORK_AT")
```

**Suggestion:** Did you mean `WORKS_AT`?

**Corrected Query:**
```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
```

---

### Pattern 7: Non-Existent Properties

**Symptom:** Query returns null or property not found error

**Detection Approach:**
1. Extract property references: `node.property`
2. For each node type, query actual properties
3. Compare against used properties
4. Flag properties that don't exist

**Example:**
```cypher
MATCH (p:Person)
RETURN p.salary, p.age
```

**Detection Schema Check:**
```cypher
MATCH (p:Person)
RETURN keys(p)
LIMIT 1
-- Returns: ["name", "age", "email"] (no "salary")
```

**Corrected Approach:**
```cypher
MATCH (p:Person)
RETURN p.name, p.age
-- Or check if salary is on different node type:
MATCH (p:Person)-[:EARNS]->(salary:Salary)
RETURN p.name, salary.amount
```

---

### Pattern 8: Type Mismatches in Comparisons

**Symptom:** Unexpected query results or type error

**Detection Approach:**
1. Extract property types from schema: `property: string|number|boolean`
2. Identify comparison operations in WHERE clauses
3. Check operand types match
4. Flag type incompatibilities

**Example:**
```sparql
FILTER (?age > "30")
```

**Detection:** Integer property compared with string literal

**Corrected Query:**
```sparql
FILTER (?age > 30)
```

---

## Query Analysis Patterns

### Pattern 9: Relationship Direction Validation

**Symptom:** Query returns no results despite valid syntax and schema

**Detection Approach:**
1. Reverse relationship directions in query
2. Check if reversed version returns results
3. Suggest direction reversal if reversed works
4. Validate against schema constraints

**Example:**
```cypher
MATCH (c:Company)-[:WORKS_AT]->(p:Person)
RETURN c, p
```

**Detection:** No results returned, but data exists

**Suggestion:** Check relationship direction. Standard pattern: `Person -[:WORKS_AT]-> Company`

**Corrected Query:**
```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN p, c
```

---

### Pattern 10: Multi-Hop Chain Breakage

**Symptom:** Multi-hop query returns no results

**Detection Approach:**
1. Decompose multi-hop query into individual hops
2. Test each hop independently
3. Identify which hop returns no results
4. Analyze the failing hop for issues

**Example Failing Query:**
```cypher
MATCH (a:Person)-[:KNOWS]->(b:Person)-[:WORKS_AT]->(c:Company)
RETURN a, b, c
```

**Debug Steps:**
```cypher
-- Hop 1: Person knows Person
MATCH (a:Person)-[:KNOWS]->(b:Person)
RETURN COUNT(*)
-- Result: 1000

-- Hop 2: Person works at Company
MATCH (b:Person)-[:WORKS_AT]->(c:Company)
RETURN COUNT(*)
-- Result: 500

-- Combined: Both conditions
MATCH (a:Person)-[:KNOWS]->(b:Person)
MATCH (b)-[:WORKS_AT]->(c:Company)
RETURN COUNT(*)
-- Result: 0 (no people who both know someone AND that someone works at a company)
```

**Analysis:** The middle node `b` satisfies neither condition in combination

**Corrected Query or Alternative:**
```cypher
-- Find people who know someone (any person)
MATCH (a:Person)-[:KNOWS]->(b:Person)
RETURN DISTINCT a.name, b.name

-- Or find persons and their employers separately
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN p, c
```

---

### Pattern 11: Cartesian Product Detection

**Symptom:** Unexpected massive result set or timeout

**Detection Approach:**
1. Identify disconnected MATCH clauses: `MATCH (a), (b)` with no connection
2. Check if result count = count(a) × count(b)
3. Suggest connecting nodes with relationships

**Example Problematic Query:**
```cypher
MATCH (p:Person), (c:Company)
RETURN p, c
```

**Detection:** Results = 10,000 people × 500 companies = 5,000,000 rows

**Corrected Query (with relationship):**
```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN p, c
```

---

### Pattern 12: Unreachable Pattern Detection

**Symptom:** Contradictory WHERE conditions causing no results

**Detection Approach:**
1. Analyze WHERE clause conditions
2. Detect logical contradictions: `p.age > 30 AND p.age < 20`
3. Detect impossible patterns: `:Label1` and `:Label2` on same node (if mutually exclusive)
4. Flag for review

**Example:**
```cypher
MATCH (p:Person)
WHERE p.age > 30 AND p.age < 20
RETURN p
```

**Detection:** Contradiction: `p.age` cannot be both > 30 and < 20

**Corrected Query:**
```cypher
MATCH (p:Person)
WHERE p.age > 30 OR p.age < 20
RETURN p
```

---

## Relationship Traversal Patterns

### Pattern 13: Label-Relationship Compatibility Check

**Symptom:** Query returns no results despite valid schema elements

**Detection Approach:**
1. Extract source label and relationship type
2. Query schema for valid target labels for that relationship
3. Check if query's target label is in valid list
4. Suggest valid target labels

**Example:**
```cypher
MATCH (p:Person)-[:MANUFACTURES]->(product:Product)
RETURN p, product
```

**Detection:** Schema shows `MANUFACTURES` only connects `Company -> Product`, not `Person -> Product`

**Corrected Query:**
```cypher
MATCH (c:Company)-[:MANUFACTURES]->(product:Product)
RETURN c, product

-- Or if finding which persons work at companies that manufacture:
MATCH (p:Person)-[:WORKS_AT]->(c:Company)-[:MANUFACTURES]->(product:Product)
RETURN p, c, product
```

---

### Pattern 14: Traversal Direction Consistency

**Symptom:** Complex multi-hop query returns no results

**Detection Approach:**
1. Extract each hop's direction: `->` vs `<-`
2. Verify consistency with domain logic
3. Check schema for relationship cardinality
4. Suggest direction corrections

**Example Query with Direction Issues:**
```cypher
MATCH (c:Company)<-[:WORKS_AT]-(p:Person)<-[:REPORTS_TO]-(mgr:Employee)
RETURN c, p, mgr
```

**Detection Issues:**
- `Company <-[:WORKS_AT]- Person`: Reversed (should be Person -> Company)
- `Person <-[:REPORTS_TO]- Employee`: Reversed (should be Employee -> Person)

**Corrected Query:**
```cypher
MATCH (c:Company)<-[:WORKS_AT]-(p:Person)<-[:REPORTS_TO]-(mgr:Employee)
-- Or more logically:
MATCH (mgr:Employee)-[:REPORTS_TO]->(p:Person)-[:WORKS_AT]->(c:Company)
RETURN c, p, mgr
```

---

### Pattern 15: Cardinality Constraint Validation

**Symptom:** Unexpected result counts or NULL values

**Detection Approach:**
1. Identify relationships with cardinality constraints (1:1, 1:N, N:M)
2. Check if query respects cardinality
3. Use OPTIONAL MATCH for zero-or-one relationships
4. Use COLLECT for one-to-many relationships

**Example:**
```cypher
MATCH (p:Person)-[:MARRIED_TO]->(spouse:Person)
RETURN p, spouse
```

**Issue:** If MARRIED_TO is 1:1 (or 0:1), query may return unexpected results for single people

**Corrected Query (with Optional):**
```cypher
MATCH (p:Person)
OPTIONAL MATCH (p)-[:MARRIED_TO]->(spouse:Person)
RETURN p, spouse
```

**Or for one-to-many relationships:**
```cypher
MATCH (c:Company)-[:EMPLOYS]->(e:Employee)
RETURN c, collect(e) as employees
GROUP BY c
```

---

## Performance Issue Patterns

### Pattern 16: Inefficient Filter Placement

**Symptom:** Query runs slowly despite small result set

**Detection Approach:**
1. Identify restrictive WHERE conditions
2. Check if conditions appear after expensive MATCH clauses
3. Suggest moving conditions to earlier MATCH clauses
4. Calculate potential rows processed

**Example Inefficient Query:**
```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
WHERE p.age > 30 AND c.industry = "Tech"
RETURN p, c
```

**Analysis:**
- Matches all Person-Company relationships first (expensive)
- Then filters (late)
- Processes: all people × all companies, then filters

**Optimized Query:**
```cypher
MATCH (p:Person)
WHERE p.age > 30
MATCH (p)-[:WORKS_AT]->(c:Company)
WHERE c.industry = "Tech"
RETURN p, c
```

**Optimization:**
- Filters Person first (restrictive)
- Then traverses relationships
- Filters Company second
- Processes fewer rows earlier

---

### Pattern 17: Index Utilization

**Symptom:** Queries run slowly on large datasets

**Detection Approach:**
1. Identify frequently filtered properties in WHERE clauses
2. Check if indexes exist on those properties
3. Suggest creating indexes on common filter columns
4. Analyze query execution plans

**Example Query Needing Index:**
```cypher
MATCH (p:Person {email: "user@example.com"})
RETURN p
```

**Optimization:**
```cypher
-- Create index
CREATE INDEX ON :Person(email)

-- Verify index usage
EXPLAIN MATCH (p:Person {email: "user@example.com"}) RETURN p
```

---

### Pattern 18: Aggregation and Grouping Efficiency

**Symptom:** Query returns too many rows or timeout on aggregation

**Detection Approach:**
1. Identify COUNT, SUM, COLLECT operations
2. Verify GROUP BY clauses are present
3. Check if aggregation is at proper scope
4. Suggest using LIMIT to reduce output

**Example:**
```cypher
MATCH (p:Person)-[:KNOWS]->(friend:Person)
RETURN p.name, friend.name
```

**Issue:** Returns all friend pairs (potentially millions)

**Optimized with Aggregation:**
```cypher
MATCH (p:Person)-[:KNOWS]->(friend:Person)
RETURN p.name, count(friend) as friend_count
GROUP BY p.name
LIMIT 100
```

---

## Best Practice Patterns

### Pattern 19: Schema-Driven Query Validation

**Pattern:** Always validate queries against schema before execution

**Implementation:**
1. Define schema explicitly (node types, properties, relationships)
2. Before query execution, check query elements against schema
3. Provide detailed error messages for mismatches
4. Suggest corrections based on schema

**Example Schema Definition:**
```json
{
  "nodes": {
    "Person": {
      "properties": {
        "name": "string",
        "age": "integer",
        "email": "string"
      }
    },
    "Company": {
      "properties": {
        "name": "string",
        "industry": "string"
      }
    }
  },
  "relationships": {
    "WORKS_AT": {
      "source": "Person",
      "target": "Company"
    }
  }
}
```

**Query Validation Against Schema:**
```cypher
-- Valid query (all elements in schema)
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
WHERE p.age > 30
RETURN p.name, c.name

-- Invalid query (Employee not in schema)
MATCH (e:Employee)-[:WORKS_AT]->(c:Company)
RETURN e
-- Error: "Employee" label not found in schema. Did you mean "Person"?
```

---

### Pattern 20: Progressive Query Testing

**Pattern:** Build and test complex queries incrementally

**Implementation:**
1. Start with simplest query (single node)
2. Add one relationship at a time
3. Test at each step
4. Isolate failures immediately

**Example Building Complex Query:**

**Step 1: Start Simple**
```cypher
MATCH (p:Person)
RETURN COUNT(p)
-- Verify Person nodes exist
```

**Step 2: Add Relationship**
```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN COUNT(*)
-- Verify relationship exists
```

**Step 3: Add Filter**
```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
WHERE c.industry = "Tech"
RETURN COUNT(*)
-- Verify filtered relationships exist
```

**Step 4: Add Another Pattern**
```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
WHERE c.industry = "Tech"
MATCH (c)-[:LOCATED_IN]->(city:City)
RETURN p, c, city
```

**Step 5: Complex Multi-Hop**
```cypher
MATCH (mgr:Person {manager:true})-[MANAGES]-(p:Person)
WHERE mgr.department = "Engineering"
MATCH (p)-[:WORKS_AT]->(c:Company)-[:LOCATED_IN]->(city:City)
WHERE city.name = "NYC"
RETURN mgr, p, c, city
GROUP BY mgr
```

---

### Pattern 21: Error Categorization Framework

**Pattern:** Classify errors into categories for targeted debugging

**Error Categories:**

1. **Syntax Errors** - Query cannot be parsed
   - Missing parentheses, brackets
   - Invalid operator usage
   - Clause ordering violations

2. **Schema Errors** - Elements don't exist in schema
   - Non-existent labels
   - Non-existent relationship types
   - Non-existent properties

3. **Logical Errors** - Query is valid but doesn't produce expected results
   - Unreachable patterns
   - Contradictory conditions
   - Incorrect variable bindings

4. **Performance Errors** - Query completes but slowly
   - Missing indexes
   - Cartesian products
   - Inefficient filter placement

5. **Data Errors** - Query returns unexpected results
   - Type mismatches
   - Missing relationships
   - Incomplete data

---

### Pattern 22: Debugging Workflow Template

**Pattern:** Structured approach to debugging any query

**Workflow:**

1. **Verify Query Syntax** → Run through parser
2. **Check Schema Elements** → Validate labels, types, properties
3. **Validate Relationships** → Ensure relationships connect correct nodes
4. **Decompose Query** → Test each hop separately
5. **Analyze Results** → Check result count and types
6. **Optimize** → Add indexes, reorder clauses
7. **Test with Real Data** → Verify against actual dataset
8. **Document Solution** → Record fix for future reference

---

## Summary

These 22 patterns provide comprehensive coverage of:

- **Syntax (4 patterns)** - Parser-level errors
- **Schema (4 patterns)** - Element validation
- **Analysis (4 patterns)** - Query structure issues
- **Traversal (3 patterns)** - Relationship navigation
- **Performance (3 patterns)** - Efficiency optimization
- **Best Practices (4 patterns)** - Systematic approaches

Apply these patterns systematically for systematic query debugging.


