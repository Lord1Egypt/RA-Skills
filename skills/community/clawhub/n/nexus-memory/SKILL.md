---
name: nexus-memory
version: 0.1.16
description: >
  Persistent memory for Claude Code powered by Qdrant. Auto-Recall injects
  relevant memories before each prompt, Auto-Capture stores facts after each
  turn. Self-hosted and private by default: embeddings run locally with
  Qwen3-Embedding-0.6B, nothing leaves the machine unless you add a cloud
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
| `NEXUS_MAX_RECALL` | `5` | Entries injected per prompt |
| `NEXUS_RECALL_CHARS` | `1600` | Character budget for the injection |

Cloud embedders are opt-in: they run only if `NEXUS_EMBEDDING_PROVIDER` names
one *and* its key is present. A fresh install sends nothing off the machine.

## What gets stored

Auto-capture writes facts, decisions and session summaries. Entries carry a
level — `public`, `trusted` or `private`. Recall shows what the agent's role is
allowed to see; `private` entries stay hidden from other agents. Tell the user
what is being stored the first time, and check the store before storing
secrets: passwords, tokens and card data do not belong there.

## Manual tools

Over MCP (`/mcp`, streamable HTTP) an agent key gets eight tools:

`recall`, `remember`, `forget`, `update`, `fact_history`, `report`, `health`,
`guardrail_check`

The graph and administrative routes need a higher role (`work` / `admin`). The
default agent role `know` can read, write and change its own entries.

## Harnesses

- **Hermes Agent**: native Python memory provider (`plugins/memory/nexus`).
- **OpenClaw**: native plugin (`plugins/openclaw`).
- **DeepSeek Harness**: `plugins/dsh`, brings its own `cordis.patch.yml` with
  the MCP wiring, so installing the plugin is enough. `scripts/install_dsh_plugin.mjs`
  enrols the harness, stores the key and installs the plugin's dependencies.

## Shared store

A memory written by Claude Code is immediately visible to the other agents and
vice versa. One brain, several agents.
