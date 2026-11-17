---
name: "mochi-quick-notes"
description: "Edit and search notes and tasks, filter tags and due dates, and export Markdown and CSV. Use for Quick Notes and Tasks."
metadata: {"openclaw": {"requires": {"bins": ["node"]}, "homepage": "https://mochilab.bz", "version": "1.1.1"}}
---

# Quick Notes and Tasks

## Capture information without losing the original

add saves kind note|task|idea, text, up to three tags and an optional YYYY-MM-DD due date. Return the real record ID so later edits select the same item. Preserve literal model numbers, names and user wording. A due date on a note is not an active reminder.

## Find, correct and complete a task

list and search support kind, status, an exact tag, dueFrom and dueTo. Search is literal and Unicode-normalized. When several records match a conversational description, show candidates and ask which one to change rather than editing all of them. update uses id and any supplied text/tags/due fields, saves prior values in history and permits due:null to remove a date. complete changes an open task to done; reopen makes a task open again. archive hides it from the default list without deleting it. Only tasks can be completed or reopened.

## Export the selected records

export accepts the same filters and a requestId. It writes notes.md as a readable checklist and notes.csv with IDs, types, statuses, tags and dates. CSV cells are quoted and spreadsheet formula prefixes in user text are neutralized. Archived items are included only when explicitly selected. Inspect actual returned paths before reporting a file as saved. Exports preserve earlier files and do not delete or move the original notes.

## Run the local helper

Prepare an input JSON file inside the active agent workspace. Use the actual workspace, not another agent's directory.

```text
node "{baseDir}/scripts/run.mjs" --workspace "CURRENT_WORKSPACE" --input "request.json"
```

Read [references/input.md](references/input.md) before preparing fields. Every mutation and export uses a stable unique requestId; an identical retry returns its saved result. Put user text in JSON, not shell code. Successful exports return actual file paths, sizes and SHA256 values under this workspace's `.mochilab/mochi-quick-notes/exports/` directory. Inspect the files before reporting completion. Previous exports are retained. No MochiLab key is needed by this standalone helper.

[User guide](README.md) · [Simplified Chinese guide](README.zh-CN.md)
