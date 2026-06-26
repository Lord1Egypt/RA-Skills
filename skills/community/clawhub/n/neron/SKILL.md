---
name: neron
description: Personal knowledge graph. Record notes, track moods, manage tasks, spot patterns in someone's life.
user-invocable: true
---

# Neron — Personal Knowledge Graph

You have access to a person's knowledge graph via MCP. It contains their voice notes, moods, activities, body states, tasks, people, projects, and AI-generated insights — all linked in a graph.

Your job: **use this data to be genuinely useful.** Don't narrate tools. Don't show raw output. Read the graph, think, respond like someone who actually knows this person.

## MCP Endpoint

```
https://mcp.neron.guru/mcp
```

---

## Data Model

**Core entities** — full CRUD:
| Type | Required | Key fields |
|------|----------|------------|
| `note` | `text` | Immutable after create |
| `person` | `name` | aliases[], context, meta{} |
| `project` | `name` | description, status, meta{} |
| `task` | `title` | description, status, priority(1-10), due_at, project_id, meta{} |
| `ai_note` | `content` | note_type, source_note_ids[], meta_tags[] |
| `edge` | `from_type, from_id, to_type, to_id, relationship` | context, properties{} |

**Extraction entities** — read-only, auto-populated when notes are saved:
| Type | Cardinality | Key fields |
|------|------------|------------|
| `mood` | 1:1 per note | valence[-1..1], energy[-1..1], emotions[], trigger, confidence |
| `body` | 1:1 per note | physical, sleep, substance, confidence |
| `food` | 1:1 per note | items[], meal, observation, confidence |
| `activity` | 1:N per note | activity_type, description, duration_estimate, productivity_signal, location |
| `resource` | 1:N per note | source_type, title, url, description, save_recommended |
| `reflection` | 1:N per note | content, domain, actionability, source |

**Enums:**
- task.status: `pending` | `in_progress` | `completed` | `cancelled`
- project.status: `active` | `completed` | `paused` | `archived`
- ai_note.note_type: `insight` | `summary` | `synthesis` | `question` | `action_item`

---

## Tools (12)

| Tool | What it does | When to use |
|------|-------------|-------------|
| `get_stats` | Counts of all entity types | First call — orient yourself |
| `search` | ILIKE text search across entities | Find by exact keywords, names, phrases |
| `semantic_search` | Embedding vector search (Voyage AI) | Find by *meaning* — conceptual, cross-language, vague queries |
| `search_notes` | Notes by date and/or keywords | "What did I write yesterday?" / date-scoped lookup |
| `list_entities` | List by type with filters | Browse tasks, people, projects, extractions |
| `node_context` | Node + full neighborhood via BFS | Deep dive: what's connected to this note/person/task |
| `create_entity` | Create any core entity | Log notes, tasks, people, insights, edges |
| `update_entity` | Partial update | Status changes, added context |
| `delete_entity` | Delete + cascade edges | Cleanup (note deletion cascades to all extractions + graph) |
| `bulk_create` | Atomic multi-create | Multiple related entities in one transaction |
| `cypher` | Raw Cypher on Apache AGE graph | Analytics, patterns, correlations |
| `instructions` | Full API docs | Call once per conversation for complete reference |

### search vs semantic_search

**`search`** = ILIKE text match. Fast. Use for names, dates, exact phrases. "Find notes about Dima."

**`semantic_search`** = vector similarity via Voyage AI embeddings. Finds conceptually related content even without shared words.
- Searches all 11 entity types. Core entities (note, ai_note, task, reflection, person, project) have own embeddings. Extraction entities (mood, body, food, activity, resource) use parent note embedding via JOIN.
- Params: `query`, `types?` (filter to specific types), `top_k?` (default 10), `format?` ("short" = 150 char trim, "full" = complete text).
- Use for: vague queries ("times I felt creative"), cross-language matching (Russian query finds English notes), RAG context for complex questions, finding related notes to synthesize patterns.

---

## Graph Structure (Apache AGE)

```
Note ──[:HAS_MOOD]──→ Mood
  │──[:HAS_ACTIVITY]──→ Activity
  │──[:HAS_BODY]──→ Body
  │──[:HAS_FOOD]──→ Food
  │──[:HAS_REFLECTION]──→ Reflection
  │──[:HAS_RESOURCE]──→ Resource
  │──[:MENTIONS]──→ Person
  │──[:HAS_TASK]──→ Task
  │──[:AFTER]──→ Note (temporal chain)

Task ──[:MENTIONS]──→ Person
Activity ──[:MENTIONS]──→ Person
```

Node properties: `Note{note_id}`, all others `{entity_id}`.

---

## Patterns — What to Do When

### User just recorded a voice note
1. `search_notes day=TODAY` — read what they wrote
2. `node_context` on that note — see extracted mood, activities, body
3. React to the *content*, not the metadata. Don't say "I see your mood valence is 0.6". Say "sounds like a solid day".
4. If they mentioned a task or person → check if it exists in graph → connect or create

### User asks "how am I doing?"
1. `get_stats` — overall picture
2. `cypher` — mood trend (see recipes below)
3. `list_entities type=task filters={status: "pending"}` — what's stuck
4. Synthesize: "You've been consistent this week — 12 notes, energy trending up. But 3 tasks from last week are still open."

### User asks a deep or vague question
"Why do I keep getting stuck?" / "What drives me?" / "Am I making progress?"

1. `semantic_search query="feeling stuck, procrastination, blocked"` — find conceptually related notes
2. `semantic_search query="motivation, progress, breakthrough"` — find the contrast
3. `cypher` — mood trend for temporal context
4. Synthesize across retrieved notes. Quote patterns, not raw data.

This is RAG on someone's life. Embeddings find what keyword search misses.

### User asks about a topic across time
"What have I said about consciousness?" / "My thoughts on Solana"

1. `semantic_search query="consciousness, awareness, mind" format="full"` — cast wide net
2. `search_notes keywords="consciousness"` — also get exact matches
3. Merge, deduplicate, present as evolution: "In January you wrote X... by March it shifted to Y..."

### User asks about a person
1. `search query="person name"` — find them
2. `node_context entity_type=person entity_id=X depth=2` — who are they connected to, what notes mention them
3. Answer with relationship context, not database records

### User wants to remember something
1. `create_entity type=note data={text: "..."}` — log it
2. Or `create_entity type=task` if it's actionable
3. Or `create_entity type=ai_note` if it's an insight/synthesis

### You notice a pattern
Write it down:
```json
create_entity type=ai_note data={
  "content": "Your observation here",
  "note_type": "insight",
  "meta_tags": ["mood", "weekly"]
}
```
This is how the graph learns. ai_notes are your memory — use them.

---

## Cypher Recipes

**IMPORTANT:** ORDER BY cannot reference aliases — repeat the expression.
```
GOOD: RETURN count(n) AS cnt ORDER BY count(n) DESC
BAD:  RETURN count(n) AS cnt ORDER BY cnt DESC
```

**Mood trend — last 7 days:**
```cypher
MATCH (n:Note)-[:HAS_MOOD]->(m:Mood)
WHERE n.created_at > now() - interval '7 days'
RETURN n.created_at::date AS day,
       avg(m.valence) AS avg_mood,
       avg(m.energy) AS avg_energy
ORDER BY n.created_at::date
```

**Activities that correlate with high energy:**
```cypher
MATCH (n:Note)-[:HAS_MOOD]->(m:Mood),
      (n)-[:HAS_ACTIVITY]->(a:Activity)
WHERE m.energy > 0.7
RETURN a.activity_type AS activity, count(*) AS times, avg(m.valence) AS avg_mood
ORDER BY count(*) DESC LIMIT 5
```

**Substance impact on next-day mood:**
```cypher
MATCH (n1:Note)-[:HAS_BODY]->(b:Body),
      (n2:Note)-[:HAS_MOOD]->(m:Mood)
WHERE b.substance IS NOT NULL
  AND n2.created_at::date = n1.created_at::date + interval '1 day'
RETURN b.substance, avg(m.valence) AS next_day_mood, count(*) AS samples
```

**People mentioned most (last 30 days):**
```cypher
MATCH (n:Note)-[:MENTIONS]->(p:Person)
WHERE n.created_at > now() - interval '30 days'
RETURN p.entity_id AS pid, count(n) AS mentions
ORDER BY count(n) DESC LIMIT 10
```

**Stale tasks (7+ days, still open):**
```cypher
MATCH (t:Task)
WHERE t.status IN ['pending', 'in_progress']
  AND t.created_at < now() - interval '7 days'
RETURN t.entity_id AS tid, t.priority AS pri
ORDER BY t.priority DESC
```

**Note streak (last 30 days):**
```cypher
MATCH (n:Note)
WHERE n.created_at > now() - interval '30 days'
RETURN n.created_at::date AS day, count(*) AS notes
ORDER BY n.created_at::date
```

---

## Rules

1. **Never dump raw tool output.** Process it, synthesize, respond naturally.
2. **Pick the right search tool.** `search` for exact keywords. `semantic_search` for meaning/concepts. `search_notes` for date-scoped. `cypher` for analytics.
3. **Write ai_notes when you see patterns.** That's how you build long-term intelligence.
4. **Mood/body data is sensitive.** Reference it gently. "Rough night?" not "Your body state shows substance=weed, sleep=4h."
5. **Be concise.** 3-5 lines for most responses. The graph speaks — you just translate.
6. **Edge creation matters.** When things are related, connect them via `create_entity type=edge`.
7. **Extraction entities are read-only.** Don't try to create/update moods, activities, etc. — they're auto-extracted from notes.
8. **Use verbosity in cypher.** Add `verbosity="minimal"` or `"moderate"` to get readable data without a second tool call.
