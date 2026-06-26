---
name: nella
description: Use this skill whenever the user is working inside a code repository and needs grounded, codebase-aware answers: locating a symbol or definition, tracing where a function is called, understanding how modules connect, reviewing dependency drift, or maintaining persistent context across a session. Trigger this skill on phrases like "where is X defined", "how is Y used", "what calls this", "search the codebase", "index this repo", or any request that benefits from semantic or hybrid code search rather than blind grep. Also use when an assumption about the codebase should be recorded for later verification, or when a long-running coding session needs continuity of context across turns. Do NOT use this skill for one-off shell commands, simple text edits, or tasks that do not require structural understanding of the repository.
---

# Nella MCP

Nella is a codebase intelligence layer for AI coding agents. It exposes the repository as a set of searchable, structured tools over the Model Context Protocol, so an agent can ground its reasoning in the actual code rather than guessing from filenames or partial snippets.

## When to reach for Nella

Use the Nella tools when any of the following is true:
- The repo is non-trivial (more than a handful of files) and a grep would return too many false positives.
- The user asks about behavior, call sites, or relationships rather than literal strings.
- The session involves multiple turns and context should persist (assumptions, prior searches, prior decisions).
- A change is being scoped and dependency drift or impact analysis matters.

If the question is purely lexical (find a literal token in one file), plain `grep` or `view` is faster and Nella is overkill.

## Setup

The package ships two binaries: `nella` (CLI) and `mcp` (stdio MCP entrypoint).

Local stdio config for an MCP client:

```json
{
  "mcpServers": {
    "nella": {
      "command": "npx",
      "args": ["-y", "@getnella/mcp", "--workspace", "/absolute/path/to/project"]
    }
  }
}
```

Hosted config (recommended for shared or always-on workspaces):

```json
{
  "mcpServers": {
    "nella": {
      "url": "https://mcp.getnella.dev/mcp",
      "headers": { "Authorization": "Bearer nella_your_key_here" }
    }
  }
}
```

Quick shortcut for Claude Code: `nella setup`. For other clients: `nella connect --client <claude|claude-code|vscode|cursor|windsurf|cline|roo-code>`.

## Available tools

| Tool | When to call it |
|------|-----------------|
| `nella_index` | First contact with a workspace, or after large refactors. Pass `--force` to rebuild from scratch. |
| `nella_search` | Default lookup. Supports `hybrid` (best general default), `semantic` (concept-level), and `lexical` (exact tokens). |
| `nella_get_context` | Pull the current session memory before answering, so prior assumptions and searches are not lost. |
| `nella_add_assumption` | Record any non-trivial assumption ("this function is only called from the worker") so it can be verified later. |
| `nella_check_assumptions` | Review recorded assumptions, especially before committing changes that depend on them. |
| `nella_check_dependencies` | Detect drift between the index and the working tree, or surface upstream impact of a change. |
| `nella_heartbeat` | Verify trust-chain continuity between tool calls in long sessions. |

## Recommended flow

1. Call `nella_get_context` at the start of a non-trivial task to load any prior session state.
2. If the workspace has not been indexed yet, call `nella_index`. Skip this if the index is already current.
3. Use `nella_search` (hybrid by default) to locate the relevant code before reading files.
4. Record any load-bearing assumption with `nella_add_assumption` so it survives across turns.
5. Before finalizing changes, run `nella_check_assumptions` and `nella_check_dependencies`.

## Search mode selection

- **hybrid**: Default. Combines lexical and semantic signals. Use when unsure.
- **semantic**: Conceptual queries ("where do we handle rate limiting", "auth flow for OAuth"). Tolerates paraphrase.
- **lexical**: Exact identifiers, error strings, or known token shapes. Faster, no embedding cost.

## Notes for the agent

- Always pass an absolute path to `--workspace`. Relative paths fail silently in some clients.
- Hosted mode requires a valid API key. If `nella_search` returns an auth error, surface it to the user rather than retrying blindly.
- The index can lag behind the working tree on large repos. If results look stale, call `nella_index` (without `--force`) for an incremental refresh.
- Treat `nella_get_context` output as authoritative for prior decisions in the session. Do not override silently.
