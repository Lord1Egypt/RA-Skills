---
name: long-project-manager
description: Create and maintain a persistent file-based workspace for long-running, multi-session, or interruption-sensitive work. Use when the user wants to start a long-term project, continue a previous project, preserve context across days or resets, keep durable handoff notes, or avoid losing decisions and next steps in chat history. Good for engineering, research, writing, planning, and operations work.
---

# Long Project Manager

Store long-project state in files, not only in chat.

Use the bundled templates in `assets/project-template/` (Chinese) or `assets/project-template-en/` (English) to create a durable project folder under `projects/<project-name>/`.

## Project folder standard

Create or maintain these files:

- `README.md` — project goal, scope, success criteria, key entry points
- `STATUS.md` — current goal, current judgment, progress, blockers, next action
- `TODO.md` — prioritized work queue
- `DECISIONS.md` — important decisions and tradeoffs
- `LOG.md` — dated work log and discoveries
- `REFERENCES.md` — important files, links, commands, and outputs
- `HANDOFF.md` — compact checkpoint for resuming later

## Start a long project

When the user asks to create a long-running project or preserve context across sessions:

1. Normalize a short hyphen-case project name.
2. Create `projects/<name>/`.
3. Choose a template language:
   - `assets/project-template/` for Chinese
   - `assets/project-template-en/` for English
4. Copy the full template.
5. Fill at least:
   - `README.md`
   - `STATUS.md`
   - `TODO.md`
6. Tell the user the project path and the resume command or resume phrasing to use later.

## Work inside the project

For every meaningful milestone, write state back to files instead of leaving it only in chat.

Update with this bias:

- Put the latest judgment and exact next action in `STATUS.md`.
- Put concrete, actionable tasks in `TODO.md`.
- Put important or irreversible choices in `DECISIONS.md`.
- Put dated discoveries, command results, and observations in `LOG.md`.
- Put durable links, paths, and commands in `REFERENCES.md`.

Prefer concise, high-signal updates.

## Resume a project later

Read in this order:

1. `README.md`
2. `STATUS.md`
3. `TODO.md`
4. `DECISIONS.md`
5. `LOG.md`
6. `HANDOFF.md`

Then summarize the project state in 3-5 bullets and continue from the first actionable next step.

## Before stopping

Always leave a clean restart point:

1. Refresh `STATUS.md`.
2. Update `HANDOFF.md`.
3. Make the next action explicit.
4. Make the first file to read explicit.

## Quality bar

Always preserve these four things for long tasks:

- **Current goal** — what must happen now
- **Current judgment** — what seems true and why
- **Open loops** — what remains unresolved
- **Next action** — the exact next step

If these four things are written down, the project can survive resets, context loss, and handoffs.

## Good defaults

- Keep entries short and concrete.
- Prefer updating existing files over scattering notes across many new files.
- Treat `STATUS.md` as the first-screen dashboard.
- Treat `HANDOFF.md` as the restart capsule.
- Treat chat as transient and project files as durable state.

## Avoid these mistakes

- Do not leave important project state only in chat.
- Do not create many extra files when the standard project files are enough.
- Do not replace durable context with vague summaries.
- Do not stop without making the next action explicit in `STATUS.md` or `HANDOFF.md`.
