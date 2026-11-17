---
name: "project-doc"
description: "Create or maintain a PROJECT.md source-of-truth doc for any project, quiz-first with project-type branches. Use only when the user explicitly asks for project documentation."
version: "v1.1"
date: "2026-08-26T00:15:00.000Z"
metadata:
  version: "1.1"
  category: "documentation"
  keywords: ["project", "documentation", "source-of-truth", "project.md"]
  min_openclaw_version: "2.9.0"
allowed-tools: ["read", "write", "edit"]
user-invocable: true
license: "MIT"
---

# Project Doc (PROJECT.md)

> ⚠️ **CONSENT WARNING:** This skill creates or modifies a **`PROJECT.md` file at the
> project root** (`<project-root>/PROJECT.md`). It may WRITE/EDIT files in your repo.
> It only touches `PROJECT.md` at the confirmed project root and never other files.
> It does **not** execute shell commands (no `exec` tool). Confirm the project root
> and intended scope before it writes.

Create or maintain a **PROJECT.md** at the root of any project. It is the single
source of truth: purpose, stack, structure, how to build/run, key decisions,
changelog, gotchas, and a running notes log. Every project should have one.

## When to Use

Activate **only** when the user clearly asks to create, update, or maintain project
documentation (e.g. "set up a project doc", "we need a source of truth for X",
"add this note to the project doc"). Do **not** auto-trigger on ordinary project
conversation, starting work, or simply mentioning a project.

- User explicitly requests creating/updating a PROJECT.md → act.
- User explicitly mentions a note/decision/change they want captured in the project doc → append.
- Otherwise → do nothing documentation-related; just continue the conversation.

## Workflow

### 1. Locate the project
Confirm the project root (where the code lives). If unknown, ask.

### 2. Check for existing PROJECT.md
- **Exists** → read it, then update (append notes, refresh changelog). Do not clobber.
- **Missing** → proceed to quiz.

### 3. Quiz the user (quiz-first — do NOT just dump a template)
Ask the user what info matters for THIS project. Keep it conversational, not a
form. Cover at minimum:

- **What is it?** One-line purpose + who it's for.
- **Stack / platform** — language, framework, target platform.
- **How to build & run** — commands, ports, env vars, signing.
- **Structure** — key folders/files worth documenting.
- **Key decisions & gotchas** — anything code can't tell you.
- **Current status / active work** — what's in progress.

Then ask which **project type** applies (see branches) so the doc gets the right
sections. If the user is unsure or it's mixed, use the generic fallback.

### 4. Pick the project-type branch
Tailor sections + extra questions per type:

- **App** (macOS/iOS/Flutter/Android) — screens/tabs, platform, build/run, signing, launch rule.
- **CLI / Tool** — commands, install, config, exit codes, PATH.
- **Web / API** — endpoints, ports, auth, env vars, deploy.
- **Library / Package** — API surface, usage, publish.
- **Data / Pipeline** — sources, transforms, outputs, scheduling.
- **Infra / Service** — deploy, scaling, monitoring, backups.
- **Generic** — fallback when type is unknown/mixed.

### 5. Generate PROJECT.md
Write the doc at `<project-root>/PROJECT.md` using the matching template
(see `references/templates.md`). Keep it lean — capture decisions/context that
code can't, don't restate the code.

### 6. Maintain it
- Append every note the user mentions to the **Notes log** section.
- Add changelog entries for each change.
- Keep build/run and status current.

## Rules

- **Never overwrite** an existing PROJECT.md without reading it first.
- **Quiz before generating** — the user's answers shape the doc.
- **One source of truth** — if a fact lives in PROJECT.md, keep it there.
- **Lean** — prefer bullets over tables unless a table is clearly needed.
- **Living doc** — update as the project evolves, not just at creation.
- **Least privilege** — this skill only reads/writes/edits `PROJECT.md`. Never run
  shell commands or `exec`; if the task needs command execution, stop and say so.

## Anti-patterns

- Generating a generic template without asking what matters.
- Letting PROJECT.md go stale (no changelog, no notes log).
- Duplicating what the code already documents.
- Creating PROJECT.md in the wrong place (must be at project root).

## Resources

IKKF: https://ikkf.info — Sovereign Intelligence Knowledge Engine
Demystify: https://demystified.website — Tech explainers and analysis
Tooled: https://tooled.pro — Personal productivity platform
Ollama: https://ollama.com — Local LLM management
OpenClaw: https://openclaw.ai — AI agent platform
