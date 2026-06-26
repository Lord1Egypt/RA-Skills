---
name: memory-mcp-cyber-bye
description: Graph-based memory MCP server with 9 consolidated tools, 8-phase auto-linking, persona tracking, emotional memory, adaptive learning, and knowledge graph entities.
version: 1.0.7
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins:
        - node
      mcp:
        - memory__memory
        - memory__entity
        - memory__relation
        - memory__short_term
        - memory__project
        - memory__context
        - memory__extract
        - memory__share
        - memory__memory_tool_search
---

# Memory MCP — Graph-Based Memory & Persona Management

> [!IMPORTANT]
> **Dependency Warning:**
> This skill requires the `memory` MCP server to be running and registered with the Model Context Protocol (MCP) host. It enables persistent memory, knowledge graph entities, context tracking, and cross-session intelligence.

This skill equips the agent to store, search, and manage memories across sessions; track entities and relationships in a knowledge graph; maintain user persona, mood, and learning patterns; and surface proactive suggestions based on memory health.

---

## Guidelines for the Agent

### 1. Tool Architecture — 9 Consolidated Tools

The memory MCP exposes **9 tools**, each with an `op` (operation) parameter:

| Tool | Prefix | Purpose | Operations |
|------|--------|---------|------------|
| `memory__memory` | `memory_` | Core memory store & search | remember, recall, search, context, stats, health, decay, boost, pin, inspect, export, import, trim, suggest, remind, dedup, backup, restore, snippet_search, contact, contact_graph |
| `memory__entity` | `entity_` | Knowledge graph entities | create, read, update, delete, search |
| `memory__relation` | `relation_` | Entity relationships | create, delete, search |
| `memory__short_term` | `short_term_` | Fast KV storage | set, get, list, delete, clear, search |
| `memory__project` | `project_` | Projects, tasks, workflows | create_project, get_project, list_projects, update_project, delete_project, plan_task, get_task, list_tasks, update_task, complete_task, delete_task, plan_workflow, get_workflow, list_workflows |
| `memory__context` | `context_` | Conversation context | better, chat_add, chat_get, chat_summary, get_summary |
| `memory__extract` | `extract_` | Extract/remember info | entities, text, keypoint, thought, note, discovery, mistake, learning, boundary |
| `memory__share` | `share_` | Share with others | share, shared_with_me, shared_by_me, get_network, person_memories |
| `memory__memory_tool_search` | — | Find tools by keyword | query |

---

### 2. Common Parameters

Every tool call requires:
- **`userId`** (required) — Who owns this data. Always pass the user identifier.
- **`op`** (required) — Which operation to perform on the tool.

Each tool also accepts optional context parameters:
- **`projectId`** — Scope to a project
- **`sessionId`** — Conversation thread identifier

---

### 3. Core Memory Operations (memory__memory)

#### Store a Memory
```json
{ "op": "remember", "userId": "u1", "userMessage": "Fixed @AuthService bug!", "agentMessage": "Great work!" }
```
Auto-features: intent detection, entity extraction (@mentions, CamelCase, URLs), auto-linking.

#### Search / Recall
```json
{ "op": "recall", "userId": "u1", "query": "auth bug" }
{ "op": "search", "userId": "u1", "query": "database config" }
```

#### Context for LLM
```json
{ "op": "context", "userId": "u1", "sessionId": "sess_123", "maxTokens": 2000 }
```

#### Memory Health & Maintenance
```json
{ "op": "health", "userId": "u1" }
{ "op": "decay", "userId": "u1", "daysUnused": 7 }
{ "op": "dedup", "userId": "u1", "threshold": 0.8, "autoMerge": false }
```

#### Smart Features
```json
{ "op": "suggest", "userId": "u1" }
{ "op": "remind", "userId": "u1", "reminderType": "followup", "title": "Check database", "priority": 8 }
{ "op": "mood", "userId": "u1", "mood": "excited", "intensity": 8, "context": "Launch day!" }
{ "op": "persona", "userId": "u1", "traits": {"creative": true}, "style": "friendly" }
{ "op": "learn", "userId": "u1", "type": "work", "pattern": "prefers morning" }
```

#### Snippet Search (Exact & Semantic with context)
```json
{
  "op": "snippet_search",
  "userId": "u1",
  "text": "Line 1: system boot\nLine 2: loading config...",
  "query": "system boot",
  "searchType": "exact",
  "beforeLimit": 1,
  "afterLimit": 1
}
```
*Supports exact/semantic matches, parameter clamping, whitespace collapsing, and SQL wildcard escaping in database fallback.*

#### Unified Contact CRUD
```json
{ "op": "contact", "contactOp": "create", "userId": "u1", "name": "vk", "role": "founder", "properties": {"status": "active"} }
{ "op": "contact", "contactOp": "get", "userId": "u1", "name": "VK" }
```
*Standardizes contact management with space-collapsed names, case-insensitive retrievals, and properties sanitization.*

#### Unified Contact Graph & Path Traversal
```json
{ "op": "contact_graph", "graphOp": "link", "userId": "u1", "fromId": "vk", "toId": "nandini", "relationType": "wife" }
{ "op": "contact_graph", "graphOp": "path", "userId": "u1", "fromId": "vk", "toId": "vk", "depth": 3 }
```
*Manages relationships with lowercase-normalized edge types, per-path visited tracking, and loop/cycle discovery.*

---

### 4. Knowledge Graph (entity + relation)

#### Create Entity
```json
{ "op": "create", "userId": "u1", "entityType": "Person", "name": "Alice", "properties": {"role": "Engineer"} }
```

#### Search Entities
```json
{ "op": "search", "userId": "u1", "entityType": "Person", "search": "alice" }
```

#### Create Relation
```json
{ "op": "create", "userId": "u1", "fromId": "e1", "toId": "e2", "type": "WORKS_WITH" }
```

---

### 5. Short-Term KV Storage (memory__short_term)

Fast key-value store for session data. Cleared periodically.

```json
{ "op": "set", "userId": "u1", "key": "active_task", "value": {"id": "t1"} }
{ "op": "get", "userId": "u1", "key": "active_task" }
{ "op": "list", "userId": "u1" }
```

---

### 6. Project & Task Management (memory__project)

```json
{ "op": "create_project", "userId": "u1", "name": "My App", "description": "A new app" }
{ "op": "plan_task", "userId": "u1", "projectId": "p1", "title": "Fix bug", "status": "pending" }
{ "op": "list_tasks", "userId": "u1", "projectId": "p1" }
{ "op": "complete_task", "id": "task_123" }
```

---

### 7. Context Tracking (memory__context)

```json
{ "op": "better", "userId": "u1", "timeRange": "week" }
{ "op": "chat_add", "userId": "u1", "role": "user", "content": "Hello" }
{ "op": "chat_get", "userId": "u1", "limit": 10 }
```

---

### 8. Extract & Remember (memory__extract)

```json
{ "op": "entities", "userId": "u1", "text": "John from Acme called" }
{ "op": "learning", "userId": "u1", "insight": "Tests first" }
{ "op": "discovery", "userId": "u1", "content": "Found new approach" }
{ "op": "mistake", "userId": "u1", "description": "Used wrong API", "resolution": "Update docs" }
```

---

### 9. Share (memory__share)

```json
{ "op": "share", "userId": "u1", "toOwnerId": "u2", "content": "Deadline Sunday" }
{ "op": "shared_with_me", "userId": "u1" }
```

---

### 10. 8-Phase Auto-Linking System

Memories are automatically linked across sessions using:

| Phase | Method | Description |
|-------|--------|-------------|
| 0 | Temporal | Same conversation flow (strongest) |
| 1 | Entity | Shared @mentions, CamelCase entities |
| 2 | Project | Same project context |
| 3 | Intent | Same detected intent |
| 4 | Keyword | Content keyword overlap |
| 5 | Cross-Project | Related across different projects |
| 6 | Temporal Chain | Within 30-minute window |
| 7 | Entity Graph | Knowledge graph traversal |

Features: bidirectional links, max 15 links per memory, adaptive boost for high-priority items.

---

### 11. Intent Detection (Auto)

The system auto-detects intent when storing memories:

| Intent | Priority | Examples |
|--------|----------|---------|
| error | 80% | bug, crash, failed |
| success | 70% | fixed, working, completed |
| learning | 80% | learned, discovered |
| question | 50% | how, why, what |
| planning | 50% | will, going to |

---

### 12. Session Workflow

**At session start:**
```json
// Get recent context
{ "op": "better", "userId": "u1", "timeRange": "week" }

// Check pending reminders
{ "op": "remind", "userId": "u1" }

// Get health overview
{ "op": "health", "userId": "u1" }
```

**During session:**
```json
// Store conversation
{ "op": "remember", "userId": "u1", "userMessage": "...", "agentMessage": "..." }

// Extract entities
{ "op": "entities", "userId": "u1", "text": "..." }

// Track mood
{ "op": "mood", "userId": "u1", "mood": "happy", "context": "..." }
```

**At session end:**
```json
// Store summary
{ "op": "chat_summary", "userId": "u1", "summary": "..." }

// Clean up short-term
{ "op": "cleanup", "userId": "u1" }
```

---

### 13. Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "id required" | Missing ID param | Add `id` field |
| "sessionId required" | Missing sessionId | Add `sessionId` field |
| "mood required" | Missing mood | Add `mood` (happy/sad/excited/etc) |
| "userId required" | Missing userId | Always pass `userId` |

---

### 14. Best Practices

1. **Always pass `userId`** — Every tool call requires it.
2. **Use entity extraction** — Extract entities from user messages to build the knowledge graph.
3. **Track mood** — Call `mood` during emotionally significant moments.
4. **Remember at end** — Store session summaries for cross-session continuity.
5. **Use context before starting** — `better` op gives you full context before you begin.
6. **Health check periodically** — Run `health` + `decay` to keep memory clean.