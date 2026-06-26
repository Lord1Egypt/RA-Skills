# SPARQL Query Guide

## Overview

SPARQL (Simple Protocol and RDF Query Language) is a query language for RDF triple stores and semantic web databases. It uses a triple-based model where all data is stored as subject-predicate-object triples.

## Basic Concepts

### RDF Triples

All data in SPARQL is represented as triples:
```
<subject> <predicate> <object>
```

Example:
```
:Alice :knows :Bob
:Alice :age 30
:Bob :name "Bob"
```

### URIs and Namespaces

```sparql
-- Full URI
<http://example.com/Alice>

-- Prefixed URI
PREFIX ex: <http://example.com/>
ex:Alice
```

## Basic Syntax

### SELECT Query

Returns specific variables:
```sparql
PREFIX ex: <http://example.com/>

SELECT ?person ?company
WHERE {
  ?person ex:works_at ?company .
}
```

### WHERE Clause

Defines the pattern to match:
```sparql
WHERE {
  ?person rdf:type ex:Person .
  ?person ex:name ?name .
}
```

### Triple Patterns

Basic pattern matching:
```sparql
?subject ?predicate ?object .
```

## Core Query Types

### CONSTRUCT (Build RDF)

Returns RDF data:
```sparql
PREFIX ex: <http://example.com/>

CONSTRUCT {
  ?person ex:knows ?friend .
}
WHERE {
  ?person ex:knows ?friend .
  ?friend rdf:type ex:Person .
}
```

### ASK (Boolean Query)

Returns true/false:
```sparql
PREFIX ex: <http://example.com/>

ASK {
  ex:Alice ex:knows ex:Bob .
}
```

### DESCRIBE (Get All Data)

Returns all data about a resource:
```sparql
PREFIX ex: <http://example.com/>

DESCRIBE ex:Alice
```

## Pattern Matching

### Basic Patterns

```sparql
PREFIX ex: <http://example.com/>

SELECT ?employee
WHERE {
  ?employee ex:works_at ex:Acme .
}
```

### Multiple Conditions

```sparql
PREFIX ex: <http://example.com/>

SELECT ?person
WHERE {
  ?person rdf:type ex:Person .
  ?person ex:age ?age .
  FILTER (?age > 30)
}
```

### Optional Patterns

```sparql
PREFIX ex: <http://example.com/>

SELECT ?person ?friend
WHERE {
  ?person rdf:type ex:Person .
  OPTIONAL {
    ?person ex:knows ?friend .
  }
}
```

## Filters

### Comparison Operators

```sparql
-- Greater than
FILTER (?age > 30)

-- Equals
FILTER (?name = "Alice")

-- Not equals
FILTER (?age != 25)

-- And/Or
FILTER (?age > 30 && ?status = "active")
FILTER (?city = "NYC" || ?city = "LA")
```

### String Functions

```sparql
-- String matching
FILTER (CONTAINS(?name, "Alice"))
FILTER (STARTS WITH ?email, "alice@")
FILTER (LANG(?label) = "en")

-- Regular expressions
FILTER (REGEX(?email, ".*@example\\.com$"))
```

### Numeric Functions

```sparql
-- Math functions
FILTER (?age >= 30 && ?age <= 65)
FILTER (ABS(?value) > 100)
FILTER (CEIL(?value) > 50)
```

## Aggregation

### GROUP BY with Aggregates

```sparql
PREFIX ex: <http://example.com/>

SELECT ?company (COUNT(?employee) as ?count)
WHERE {
  ?employee ex:works_at ?company .
}
GROUP BY ?company
```

### Aggregate Functions

```sparql
-- COUNT
SELECT (COUNT(?person) as ?total)
WHERE {
  ?person rdf:type ex:Person .
}

-- SUM
SELECT (SUM(?salary) as ?total_salary)
WHERE {
  ?employee ex:salary ?salary .
}

-- AVG, MIN, MAX
SELECT (AVG(?age) as ?avg_age) (MIN(?age) as ?min) (MAX(?age) as ?max)
WHERE {
  ?person rdf:type ex:Person .
  ?person ex:age ?age .
}
```

## Advanced Patterns

### UNION (Multiple Patterns)

```sparql
PREFIX ex: <http://example.com/>

SELECT ?name
WHERE {
  {
    ?person ex:name ?name .
    ?person rdf:type ex:Person .
  }
  UNION
  {
    ?company ex:name ?name .
    ?company rdf:type ex:Company .
  }
}
```

### Negation (NOT EXISTS)

```sparql
PREFIX ex: <http://example.com/>

SELECT ?person
WHERE {
  ?person rdf:type ex:Person .
  NOT EXISTS {
    ?person ex:knows ex:Alice .
  }
}
```

### VALUES (Inline Data)

```sparql
PREFIX ex: <http://example.com/>

SELECT ?person ?department
WHERE {
  ?person ex:works_in ?department .
  VALUES ?department { ex:HR ex:IT ex:Sales }
}
```

## Result Modifiers

### DISTINCT

Returns unique results:
```sparql
SELECT DISTINCT ?city
WHERE {
  ?person ex:lives_in ?city .
}
```

### ORDER BY

Sorts results:
```sparql
SELECT ?person ?age
WHERE {
  ?person rdf:type ex:Person .
  ?person ex:age ?age .
}
ORDER BY DESC(?age)
```

### LIMIT and OFFSET

```sparql
SELECT ?person
WHERE {
  ?person rdf:type ex:Person .
}
ORDER BY ?name
LIMIT 10
OFFSET 5
```

## Property Paths

### Simple Path Patterns

```sparql
PREFIX ex: <http://example.com/>

-- One step
SELECT ?friend
WHERE {
  ex:Alice ex:knows ?friend .
}

-- Multiple steps
SELECT ?distant
WHERE {
  ex:Alice ex:knows/ex:knows ?distant .
}

-- Any number of steps
SELECT ?connected
WHERE {
  ex:Alice ex:knows* ?connected .
}

-- One or more steps
SELECT ?connected
WHERE {
  ex:Alice ex:knows+ ?connected .
}

-- Optional step
SELECT ?connected
WHERE {
  ex:Alice ex:knows? ?connected .
}
```

### Complex Path Expressions

```sparql
-- Either knows or works_with
SELECT ?connected
WHERE {
  ex:Alice (ex:knows|ex:works_with) ?connected .
}
```

## SPARQL Endpoints

Query remote RDF stores:

```sparql
-- Example: Query DBpedia
SELECT ?person ?abstract
WHERE {
  ?person rdf:type dbo:Person .
  ?person dbo:abstract ?abstract .
  FILTER (LANG(?abstract) = "en")
}
LIMIT 10
```

## Performance Tips

1. **Use specific patterns**: Avoid overly generic patterns
   ```sparql
   -- Better
   ?person rdf:type ex:Person .
   ?person ex:works_at ex:Acme .
   
   -- Slower
   ?person ?p ?o .
   ```

2. **Filter early**: Put FILTER clauses close to matching patterns
   ```sparql
   SELECT ?person
   WHERE {
     ?person rdf:type ex:Person .
     FILTER (?age > 30)  -- Filter right after pattern
   }
   ```

3. **Limit results**:
   ```sparql
   SELECT ?person
   WHERE {
     ?person rdf:type ex:Person .
   }
   LIMIT 100
   ```

4. **Use DISTINCT carefully**: Can be expensive
5. **Index frequently-searched predicates**

## Common Mistakes

✗ Forgetting namespace prefixes  
✗ Not using FILTER in WHERE clause  
✗ Mixing LIMIT with GROUP BY incorrectly  
✗ Overly complex path expressions  
✗ Missing dot (.) at end of triple patterns  

## See Also

- [SPARQL Specification](https://www.w3.org/TR/sparql11-query/)
- [SPARQL Tutorial](https://www.w3.org/2004/SPARQL/tutorial.html)
- [Apache Jena SPARQL](https://jena.apache.org/tutorials/sparql.html)

