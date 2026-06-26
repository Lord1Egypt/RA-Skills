# Architecture

## Design Principles

1. **Files, not databases.** Everything is Markdown or JSONL. No vector DB, no SQLite, no external services. `cat` and `grep` are valid queries.

2. **Framework agnostic.** Engram watches a folder. Any agent that writes daily logs to a folder can use Engram. Clawdbot, AutoGPT, CrewAI, bare scripts — doesn't matter.

3. **Cheap extraction.** We use the cheapest available LLM (Gemini Flash) for extraction. One API call per day. Total cost: ~$0.01/day.

4. **Human readable.** Every artifact Engram creates is a Markdown file you can open in Obsidian, VS Code, or `cat`. No binary formats.

5. **Append-only history.** Entity pages are temporal logs, not mutable documents. We never overwrite — we append new observations with dates.

## Components

### Extractor
Takes a daily log file → produces entities, triplets, events via LLM.

Input: `memory/2026-02-17.md` (unstructured markdown)
Output: JSON with entities, triplets, events

### Entity Store
Wiki-style Markdown files in `memory/entities/`.

Structure per entity:
```
# EntityName
**Type:** person|company|project|tool|concept

## Facts
- Permanent attributes

## Timeline
### [[2026-02-17]]
- What happened on this date

## Relations
- [[OtherEntity]] predicate → this
```

### Graph Store
JSONL file at `memory/graph.jsonl`.

Each line: `{"subject": "A", "predicate": "verb", "object": "B", "date": "2026-02-17"}`

### Surprise Scorer
Compares world model (MEMORY.md) against reality (today's log).

Algorithm:
1. Inject MEMORY.md as context
2. Prompt: "Predict what happened today"
3. Compare prediction to actual events
4. Score each actual event by how well the model predicted it
5. High delta = high surprise = important

### Consolidator
Reads surprise scores → updates MEMORY.md with high-surprise items.

Threshold: Only items with surprise > 0.5 get consolidated.

### Decay Engine (planned)
Tracks last-referenced date per entity.
After N days without reference → archive to `memory/entities/archive/`.
Referenced again → restore from archive.

## Data Flow

```
Input (daily markdown log)
    │
    ▼
[Extractor] ──────────────────┐
    │                          │
    ├──▶ Entity Store          │
    │    (wiki pages)          │
    │                          │
    ├──▶ Graph Store           │
    │    (triplets)            │
    │                          │
    └──▶ Events                │
         (for surprise)        │
                               ▼
                    [Surprise Scorer]
                         │
                         ▼
                    [Consolidator]
                         │
                         ▼
                    MEMORY.md (long-term)
```

## Multi-Agent

Multiple agents can share one Engram instance:
- Symlink `memory/entities/` into each agent's workspace
- Each agent runs extraction on their own daily log
- All writes go to the same entity pages
- Deduplication prevents double-entries

Alternative: Each agent has its own Engram instance, with periodic sync.
