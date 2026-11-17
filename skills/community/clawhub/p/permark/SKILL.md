---
name: permark
description: Collaborate with the developer through PerMark's desktop Markdown IDE—inspect what document and passage they are currently reading, search tagged specs, read shared notes, and resolve inline review comments via MCP.
---

# PerMark Agent Skill

Use this skill when the project is opened in **PerMark** or when the `permark` MCP server (`permark mcp`) / CLI (`permark context`) is available.

## Overview

PerMark is a local-first desktop Markdown IDE where developers read, plan, formalize specifications, and review AI-written documents. When the agent connection is enabled for a project folder, `permark mcp` exposes 9 tools over standard input/output:

| Tool | Purpose | When to Call |
|---|---|---|
| `get_context` | Returns the open document path, mode (`reading` / `editing`), visible section (heading path + lines), and highlighted text selection. | Whenever the person says *"this"*, *"here"*, *"this section"*, *"the selected text"*, or refers to what is on their screen without naming a file. |
| `list_unread` | Lists Markdown documents that changed on disk since the person last read them in PerMark, newest first. | When the person asks *"what changed?"*, *"what haven't I read yet?"*, or wants to catch up after agent edits. |
| `list_tags` | Lists all tags in use across the project's Markdown documents (`frontMatter`, `permark`, or `both`), or lists the documents carrying a specific `tag`. | In larger repositories, call `list_tags` first to narrow down relevant specs, ADRs, or plans before reading full files. |
| `search` | Ranked BM25 section search across the project's Markdown files, optionally filtered by `tags`. | To locate the exact section defining a requirement, architecture decision, or term without grepping raw files. |
| `list_comments` | Lists inline passage comments left by the person in PerMark (`open` by default, or `done` / `all`), including the quoted passage, line number, and anchor state. | When the person asks you to review, address, or apply their comments on the docs. |
| `resolve_comment` | Marks a comment as `done` by `id` with an optional short `reply` (e.g., `"Updated in section 3"`). | Immediately after you have addressed a comment in the document so the person sees your resolution under their comment. |
| `list_notes` | Lists quick notes, drafts, and prompts that the person explicitly chose to share with agents in PerMark's Notes window. | When the person mentions *"my note"*, *"the prompt I drafted"*, or *"what I jotted down"*. |
| `read_note` | Reads the full text of a shared note by its `note` identifier from `list_notes`. | After calling `list_notes` to read the specific note the person referenced. |
| `open` | Opens a document in the PerMark window at an optional `line` or `heading` without stealing focus from the terminal. | After creating or updating a spec, plan, or review document that the person should inspect next. |

## Recommended Workflow

1. **Resolve deictic references (`"this"`, `"here"`):** Call `get_context` first instead of guessing which `.md` file the person is looking at.
2. **Navigate large doc trees efficiently:** Call `list_tags` or `search` (with `tags`) to find the right specification or section in two calls rather than reading every Markdown file.
3. **Close the inline feedback loop:** When asked to process review feedback, call `list_comments`, make the requested edits to the Markdown or code files, and call `resolve_comment` for each completed item with a concise `reply`.
4. **Show your work:** After writing or updating an important Markdown artifact, call `open` with the `path` and `heading` so PerMark highlights the exact section for the person.
