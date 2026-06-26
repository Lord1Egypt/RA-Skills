# Cypher Cheatsheet

## Create

```cypher
CREATE (n:Person {name: "Alice", age: 30})
CREATE (a:Person)-[r:KNOWS {since: 2020}]->(b:Person)
```

## Match

```cypher
MATCH (n:Person) RETURN n
MATCH (a:Person)-[:KNOWS]->(b:Person) RETURN a.name, b.name
MATCH (n:Person {name: "Alice"}) RETURN n
```

## Update

```cypher
MATCH (n:Person {name: "Alice"}) SET n.age = 31
MATCH (n:Person {name: "Alice"}) SET n += {city: "NYC"}
```

## Delete

```cypher
MATCH (n:Person {name: "Alice"}) DELETE n
MATCH (n:Person) DETACH DELETE n  // delete node + all relationships
MATCH ()-[r:KNOWS]->() DELETE r
```

## Advanced

```cypher
// Shortest path
MATCH path = shortestPath((a:Person {name:"Alice"})-[*..4]-(b:Person {name:"Bob"})) RETURN path

// Count
MATCH (n:Person) RETURN count(n)

// Aggregation
MATCH (n:Person) RETURN n.city, count(n) as cnt ORDER BY cnt DESC
```
