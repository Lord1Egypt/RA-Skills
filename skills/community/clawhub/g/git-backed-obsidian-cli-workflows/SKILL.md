---
name: git-backed-obsidian-cli-workflows
description: Use the official Obsidian CLI for note workflows in a Git-backed vault, including search, read, links/backlinks-style queries, daily-note operations, and lightweight note writes that auto-sync after successful write operations. Use when the official Obsidian CLI is already installed and usable on any supported environment, and the task is about querying or updating notes in an Obsidian vault with Git-backed backup behavior.
---

# Git Backed Obsidian CLI Workflows

Use the official Obsidian CLI as the primary workflow surface. Treat Git sync as a write-only follow-up, not part of read/query operations.

## Core rules

- Assume the official Obsidian CLI is already installed and usable.
- Use CLI-native read/query commands first for search, read, links, outline, tags, tasks, and related vault inspection.
- Use CLI-native write commands first for `daily`, `daily:append`, `create`, and similar lightweight note updates.
- After successful write operations, run the vault backup/sync script.
- Do not run Git sync after read-only operations.
- If a write-oriented CLI path is unavailable or unsuitable, fall back to direct file writing only when the workflow explicitly supports it.
- If sync fails after a successful write, report that the note was written but not synced.

## Environment model

This skill is **not server-only**. Use it anywhere the official Obsidian CLI is already available:
- desktop Linux
- macOS
- Windows environments where the official CLI is working
- headless/server environments that have already been adapted

If the environment is a headless server and the official CLI is not yet usable, use `obsidian-official-cli-headless` first. That skill handles server adaptation and installation. This skill handles the day-to-day note workflows after the CLI works.

## Fast path

1. Classify the request as either:
   - read/query
   - write/update
2. For read/query tasks, use the official CLI directly.
3. For write/update tasks, use the official CLI first, then run backup/sync.
4. Use fallback file writing only for supported write workflows when CLI writing is unavailable.
5. Report the target note/path, whether CLI or fallback was used, and whether sync succeeded.

## Common read/query commands

Prefer commands such as:

```bash
obs search query="..."
obs read file="..."
obs daily:read
obs links file="..."
obs outline file="..."
obs tags
obs tasks daily
obs vault
```

Use exact commands supported by the installed official CLI.

## Common write/update commands

Prefer commands such as:

```bash
obs daily
obs daily:append content="..."
obs create name="..." content="..."
```

After a successful write, run the backup script.

## Bundled scripts

Use `scripts/notes_workflow.py` when you need a deterministic wrapper for:
- daily-note append with sync
- lightweight memo/inbox capture with fallback write
- simple note create/append workflows with post-write sync

Use `scripts/backup.sh` as the default post-write Git sync path for this skill.

## References

- Read `references/query-vs-write.md` to choose whether a task should trigger sync.
- Read `references/fallbacks.md` for the fallback policy and reporting rules.
- Read `references/workflow-surface.md` to understand why the wrapper script supports a narrower write surface than the full official CLI.
- Read `references/environment-note.md` for the split between general CLI workflows and headless/server adaptation.

## What not to do

- Do not use this skill to install or configure the official CLI environment; use `obsidian-official-cli-headless` for that.
- Do not force-push from automation.
- Do not expand into full vault restructuring, plugin setup, or GUI management.

## What to report

Keep the result minimal:
- command or workflow used
- target note/path
- whether sync ran
- whether sync succeeded
