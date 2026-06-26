# Basic Translations

This document provides simple, practical examples of natural language to graph query translations at beginner level.

## Simple Lookups

### Example 1: Find Person by Name

**Natural Language:**
```
Find all people named Alice
```

**Cypher:**
```cypher
MATCH (p:Person {name: "Alice"})
RETURN p
```

**SPARQL:**
```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ex: <http://example.com/>

SELECT ?person
WHERE {
  ?person rdf:type foaf:Person .
  ?person foaf:name "Alice" .
}
```

**Translation Steps:**
1. Entity: "Alice" → Person
2. Relationship: None
3. Query type: Node lookup with property filter
4. Translate to query language

---

### Example 2: Find All Companies

**Natural Language:**
```
Show all companies
```

**Cypher:**
```cypher
MATCH (c:Company)
RETURN c
```

**SPARQL:**
```sparql
SELECT ?company
WHERE {
  ?company rdf:type ex:Company .
}
```

---

### Example 3: Find with Multiple Filters

**Natural Language:**
```
Find employees older than 30
```

**Cypher:**
```cypher
MATCH (e:Employee)
WHERE e.age > 30
RETURN e
```

**SPARQL:**
```sparql
SELECT ?employee
WHERE {
  ?employee rdf:type ex:Employee .
  ?employee ex:age ?age .
  FILTER (?age > 30)
}
```

---

## Single-Hop Relationships

### Example 4: Find Related Nodes

**Natural Language:**
```
Find employees who work at Acme
```

**Cypher:**
```cypher
MATCH (e:Employee)-[:WORKS_AT]->(c:Company {name: "Acme"})
RETURN e
```

**SPARQL:**
```sparql
SELECT ?employee
WHERE {
  ?employee rdf:type ex:Employee .
  ?employee ex:works_at ex:Acme .
  ex:Acme rdf:type ex:Company .
}
```

---

### Example 5: Show Both Sides of Relationship

**Natural Language:**
```
Show all employees and the companies they work at
```

**Cypher:**
```cypher
MATCH (e:Employee)-[:WORKS_AT]->(c:Company)
RETURN e, c
```

**SPARQL:**
```sparql
SELECT ?employee ?company
WHERE {
  ?employee rdf:type ex:Employee .
  ?employee ex:works_at ?company .
  ?company rdf:type ex:Company .
}
```

---

### Example 6: Find Related People

**Natural Language:**
```
Show people that Alice knows
```

**Cypher:**
```cypher
MATCH (alice:Person {name: "Alice"})-[:KNOWS]->(known:Person)
RETURN known
```

**SPARQL:**
```sparql
SELECT ?known
WHERE {
  ex:Alice rdf:type foaf:Person .
  ex:Alice foaf:knows ?known .
  ?known rdf:type foaf:Person .
}
```

---

## Bidirectional Relationships

### Example 7: Undirected Relationship

**Natural Language:**
```
Find all people who know Alice
```

**Cypher:**
```cypher
MATCH (p:Person)-[:KNOWS]-(alice:Person {name: "Alice"})
RETURN p
```

**SPARQL:**
```sparql
SELECT ?person
WHERE {
  {
    ?person foaf:knows ex:Alice .
  }
  UNION
  {
    ex:Alice foaf:knows ?person .
  }
}
```

---

## Counting and Aggregation

### Example 8: Count Results

**Natural Language:**
```
How many employees work at Acme?
```

**Cypher:**
```cypher
MATCH (e:Employee)-[:WORKS_AT]->(c:Company {name: "Acme"})
RETURN COUNT(e) as employee_count
```

**SPARQL:**
```sparql
SELECT (COUNT(?employee) as ?count)
WHERE {
  ?employee rdf:type ex:Employee .
  ?employee ex:works_at ex:Acme .
}
```

---

### Example 9: Unique Results

**Natural Language:**
```
List all unique cities where our employees live
```

**Cypher:**
```cypher
MATCH (e:Employee)-[:LIVES_IN]->(city:City)
RETURN DISTINCT city.name
```

**SPARQL:**
```sparql
SELECT DISTINCT ?city
WHERE {
  ?employee rdf:type ex:Employee .
  ?employee ex:lives_in ?city_obj .
  ?city_obj foaf:name ?city .
}
```

---

## Limiting Results

### Example 10: Get First N Results

**Natural Language:**
```
Show the first 10 employees
```

**Cypher:**
```cypher
MATCH (e:Employee)
RETURN e
LIMIT 10
```

**SPARQL:**
```sparql
SELECT ?employee
WHERE {
  ?employee rdf:type ex:Employee .
}
LIMIT 10
```

---

## Ordering Results

### Example 11: Sort by Name

**Natural Language:**
```
List all companies sorted alphabetically
```

**Cypher:**
```cypher
MATCH (c:Company)
RETURN c
ORDER BY c.name ASC
```

**SPARQL:**
```sparql
SELECT ?company
WHERE {
  ?company rdf:type ex:Company .
}
ORDER BY ?company
```

---

### Example 12: Sort by Numeric Value Descending

**Natural Language:**
```
Show employees ordered by salary from highest to lowest
```

**Cypher:**
```cypher
MATCH (e:Employee)
RETURN e
ORDER BY e.salary DESC
```

**SPARQL:**
```sparql
SELECT ?employee ?salary
WHERE {
  ?employee rdf:type ex:Employee .
  ?employee ex:salary ?salary .
}
ORDER BY DESC(?salary)
```

---

## Optional Relationships

### Example 13: Left Join Pattern

**Natural Language:**
```
Show all employees and their managers, even if they don't have one
```

**Cypher:**
```cypher
MATCH (e:Employee)
OPTIONAL MATCH (e)-[:MANAGES_BY]->(m:Manager)
RETURN e, m
```

**SPARQL:**
```sparql
SELECT ?employee ?manager
WHERE {
  ?employee rdf:type ex:Employee .
  OPTIONAL {
    ?employee ex:manages_by ?manager .
  }
}
```

---

## Multiple Conditions

### Example 14: AND Conditions

**Natural Language:**
```
Find employees who are in Sales and earn more than $50,000
```

**Cypher:**
```cypher
MATCH (e:Employee)-[:IN_DEPARTMENT]->(d:Department {name: "Sales"})
WHERE e.salary > 50000
RETURN e
```

**SPARQL:**
```sparql
SELECT ?employee
WHERE {
  ?employee rdf:type ex:Employee .
  ?employee ex:in_department ex:Sales .
  ?employee ex:salary ?salary .
  FILTER (?salary > 50000)
}
```

---

### Example 15: OR Conditions

**Natural Language:**
```
Find employees in either Sales or Marketing department
```

**Cypher:**
```cypher
MATCH (e:Employee)-[:IN_DEPARTMENT]->(d:Department)
WHERE d.name = "Sales" OR d.name = "Marketing"
RETURN e
```

**SPARQL:**
```sparql
SELECT ?employee
WHERE {
  ?employee rdf:type ex:Employee .
  ?employee ex:in_department ?dept .
  ?dept foaf:name ?dept_name .
  FILTER (?dept_name = "Sales" || ?dept_name = "Marketing")
}
```

---

## Common Mistakes and Fixes

### Mistake 1: Forgetting Labels

❌ **Wrong:**
```cypher
MATCH (n {name: "Alice"})
RETURN n
```

✅ **Right:**
```cypher
MATCH (n:Person {name: "Alice"})
RETURN n
```

---

### Mistake 2: Missing Relationship Type

❌ **Wrong:**
```cypher
MATCH (e)--(c)
RETURN e, c
```

✅ **Right:**
```cypher
MATCH (e:Employee)-[:WORKS_AT]->(c:Company)
RETURN e, c
```

---

### Mistake 3: No WHERE Clause When Filtering

❌ **Wrong:**
```cypher
MATCH (e:Employee {age > 30})
RETURN e
```

✅ **Right:**
```cypher
MATCH (e:Employee)
WHERE e.age > 30
RETURN e
```

---

## Summary

These basic translation patterns cover:
- ✅ Simple entity lookups
- ✅ Property filters
- ✅ Single-hop relationships
- ✅ Counting and aggregation
- ✅ Result limiting and ordering
- ✅ Optional relationships
- ✅ Multiple conditions

For more advanced patterns, see [Multi-Hop Queries](multi-hop-queries.md) and [Parameterized Queries](parameterized-queries.md).

