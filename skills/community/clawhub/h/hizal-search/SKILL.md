---
name: hizal-search
description: Retrieve existing context before building anything. Self-triggering — fires whenever the agent is about to search the codebase, recall prior decisions, look for conventions, check memory, investigate patterns, or gather background knowledge before starting work. Covers all Hizal search and read tools (semantic search, query_key lookup, scope filtering, compaction, version history). Triggers on phrases like "let me check", "I need to find", "what do we know about", "search for", "look into", "have we done this before", "check existing", "find related", "recall", or any moment the agent would otherwise start Googling or grep-ing without first consulting Hizal.
---

# Hizal Search

Search before you build. Don't rediscover what the team already decided.

## Semantic Search

Start with 2-3 broad searches using different phrasings:

```
hizal__search_context(query="<key concept from the task>")
hizal__search_context(query="<ticket id or feature name>")
hizal__search_context(query="<related subsystem or endpoint>")
```

### Narrow by Scope

```
# Project-specific knowledge and conventions
hizal__search_context(query="<concept>", scope="PROJECT", project_id="<id>")

# Prior agent memory / investigation notes
hizal__search_context(query="<concept>", scope="AGENT", chunk_type="MEMORY")

# Org-wide principles and standards
hizal__search_context(query="<concept>", scope="ORG")
```

### Filter by Chunk Type

```
hizal__search_context(query="<concept>", chunk_type="KNOWLEDGE")
hizal__search_context(query="<concept>", chunk_type="CONVENTION")
hizal__search_context(query="<concept>", chunk_type="MEMORY")
```

## Exact Lookup by query_key

When you know the exact key:

```
hizal__read_context(query_key="<exact-query-key>", project_id="<id>")
```

## Read a Specific Chunk

```
hizal__read_context(id="<chunk-uuid>")
```

## Synthesize Related Context

Pull related chunks for synthesis (read-only, never delete source chunks):

```
hizal__compact_context(query="<concept>")
hizal__compact_context(query="<concept>", scope="PROJECT", project_id="<id>")
```

## Version History

Inspect how a chunk evolved:

```
hizal__get_context_versions(id="<chunk-uuid>")
```

## Search Strategy

1. **Broad first** — 2-3 searches with different phrasings
2. **Read the results** — chunks contain architecture decisions, conventions, and prior work
3. **Narrow by scope** if broad search returns too much noise
4. **Use query_key** if you already know the key
5. **If an AGENT memory chunk is broadly useful** — promote it with `write_knowledge` or `write_convention`

See `hizal-write` skill for writing back to Hizal.
