---
name: memos-cloud-server
description: External long-term memory and knowledge base backed by the MemOS Cloud API. Capabilities — search prior memory, add conversation messages, delete or correct memories via feedback, retrieve a consolidated user profile (facts, preferences, tool history), and manage knowledge bases and their documents. Use proactively on every user turn (search memory before answering and persist the exchange after), and whenever the user references past context, their identity, preferences, or history, or asks to remember, recall, modify, forget, or correct something (e.g., "who am I", "what do I like", "remember that...", "forget X", "you got it wrong"). Also use when uploading, listing, or deleting knowledge base files.
user-invocable: true
metadata: {"openclaw":{"emoji":"☁️","os":["darwin","linux","win32"],"requires":{"bins":["python3"],"env":["MEMOS_API_KEY", "MEMOS_USER_ID"]}}}
---

# MemOS Cloud Server Skill

This skill allows the Agent to interact with MemOS Cloud APIs for memory search, addition, deletion, knowledge base management, and feedback.

## ⚠️ Setup & Safety Rules (MUST READ)

Before executing any API operations, ensure these environment variables are configured. Each variable has an **ownership layer** — who is responsible for setting it — which determines whether it should ever be overridden at call time.

| Variable | Required | Ownership layer | Per-call override? | Notes |
|---|---|---|---|---|
| `MEMOS_API_KEY` | Yes | User / deployment secret | No | Auth token. Never expose to the LLM. |
| `MEMOS_USER_ID` | Yes | User / host platform | No | Must be deterministic (hashed email, employee ID). Do NOT use random or per-session IDs. |
| `MEMOS_CLOUD_URL` | No | Deployment | No | API base URL. Default: `https://memos.memtensor.cn/api/openmem/v1`. |
| `MEMOS_AGENT_ID` | No | Host platform (per-process injection) | **Yes** — via `--agent-id` on `add_message` / `add_feedback` | Isolates memories per agent. A single global env var only supports one agent per machine; for multi-agent on one device, either let the host platform inject this per-process or pass `--agent-id` per call. |
| `MEMOS_APP_ID` | No | Host platform | **Yes** — via `--app-id` on `add_message` / `add_feedback` | Isolates memories per application. Same multi-tenant caveat as `MEMOS_AGENT_ID`. |
| `MEMOS_ALLOW_PUBLIC` | No | Admin / security policy | No | `true`/`false`, default `false`. Security boundary — never let the LLM toggle this per call. |
| `MEMOS_ASYNC_MODE` | No | Deployment | No | `true`/`false`, default `true`. Whether `add_message` returns before processing completes. |

**Multi-agent isolation pattern**: Prefer per-process env injection by the host platform (each agent gets its own process tree with a distinct `MEMOS_AGENT_ID`). When the platform cannot inject env vars, fall back to passing `--agent-id` / `--app-id` on each call — the CLI flag takes precedence over the env var. These values must come from the orchestrator/platform; the LLM must not invent them.

If required variables are missing, prompt the user to configure them (globally or per-process) before retrying.

## ⚠️ Mandatory Workflow (MUST FOLLOW)

### Always-On (No User Opt-In Required)
This system runs **automatically for every turn**. Do NOT wait for the user to say "use memory", "search memory", or "remember this". The agent is responsible for auto-invoking the tools.

### Every Turn: 3-Step Workflow (AUTO-INVOKED)
```
Every user message (including greetings, simple questions, ANYTHING)
  → 1) search_memory (AUTO, BEFORE answering — even for simple questions)
  → 2) Answer (use only relevant memories; ignore noise)
  → 3) add_message (AUTO, AFTER answering — save conversation history)
```

### Identity & Preference Queries (MANDATORY)
When the user asks about themselves, call BOTH `search_memory` AND `get_user_profile`:
- "What do I like?"
- "Who am I?"
- "What do you know about me?"
- "What are my preferences?"
- Any question about the user's identity, habits, or preferences (in any language)

### Tool Choice Rules (STRICT)

| User Intent | Correct Tool | Wrong Tool |
|---|---|---|
| ANY question (auto, before answering) | `search_memory` | - |
| Identity / preference query ("What do I like?") | `search_memory` + `get_user_profile` | - |
| New information / remember something | `add_message` | NOT `add_feedback` |
| Modify / correct existing memory | `add_feedback` | NOT `add_message` |
| Delete memory (no ID specified) | `search` → `delete` → `add_feedback` | NOT `add_message` |
| Delete memory (ID specified) | `delete` directly | - |

### Modification Workflow
When user wants to **modify** a memory:
1. Call `add_feedback` with the correction in natural language
2. Example: `feedback_content = "User prefers dark mode, not light mode"`
3. **FORBIDDEN**: Do NOT call `add_message` to "replace" the old memory

### Deletion Workflow (No ID)
When user wants to **delete** a memory but doesn't have the ID:
1. `search_memory` — find the relevant memory IDs
2. `delete` — delete with the found IDs
3. `add_feedback` — confirm deletion intent (e.g., "User wants to delete memories about X")
4. **CRITICAL**: feedback_content must be **user's natural language intent**, NOT technical details like "IDs [x, y]"

### Deletion Workflow (With ID)
When user provides specific memory IDs:
1. `delete` — directly delete with the IDs

### FORBIDDEN Actions
- Do NOT use `add_message` to modify/update existing memories
- Do NOT use `add_message` as part of "delete old + add new" workaround
- Do NOT include memory IDs or technical metadata in `feedback_content`
- Do NOT retry `add_feedback` if it seems to fail (fire and forget)
- Do NOT pass `--agent-id` / `--app-id` by default. Omit both flags unless one of the following is true: (a) the user explicitly tells you the ID to use in this turn, or (b) the system prompt / orchestrator context explicitly provides the ID. Never invent, guess, or carry over IDs from prior turns. When the flags are omitted, the env var (if set) takes effect transparently.
- Do NOT attempt to override `MEMOS_ALLOW_PUBLIC` at call time — it is a security boundary owned by the deployment.

### When NOT to Invoke (Negative Triggers)
The default policy is "search-before-answer on every turn". Skip invocation only in these narrow cases:
- The user explicitly opts out for the current turn (e.g., "don't search memory", "skip memory", "answer without memory").
- The turn is a pure tool/system action with no semantic content (e.g., the user only pastes a stack trace to fix and asks for no personalization).
- Required env vars (`MEMOS_API_KEY`, `MEMOS_USER_ID`) are missing — prompt the user to configure them first instead of calling the API.
- A previous call in the same turn already returned the needed memories; do not call `search_memory` twice for the same query.

When in doubt, prefer to invoke — false positives are cheap, missed context is expensive.

---

## 🧵 Conversation ID Strategy (MUST FOLLOW)

`conversation_id` groups memories that belong to the **same chat session**. It is used by the server to (a) weight `search_memory` results by in-session context, (b) anchor `add_feedback` so corrections target the right session's memories, and (c) let `add_message` accumulate a coherent turn history.

**Stability rule**: within one chat session every `search` / `add_message` / `add_feedback` call MUST use the **same** `conversation_id`. Across sessions it MUST rotate.

### How to derive it (in priority order)

1. **Host-provided id** — if the orchestrator / platform exposes a session id (env var, CLI arg, framework variable), pass it via `--conversation-id` directly. Most reliable.
2. **First-message derivation** — if no session id is available, pick the **very first user message of the current chat session** and pass that exact same string as `--conversation-first-message` on every subsequent call in this session. The script MD5-hashes `user_id + first_message` deterministically, so the same input always yields the same id (see `payloads.py::generate_conversation_id`).
3. **Never** pass the *current* turn's user message as `--conversation-first-message`. That re-rotates the id every turn and silently breaks feedback + context weighting.

### What "new conversation" means

A new `conversation_id` SHOULD be generated when, and only when:
- The host platform opens a new chat session / clears history, OR
- The user explicitly says "new topic" / "start over" / "let's talk about something else entirely" and you decide to drop the prior context.

A new id MUST NOT be generated just because:
- The user changes subject mid-conversation (still the same session).
- The agent's own context window was truncated (the session is logically the same).
- You forgot the previous id (re-derive it from the same first message — do not invent a new one).

### Operational checklist for the agent

- **Session start**: capture the first user message of the session verbatim, treat it as the session anchor, and keep it in your working notes.
- **Every subsequent call** in this session: reuse that exact anchor string for `--conversation-first-message` (or reuse the resolved `conversation_id` if the host provided one).
- **Feedback / correction**: must use the *same* `conversation_id` (or the same anchor first-message) that was used when the targeted memory was written.
- **New chat detected**: drop the old anchor, capture the new session's first user message, start over.

---

## 🛠 Core Commands

Run operations through `scripts/memos_cloud.py`. The script automatically reads environment variables; all requests and responses use JSON.

---

### 1. Search Memory (`/search/memory`)

Search for long-term memories relevant to the user's query.

```bash
python3 scripts/memos_cloud.py search [user_id] "<query>" [options]
```

Options:
- `--conversation-id <id>` — Conversation ID for context weighting. See [Conversation ID Strategy](#-conversation-id-strategy-must-follow).
- `--conversation-first-message "<msg>"` — Session anchor (the **first user message of the current session**, reused on every call this session). MD5-derives a stable conversation_id. **Do NOT pass the current turn's message** — that rotates the id every turn and breaks context weighting.
- `--filter '<json>'` — Filter conditions as JSON string
- `--knowledgebase-ids "<ids>"` — Comma-separated KB IDs, or `"all"`
- `--memory-limit-number <n>` — Max factual memories (default 9, max 25)
- `--include-preference <bool>` — Enable preference recall (default true)
- `--preference-limit-number <n>` — Max preference memories (default 9, max 25)
- `--include-tool-memory <bool>` — Enable tool memory recall (default false)
- `--tool-memory-limit-number <n>` — Max tool memories (default 6, max 25)
- `--include-skill <bool>` — Enable skill recall (default false)
- `--skill-limit-number <n>` — Max skills (default 6, max 25)
- `--relativity <float>` — Relevance threshold 0-1 (default 0.45)

Example:

```bash
python3 scripts/memos_cloud.py search "$MEMOS_USER_ID" "Python related project experience"
python3 scripts/memos_cloud.py search "$MEMOS_USER_ID" "tools" --include-tool-memory true --include-skill true
```

---

### 2. Add Message (`/add/message`)

Store high-value content from multi-turn conversations.

```bash
python3 scripts/memos_cloud.py add_message [user_id] [conversation_id] '<messages_json>' [options]
```

Options:
- `--conversation-first-message "<msg>"` — Alternative to positional `conversation_id`. Must be the **session anchor** (first user message of the current session), reused on every call this session. See [Conversation ID Strategy](#-conversation-id-strategy-must-follow). Passing a different string each turn will silently fragment the conversation into many single-turn sessions.
- `--tags "<tags>"` — Comma-separated tags
- `--info '<json>'` — Custom metadata as JSON string
- `--allow-knowledgebase-ids "<ids>"` — Comma-separated KB IDs for memory write scope
- `--agent-id "<id>"` — Opt-in override of `MEMOS_AGENT_ID`. **Omit by default**; pass only when the user or orchestrator context explicitly supplies the ID.
- `--app-id "<id>"` — Opt-in override of `MEMOS_APP_ID`. Same rule as `--agent-id`.

Resolution order for `agent_id` / `app_id`: CLI flag (only when explicitly provided) > env var > unset.

Environment-only options (no per-call override):
- `allow_public` from `MEMOS_ALLOW_PUBLIC`
- `async_mode` from `MEMOS_ASYNC_MODE`

Example:

```bash
# Preferred: host-supplied conversation_id, reused for the whole session
python3 scripts/memos_cloud.py add_message "$MEMOS_USER_ID" "$SESSION_ID" '[{"role":"user","content":"I like apples"},{"role":"assistant","content":"Okay, I noted that"}]'

# Fallback: derive a stable id from the session's FIRST user message.
# Reuse the EXACT same --conversation-first-message string on every call this session
# (search / add_message / add_feedback). Do NOT substitute the current turn's message.
ANCHOR="What's the weather?"   # captured once at session start
python3 scripts/memos_cloud.py add_message "$MEMOS_USER_ID" --conversation-first-message "$ANCHOR" '[{"role":"user","content":"What's the weather?"}]'
python3 scripts/memos_cloud.py add_message "$MEMOS_USER_ID" --conversation-first-message "$ANCHOR" '[{"role":"user","content":"And tomorrow?"}]'
```

---

### 3. Delete Memory (`/delete/memory`)

Delete stored memories by comma-separated memory IDs.

```bash
python3 scripts/memos_cloud.py delete "<memory_ids>"
```

Example:

```bash
python3 scripts/memos_cloud.py delete "id1,id2,id3"
```

---

### 4. Add Feedback (`/add/feedback`)

Add feedback to correct or reinforce memory. Used when the user wants to modify or delete memories.

```bash
python3 scripts/memos_cloud.py add_feedback [user_id] [conversation_id] "<feedback_content>" [options]
```

Options:
- `--conversation-first-message "<msg>"` — Alternative to positional `conversation_id`. Must be the **same session anchor** used when the targeted memory was written (otherwise the feedback will not be linked to the right session). See [Conversation ID Strategy](#-conversation-id-strategy-must-follow).
- `--allow-knowledgebase-ids "<ids>"` — Comma-separated KB IDs
- `--feedback-time "<time>"` — Feedback time string
- `--agent-id "<id>"` — Opt-in override of `MEMOS_AGENT_ID`. **Omit by default**; pass only when the user or orchestrator context explicitly supplies the ID.
- `--app-id "<id>"` — Opt-in override of `MEMOS_APP_ID`. Same rule as `--agent-id`.

Resolution order for `agent_id` / `app_id`: CLI flag (only when explicitly provided) > env var > unset.

Environment-only options (no per-call override):
- `allow_public` from `MEMOS_ALLOW_PUBLIC`

Example:

```bash
# Same session anchor as the add_message calls in this session:
python3 scripts/memos_cloud.py add_feedback "$MEMOS_USER_ID" --conversation-first-message "$ANCHOR" "The previous answer was not detailed enough"

# Or with an explicit id from the host:
python3 scripts/memos_cloud.py add_feedback "$MEMOS_USER_ID" "$SESSION_ID" "The previous answer was not detailed enough"
```

---

### 5. Add Knowledge Base Document (`/add/knowledgebase-file`)

Upload files to a knowledge base. Supports online URLs, local files, and stdin input.

```bash
python3 scripts/memos_cloud.py add_kb_doc <knowledgebase_id> <file1> [file2 ...] [--type document|skill]
python3 scripts/memos_cloud.py add_kb_doc <knowledgebase_id> --stdin [--name filename.ext] [--type document|skill]
```

Parameters:
- `knowledgebase_id`: Target knowledge base ID.
- `files`: URLs (`https://example.com/doc.pdf`) or local file paths (mime_type auto-detected, content auto-converted to base64).
- `--stdin`: Read base64 content from stdin. Prefer this for large files to avoid loading their content into the agent context.
- `--name`: Filename for stdin content (recommended whenever `--stdin` is used so the server can infer the mime type).
- `--type`: `document` (default) or `skill`.

---

### 6. Get User Profile (`/get/memory`)

Retrieve the consolidated User Memory Profile — factual memories, preferences, and tool trajectories.

```bash
python3 scripts/memos_cloud.py get_user_profile [user_id] [options]
```

Options:
- `--page <n>` — Page number (default 1)
- `--size <n>` — Page size (default 10, max 50)
- `--filter '<json>'` — Filter conditions as JSON string
- `--include-preference <bool>` — Include preference memories (default true)
- `--include-tool-memory <bool>` — Include tool memories (default false)

Example:

```bash
python3 scripts/memos_cloud.py get_user_profile "$MEMOS_USER_ID"
python3 scripts/memos_cloud.py get_user_profile "$MEMOS_USER_ID" --include-tool-memory true --page 2
```

---

### 7. Create Knowledge Base (`/create/knowledgebase`)

Create a named container for structured documents.

```bash
python3 scripts/memos_cloud.py create_kb "<name>" [--description "<desc>"]
```

Example:

```bash
python3 scripts/memos_cloud.py create_kb "My Project KB" --description "Project documentation"
```

---

### 8. Get Knowledge Base Documents (`/get/knowledgebase-file`)

Get document metadata/details. Two mutually exclusive modes:

```bash
# By file IDs
python3 scripts/memos_cloud.py get_kb_docs --file-ids "id1,id2"

# By knowledge base ID (with optional filters)
python3 scripts/memos_cloud.py get_kb_docs --knowledgebase-id "kb-1" [--type document|skill] [--page 1] [--page-size 20]
```

---

### 9. Delete Knowledge Base Documents (`/delete/knowledgebase-file`)

Delete specified documents from the knowledge base by file IDs.

```bash
python3 scripts/memos_cloud.py delete_kb_docs "<file_ids>"
```

Example:

```bash
python3 scripts/memos_cloud.py delete_kb_docs "file-id-1,file-id-2"
```

---

### 10. Remove Knowledge Base (`/delete/knowledgebase`)

Remove a knowledge base from the current project.

```bash
python3 scripts/memos_cloud.py remove_kb "<knowledgebase_id>"
```

Example:

```bash
python3 scripts/memos_cloud.py remove_kb "kb-123"
```
