---
name: handoff
description: Create temporary handoff docs and propose/apply permanent knowledge updates in a shared Obsidian vault.
metadata:
  {
    "openclaw": {
      "emoji": "🧷"
    }
  }
---

# Handoff (shared)

Create **temporary** handoff documents and (optionally) propose/apply updates to **permanent** docs.

## Shared vault layout

Root: `$HOME/.openclaw/shared/` (Obsidian vault)

- Temporary handoffs: `$HOME/.openclaw/shared/handoff/<project>/<YYYY-MM-DD>/...`
- Permanent knowledge: `$HOME/.openclaw/shared/knowledge/<project>/...`

## Invocation

This skill is usually invoked via slash command (Telegram nativeSkills):

- `/handoff <project> [options]` (default mode)
- `/handoff load <project> [--date YYYY-MM-DD]` (subcommand)

If native skill commands are unavailable, use: `/skill handoff <input>`.

## Supported forms (v1)

This skill currently supports **only** two user-facing forms:

1) **Default**: `/handoff <project> [options]`
2) **Load**: `/handoff load <project> [--date YYYY-MM-DD]`

### Subcommand parsing rules (must follow)

- Treat the first token after `/handoff` as either:
  - a `<project>` (default mode), **or**
  - the literal subcommand `load`.
- Only `load` is supported as a subcommand in v1.
- Any other token that looks like a subcommand (e.g. `integrity`, `list`, `help`, `:` variants) must be treated as **unsupported**. In that case:
  1) explain it’s unsupported,
  2) show the two supported forms above,
  3) ask the user to restate.

### `/handoff load` behavior

Goal: help the user quickly locate the most relevant existing handoff doc for a project.

When invoked as `/handoff load <project> [--date YYYY-MM-DD]`:

1) Search under: `$HOME/.openclaw/shared/handoff/<project>/`
2) Prefer checking an `INDEX.md` if present; otherwise search by recency.
3) If `--date` is provided, narrow to that date folder first.
4) Output:
   - The best matching handoff path(s)
   - A 3–8 bullet summary of what each file contains (read only)
   - Ask whether to update an existing file or create a new one.

No file writes in `load` mode unless the user explicitly asks to update/create.

## Inputs (suggested schema)

When the user provides options, interpret them like:

- `--new` force creating a new handoff file
- `--update` prefer updating an existing relevant handoff file
- `--log` also generate a matching `_work_log.md`
- `--name <name>` optional short name ("slug") for the file base name
- `--permanent <target_doc_path>` permanent-doc mode (ONLY propose updates unless `--apply`)
- `--apply` apply the proposed permanent-doc patch (requires explicit user confirmation)

If options are omitted:
- default is to **search for a relevant existing handoff** for the same `<project>` and ask whether to update it or create a new one (default suggestion: update).

## Critical principles (must follow)

### Confirm before writing
Before **any** `write` or `edit`, you MUST:
1) state the resolved absolute path(s) you intend to write, and
2) ask the user to confirm.

### Permanent docs: propose first
In `--permanent` mode you MUST:
- read the target doc if it exists,
- analyze its existing style/purpose,
- output a **PROPOSED PATCH** (clear section-level changes),
- STOP and ask for explicit confirmation.

Only after explicit confirmation AND `--apply` should you write/edit the file.

### Focus of permanent docs
Permanent docs should capture long-term maintainable knowledge:
- architecture/procedures/debugging workflows
- the evolution of understanding (wrong assumptions → what became clear)

### Temporary handoff doc requirements
A handoff doc is meant to be discarded after use. It must include:

1) Title: `Project Handoff: <project>`
2) Header note: temporary/discard after use
3) Key document links (permanent docs). If any new permanent docs were created in THIS session, link them here and explain each link in 1 sentence.
4) Session Goal
5) Work Done (concise)
6) Current Status (artifact/knowledge state, not actions)
7) Next Steps (actionable)
8) If `--log` used: link to the work log file

Also include a YAML header for indexing:

```yaml
---
type: handoff
temporary: true
project: <project>
date: <YYYY-MM-DD>
created_at: <ISO8601>
author: <agentId>
session: <sessionKey if available>
---
```

### Work log document (only with --log)
Work log is detailed and command-ish:
- commands executed + key outputs
- files read/modified + summary of changes
- hypotheses/decisions/errors
Avoid duplicating overview/goal/status/next steps from the handoff.

## Implementation hints

- Prefer relative Obsidian-friendly links inside the vault when linking other vault docs.
- Each project should keep: `$HOME/.openclaw/shared/handoff/<project>/INDEX.md` pointing to recent handoffs.
- If no `<project>` exists yet, propose creating the project folder + INDEX.md and ask for confirmation before writing.
- Ask the user if anything is unclear before proceeding when requirements are ambiguous.
