---
name: omnifocus-mcp
description: Review what is due, capture new tasks, build projects from notes, and organize OmniFocus from natural language in OpenClaw on macOS. Use this when the user wants to read or update OmniFocus tasks, projects, folders, tags, or perspectives; the upstream OmniFocus-MCP project by themotionmachine provides the connection layer.
metadata: {"openclaw":{"emoji":"✅","homepage":"https://github.com/themotionmachine/OmniFocus-MCP","os":["darwin"],"requires":{"bins":["node","npm","omnifocus-mcp"]},"install":[{"id":"node","kind":"node","package":"omnifocus-mcp","bins":["omnifocus-mcp"],"label":"Install OmniFocus MCP (node)"}]}}
homepage: https://github.com/themotionmachine/OmniFocus-MCP
user-invocable: true
---

# Manage OmniFocus

Use this skill to connect OpenClaw to OmniFocus and work with your tasks, projects, folders, tags, and perspectives in natural language.

Technical note:
- this skill uses the upstream OmniFocus MCP server behind the scenes, but the main goal is helping users review, organize, and update their OmniFocus system faster

Typical things this skill can help with:
- review what is due today or this week
- find flagged tasks, inbox items, or next actions
- create tasks and projects from notes, transcripts, or plans
- reorganize tags, folders, projects, and task metadata
- inspect available perspectives and read what they contain

Quick examples:
- `Use $omnifocus-mcp to show me tasks due today.`
- `Use $omnifocus-mcp to list my flagged tasks for this week.`
- `Use $omnifocus-mcp to show my Inbox items and suggest how to organize them.`
- `Use $omnifocus-mcp to create a project called Product Launch with tasks for copy, design, and QA.`
- `Use $omnifocus-mcp to show the next actions in my Work folder.`

## Attribution

This skill is an OpenClaw-focused wrapper around the upstream OmniFocus MCP server created by [themotionmachine](https://github.com/themotionmachine).

Upstream project:
- `OmniFocus-MCP`
- GitHub: `https://github.com/themotionmachine/OmniFocus-MCP`
- npm: `https://www.npmjs.com/package/omnifocus-mcp`

This skill package does not reimplement the MCP server. It documents installation, registration, and OpenClaw-specific usage around the original package.

Refactor credit:
- original MCP server and tool implementation: `themotionmachine`
- OpenClaw skill adaptation and packaging assistance: `OpenAI`
- final packaged release, testing, and publishing: the skill publisher

This skill assumes:
- OpenClaw is being used on macOS.
- OmniFocus Pro for Mac is installed locally.
- OmniFocus 3 or later is the safest minimum assumption for this skill.
- The `omnifocus-mcp` package is installed globally with `npm install -g omnifocus-mcp`.
- The OpenClaw MCP registry includes an `omnifocus` server using the `omnifocus-mcp` executable.

Important compatibility note:
- OmniGroup documents AppleScript support as a Pro feature.
- The upstream MCP server depends on AppleScript.
- The upstream roadmap mentions future support for the `planned` date added in OmniFocus 4.7, which implies OmniFocus 4.7 is not required for the current feature set.

If the package is missing, OpenClaw can install it from the skill metadata using the configured node manager.

Use `{baseDir}` when referencing bundled files.

## Quick Start

If the MCP server is not configured yet, register it first:

```bash
{baseDir}/scripts/register_mcp.sh
```

To verify the local environment before using the skill:

```bash
{baseDir}/scripts/check_setup.sh
```

The intended OpenClaw MCP definition is:

```json
{
  "command": "omnifocus-mcp",
  "args": []
}
```

If you want to inspect the registered server after setup:

```bash
openclaw mcp show omnifocus --json
```

## Core Workflow

1. Confirm the request is really about OmniFocus, not generic planning advice.
2. Prefer targeted reads before broad dumps.
3. Use the smallest tool that answers the question.
4. Reflect back ambiguous destructive operations before applying them.
5. After write operations, summarize what changed in plain language.

## Tool Selection

Prefer these tools in this order:

- `query_omnifocus` for targeted reads, counts, filtered searches, and lightweight summaries.
- `list_tags` when you need to discover valid tags before suggesting or applying them.
- `list_perspectives` and `get_perspective_view` for perspective-driven workflows.
- `dump_database` only when the user explicitly needs a broad inventory, deep analysis across the whole database, or the targeted query surface cannot answer the request.
- `add_omnifocus_task`, `add_project`, `edit_item`, `remove_item` for single-item mutations.
- `batch_add_items` and `batch_remove_items` for transcript ingestion, bulk cleanup, or hierarchical task creation.

If the MCP tools are unavailable in the current session, check setup first instead of improvising a replacement workflow.

## Query Strategy

Default to `query_omnifocus`.

Use it for:
- tasks due today, overdue, due this week, or deferred until a date
- next actions, available tasks, blocked tasks, or flagged work
- counts by project or folder
- tasks in a named project or inbox
- project or folder discovery without loading everything

When using `query_omnifocus`:
- request only the fields you need
- set `limit` for potentially large result sets
- use `summary: true` for counts or quick status checks
- sort by `dueDate` or `modificationDate` when ordering matters

See `{baseDir}/references/query_omnifocus.md` for concrete filter guidance.

## Mutation Rules

When creating or editing items:
- preserve the user's stated project, folder, tag, defer date, due date, and flag intent
- prefer exact IDs when available; otherwise fall back to names
- use ISO dates for `dueDate`, `deferDate`, and `plannedDate`
- preserve notes instead of overwriting them casually unless the user asked for replacement
- use `batch_add_items` when the request naturally contains multiple sibling tasks or parent/child structure

For destructive actions:
- `remove_item` and `batch_remove_items` should be used only when the user clearly asked to delete or remove the items
- if the target is ambiguous by name, resolve the ambiguity before removing anything

## Common Patterns

### Daily review

- Fetch urgent work with `query_omnifocus` on `tasks`
- filter for `status`, `flagged`, `dueWithin`, or `dueOn`
- return a concise agenda, then offer follow-up edits only if requested

### Inbox processing

- use `query_omnifocus` with inbox-focused filters first
- group similar tasks
- if the user wants changes, apply them with `edit_item` or `batch_add_items`

### Project build-out from notes or transcripts

- extract deliverables and action items
- create a project with `add_project` if needed
- create structured tasks with `batch_add_items`
- use `tempId` and `parentTempId` for hierarchy when subtasks are obvious

### Tag cleanup

- call `list_tags` first if tag names may be uncertain
- identify missing or inconsistent tags with `query_omnifocus`
- propose the cleanup before mass edits

## Perspective Workflows

Use:
- `list_perspectives` to enumerate built-in and custom perspectives
- `get_perspective_view` to inspect a named perspective

Important limitation:
- the server can read a named perspective view, but due to OmniJS limitations it cannot programmatically switch perspectives in the GUI

## When To Use `dump_database`

Use `dump_database` only when one of these is true:
- the user asks for a full OmniFocus inventory
- the user wants cross-cutting analysis that is awkward with targeted queries
- you need a broad export-style snapshot

Avoid it for simple reads because it is slower and heavier than `query_omnifocus`.

## Response Style

When reporting results:
- lead with the answer, not the raw tool call
- keep large task lists grouped and easy to scan
- mention important assumptions, especially around date interpretation
- for write operations, state exactly what was added, edited, or removed

## References

- Query filter details: `{baseDir}/references/query_omnifocus.md`
- OpenClaw MCP registration helper: `{baseDir}/scripts/register_mcp.sh`
- Local setup check: `{baseDir}/scripts/check_setup.sh`
