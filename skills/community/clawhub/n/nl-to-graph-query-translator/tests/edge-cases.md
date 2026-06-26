# Known Limitations & Edge Cases

## Known Limitations

### 1. Complex Temporal Reasoning

The translator currently has limited support for complex temporal expressions.

**Limitation:**
```
"Find employees hired between 2020 and 2022 who left after 2025"
```

May generate incomplete queries due to multi-stage temporal logic.

**Workaround:**
Break into simpler queries or use explicit property filters:
```cypher
MATCH (e:Employee)
WHERE e.hired_date >= date('2020-01-01') AND e.hired_date <= date('2022-12-31')
  AND e.left_date > date('2025-01-01')
RETURN e
```

---

### 2. Nested Aggregations

The translator doesn't reliably handle deeply nested aggregations.

**Limitation:**
```
"For each department, find the average salary by role, then rank departments"
```

**Workaround:**
Use multiple query passes or raw Cypher:
```cypher
MATCH (e:Employee)-[:IN_DEPARTMENT]->(d:Department)-[:HAS_ROLE]->(r:Role)
WITH d, r, AVG(e.salary) as avg_salary
WITH d, COLLECT({role: r.name, avg: avg_salary}) as role_salaries
RETURN d, role_salaries
```

---

### 3. Ambiguous Entity Resolution

When entity names are ambiguous, the translator may choose incorrectly.

**Limitation:**
```
"Show Alice's connections"
- Alice could be a person, company, or place
- Without context, hard to disambiguate
```

**Workaround:**
Provide schema hints or be more specific:
```
"Show the person Alice's connections"
"Show employee Alice's connections"
```

---

### 4. Relationship Direction Inference

The translator may guess relationship direction incorrectly.

**Limitation:**
```
"Companies that work with Acme"
- Is it: Company -[WORKS_WITH]-> Acme or Acme -[WORKS_WITH]-> Company?
```

**Workaround:**
Be explicit about direction:
```
"Show companies that Acme works with"
"Show companies working for Acme"
```

---

### 5. Unsupported Query Constructs

Some advanced query features are not automatically translated.

**Unsupported:**
- Complex CASE expressions with multiple conditions
- Window functions (ROW_NUMBER, RANK)
- Recursive CTEs (Common Table Expressions)
- Custom aggregate functions

**Workaround:**
Use raw query syntax for these features.

---

### 6. Performance on Large Graphs

Unbounded path queries (`[*]`) can be very expensive on large graphs.

**Limitation:**
```
"Find people connected to Alice"
- Without hop limits, may timeout on graphs with millions of nodes
```

**Workaround:**
Always limit path length:
```cypher
MATCH (alice:Person {name: "Alice"})-[*1..5]-(connected)
RETURN connected
LIMIT 1000
```

---

### 7. Cross-Language Semantic Differences

Cypher and SPARQL have different semantics and features.

**Difference:**
```
Cypher: MATCH (n) RETURN count(n)  -- Returns 0 if no matches
SPARQL: SELECT (COUNT(?n) AS ?count) WHERE { ?n a rdfs:Resource }  -- Returns 0
```

Queries may not translate perfectly between languages.

---

### 8. Property Type Inference

The translator may not correctly infer property types.

**Limitation:**
```
"Find companies with revenue > 1 million"
- Is revenue a string, number, or currency object?
```

**Workaround:**
Provide schema with explicit property types.

---

## Edge Cases

### Edge Case 1: Pronoun Resolution

**Scenario:**
```
"Alice works at Acme. She manages the sales team."
- "She" refers to Alice, but may not be correctly resolved
```

**Expected behavior:**
```cypher
MATCH (alice:Person {name: "Alice"})-[:MANAGES]->(team:Team {name: "sales"})
RETURN alice, team
```

**Actual behavior:**
May fail to link "She" to Alice without explicit context.

**Mitigation:**
Provide coreference resolution hints or explicit names.

---

### Edge Case 2: Implicit Relationships

**Scenario:**
```
"The CEO of Acme is wealthy"
- "CEO of" is an implicit relationship (MANAGES or LEADS implied)
```

**Expected behavior:**
```cypher
MATCH (ceo:Person)-[:MANAGES|:LEADS]->(acme:Company {name: "Acme"})
RETURN ceo
```

**Actual behavior:**
May not infer implicit relationships correctly.

**Mitigation:**
Make relationships explicit:
```
"The person who manages Acme is wealthy"
```

---

### Edge Case 3: Singular vs. Plural Ambiguity

**Scenario:**
```
"Show products and their categories"
- "products" (plural) vs. "categories" (plural)
- Are these collections or individual items?
```

**Expected behavior:**
Handles both as sets.

**Potential issue:**
May incorrectly treat as singular count.

---

### Edge Case 4: Negation Scope

**Scenario:**
```
"Find employees not working at Acme or in Sales"
- Does this mean: (NOT at Acme) OR (NOT in Sales)?
- Or: NOT (at Acme OR in Sales)?
```

**Expected behavior:**
```cypher
-- Interpretation 1
MATCH (e:Employee)
WHERE NOT (e)-[:WORKS_AT]->(c:Company {name: "Acme"})
   OR NOT (e)-[:IN_DEPARTMENT]->(d:Department {name: "Sales"})
RETURN e

-- Interpretation 2
MATCH (e:Employee)
WHERE NOT ((e)-[:WORKS_AT]->(c:Company {name: "Acme"})
        OR (e)-[:IN_DEPARTMENT]->(d:Department {name: "Sales"}))
RETURN e
```

**Mitigation:**
Clarify with explicit grouping:
```
"Find employees who are either (not at Acme) or (not in Sales)"
vs.
"Find employees not in (Acme or Sales)"
```

---

### Edge Case 5: Numeric Comparison with Ambiguous Units

**Scenario:**
```
"Find employees earning more than 50"
- More than $50? $50,000? 50 units of currency X?
```

**Expected behavior:**
Parse with schema or context.

**Issue:**
Without context, may fail to generate query.

**Mitigation:**
Provide explicit units:
```
"Find employees earning more than $50,000"
"Find employees earning more than 50k"
```

---

### Edge Case 6: Date Format Variations

**Scenario:**
```
Different date formats:
- "March 8, 2026"
- "2026-03-08"
- "08/03/2026" (ambiguous: US or EU format?)
- "last Tuesday"
- "2 weeks ago"
```

**Issue:**
Parser may not handle all formats consistently.

**Mitigation:**
Use ISO 8601 format (`YYYY-MM-DD`) when possible.

---

### Edge Case 7: String Matching Sensitivity

**Scenario:**
```
"Find employee 'bob'"
vs.
"Find employee 'Bob'"
vs.
"Find employee 'BOB'"
```

**Issue:**
Case sensitivity varies by backend and configuration.

**Mitigation:**
Use explicit case handling:
```cypher
MATCH (e:Employee)
WHERE toLower(e.name) = toLower("bob")
RETURN e
```

---

### Edge Case 8: Unicode and Special Characters

**Scenario:**
```
"Find company 'Café Étoile'"
or
"Find entity with symbol @, #, etc."
```

**Issue:**
May not handle non-ASCII characters correctly.

**Mitigation:**
Test with your actual data; ensure proper encoding.

---

## Testing Strategy

### Unit Tests

Test individual components:

```python
def test_entity_extraction():
    text = "Find employees at Acme earning $60,000"
    entities = extract_entities(text)
    assert any(e.label == "PERSON" for e in entities)
    assert any(e.text == "Acme" for e in entities)

def test_relationship_extraction():
    text = "Alice works at Acme"
    rels = extract_relationships(text)
    assert any(r.relation_type == "WORKS_AT" for r in rels)
```

### Integration Tests

Test end-to-end translation:

```python
def test_translation_accuracy():
    result = translate_nl_to_query("Find employees at Acme", "cypher")
    assert "WORKS_AT" in result.query
    assert "Company" in result.query
    assert result.confidence > 0.8
```

### Edge Case Tests

```python
def test_ambiguous_entities():
    result = translate_nl_to_query("Find Alice", "cypher")
    assert result.alternative_queries  # Should provide alternatives
    assert result.confidence < 1.0

def test_negation():
    result = translate_nl_to_query("Find employees not at Acme", "cypher")
    assert "NOT" in result.query or "WHERE NOT" in result.query
```

---

## Troubleshooting

### Query Returns No Results

**Check:**
1. Are entity names spelled correctly?
2. Do entities exist in the database?
3. Check with exact labels: `MATCH (n:Person {name: "Alice"}) RETURN n`

### Query Times Out

**Check:**
1. Is the query unbounded (`[*]`)? Add a limit: `[*1..5]`
2. Are relationship types too broad? Specify exact types
3. Use `LIMIT` clause to reduce result set

### Query Returns Too Many Results

**Check:**
1. Add more specific filters
2. Use `LIMIT` to cap results
3. Add `DISTINCT` if seeing duplicates

---

## Reporting Issues

When reporting edge cases or limitations:

1. **Provide the exact natural language input**
2. **Show expected Cypher/SPARQL query**
3. **Show actual query generated (if any)**
4. **Describe the difference/issue**
5. **Include database schema if relevant**
6. **Note any workarounds found**

Example issue report:

```
Title: Pronoun resolution failing for "She manages..."

Input NL: "Alice works at Acme. She manages the sales team."

Expected Cypher:
MATCH (alice:Person {name: "Alice"})-[:MANAGES]->(team:Team)
RETURN alice, team

Actual: (fails to resolve "She")

Workaround: Use explicit name: "Alice works at Acme. Alice manages the sales team."

Database: Neo4j 5.0, schema with Person, Company, Team labels
```

---

## Future Improvements

Planned enhancements:

- ✅ Better coreference resolution (pronoun tracking)
- ✅ Support for window functions
- ✅ Recursive query generation
- ✅ Temporal reasoning improvements
- ✅ Multi-language NL support
- ✅ Custom domain vocabularies
- ✅ Query optimization suggestions
- ✅ Performance profiling integration

---

## See Also

- [Architecture & Design](../architecture.md)
- [Query Patterns Reference](../references/query-patterns.md)
- [API Reference](../references/api-reference.md)

