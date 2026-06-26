# Query Patterns

Cypher templates for all `weave.query` modes. Never use SQL. Parameters use `$name` syntax.

## lookup

```cypher
MATCH (p:Person {id: $person_id})
OPTIONAL MATCH (p)-[r:Knows]->(other:Person)
OPTIONAL MATCH (p)-[:HasPreference]->(pref:Preference)
RETURN p,
  collect(DISTINCT {rel_type: r.rel_type, name: other.name, id: other.id}) AS relationships,
  collect(DISTINCT {category: pref.category, value: pref.value, valence: pref.valence, confidence: pref.confidence}) AS preferences
```

By name (fuzzy):
```cypher
MATCH (p:Person)
WHERE lower(p.name) CONTAINS lower($name_query)
RETURN p.id, p.name, p.org, p.location_city
ORDER BY p.name LIMIT 10
```

## connection

Shortest path:
```cypher
MATCH path = shortestPath(
  (a:Person {id: $from_id})-[:Knows*1..4]-(b:Person {id: $to_id})
)
RETURN path
```

All paths up to depth 3 (use sparingly on large graphs):
```cypher
MATCH path = (a:Person {id: $from_id})-[:Knows*1..3]-(b:Person {id: $to_id})
RETURN path ORDER BY length(path) LIMIT 5
```

## serendipity

Shared preferences:
```cypher
MATCH (a:Person {id: $person_a_id})-[:HasPreference]->(pa:Preference)
MATCH (b:Person {id: $person_b_id})-[:HasPreference]->(pb:Preference)
WHERE pa.category = pb.category AND pa.valence = 'like' AND pb.valence = 'like'
  AND lower(pa.value) = lower(pb.value)
RETURN pa.category AS category, pa.value AS shared_interest
```

Mutual connections:
```cypher
MATCH (a:Person {id: $person_a_id})-[:Knows]-(mutual:Person)-[:Knows]-(b:Person {id: $person_b_id})
WHERE a.id <> b.id
RETURN mutual.name, mutual.id, mutual.org
```

## city

```cypher
MATCH (p:Person)
WHERE lower(p.location_city) = lower($city)
RETURN p.name, p.org, p.occupation, p.id
ORDER BY p.name
```

## summarize

```cypher
MATCH (p:Person {id: $person_id})
OPTIONAL MATCH (p)-[r:Knows]->(other:Person)
OPTIONAL MATCH (p)-[:HasPreference]->(pref:Preference)
WHERE pref.confidence >= 0.6
RETURN
  p.name AS name, p.org AS org, p.occupation AS role, p.location_city AS city,
  collect(DISTINCT {rel_type: r.rel_type, name: other.name}) AS relationships,
  collect(DISTINCT {category: pref.category, value: pref.value, valence: pref.valence}) AS preferences
```

Present as: who they are, how you know them, what to know (like), what to avoid (dislike/constraint).

## gift

```cypher
MATCH (p:Person {id: $person_id})-[:HasPreference]->(pref:Preference)
WHERE pref.valence = 'like' AND pref.confidence >= 0.5
  AND pref.category IN ['gift', 'food', 'interest', 'travel']
RETURN pref.category, pref.value, pref.confidence
ORDER BY pref.confidence DESC
```

Never fabricate preferences not in the graph.

## sync diff

Modified since last sync:
```cypher
MATCH (p:Person)
WHERE p.record_time > $last_sync_at
RETURN p.id, p.name, p.email, p.phone, p.org, p.record_time
ORDER BY p.record_time DESC
```

Not yet synced to Google:
```cypher
MATCH (p:Person) WHERE p.google_resource_name IS NULL
RETURN p.id, p.name, p.email
```

Not yet synced to Clay:
```cypher
MATCH (p:Person) WHERE p.clay_id IS NULL
RETURN p.id, p.name, p.email
```

## weave.status queries

```cypher
CALL show_tables() RETURN *;
MATCH (p:Person) RETURN count(p) AS people;
MATCH ()-[r:Knows]->() RETURN count(r) AS relationships;
MATCH (pref:Preference) RETURN count(pref) AS preferences;
CALL show_warnings() RETURN *;
```

## Error handling

Person not found by ID -- halt. Report: "No Person with id={id}." Do not create a placeholder.
Person not found by name, 0 results -- report: "No match for '{name}'. Use weave.upsert.person."
Person not found by name, 2+ results -- return candidate list, ask which to use.
Lock error -- surface immediately. Identify which process holds the lock. Do not retry silently.
Write read-back returns no row -- report: "Write may have failed — read-back returned no result."
COPY FROM with ignore_errors -- always follow with `CALL show_warnings()` and report skipped rows.
