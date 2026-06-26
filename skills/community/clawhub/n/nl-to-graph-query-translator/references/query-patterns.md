# Query Patterns Reference

## Translation Strategy

The natural language to graph query translation follows a systematic 5-step process:

### 1. Identify Entities

Extract noun phrases and proper nouns that represent graph nodes:

**Example:**
```
Input: "Find employees who work at Acme"

Entities:
- "employees" → Person/Employee label
- "Acme" → Company label
```

**Extraction patterns:**
- Proper nouns → Likely node identifiers
- Count nouns (people, companies) → Node labels
- Named locations → Geography nodes

### 2. Identify Relationships

Extract verbs and prepositions that represent connections:

**Example:**
```
Input: "Find employees who work at Acme"

Relationships:
- "work at" → WORKS_AT relationship type
```

**Common relationship mappings:**
- "work at" → WORKS_AT
- "located in" → LOCATED_IN
- "knows" → KNOWS
- "purchased" → PURCHASED
- "owns" → OWNS
- "manages" → MANAGES

### 3. Determine Query Type

Classify the request into one of these categories:

- **Node Query**: Find specific nodes
  - "Find all employees"
  - "Show companies in California"

- **Relationship Query**: Find connections
  - "Who does Alice work with?"
  - "List all supplier relationships"

- **Path Query**: Find paths between nodes
  - "How are Alice and Bob connected?"
  - "Find shortest path between A and B"

- **Count/Aggregation**: Numerical results
  - "How many employees work at Acme?"
  - "Average salary by department"

- **Filter**: Conditional results
  - "Find employees with salary > 50k"
  - "Show inactive accounts"

### 4. Construct Query Pattern

Build the graph pattern using the identified entities and relationships:

**Example:**
```
NL: "Find employees who work at Acme earning more than $50,000"

Pattern: (person:Person)-[:WORKS_AT]->(company:Company {name: "Acme"})
         where person.salary > 50000
```

### 5. Generate Query Syntax

Convert the pattern into Cypher or SPARQL:

**Cypher:**
```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company {name: "Acme"})
WHERE p.salary > 50000
RETURN p
```

**SPARQL:**
```sparql
SELECT ?person
WHERE {
  ?person rdf:type ex:Person .
  ?person ex:salary ?salary .
  ?person ex:works_at ex:Acme .
  FILTER (?salary > 50000)
}
```

---

## Common Graph Patterns

### Pattern 1: Simple Entity Lookup

**Natural Language:**
```
"Find all people named Alice"
```

**Cypher:**
```cypher
MATCH (p:Person {name: "Alice"})
RETURN p
```

**SPARQL:**
```sparql
SELECT ?person
WHERE {
  ?person rdf:type ex:Person .
  ?person foaf:name "Alice" .
}
```

---

### Pattern 2: Single-Hop Relationship

**Natural Language:**
```
"Show companies where employees work"
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

### Pattern 3: Multi-Hop Query (Fixed Depth)

**Natural Language:**
```
"Find people connected to Alice within two relationships"
```

**Cypher:**
```cypher
MATCH (alice:Person {name: "Alice"})-[*1..2]-(connected)
RETURN connected
```

**SPARQL:**
```sparql
SELECT ?connected
WHERE {
  {
    ex:Alice (ex:knows|ex:works_with) ?connected .
  }
  UNION
  {
    ex:Alice (ex:knows|ex:works_with)/(ex:knows|ex:works_with) ?connected .
  }
}
```

---

### Pattern 4: Filtered Results

**Natural Language:**
```
"Find employees earning more than $60,000"
```

**Cypher:**
```cypher
MATCH (e:Employee)
WHERE e.salary > 60000
RETURN e
```

**SPARQL:**
```sparql
SELECT ?employee
WHERE {
  ?employee rdf:type ex:Employee .
  ?employee ex:salary ?salary .
  FILTER (?salary > 60000)
}
```

---

### Pattern 5: Aggregation/Count

**Natural Language:**
```
"Count how many employees work at each company"
```

**Cypher:**
```cypher
MATCH (e:Employee)-[:WORKS_AT]->(c:Company)
RETURN c.name, COUNT(e) as employee_count
GROUP BY c.name
```

**SPARQL:**
```sparql
SELECT ?company (COUNT(?employee) as ?count)
WHERE {
  ?employee rdf:type ex:Employee .
  ?employee ex:works_at ?company .
}
GROUP BY ?company
```

---

### Pattern 6: Optional Relationships

**Natural Language:**
```
"Find all people and their managers if they have one"
```

**Cypher:**
```cypher
MATCH (p:Person)
OPTIONAL MATCH (p)-[:MANAGED_BY]->(manager:Person)
RETURN p, manager
```

**SPARQL:**
```sparql
SELECT ?person ?manager
WHERE {
  ?person rdf:type ex:Person .
  OPTIONAL {
    ?person ex:managed_by ?manager .
  }
}
```

---

### Pattern 7: Conditional Logic

**Natural Language:**
```
"Show employees categorized as senior (>10 years) or junior"
```

**Cypher:**
```cypher
MATCH (e:Employee)
RETURN e.name, 
       CASE 
         WHEN e.years_employed > 10 THEN "Senior"
         ELSE "Junior"
       END as category
```

**SPARQL:**
```sparql
SELECT ?employee ?category
WHERE {
  ?employee rdf:type ex:Employee .
  ?employee ex:years_employed ?years .
  BIND(
    IF(?years > 10, "Senior", "Junior") AS ?category
  )
}
```

---

### Pattern 8: Multiple Paths (UNION)

**Natural Language:**
```
"Find all people who either work at or founded companies"
```

**Cypher:**
```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN p, c
UNION
MATCH (p:Person)-[:FOUNDED]->(c:Company)
RETURN p, c
```

**SPARQL:**
```sparql
SELECT ?person ?company
WHERE {
  {
    ?person ex:works_at ?company .
  }
  UNION
  {
    ?person ex:founded ?company .
  }
}
```

---

### Pattern 9: Negation

**Natural Language:**
```
"Find employees who don't report to Alice"
```

**Cypher:**
```cypher
MATCH (e:Employee)
WHERE NOT (e)-[:REPORTS_TO]->(:Person {name: "Alice"})
RETURN e
```

**SPARQL:**
```sparql
SELECT ?employee
WHERE {
  ?employee rdf:type ex:Employee .
  NOT EXISTS {
    ?employee ex:reports_to ex:Alice .
  }
}
```

---

### Pattern 10: Distinct Results with Ordering

**Natural Language:**
```
"Show unique cities where our employees live, sorted alphabetically"
```

**Cypher:**
```cypher
MATCH (e:Employee)-[:LIVES_IN]->(city:City)
RETURN DISTINCT city.name
ORDER BY city.name ASC
```

**SPARQL:**
```sparql
SELECT DISTINCT ?city
WHERE {
  ?employee rdf:type ex:Employee .
  ?employee ex:lives_in ?city_node .
  ?city_node foaf:name ?city .
}
ORDER BY ?city
```

---

## Entity Recognition Patterns

Common entity types and their indicators:

| Entity Type | Indicators | Example |
|------------|-----------|---------|
| Person | "person", "employee", "user", "people", proper names | "Alice", "Bob", "John Smith" |
| Organization | "company", "organization", "department", "team" | "Acme", "Engineering", "HR" |
| Location | "city", "country", "place", "location" | "New York", "California", "London" |
| Product | "product", "item", "service" | "iPhone", "Database", "Software" |
| Date/Time | "today", "yesterday", "date", month/year | "March 2026", "2026-03-08" |

---

## Relationship Type Mapping

Common natural language phrases mapped to relationship types:

| NL Phrase | Relationship Type | Direction | Example |
|-----------|------------------|-----------|---------|
| "works at" | WORKS_AT | → | Employee works at Company |
| "located in" | LOCATED_IN | → | Company located in City |
| "knows" | KNOWS | ↔ | Person knows Person |
| "purchased" | PURCHASED | → | Customer purchased Product |
| "owns" | OWNS | → | Person owns Company |
| "manages" | MANAGES | → | Manager manages Employee |
| "reports to" | REPORTS_TO | → | Employee reports to Manager |
| "has" | HAS | → | Company has Department |
| "created" | CREATED | → | Person created Product |

---

## Query Type Classification

Determine output type based on NL indicators:

**SELECT (Return data):**
- "Find", "Show", "List", "Get", "What", "Who", "Which"

**COUNT (Aggregation):**
- "How many", "Count", "Total", "Number of"

**EXISTS (Boolean):**
- "Does", "Is there", "Do any"

**PATH (Traversal):**
- "Connect", "Path", "Route", "How are they related"

**AGGREGATE:**
- "Average", "Sum", "Max", "Min", "Group by"

---

## Ambiguity Resolution

When NL is ambiguous:

1. **Relationship direction**: Assume directed unless bidirectional is specified
   - "Alice works with Bob" → Could be WORKS_WITH (↔) or directional
   
2. **Hop depth**: Default to direct relationship unless specified
   - "Connected to" → Could mean direct or multi-hop
   
3. **Property matching**: Use exact match unless comparison is explicit
   - "Find companies" vs "Find companies with > 1000 employees"

4. **Label inference**: Use context to infer node labels
   - "Find Alice" → Person (if context shows Alice is a person)
   - "Find Acme" → Company (if context shows Acme is a company)

---

## See Also

- [Cypher Query Guide](cypher-query-guide.md)
- [SPARQL Query Guide](sparql-query-guide.md)
- [Entity Recognition](entity-recognition.md)
- [Relationship Extraction](relationship-extraction.md)

