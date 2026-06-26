# long-project-manager

A shareable OpenClaw skill for turning long-running work into a durable, file-based project workspace.

Instead of relying on transient chat context, this skill turns ongoing work into durable project state on disk.

## What it solves

Chat history is fragile for multi-day work.

This skill gives the agent a standard way to:
- create a persistent project folder
- capture current status and decisions
- keep a prioritized task list
- leave clean handoff notes
- resume after `/new`, `/reset`, interruptions, or model context loss

It is useful for engineering, research, writing, planning, operations, and any task that spans multiple sessions.

## What the skill creates

The skill works with a project folder like:

```text
projects/<project-name>/
├── README.md
├── STATUS.md
├── TODO.md
├── DECISIONS.md
├── LOG.md
├── REFERENCES.md
└── HANDOFF.md
```

## File roles

- **README.md** — project goal, scope, success criteria, key entry points
- **STATUS.md** — current goal, current judgment, progress, blockers, next action
- **TODO.md** — prioritized tasks
- **DECISIONS.md** — important decisions and tradeoffs
- **LOG.md** — dated work log and discoveries
- **REFERENCES.md** — important files, links, commands, outputs
- **HANDOFF.md** — compact restart note for the next session

## When to use it

Use this skill when the user wants to:
- start a long-term project
- continue a complex project later
- avoid losing context across days
- keep decisions and next steps outside chat history
- leave a clean handoff for future sessions

## Example prompts

- "Start a long-term project for rebuilding my quant trading system."
- "Create a durable project workspace for this research task."
- "Continue my previous long-running project and tell me the next step."
- "Set up a persistent handoff structure so we can resume this later."

## Workflow

### 1. Start
Create `projects/<project-name>/` and choose a template:
- `assets/project-template/` for Chinese
- `assets/project-template-en/` for English

At minimum, fill:
- `README.md`
- `STATUS.md`
- `TODO.md`

### 2. Work
As progress happens, write important state back to files instead of relying on chat memory.

### 3. Pause
Before stopping, refresh:
- `STATUS.md`
- `HANDOFF.md`

Make the next action explicit.

### 4. Resume
Read in this order:
1. `README.md`
2. `STATUS.md`
3. `TODO.md`
4. `DECISIONS.md`
5. `LOG.md`
6. `HANDOFF.md`

Then continue from the first actionable next step.

## Design principles

This skill is built around four durable state anchors:
- current goal
- current judgment
- open loops
- next action

If those are always written down, long projects survive resets.

## Included assets

- `assets/project-template/` — Chinese project-file templates
- `assets/project-template-en/` — English project-file templates

## Repository contents

```text
long-project-manager/
├── SKILL.md
├── README.md
└── assets/
    ├── project-template/
    │   ├── README.md
    │   ├── STATUS.md
    │   ├── TODO.md
    │   ├── DECISIONS.md
    │   ├── LOG.md
    │   ├── REFERENCES.md
    │   └── HANDOFF.md
    └── project-template-en/
        ├── README.md
        ├── STATUS.md
        ├── TODO.md
        ├── DECISIONS.md
        ├── LOG.md
        ├── REFERENCES.md
        └── HANDOFF.md
```

## Notes

This repository intentionally keeps the skill simple:
- no extra automation scripts
- no opinionated tooling
- no domain-specific examples

The goal is a small, reusable foundation that can fit many kinds of long-running work.
