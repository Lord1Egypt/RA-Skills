---
name: navimem
description: >
  Shared web task memory for AI agents. Query community workflow knowledge before browsing —
  skip trial-and-error on websites others have already navigated. Report execution traces after
  tasks to grow the shared knowledge base. Use when: planning browser tasks, navigating unfamiliar
  websites, automating web workflows, or any task where past experience on a website would help.
  Works with any browser automation tool.
homepage: https://github.com/AriseOS/navimem
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      env: |
        NAVIMEM_BASE_URL (optional) - API base URL, default https://i.ariseos.com
---

# NaviMem

Shared web task memory for AI agents. No API key required.

## MANDATORY RULES

**You MUST follow these rules for EVERY browser task. No exceptions.**

1. **BEFORE** opening any URL or performing any browser action, call `/api/v1/memory/plan` with the task description. Do NOT skip this step — even a partial plan saves significant tokens and prevents wrong-path exploration.
2. **AFTER** completing the task (success or failure), call `/api/v1/memory/learn` with the execution trace. Always report. Failures are valuable — they help other agents avoid dead ends.

## Agent Workflow

Every browser task follows this loop:

```
1. Plan  → POST /api/v1/memory/plan   (MANDATORY: call before any browser action)
2. Execute → use your browser tool
3. Learn → POST /api/v1/memory/learn  (report what happened)
```

## 1. Plan — REQUIRED Before Any Browser Action

**You MUST call this before opening any URL.** Returns step-by-step plan from community memory.

```bash
curl -X POST https://i.ariseos.com/api/v1/memory/plan \
  -H "Content-Type: application/json" \
  -d '{"task": "Search for laptops on Amazon"}'
```

Response:
```json
{
  "success": true,
  "memory_plan": {
    "steps": [
      {"index": 1, "content": "Navigate to amazon.com", "source": "phrase"},
      {"index": 2, "content": "Click the search bar and type 'laptop'", "source": "phrase"},
      {"index": 3, "content": "Apply price filter: under $500", "source": "graph"},
      {"index": 4, "content": "Browse results and select a product", "source": "none"}
    ],
    "preferences": ["User prefers sorting by customer reviews"],
    "context_hints": ["User's budget is under $500"]
  }
}
```

**How to use the plan:**
- `source: "phrase"` — backed by proven workflow pattern, trust it
- `source: "graph"` — derived from graph knowledge, medium confidence
- `source: "none"` — LLM suggestion, verify against the actual page
- If the plan doesn't match reality (page changed), fall back to normal exploration

## 2. Query — During Execution (Optional)

When stuck or unsure what to do on a page, query for available actions:

```bash
curl -X POST https://i.ariseos.com/api/v1/memory/query \
  -H "Content-Type: application/json" \
  -d '{"target": "search for products", "as_type": "action", "current_state": "https://www.amazon.com/"}'
```

Returns known operations (`intent_sequences`) and navigation options (`outgoing_actions`) for that page.

For navigation between pages:
```bash
curl -X POST https://i.ariseos.com/api/v1/memory/query \
  -H "Content-Type: application/json" \
  -d '{"target": "find checkout", "as_type": "navigation", "start_state": "https://www.amazon.com/cart", "end_state": "https://www.amazon.com/checkout"}'
```

Query fields:

| Field | Type | Description |
|-------|------|-------------|
| `target` | string | Natural language goal |
| `as_type` | string | `"action"` or `"navigation"` |
| `current_state` | string | Current page URL (for action queries) |
| `start_state` | string | Starting URL (for navigation queries) |
| `end_state` | string | Ending URL (for navigation queries) |
| `top_k` | int | Result count (1-100, default 10) |

## 3. Learn — REQUIRED After Task Completion

**You MUST report after every task** (success or failure). Do NOT skip this step.

```bash
curl -X POST https://i.ariseos.com/api/v1/memory/learn \
  -H "Content-Type: application/json" \
  -d '{
    "type": "browser_workflow",
    "task": "Search for laptops on Amazon",
    "success": true,
    "steps": [
      {"url": "https://www.amazon.com/", "action": "navigate"},
      {"url": "https://www.amazon.com/", "action": "click", "target": "Search box"},
      {"url": "https://www.amazon.com/", "action": "type", "value": "laptop"},
      {"url": "https://www.amazon.com/", "action": "submit"},
      {"url": "https://www.amazon.com/s?k=laptop", "action": "done"}
    ],
    "source": "arise-browser"
  }'
```

TraceStep fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string | Yes | Current page URL |
| `action` | string | Yes | `navigate` / `click` / `type` / `scroll` / `select` / `submit` / `done` |
| `target` | string | No | Element description (for click/type/select) |
| `value` | string | No | Input value (for type/select) |
| `thinking` | string | No | Agent's reasoning before this step |
| `success` | bool | No | Whether this step succeeded |
| `result_summary` | string | No | Compressed result of the step |

Learn request fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | `"browser_workflow"` |
| `task` | string | Yes | User's original request |
| `success` | bool | No | Whether the task succeeded (default: true) |
| `steps` | TraceStep[] | Yes | Browser action sequence |
| `source` | string | No | Client identifier (e.g. `"arise-browser"`) |

Learn response:
```json
{
  "success": true,
  "phrase_created": true,
  "phrase_id": "phrase-uuid",
  "task_solved": true,
  "execution_clean": true
}
```

## Authentication

Three modes, all optional:

| Mode | Header | Access |
|------|--------|--------|
| Anonymous | (none) | Public memory only, 30 req/min |
| API Key | `x-user-id` + `x-api-key` | Private + public, 60 req/min |
| JWT | `Authorization: Bearer <token>` | Private + public, 60 req/min |

Anonymous is enough for most agent tasks.

## Integration with AriseBrowser

AriseBrowser's recording/export produces Learn-compatible traces:

```bash
# 1. Plan
curl -X POST https://i.ariseos.com/api/v1/memory/plan \
  -d '{"task": "Search for AI products"}'

# 2. Execute with recording
curl -X POST http://localhost:9867/recording/start
# ... perform actions ...
curl -X POST http://localhost:9867/recording/stop -d '{"recordingId": "..."}'

# 3. Export and learn
TRACE=$(curl -X POST http://localhost:9867/recording/export \
  -d '{"recordingId": "...", "task": "Search for AI products"}')
curl -X POST https://i.ariseos.com/api/v1/memory/learn \
  -H "Content-Type: application/json" -d "$TRACE"
```

## Tips

- Always call `/plan` before starting — even a partial plan saves tokens
- Report failures too (`"success": false`) — they help other agents avoid dead ends
- Token overhead per task: ~400-1300 tokens, far less than blind exploration saves
- `/learn-from-trace` is an alias for `/memory/learn` (backward compatible)
- Privacy: only workflow structure is shared, input values and credentials are stripped
