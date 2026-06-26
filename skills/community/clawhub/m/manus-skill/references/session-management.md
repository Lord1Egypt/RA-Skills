# Session Management — Full Design

This document covers everything about how sessions are tracked, resolved, archived, and resumed when interacting with the Manus API.

## Table of Contents

1. [Why Session Tracking Matters](#why-session-tracking-matters)
2. [Registry File Format](#registry-file-format)
3. [Session Lifecycle](#session-lifecycle)
4. [Session Resolution Algorithm](#session-resolution-algorithm)
5. [Archival Rules](#archival-rules)
6. [Naming Conventions](#naming-conventions)
7. [Search & Matching](#search--matching)
8. [Multi-Agent Considerations](#multi-agent-considerations)
9. [Edge Cases & Recovery](#edge-cases--recovery)

---

## Why Session Tracking Matters

The Manus API is stateless from the caller's perspective. Every `POST /v1/tasks` creates a new task unless you explicitly pass `"taskId"` referencing an existing one. This means:

- Forgetting to pass `taskId` = new task = lost context + wasted credits (~150 credits each)
- An agent that re-runs a script from scratch will create duplicates every invocation
- After 50+ sessions, the user says "go back to that auth thing" — without a registry, you have no way to resolve this

The session registry solves all three problems by maintaining a local index of every Manus session with enough metadata to find, resume, or archive them.

---

## Registry File Format

File: `.manus_sessions.json` in the project root.

```json
{
  "active": {
    "security-audit": {
      "task_id": "TeBim6FDQf9peS52xHtAyh",
      "task_title": "Security Audit - Auth Module",
      "task_url": "https://manus.im/app/TeBim6FDQf9peS52xHtAyh",
      "description": "Reviewing authentication code for vulnerabilities in the auth module",
      "tags": ["security", "auth", "code-review", "vulnerabilities"],
      "project_id": "proj_abc123",
      "project_name": "Code Reviews",
      "agent_profile": "manus-1.6",
      "task_mode": "agent",
      "created_at": 1711900000,
      "last_used": 1711950000,
      "last_status": "running",
      "turn_count": 3,
      "first_prompt": "Review the auth module for security vulnerabilities",
      "last_prompt": "Now check the token refresh logic"
    }
  },
  "archived": {
    "q2-report": {
      "task_id": "XkLm9pQrStUvWxYz1234",
      "task_title": "Q2 Revenue Analysis",
      "task_url": "https://manus.im/app/XkLm9pQrStUvWxYz1234",
      "description": "Analyzed Q2 revenue trends with regional breakdown",
      "tags": ["revenue", "q2", "analysis", "finance"],
      "project_id": null,
      "project_name": null,
      "agent_profile": "manus-1.6",
      "task_mode": "agent",
      "created_at": 1711800000,
      "last_used": 1711850000,
      "last_status": "completed",
      "turn_count": 5,
      "first_prompt": "Analyze Q2 revenue trends and create a summary",
      "last_prompt": "Add the regional breakdown chart",
      "archived_at": 1711860000,
      "archived_reason": "completed"
    }
  }
}
```

### Field Descriptions

**Required fields** (set on session creation):
- `task_id` — The Manus task ID returned by `POST /v1/tasks`. The only value needed for multi-turn.
- `task_title` — Returned by Manus. May be auto-generated from the prompt.
- `task_url` — Direct link to the task in the Manus webapp.
- `first_prompt` — Verbatim first prompt sent. Used for matching user intent later.
- `created_at` — Unix timestamp when the session was created.
- `last_used` — Unix timestamp, updated on every interaction.
- `last_status` — Last known task status: `running`, `pending`, `completed`, `failed`.
- `turn_count` — Incremented on every `send()`.

**Recommended fields** (improve searchability):
- `description` — Agent-generated summary of the session's purpose. Be specific: "Reviewing auth module for XSS and CSRF vulnerabilities" beats "Security review."
- `tags` — Keywords from prompt and context. Include domain, action type, specific entities. Auto-generate if the user doesn't provide them.
- `agent_profile` — Model used (`manus-1.6`, `manus-1.6-lite`, `manus-1.6-max`).
- `task_mode` — `chat`, `adaptive`, or `agent`.

**Optional fields**:
- `project_id` / `project_name` — If the session belongs to a Manus project.
- `last_prompt` — Updated on every turn. Helps with context recall.
- `archived_at` / `archived_reason` — Set when moving to archived.

---

## Session Lifecycle

```
User request arrives
        |
        v
[Search registry for matching session]
        |
   +-----------+-----------+
   |           |           |
 1 match    0 matches   >1 match
   |           |           |
   v           v           v
 Use it    Search       Present list,
           archived     ask user to pick
              |
         +---------+----------+
         |         |          |
       1 match  0 matches  >1 match
         |         |          |
         v         v          v
  Ask: resume   Create     Present list,
  or fresh?     new task   ask user to pick
        |           |
        v           v
[Send to Manus API with/without taskId]
        |
        v
[Save/update registry entry]
        |
        v
[Poll for status if needed]
        |
        v
[If completed/failed -> auto-archive]
```

### Creating a Session

1. Generate a descriptive session name slug: `security-audit`, `pr-142-review`, `q2-revenue`. Auto-generate from prompt if user doesn't provide one.
2. Call `POST /v1/tasks` WITHOUT `taskId`.
3. Immediately save the returned `task_id` plus all metadata to `active`.
4. Generate `description` and `tags` from the prompt content.

### Continuing a Session

1. Look up the session in the registry.
2. Call `POST /v1/tasks` WITH `"taskId": "<stored_task_id>"`.
3. Update `last_used`, `last_prompt`, `turn_count`, and `last_status`.

### Archiving a Session

When a task reaches `completed` or `failed`:
1. Move the entry from `active` to `archived`.
2. Set `archived_at` to current timestamp.
3. Set `archived_reason` to the status.
4. The entry remains fully searchable.

### Resuming an Archived Session

1. Move the entry from `archived` back to `active`.
2. Remove `archived_at` and `archived_reason`.
3. Continue as normal with `taskId`.

---

## Session Resolution Algorithm

### Step 1: Extract Search Terms

From the user's message, extract:
- Explicit session names: "go back to security-audit"
- Topic keywords: "the auth review", "that revenue analysis"
- Project references: "the code review project"
- Time references: "the one from yesterday", "my most recent task"
- Task IDs: "task TeBim6FDQf9peS52xHtAyh"

### Step 2: Search Active Sessions

Search across these fields (in priority order):
1. **Exact name match** — `session_name == search_term` → immediate hit
2. **Task ID match** — `task_id == search_term` → immediate hit
3. **Tag match** — any tag contains the search term
4. **Description match** — description contains the search term
5. **Prompt match** — `first_prompt` or `last_prompt` contains the search term
6. **Title match** — `task_title` contains the search term
7. **Project match** — `project_name` contains the search term

### Step 3: Rank Results

When multiple sessions match, rank by:
1. Exact name match first (score: 100)
2. Partial name match (score: 50)
3. Tag hits (score: 20 per matching tag)
4. Description match (score: 15)
5. Prompt match (score: 10 per field)
6. Recency bonus (up to 10, decays over 7 days)

### Step 4: Present or Use

- **1 match**: Use it directly.
- **0 matches in active**: Search archived with same algorithm. If found, ask "This session is archived. Resume it or start a new one?"
- **>1 match**: Present top 3-5 to user:

```
I found multiple matching sessions:

1. [active] security-audit — "Reviewing auth module for vulnerabilities" (3 turns, 2h ago)
2. [active] api-auth-fix — "Fixing OAuth token refresh bug" (1 turn, yesterday)
3. [archived] auth-refactor — "Refactoring auth middleware" (completed 5 days ago)

Which one do you want to continue?
```

---

## Archival Rules

### Auto-Archive Triggers

A session moves to `archived` when:
- **Polling detects `completed`** — after `poll_until_done()` finishes.
- **Polling detects `failed`** — after `poll_until_done()` finishes.
- **Manual status check** — `get_task()` returns completed/failed.

A session stays `active` when:
- Status is `running` — task still in progress.
- Status is `pending` — task waiting for user input (keep active so user sees it).

### Manual Operations

- **Unarchive**: Move from `archived` to `active` for resuming.
- **Delete from registry**: Remove entry entirely (Manus task still exists unless also deleted via API).
- **Bulk cleanup**: Remove archived sessions older than N days.

---

## Naming Conventions

Good session names:
- `security-audit-auth` — specific component
- `pr-142-review` — tied to specific PR
- `q2-revenue-analysis` — clear scope
- `deploy-checklist-v2` — versioned

Bad session names:
- `task1`, `test`, `temp` — meaningless
- `my-task` — not descriptive
- `analysis` — too vague with 10 analyses

When auto-generating from prompts, extract key action + subject:
- "Review the auth module for security" → `security-review-auth`
- "Analyze Q2 revenue by region" → `q2-revenue-by-region`

---

## Search & Matching

The search is case-insensitive, supports partial matches, and scores across multiple fields:

```python
def search(query):
    query_lower = query.lower().strip()
    query_terms = query_lower.split()
    results = []

    for section in ("active", "archived"):
        for name, entry in registry[section].items():
            score = 0

            # Exact name match = highest
            if query_lower == name.lower():
                score += 100
            elif query_lower in name.lower():
                score += 50

            # Task ID match
            if query_lower == entry.get("task_id", "").lower():
                score += 100

            # Tag matches
            tags = [t.lower() for t in entry.get("tags", [])]
            score += sum(20 for term in query_terms if any(term in t for t in tags))

            # Description match
            if any(term in entry.get("description", "").lower() for term in query_terms):
                score += 15

            # Prompt matches
            for field in ("first_prompt", "last_prompt"):
                if any(term in entry.get(field, "").lower() for term in query_terms):
                    score += 10

            # Recency bonus (decays over 7 days)
            age_days = (time.time() - entry.get("last_used", 0)) / 86400
            score += max(0, 10 - age_days)

            if score > 0:
                results.append({"name": name, "section": section, "score": score, **entry})

    return sorted(results, key=lambda x: x["score"], reverse=True)
```

---

## Multi-Agent Considerations

- **Atomic writes**: The script writes to a temp file then renames, preventing partial-write corruption.
- **Concurrent access**: Single-user workflows are fine. For multiple agents sharing a registry, consider a `.manus_sessions.lock` file.
- **Name collisions**: If two agents create the same session name, the second write wins. Use agent-prefixed names if needed (`agent1/security-audit`).

---

## Edge Cases & Recovery

### Registry file missing or corrupted
The script creates a fresh `{"active": {}, "archived": {}}`. Existing tasks still live on the Manus server — recover by listing via `GET /v1/tasks` and using `import-task`.

### Task deleted on server but still in registry
When continuing returns 404, the script removes the session from the registry and reports the task no longer exists.

### Session name collision
If creating a session with a name that already exists:
- In active: ask "Session 'X' exists (N turns, last used Y ago). Continue it, or create new with different name?"
- In archived: ask "Archived session 'X' exists (completed N days ago). Resume it, or create new?"

### Orphaned tasks
Tasks created outside the tracker (Manus webapp, raw API) won't appear in the registry. Import them:
```bash
python scripts/manus_session.py import-task <task_id> --name "imported-task"
```

### Credits audit
```bash
python scripts/manus_session.py sessions --all
```
Shows credit usage per session (fetched from API on demand via `status` command).
