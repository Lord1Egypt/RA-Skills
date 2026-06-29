---
name: ModelBound
description: Pull team skills, rules, and knowledge from the ModelBound hosted MCP server. Use whenever the user references their ModelBound team, asks to sync skills/rules, search team knowledge, or propose edits to a team-managed `SKILL.md` / `AGENTS.md` / `CLAUDE.md`.
---

# ModelBound

ModelBound is the source of truth for AI team skills, rules, system prompts, and knowledge bases. This skill connects OpenClaw to ModelBound's hosted MCP server so you can search and pull team context on demand instead of copy-pasting files.

## Setup

Required env:

- `MODELBOUND_API_KEY` — get one at <https://modelbound.co/api-keys>

Optional:

- `MODELBOUND_TEAM_ID` — scope all calls to a specific team
- `MODELBOUND_ENDPOINT` — defaults to `https://mcp.modelbound.co`

The MCP server is plain HTTPS JSON-RPC. No daemon, no shell-out.

## Lean-first protocol

ModelBound exposes 45+ tools. **Do not advertise them all.** Instead, call this small surface and let the server route:

| Tool | Purpose |
| --- | --- |
| `modelbound.listTools` | List every available tool with its scope. Always call first if you don't know what's available. |
| `modelbound.callTool` | Invoke any tool by name. Use this for everything else. |
| `help` | Plain-English description of a tool or workflow. |
| `search.all` | Hybrid search across skills, rules, prompts, and corpora. |
| `search.summary` | Reranked top-N answer to a question. |
| `files.get` | Fetch a specific file by ID or slug. |
| `skills.proposeDraft` | Propose an edit to a team-managed skill. Returns a `review_url`. |
| `gateway.setWorkspace` | Scope subsequent calls to one team / repo. |

If a workflow below references a tool not on this list, route it through `modelbound.callTool` with the name from `reference/tools.md`.

## Workflows

### 1. Pull a team skill into the working directory

1. `gateway.setWorkspace` with the user's team or repo slug.
2. `search.all` for the skill name (or `skills.list` via `modelbound.callTool` for an exhaustive list).
3. `files.get` to fetch the `SKILL.md` body.
4. Write it to `./.claude/skills/<name>/SKILL.md` (or whatever location the user's IDE expects).

### 2. Answer a question from team knowledge

1. `search.summary` with the user's question.
2. If the summary cites file IDs, follow up with `files.get` for the full text.
3. Cite the ModelBound URL the server returns — never fabricate one.

### 3. Read a specific file the user mentioned

`files.get` with the slug or URL fragment. If ambiguous, `search.all` first to disambiguate.

### 4. Propose an edit back to ModelBound

**Never** call `skills.update` directly. Always use `skills.proposeDraft`:

1. `files.get` the current version.
2. Compute the new content locally.
3. `skills.proposeDraft` with `{ skill_id, content, summary }`.
4. Show the user the `review_url` it returns. A teammate approves the change in the ModelBound UI.

### 5. Discover more capabilities

If the user asks for something this skill doesn't cover (evals, agents, corpora ingestion, MCP gateway), call `modelbound.listTools` and pick from the result. `reference/tools.md` has a categorized index.

## Auth fallback

If a call returns `401 unauthorized`, tell the user:

> Set `MODELBOUND_API_KEY` to a key from <https://modelbound.co/api-keys>, then re-run the request.

Don't try to recover by guessing or by hitting other endpoints.

## Safety rules

- HTTP only. Never shell out, never write to ModelBound files on disk other than under the user's IDE skill directory.
- Read tools (`search.*`, `files.get`, `*.list`) are safe to call freely.
- Write tools (`skills.proposeDraft`, `corpus.upload`, `webhooks.create`, etc.) require explicit user confirmation in chat first.
- The skill bans `skills.update` outright — propose drafts instead.

## More

- `reference/tools.md` — categorized index of all 45+ ModelBound MCP tools.
- `reference/examples.md` — three end-to-end JSON-RPC recipes.
