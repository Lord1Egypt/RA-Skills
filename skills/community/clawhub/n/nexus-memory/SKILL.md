---
name: nexus-memory
version: 0.1.17
description: >
  Persistent memory for Claude Code powered by Qdrant. Auto-Recall injects
  relevant memories before each prompt, Auto-Capture stores facts after each
  turn. Every stored memory names its author in `agent`, and a write without
  one is refused. Self-hosted and private by default: embeddings run locally
  with Qwen3-Embedding-0.6B, nothing leaves the machine unless you add a cloud
  key. Shares one store with Hermes Agent, OpenClaw and the DeepSeek Harness,
  each agent with its own key. Use when the user asks to "remember", "recall",
  "search memory", or when project context from past sessions is needed.
---

# Nexus Memory

Nexus Memory gives Claude Code persistent memory across sessions, backed by a
local Qdrant instance. The same store is shared with Hermes Agent, OpenClaw and
the DeepSeek Harness — one brain, several agents, each with its own identity.

## How it works

- **Auto-Recall** (UserPromptSubmit hook): before each prompt it searches the
  store and injects the most relevant entries.
- **Auto-Capture** (Stop hook): after each turn it extracts notable facts and
  stores them.
- **Session Start** hook: loads project-related memories at the start.

## Keys: two different things

The service distinguishes an *installation key* from *agent keys*.

- The **installation key** comes from the server setup. It opens exactly one
  route, `POST /enroll`, and only from the machine itself. Every data route
  answers `401 plugin update required` when it is used.
- An **agent key** belongs to one harness. It is created once through
  `POST /enroll` and stored as `~/.nexus-memory/agent_keys/<agent>.key`. From
  then on it names the agent on every call; a header claiming a different agent
  is ignored.

Never copy an agent key from one machine to another: enrol instead, so each
harness gets its own entry in the register. An entry that already has its own
key is never taken over by a second enrol.

## Configuration

Environment variables (`.env` or shell):

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXUS_SERVICE_URL` | `http://127.0.0.1:9122` | Service base URL |
| `NEXUS_DATA_DIR` | `~/.nexus-memory` | Keys, reports, service state |
| `NEXUS_QDRANT_URL` | `http://localhost:6333` | Qdrant server URL |
| `NEXUS_COLLECTION` | `nexus` | Collection name |
| `NEXUS_EMBEDDING_PROVIDER` | local | `local`, `ollama`, `openai`, `google`, `jina` |
| `NEXUS_EMBEDDING_MODEL` | `Qwen/Qwen3-Embedding-0.6B` | Local model, 1024 dimensions |
| `NEXUS_MAX_RECALL` | `3` | Entries injected per prompt |
| `NEXUS_RECALL_BUDGET` | `800` | Character budget for the injected block |
| `NEXUS_RECALL_MIN_SCORE` | `0` | Minimum relevance; `0` means no threshold |
| `NEXUS_RECALL_EXCLUDE_CATEGORIES` | `session,entity` | Never injected; an empty value turns the filter off |

The recall decision is taken in one place: three entries, an 800-character
budget, session logs and entity labels out, and no minimum score — a threshold
filtered nothing up to 0.45 and above that cost matching entries first.

Cloud embedders are opt-in: they run only if `NEXUS_EMBEDDING_PROVIDER` names
one *and* its key is present. A fresh install sends nothing off the machine.

## What gets stored

Auto-capture writes facts, decisions and session summaries. Entries carry a
level — `public`, `trusted` or `private`. Recall shows what the agent's role is
allowed to see; `private` entries stay hidden from other agents. Tell the user
what is being stored the first time, and check the store before storing
secrets: passwords, tokens and card data do not belong there.

## Who wrote a memory (`agent`)

Every stored memory names its author in the payload field `agent`. The id comes
from the context of the call — the agent key that signed the request, or the
plugin's own `NEXUS_AGENT_ID` — never from a field a caller may invent; a header
claiming another agent is ignored. Since 22.11.2026 the field is mandatory: a
write that names nobody is refused instead of leaving a point with no owner.
Nothing is stored, and the refusal names the reason: over MCP `{"status":
"rejected", "reason": "..."}`, over `POST /write` an HTTP 422. A request without
a valid agent key gets no further than `401` and never reaches a write.

The maintenance passes that write directly carry `writer: consolidation` or
`writer: dreaming` instead and leave `agent` empty, because a consolidation
merges several agents' statements whose originals are gone and any attribution
would be a guess; a query can filter those points out on `writer`. Older entries
with neither field stay as they are — no migration, no backfill.

## Manual tools

Over MCP (`/mcp`, streamable HTTP) an agent key gets eight tools:

`recall`, `remember`, `forget`, `update`, `fact_history`, `report`, `health`,
`guardrail_check`

The graph and administrative routes need a higher role (`work` / `admin`). The
default agent role `know` can read, write and change its own entries.

## Backups

The service writes a full backup every six hours into `<data dir>/backups`
(`NEXUS_BACKUP_DIR` moves the folder, `NEXUS_AUTO_BACKUP=0` switches the
automatic pass off). A dump carries payloads only: the collection stores named
vectors, so one file holds no vectors and a restore re-embeds from the text
(`reembed=true`). The folder is created `0700` and every file `0600`, so other
accounts on the machine cannot read private entries even under a lax umask. The
newest four dumps are kept — one day at the six-hour cadence — and older
`nexus-backup-*` files are pruned. The `backup` tool (admin role) writes one on
demand.

## Harnesses

- **Hermes Agent**: native Python memory provider (`plugins/memory/nexus`).
- **OpenClaw**: native plugin (`plugins/openclaw`).
- **DeepSeek Harness**: `plugins/dsh`, brings its own `cordis.patch.yml` with
  the MCP wiring, so installing the plugin is enough. `scripts/install_dsh_plugin.mjs`
  enrols the harness, stores the key and installs the plugin's dependencies.

## Shared store

A memory written by Claude Code is immediately visible to the other agents and
vice versa. One brain, several agents.
