---
name: openspec
description: Use OpenSpec (`@fission-ai/openspec`) for spec-driven development when implementing non-trivial changes in existing projects. Use when the environment exposes openspec tools (`openspec_init`, `openspec_list`, `openspec_show`, `openspec_validate`, `openspec_archive`, `openspec_status`, `openspec_update`, `openspec_run`). Triggered by user phrases like "propose a change", "spec this out", "open a change for X", or when starting a multi-step feature in a repo that already has an `openspec/` directory.
---

# OpenSpec

Use OpenSpec to align on **what** before writing **how**. Specs and proposals live under `openspec/` in the project. Each in-flight change gets its own folder with `proposal.md`, `specs/`, `design.md`, and `tasks.md`.

## When to use

- The user asks to propose, scope, or specify a change before coding.
- The project already has `openspec/` — keep using it.
- The change touches multiple files or modules and benefits from a checklist.
- The user wants to archive a completed change ("close out the dark-mode change").

Skip OpenSpec for trivial edits (one-line fixes, typos, log tweaks). The ceremony is not worth it.

## Core workflow

1. **Confirm the project is OpenSpec-enabled.** Look for `openspec/` at the project root. If missing and the user wants to start: `openspec_init` with the appropriate `tools` list for their AI assistant.
2. **Read state first.** `openspec_list { kind: "changes" }` shows active changes. `openspec_status` shows artifact completion.
3. **Propose a change.** Create `openspec/changes/<change-name>/` with:
   - `proposal.md` — why this change, what it changes, who benefits
   - `specs/` — requirements grouped by capability
   - `design.md` — technical approach
   - `tasks.md` — implementation checklist (each task on its own line)
4. **Validate.** `openspec_validate { name: "<change-name>" }` catches structural issues.
5. **Apply (implement).** Work through `tasks.md`, ticking each item as you finish. Keep diffs scoped — one task at a time.
6. **Sync / archive.** `openspec_archive { changeName: "<change-name>", yes: true }` rolls the change's specs into the main spec set and moves the folder under `openspec/changes/archive/<date>-<name>/`.

## Tool reference

| Tool | Purpose |
| --- | --- |
| `openspec_init` | Scaffold `openspec/` in a project, optionally with `--tools <ids>` and `--profile <name>` |
| `openspec_update` | Regenerate AI assistant instructions after upgrading openspec |
| `openspec_list` | List active changes (default) or specs |
| `openspec_show` | Show a single change/spec, optionally include raw files via `includeFiles: true` |
| `openspec_validate` | Validate change/spec structure |
| `openspec_archive` | Archive a completed change |
| `openspec_status` | Artifact completion status for the project or a change |
| `openspec_run` | Escape hatch for `openspec` subcommands not surfaced above |

## Anti-patterns

- Do not invent specs for changes the user did not ask to formalize. Use OpenSpec when the user wants spec-driven flow, not as a tax on every edit.
- Do not skip `openspec_validate` before declaring a change ready.
- Do not archive a change that still has unchecked items in `tasks.md` unless the user explicitly accepts the partial state.
- Do not edit `openspec/specs/` directly in the middle of a change — drive spec updates through the change folder and let archive roll them in.

For longer examples and trigger patterns, see `references/workflow.md`.
