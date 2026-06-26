# Neo4j Design Patterns

## Node Labels

- Use nouns for labels: `Person`, `Company`, `Product`
- Avoid overly generic labels like `Node`

## Relationship Types

- Use verbs: `WORKS_AT`, `BOUGHT`, `KNOWS`
- Direction matters: `(a)-[:KNOWS]->(b)` implies a knows b

## Indexing

```cypher
CREATE INDEX person_name FOR (n:Person) ON (n.name)
```

## Constraints

```cypher
CREATE CONSTRAINT person_id FOR (n:Person) REQUIRE n.id IS UNIQUE
```

## Idempotency

Use MERGE for upsert operations:

```cypher
MERGE (n:Person {name: "Alice"})
ON CREATE SET n.created = timestamp()
ON MATCH SET n.updated = timestamp()
```
