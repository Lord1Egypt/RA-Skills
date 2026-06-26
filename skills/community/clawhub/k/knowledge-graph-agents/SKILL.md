---
name: knowledge-graph-for-agents
description: Add a knowledge graph layer to an AI agent for relationship reasoning and multi-hop recall. Use when agents need to answer "who works with whom", "what's connected to X", or any relationship-based queries that flat search can't handle. Triggers on "knowledge graph", "Neo4j for agents", "entity extraction", "relationship search", "graph memory", "connected entities".
---

You are an expert in knowledge graphs for AI agent systems. Help the user add a graph layer that captures entities and relationships from their data, enabling multi-hop reasoning that vector and keyword search can't do.

## Why a Knowledge Graph?

Vector search finds *similar* documents. BM25 finds *matching* keywords. Neither answers:

- "Who works with Alice at Acme Corp?"
- "What services are running on the production server?"
- "Which projects depend on PostgreSQL?"

These require **relationship traversal** — following connections between entities. That's what a knowledge graph does.

## Architecture

```
Ingest → Entity Extraction → Graph Storage → Query
                                    ↓
                            Spreading Activation
                            (2-hop traversal)
```

### Entity Extraction (at ingest time)

Extract entities from every chunk of text you index:

```python
def extract_entities(text):
    """Simple heuristic entity extraction — no LLM needed."""
    entities = []
    # Title-case words (proper nouns)
    for word in text.split():
        if word[0].isupper() and len(word) > 2:
            entities.append({"name": word, "label": "Entity"})
    # Email addresses → Person
    for email in re.findall(r'[\w.+-]+@[\w.-]+\.\w+', text):
        entities.append({"name": email.split("@")[0].title(), "label": "Person"})
    return entities
```

For production, use spaCy NER or an LLM-based extractor for higher quality.

### Graph Storage

**SQLite graph** (simple, zero dependencies):

```sql
CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    label TEXT,
    properties_json TEXT DEFAULT '{}'
);

CREATE TABLE edges (
    source_id INTEGER REFERENCES nodes(id),
    target_id INTEGER REFERENCES nodes(id),
    rel_type TEXT DEFAULT 'RELATED_TO',
    weight REAL DEFAULT 1.0
);
```

**Neo4j** (production, scales better):

```cypher
CREATE (n:Entity {name: "Alice", label: "Person"})
CREATE (m:Entity {name: "Acme Corp", label: "Organisation"})
CREATE (n)-[:WORKS_AT]->(m)
```

### Co-occurrence Edges

When two named entities appear in the same chunk, create a `CO_OCCURS` edge:

```python
NAMED_LABELS = {"Person", "Place", "Organisation", "Event", "Product"}

for i, e1 in enumerate(chunk_entities):
    for e2 in chunk_entities[i+1:]:
        if e1["label"] in NAMED_LABELS and e2["label"] in NAMED_LABELS:
            graph.add_edge(e1["name"], e2["name"], "CO_OCCURS")
```

This is what gives the graph traversal value — connecting entities that appear together in context.

### Querying: Spreading Activation (2-hop)

Don't just match entities — traverse their connections:

```sql
-- Find entities connected to the query entity within 2 hops
WITH start_nodes AS (
    SELECT id, name FROM nodes WHERE name LIKE '%Alice%'
),
hop1 AS (
    SELECT CASE WHEN e.source_id = s.id THEN e.target_id ELSE e.source_id END as mid_id
    FROM start_nodes s JOIN edges e ON (e.source_id = s.id OR e.target_id = s.id)
    WHERE e.weight >= 0.5
),
hop2 AS (
    SELECT CASE WHEN e.source_id = h.mid_id THEN e.target_id ELSE e.source_id END as end_id,
           h.mid_id
    FROM hop1 h JOIN edges e ON (e.source_id = h.mid_id OR e.target_id = h.mid_id)
)
SELECT DISTINCT n.name, n.label FROM hop2 JOIN nodes n ON n.id = hop2.end_id;
```

### Hebbian Strengthening

Edges between co-accessed entities get stronger over time:

```python
def hebbian_strengthen(accessed_entities):
    """Strengthen edges between entities accessed in the same query."""
    for i, e1 in enumerate(accessed_entities):
        for e2 in accessed_entities[i+1:]:
            graph.update_edge_weight(e1, e2, delta=0.1)
```

## Integration with Hybrid Search

The graph layer works alongside BM25 and vector search:

1. **Extract entities from query** — "What services does Alice use?" → entities: [Alice, services]
2. **Query graph** — find Alice node, traverse USES relationships
3. **Boost matching chunks** — chunks mentioning graph-discovered entities get a score boost
4. **Fuse with other layers** — graph results merge into the unified ranking

## Common Patterns

### Resolving Ambiguity

```python
# Merge duplicate entities
graph.merge("Alice", "Alice Smith")  # Same person, different references
```

### Temporal Edges

```python
# Add timestamps to relationships
graph.add_edge("Alice", "Project Alpha", "WORKS_ON", 
               properties={"since": "2024-01-15"})
```

### Entity Types for Agents

| Label | Examples | Use Case |
|-------|----------|----------|
| Person | team members, contacts | Who questions |
| Organisation | companies, teams | Affiliation queries |
| Project | initiatives, repos | What's connected |
| System | services, tools | Infrastructure queries |
| Place | offices, cities | Location queries |

## Pitfalls

1. **Edge explosion** — don't create edges between ALL entities, only named ones (Person, Place, Org). Topic words create too many low-value edges.
2. **No graph layer** — you'll hit a ceiling where flat retrieval can't answer relationship questions.
3. **Over-reliance on LLM extraction** — heuristic extraction (capitalisation + patterns) is 80% as good at 0% of the cost.
4. **Forgetting to prune** — graphs grow. Schedule periodic cleanup of orphan nodes and weak edges.

## Getting Started

1. Pick a backend: SQLite (simple) or Neo4j (production)
2. Add entity extraction to your ingest pipeline
3. Create co-occurrence edges between named entities per chunk
4. Add 2-hop spreading activation to your search
5. Fuse graph results with your existing BM25/vector search
6. Set up a simple evaluation (test queries → expected results)
