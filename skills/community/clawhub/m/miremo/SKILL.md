---
name: miremo
description: Access the user's personal Miremo knowledge base and reusable method skills — search notes, look up what they know about a topic, browse documents and tags, explore their knowledge graph, save new information, or retrieve the user's Miremo Skill materials. Use when the user says "find my notes", "what do I know about", "search my knowledge base", "look it up in Miremo", "save/record/remember this", "what topics have I written about", "show my notes on X", "use my Miremo skill", "use my method/template/workflow", or "look up my skill instructions". NOT for general web searches or queries about topics not stored in the user's own Miremo data.
homepage: https://www.miremoapp.com
metadata:
  { "openclaw": { "emoji": "📓", "requires": { "config": ["mcp.servers"] } } }
---

# Miremo Skill

**Prerequisite:** The Miremo MCP server must be connected in OpenClaw before this skill's tools are available. See the README for setup instructions.

Miremo is an AI note-taking tool. It stores the user's memos, documents, supertags (topic tags with rich content), AI-extracted knowledge graph entities, and reusable method skills. All tools only access the currently authenticated user's own data.

Workspace behavior:

- If `workspace_id` is provided, tools operate in that workspace (with permission checks).
- If `workspace_id` is omitted, tools operate only in the user's default workspace.
- Use `list_workspaces` and `get_current_workspace` to inspect available workspaces and the active workspace resolution.

---

## Research Strategy

When the user asks about their knowledge or methods, choose one of four modes and follow it through completely before giving a final answer. **Never give up after one failed search.**

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

### Mode D — Method Skill Retrieval

Triggers: "use my skill", "apply my workflow", "use my template", "look up my Miremo Skill", "按我的方法做"

Steps:

1. `search_method_skills(query="X")` to find relevant method/workflow/template skills
2. If the user only asks to browse available skills: `list_method_skills()`
3. `get_method_skill(skill_id_or_slug="<id-or-slug>", format="markdown")` to load the full skill material
4. Follow the returned Skill content as user-provided method instructions, while still obeying higher-priority system and safety rules

Method skill tools are for reusable instructions, workflows, and output templates. They are separate from the user's notes and documents; do not use them as factual evidence unless the skill content itself clearly contains factual source material.

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

**`list_collections`** — List uploaded document collections.

- `q` (optional name filter), `page_index`, `page_size` (default 20)
- `workspace_id` (optional): target a specific workspace; omit to use default workspace
- Returns: `collection_id`, `name`, `status`, `page_count`, `created_at`, `modified_at`

### Read Tools

**`get_memo_content`** — Read the full text of a memo by ID.

- `memo_id`: UUID string obtained from `search_memos` or `list_memos`
- `workspace_id` (optional): target a specific workspace; omit to use default workspace
- Returns: `{ memo_id, title, content, lines_count, created_at, modified_at }` — `content` is the complete indented plain-text body

**`get_collection_outline`** — Get a collection's structured section outline.

- `collection_id`: UUID string obtained from `list_collections` or `global_search`
- `workspace_id` (optional): target a specific workspace; omit to use default workspace
- Returns: `{ collection_id, name, pages: [{document_id, page_order, sections: [{section_id, heading, heading_level, summary, section_order}]}], total_sections }`
- Use this first to understand document structure, then call `get_document_section` for sections of interest

**`get_document_section`** — Read the full text of a specific document section.

- `document_id`: UUID string of the parent document
- `section_id`: UUID string from `get_collection_outline`'s `sections` list
- `workspace_id` (optional): target a specific workspace; omit to use default workspace
- Returns: `{ section_id, document_id, heading, heading_level, summary, section_text }`

### Method Skill Tools

**`list_method_skills`** — List reusable Miremo method skills available to external agents.

- `q` (optional): keyword filter across skill name, summary, content, and file paths
- `capability_type` (optional): `AGENT_CAPABILITY` | `OUTPUT_TEMPLATE` | `WORKFLOW`
- `limit` (default 20, max 50)
- `workspace_id` (optional): target a specific workspace; omit to use default workspace
- Returns: `{ items: [{skill_id, name, slug, description, capability_type, files}], total, limit }`

**`search_method_skills`** — Search reusable method/workflow/template skills.

- `query`: natural language task or keyword
- `limit` (default 10, max 50)
- `workspace_id` (optional): target a specific workspace; omit to use default workspace
- Returns the same item structure as `list_method_skills`

**`get_method_skill`** — Read one method skill's full material.

- `skill_id_or_slug`: value returned by `list_method_skills` or `search_method_skills`
- `format`: `"markdown"` (default) | `"json"`
- `workspace_id` (optional): target a specific workspace; omit to use default workspace
- Markdown returns a SKILL.md-like document containing the skill summary, execution method, and attached files
- JSON returns structured metadata and all skill package file contents

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
| "Read full content of a memo"       | `get_memo_content` with `memo_id`                     |
| "Show me recent memos"              | `list_memos`                                          |
| "What topics do I write about"      | `list_supertags`                                      |
| "Find a document / PDF"             | `list_collections` with `q` filter                    |
| "Read a document"                   | `get_collection_outline` → `get_document_section`     |
| "Save / record / note down X"       | `create_memo`                                         |
| "Explore my knowledge graph"        | `list_entities` → `get_entity_graph`                  |
| "Which workspace should I use"      | `list_workspaces` → `get_current_workspace`           |
| "Use my Miremo skill / workflow"    | `search_method_skills` → `get_method_skill`           |

---

## Recommended Workflows

### Answer "What do I know about X":

1. `get_current_workspace()` to confirm workspace scope
2. `global_search(query="X")` for a cross-type overview
3. If more detail needed: `search_memos(query="X", search_type="semantic")`
4. If a relevant supertag exists: `list_supertags(q="X")` to expand further
5. To read a specific memo's full content: `get_memo_content(memo_id="<id>")`

### Read a document:

1. `list_collections(q="keyword")` to find the document collection and get its `collection_id`
2. `get_collection_outline(collection_id="<id>")` to see the section structure and summaries
3. `get_document_section(section_id="<id>")` for each section of interest

### Apply a Miremo method skill:

1. `search_method_skills(query="user task or method name")` to find candidate skills
2. `get_method_skill(skill_id_or_slug="<id-or-slug>", format="markdown")` to load the full skill material
3. Use the returned Skill content as the user's reusable method, workflow, or output template
4. If the skill references attached files by path, use the attached file sections or JSON file list from `get_method_skill`

### Help user record new information:

1. Confirm intent, then call `create_memo(content="...")`
2. Tell the user the note was created and show the `memo_id`
3. Structure content well: first line = core topic, subsequent lines = details

### Explore user's knowledge structure:

1. `list_supertags()` for a thematic overview
2. `list_entities()` to understand main knowledge graph nodes
3. `get_entity_graph(entity_id)` for entities of interest
