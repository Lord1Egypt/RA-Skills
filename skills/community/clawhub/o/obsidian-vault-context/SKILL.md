---
name: obsidian-vault-context
description: |
  Teach Claude to use an Obsidian vault as a shared workspace with persistent
  state across sessions. Covers vault navigation, orchestration file management,
  output routing, and bidirectional collaboration via Obsidian Headless. Use when
  the agent needs to read vault context, write output to the vault, update
  status/task files, or navigate folder structure. Triggers on "check status",
  "what's in the vault", "update tasks", "save this to the vault", "where should
  I put this", or any vault-related file operation.
compatibility: |
  Works across Claude.ai, Claude Code, and API. Obsidian Headless (optional)
  enables bidirectional sync for server deployments.
metadata:
  author: tesfandiari
  version: 1.0.0
---

# Obsidian Vault Context

The vault is the interface. Not chat. Not a terminal. A shared folder of markdown files that both you and the user can see and edit. Treat it like a shared codebase, not a reference library.

## Session Startup

1. Read `_context/context-map.md` if it exists — it maps projects to source files.
2. If no context map, scan top-level folders and infer context from names.
3. Read `_context/status.md` to understand what's active, blocked, and completed.
4. If this is a fresh vault with no orchestration files, create them. See `references/orchestration-files.md` for templates.

## Orchestration Files

Lightweight `.md` files in `_context/` (or `_Claude/`) that give you persistent state across sessions.

| File | Purpose |
|------|---------|
| `status.md` | What's active, blocked, completed. Update every session. |
| `tasks.md` | Prioritized task list with `#tags`. Update when tasks change. |
| `decisions.md` | Decision log with context, options, rationale. Append-only. |
| `context-map.md` | Project-to-file index (optional). |
| `scratchpad.md` | Working memory, cleared daily (optional). |
| `learnings.md` | Operational knowledge across sessions (optional). |

**Rules:** Read before writing. Update immediately, not at session end. Append to decisions and learnings, never overwrite. Keep entries lean — one line per task, one paragraph per decision.

For detailed format and examples, see `references/orchestration-files.md`.

## Vault Navigation

Folder placement carries meaning. Respect the structure when creating files:

| Pattern | Meaning |
|---------|---------|
| `foundations/` or `core/` | Strategy, vision, frameworks |
| `product/` | Specs, features, sprints, architecture |
| `company/` or `business/` | Operations, legal, marketing, hiring |
| `research/` or `engine/` | Technical research, analysis |
| `journal/` | Session logs, daily notes, reviews |
| `decisions/` | Past decisions with rationale |
| `work/` | Agent output: drafts, research, deliverables |
| `archive/` | Superseded files (read-only reference) |

Use `[[wikilinks]]` for all cross-references so the user can click through in Obsidian.

For a recommended starter layout, see `references/vault-structure-template.md`.

## Output Routing

Save work to the vault so the user sees it in Obsidian — don't present everything in chat.

| Output | Save To |
|--------|---------|
| Research briefs | `work/research/` or `research/` |
| Drafts | `work/drafts/` or `drafts/` |
| Final deliverables | `work/output/` or `output/` |
| Quick notes | `_context/scratchpad.md` (append) |

Add YAML frontmatter (`title`, `type`, `status`, `created`, `updated`, `tags`) to any file that will be referenced again.

**Naming:** Use descriptive file names (`competitor-analysis-march-2026.md`), not generic ones (`output-1.md`). Always update `status.md` so the user knows what changed.

## Bidirectional Collaboration

When Obsidian Headless is configured, changes flow both ways:

- **User -> Agent:** User edits in Obsidian (Mac/iPhone/iPad), syncs to server, you read the update.
- **Agent -> User:** You write to the vault, syncs to all user devices.

This means neither party needs to explain what the other already wrote down. You write output to the vault. The user reads it in Obsidian. Both can work on the same document asynchronously.

For server sync setup, see `references/obsidian-headless-setup.md`.

## Boundaries

- **Read and write only within the vault directory.** Do not access files outside the vault root.
- **Never modify skill files, agent config, or workflow definitions** unless the user explicitly asks you to. Your workspace is `_context/` and `work/` — not the files that define your own behavior.
- **Treat `company/legal/` as read-only.** Do not create, edit, or delete files in legal directories.
- **Do not store or log credentials.** If a workflow requires authentication, defer to the user.

## Context Safety

If context compaction triggers mid-session, write working state to disk immediately:

1. Current progress -> `_context/scratchpad.md`
2. State changes -> `_context/status.md`

These files reconstitute the session after compaction.
