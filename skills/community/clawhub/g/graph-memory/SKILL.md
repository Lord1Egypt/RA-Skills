---
name: graph-memory
description: "Query the agent's knowledge graph for entities, relationships, and statistics. Enables natural language exploration of accumulated session memory without shell commands."
metadata:
  {
    "openclaw":
      {
        "emoji": "🕸️",
        "requires": { "modules": ["better-sqlite3"] },
        "install":
          [
            {
              "id": "npm-better-sqlite3",
              "kind": "npm",
              "package": "better-sqlite3",
              "label": "Install better-sqlite3 (npm)",
            },
          ],
      },
  }
---

# Graph Memory

Query the agent's persistent knowledge graph — entities extracted from sessions, their relationships, and graph-wide statistics.

The graph is built from session history and contains people, projects, tools, concepts, files, errors, and more. Use this skill when the user asks about "what do you know about X", "how is X connected to Y", or when you need context about past work.

## Functions

### `graph_search(query, options)`

Search the graph for entities matching a text query.

**Parameters:**
- `query` (string, required) — Text to search for in entity names and canonical names
- `options` (object, optional):
  - `type` (string) — Filter by entity type (e.g. `person`, `project`, `tool`, `concept`, `file`)
  - `deep` (boolean) — Include relationship neighbors for each result (default: `false`)
  - `limit` (number) — Max results to return (default: `20`)

**Returns:** Markdown string with matching entities, their types, mention counts, and optional neighbor lists.

**Example:**
```js
graph_search("chimera", { type: "project", deep: true })
```

**Error cases:**
- Graph DB missing → `"Graph memory database not found at <path>"`
- No results → `"No entities matching '<query>' found in graph memory."`
- Runtime error → `"Graph query error: <message>"`

---

### `graph_stats()`

Return high-level statistics about the graph.

**Parameters:** None

**Returns:** Markdown string with:
- Total entity count
- Total relationship count
- Sessions processed count
- Entity type breakdown
- Top 10 entities by mention count

**Example:**
```js
graph_stats()
```

**Error cases:**
- Graph DB missing → `"Graph memory database not found at <path>"`
- Runtime error → `"Graph query error: <message>"`

---

### `graph_related(entity, depth)`

Traverse the graph from a starting entity, showing connected entities up to N hops away.

**Parameters:**
- `entity` (string, required) — Exact or approximate entity name to start from
- `depth` (number, optional) — Max traversal depth (default: `2`, max: `5`)

**Returns:** Markdown relationship tree showing paths from the starting entity to connected entities, with relationship types and entity details.

**Example:**
```js
graph_related("deepak", 2)
```

**Error cases:**
- Graph DB missing → `"Graph memory database not found at <path>"`
- Entity not found → `"Entity '<entity>' not found in graph memory."`
- No relationships → `"No relationships found for this entity in graph memory."`
- Runtime error → `"Graph query error: <message>"`

---

## Entity Types

Common types in the graph:

| Type | Description |
|------|-------------|
| `person` | People mentioned in sessions |
| `project` | Projects, repositories, systems |
| `tool` | Software tools, libraries, CLIs |
| `concept` | Ideas, theories, patterns |
| `file` | Specific files referenced |
| `error` | Error types or failure modes |
| `topic` | Broad subject areas |
| `institution` | Organizations, universities |
| `research_paper` | Academic papers |

## Notes

- The graph database lives at `~/.openclaw/workspace/.openclaw_memory/graph.db`
- It is populated by a background queue worker that processes session history
- Not all sessions have been processed; extraction quality varies
- Relationship density is highest for project/file connections; person-to-project links are sparse
- Use `graph_search` with `deep: true` to see immediate neighbors without full traversal
