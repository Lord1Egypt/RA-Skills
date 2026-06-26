---
name: miremo
description: Access the user's personal Miremo knowledge base — search notes, look up what they know about a topic, browse their documents and tags, explore their knowledge graph, or save new information. Use when the user says "find my notes", "what do I know about", "search my knowledge base", "look it up in Miremo", "save/record/remember this", "what topics have I written about", or "show my notes on X". NOT for general web searches or queries about topics not stored in the user's own notes.
homepage: https://www.miremoapp.com
metadata:
  { "openclaw": { "emoji": "📓", "requires": { "config": ["mcp.servers"] } } }
---

# Miremo Skill

**Prerequisite:** The Miremo MCP server must be connected in OpenClaw before this skill's tools are available. See the README for setup instructions.

Miremo is an AI note-taking tool. It stores the user's memos, documents, supertags (topic tags with rich content), and AI-extracted knowledge graph entities. All tools only access the currently authenticated user's own data.

Workspace behavior:

- If `workspace_id` is provided, tools operate in that workspace (with permission checks).
- If `workspace_id` is omitted, tools operate only in the user's default workspace.
- Use `list_workspaces` and `get_current_workspace` to inspect available workspaces and the active workspace resolution.

---

## Research Strategy

When the user asks about their knowledge, choose one of three research modes and follow it through completely before giving a final answer. **Never give up after one failed search.**

### Mode A — Browse (user wants an overview)

Triggers: "what notes do I have", "show me my recent notes", "what have I been writing about", "give me an overview"

Steps:

1. `list_workspaces()` to understand all accessible workspaces
2. `get_current_workspace()` to confirm default workspace before browsing
3. `list_memos(page_size=30)` to sample recent memos
4. `list_supertags()` to see all topic tags at a glance
5. Synthesize a structured overview from both results

### Mode B — Topic Research (most common)

Triggers: "what do I know about X", "find notes about X", "anything related to X", "my thoughts on X"

Steps:

1. `list_workspaces()` when user asks for cross-workspace research
2. `global_search(query="X")` — cross-type overview (memos + docs + supertags)
3. `search_memos(query="X", search_type="semantic")` for deeper semantic matches
4. If a relevant supertag appears: `list_supertags(q="X")` to expand via that tag
5. For people, concepts, or events that matter: `list_entities()` → `get_entity_graph(entity_id)` to explore relationships

**Iteration rules (critical):**

- If initial search returns few results, retry with synonyms, English equivalents, or split keywords before concluding "nothing found"
- Lower `similarity_threshold` to 0.25–0.35 on the second attempt
- `hit_text` is only a snippet — do not draw conclusions from it alone; use `global_search` to confirm scope across types
- Declare "no relevant notes found" only after at least 2–3 distinct search strategies all return empty

### Mode C — Exact Lookup

Triggers: "do I have a note about X", "find the exact note where I wrote Y", "the note titled Z"

Steps:

1. `search_memos(query="Y", search_type="full_text")` for precise phrase matching
2. If not found, fall back to Mode B with semantic search

---

## Available Tools

### Search Tools

**`search_memos`** — Search memos by keyword or natural language.

- `query`: search text, e.g. "Python async programming notes"
- `limit`: max results (default 10, recommend ≤ 20)
- `search_type`: `"hybrid"` (default, most comprehensive) | `"semantic"` (natural language) | `"full_text"` (exact match)
- `workspace_id` (optional): target a specific workspace; omit to use default workspace
- Returns: `id`, `hit_text`, `similarity_score`, `created_at`, `modified_at`

**`global_search`** — Cross-type search across memos, documents, and supertags.

- `query`: search text
- `limit`: max results per type (default 10)
- `include_memos` / `include_documents` / `include_supertags`: toggle each type (all true by default)
- `workspace_id` (optional): target a specific workspace; omit to use default workspace
- Returns items with `type` (`"memo"` / `"document"` / `"supertag"`), `id`, `title`, `description`, `score`

### List Tools

**`list_memos`** — Paginated list of memos.

- `page_index`, `page_size` (default 20), `q` (optional fuzzy filter)
- `workspace_id` (optional): target a specific workspace; omit to use default workspace
- Returns: `{ items: [{id, outline_preview, created_at, ...}], total, page_size, page_index }`

**`list_supertags`** — List topic supertags.

- `q` (optional filter), `page_index`, `page_size` (default 50)
- `workspace_id` (optional): target a specific workspace; omit to use default workspace
- Default page size of 50 usually retrieves all tags in one call

**`list_documents`** — List uploaded documents (PDFs, files).

- `q` (optional name filter), `page_index`, `page_size` (default 20)
- `workspace_id` (optional): target a specific workspace; omit to use default workspace
- Returns: `document_id`, `name`, `created_at`, `modified_at`, `status`

### Create Tools

**`create_memo`** — Create a new memo.

- `content`: memo body, multi-line supported. First line becomes the top-level title; subsequent lines become sub-content.
- `workspace_id` (optional): target a specific workspace for writing; omit to write into default workspace
- Returns: `{ memo_id: "<new UUID>" }`
- After creation, vectorization and knowledge graph updates run automatically in the background.

### Workspace Tools

**`list_workspaces`** — List all workspaces accessible to the current user.

- Returns workspace metadata including `workspace_id`, `name`, `role`, `is_default`

**`get_current_workspace`** — Get the effective workspace for current tool call context.

- `workspace_id` (optional): if provided, validates and resolves explicit workspace
- Without parameter, resolves to default workspace
- Returns `source` (`explicit` or `default`) and current workspace metadata

### Knowledge Graph Tools

**`list_entities`** — List AI-extracted knowledge graph entities.

- `entity_type` (optional): `person`, `concept`, `place`, `organization`, `event`, etc.
- `page_index`, `page_size` (default 20)
- Omit `entity_type` to get all types mixed

**`get_entity_graph`** — Get an entity's 1-hop relationship graph.

- `entity_id`: obtain via `list_entities` first
- Returns: `{ entity: {entity_id, name, entity_type, summary}, related_entities: [...], relationships: [{source_entity_id, target_entity_id, description}] }`

---

## When to Use Which Tool

| User intent                         | Recommended tool                                      |
| ----------------------------------- | ----------------------------------------------------- |
| "Find notes about X"                | `global_search` first, then `search_memos` for detail |
| "Find notes with exact phrase"      | `search_memos` with `search_type="full_text"`         |
| "What do I know about X" (semantic) | `search_memos` with `search_type="semantic"`          |
| "Show me recent memos"              | `list_memos`                                          |
| "What topics do I write about"      | `list_supertags`                                      |
| "Find a document / PDF"             | `list_documents` with `q` filter                      |
| "Save / record / note down X"       | `create_memo`                                         |
| "Explore my knowledge graph"        | `list_entities` → `get_entity_graph`                  |
| "Which workspace should I use"      | `list_workspaces` → `get_current_workspace`           |

---

## Recommended Workflows

### Answer "What do I know about X":

1. `get_current_workspace()` to confirm workspace scope
2. `global_search(query="X")` for a cross-type overview
3. If more detail needed: `search_memos(query="X", search_type="semantic")`
4. If a relevant supertag exists: `list_supertags(q="X")` to expand further

### Help user record new information:

1. Confirm intent, then call `create_memo(content="...")`
2. Tell the user the note was created and show the `memo_id`
3. Structure content well: first line = core topic, subsequent lines = details

### Explore user's knowledge structure:

1. `list_supertags()` for a thematic overview
2. `list_entities()` to understand main knowledge graph nodes
3. `get_entity_graph(entity_id)` for entities of interest
