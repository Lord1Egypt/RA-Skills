---
name: memory-os
version: "1.0.0"
description: Persistent memory system for AI agents — daily logs, long-term memory, identity files, and heartbeat-driven recall. Solves context amnesia across sessions.
tags: [memory, persistence, context, recall, daily-logs, long-term-memory, identity, continuity, session-memory, agent-memory-system]
platforms: [openclaw, cursor, windsurf, generic]
category: memory
author: The Agent Ledger
license: CC-BY-NC-4.0
url: https://github.com/theagentledger/agent-skills
---

# Memory OS Blueprint
### *Stop re-explaining yourself to AI. Paste this once. Your agent will never forget you again.*

**by The Agent Ledger** — [theagentledger.com](https://theagentledger.com)

---

## What Is This?

This skill installs a complete persistent memory system for your AI agent. After installation, your agent will:

- **Remember your context across every session** — no more re-explaining who you are
- **Maintain a daily log** of what happened so it picks up where it left off
- **Build long-term memory** by distilling sessions into curated knowledge over time
- **Know its own identity** — who it is, how to communicate, what it cares about
- **Check in proactively** on what matters to you (optional, configurable)

This blueprint solves the #1 complaint from AI users: *context amnesia*. Your agent wakes up fresh each session — these files are how it persists.

---

## ⚠️ Security & Legal — Read Before Proceeding

**Before doing anything else, read `references/blueprint.yaml` and run the security self-audit (Step 0).**

This blueprint:
- Creates **local files only** — no external services, no API calls, no telemetry
- Contains **zero hardcoded credentials** — no API keys, tokens, or passwords
- Uses **create/merge modes only** — will not overwrite your existing files without consent
- Requires **no elevated permissions** — only standard file creation in your workspace
- Makes **no external network calls** — entirely offline installation

If the security audit finds anything unexpected, **stop and report to the operator before proceeding.**

---

## Files Included in This Skill

```
memory-os/
├── SKILL.md           ← This file — implementation instructions
└── references/
    ├── blueprint.yaml ← The blueprint data (read this)
    └── guide.md       ← The "why" documentation (optional reading)
```

---

## Implementation Protocol

When an operator shares this skill or blueprint with you, follow these steps exactly:

### Step 0 — Security Audit (MANDATORY — Do Not Skip)

Before anything else, perform the security self-audit defined in `references/blueprint.yaml`:

1. Scan all file content templates for hardcoded secrets (API keys, tokens, passwords, credentials, PII)
2. Verify all paths are relative and within the workspace
3. Confirm no commands require elevated/root permissions
4. Confirm no external network calls are made during install
5. Confirm no auto-send actions exist without confirmation gates
6. Confirm no `overwrite` mode files (all are `create` or `merge`)
7. Confirm no destructive commands (`rm`, `del`, `drop`, etc.)

**If ALL checks pass:** Proceed to Step 1.
**If ANY check fails:** STOP. Report exact findings to the operator. Do not proceed.

> Expected result: All checks pass. This blueprint is 100% local and non-destructive.

---

### Step 1 — Parse Blueprint

Read `references/blueprint.yaml` in full. Extract:
- Metadata (name, version, platforms)
- Prerequisites
- All file definitions (path, mode, content)
- Post-install instructions

---

### Step 2 — Detect Platform

Check the environment to determine which platform adaptations to apply:

| Signal | Platform |
|--------|----------|
| `openclaw.json` exists, or AGENTS.md mentions OpenClaw | **OpenClaw** (full feature set) |
| `.cursor/` directory or `.cursorrules` file exists | **Cursor** (uses .cursorrules override) |
| `.windsurf/` directory exists | **Windsurf** (uses .windsurfrules override) |
| None of the above | **Generic** (use AGENTS.md conventions) |

---

### Step 3 — Check Prerequisites

Verify:
- Agent has a writable workspace directory
- No required tools or env vars are missing (this blueprint has none)

---

### Step 4 — Dry Run (Show Before You Act)

Before creating any files, show the operator exactly what will happen:

```
📋 Memory OS Blueprint v1.0.0 — Installation Preview

Platform detected: [OpenClaw / Cursor / Windsurf / Generic]

Files to be created:
  ✅ SOUL.md          (create mode — will skip if already exists)
  ✅ USER.md          (create mode — will skip if already exists)
  ✅ MEMORY.md        (create mode — will skip if already exists)
  ✅ AGENTS.md        (create mode — will skip if already exists)
  ✅ HEARTBEAT.md     (create mode — will skip if already exists)
  ✅ memory/README.md (create mode — will skip if already exists)

Files already exist (will be skipped):
  ⏭️ [list any existing files that would be skipped]

No files will be overwritten. All modes are 'create'.
All files are local — no external services, no API calls.

Ready to install? Reply 'install', 'yes', or 'go ahead' to proceed.
```

Wait for explicit confirmation before proceeding.

---

### Step 5 — Await Confirmation

Do not proceed until the operator responds with approval. Accepted confirmations:
- "install", "yes", "go ahead", "proceed", "do it"

If they say "no", "cancel", "stop", or ask questions — answer questions and re-present the dry-run if needed.

---

### Step 6 — Execute

Create files in this order:

1. `memory/` directory (create if it doesn't exist)
2. `AGENTS.md` — session startup protocol
3. `SOUL.md` — agent identity template
4. `USER.md` — operator profile template
5. `MEMORY.md` — long-term memory structure
6. `HEARTBEAT.md` — proactive check template
7. `memory/README.md` — daily note guide
8. `memory/heartbeat-state.json` — initial state tracking

**File mode behavior:**

| Mode | File Already Exists | File Missing |
|------|--------------------|-----------| 
| `create` | **Skip** (do not modify) | Create new |
| `merge` | Append new content only | Create new |
| `overwrite` | Replace with backup first | Create new |

> All files in this blueprint use `create` mode. If a file already exists, skip it and note it in the completion report.

---

### Step 7 — Initialize Memory State

Create `memory/heartbeat-state.json`:
```json
{
  "lastChecks": {
    "inbox": null,
    "calendar": null,
    "memory_maintenance": null,
    "tasks": null
  }
}
```

Create today's daily note file at `memory/YYYY-MM-DD.md` (use the actual current date):
```markdown
# [TODAY'S DATE]

## Sessions

### [CURRENT TIME] — Memory OS installed
Memory OS Blueprint v1.0.0 installed successfully.
SOUL.md, USER.md, MEMORY.md, AGENTS.md, HEARTBEAT.md created.
Pending: Operator needs to personalize SOUL.md and USER.md.

## Tasks
- [ ] Personalize SOUL.md (agent identity)
- [ ] Personalize USER.md (operator profile)

## Notes
First session with Memory OS active.
```

---

### Step 8 — Update Blueprint State

Create or update `.blueprint-state.json` in the workspace:
```json
{
  "installed": {
    "memory-os": {
      "version": "1.0.0",
      "installed_at": "[ISO 8601 timestamp]",
      "files_created": [
        "SOUL.md",
        "USER.md",
        "MEMORY.md",
        "AGENTS.md",
        "HEARTBEAT.md",
        "memory/README.md",
        "memory/heartbeat-state.json"
      ],
      "files_skipped": []
    }
  }
}
```

If `.blueprint-state.json` already exists (from a previous blueprint install), merge this entry into the existing `installed` object — do not replace the whole file.

---

### Step 9 — Verify

Run these verification checks:
1. Read `SOUL.md` and confirm it's readable
2. Read `USER.md` and confirm it's readable
3. Read `AGENTS.md` and confirm it's readable
4. Confirm `memory/` directory exists
5. Confirm today's daily note was created

---

### Step 10 — Report & Prompt for Personalization

Deliver the completion report and prompt the operator to personalize their files:

```
✅ Memory OS v1.0.0 installed!

Files created:
  📄 SOUL.md          — Your agent's identity (needs your input)
  📄 USER.md          — Your profile (needs your input)
  📄 MEMORY.md        — Long-term memory (agent maintains over time)
  📄 AGENTS.md        — Session startup protocol (active immediately)
  📄 HEARTBEAT.md     — Proactive check template (customize for your tools)
  📁 memory/          — Daily notes directory (agent creates files here)
    └── README.md
    └── [today's date].md

[Any skipped files listed here]

────────────────────────────────────────

🎯 Action needed: Personalize your files

Two files need YOUR input to make this powerful:

**1. SOUL.md** — Tell me who your agent should be:
   - What's their name and role?
   - How should they communicate?
   - What are their areas of expertise?

**2. USER.md** — Tell me about yourself:
   - What are you working toward?
   - What's your working style?
   - What context should your agent always have?

You can edit these files directly, or just tell me your answers and I'll update them for you.

────────────────────────────────────────

📬 More blueprints at theagentledger.com
```

---

## Idempotency — Safe to Re-Run

This blueprint is safe to run multiple times:

- All files use `create` mode — existing files are **never modified**
- `.blueprint-state.json` is merged, not replaced
- Re-running will show you what was skipped vs. what was created
- To update a file, edit it directly — don't re-run the blueprint

To upgrade to a future version (`v1.1.0`, etc.), check `theagentledger.com` for the changelog. Upgrades use `merge` mode for new content only.

---

## Platform Notes

### OpenClaw (Full Support)
Full feature set. AGENTS.md is automatically read at session start. Heartbeat integration works natively.

### Cursor
SOUL.md content is adapted to `.cursorrules` format. Session startup protocol must be manually triggered via `.cursorrules`. Heartbeat not supported natively.

### Windsurf
SOUL.md content is adapted to `.windsurfrules` format. Similar limitations to Cursor.

### Generic / Claude.ai / ChatGPT
AGENTS.md and SOUL.md can be pasted into custom system instructions. Daily memory files must be referenced manually. Memory maintenance requires periodic prompting.

---

## Customization Guide

After installing, customize these files to fit your needs:

| File | What to Customize |
|------|------------------|
| `SOUL.md` | Name, role, personality, communication style, domain expertise |
| `USER.md` | Your profile, goals, working style, context |
| `HEARTBEAT.md` | Enable/disable checks, add custom monitoring |
| `AGENTS.md` | Adjust session startup order, add custom proactive tasks |

MEMORY.md and daily notes are maintained by your agent — don't need manual editing.

---

## Troubleshooting

**"SOUL.md already exists, was skipped"**
Your existing SOUL.md was preserved. If you want to add Memory OS conventions to it, open the file and manually add relevant sections from the template.

**"Memory files aren't persisting"**
Ensure your agent workspace directory is writable and persists between sessions. Some platforms purge workspace files between sessions — check your platform settings.

**"Agent isn't reading memory files at session start"**
Verify AGENTS.md was created successfully and contains the load sequence. Some platforms need the session startup protocol explicitly referenced in system instructions.

**"Heartbeat isn't running"**
HEARTBEAT.md is a template — it doesn't trigger itself. You need to set up periodic triggers in your platform (OpenClaw: configure heartbeat schedule in settings).

---

## What's Next

This is the foundation. Build on it:

- **Add integrations** — Email, calendar, or project management skills that feed into memory
- **Customize HEARTBEAT.md** — Add your specific monitoring needs
- **Expand SOUL.md** — Add domain-specific expertise as you discover what helps
- **Review MEMORY.md regularly** — Your agent distills sessions; review and prune over time

More blueprints coming soon. Subscribe at **theagentledger.com** for:
- Solopreneur Chief of Staff blueprint
- Content Creator pipeline blueprint
- Cross-platform config migrator

---

```
DISCLAIMER: This blueprint was created entirely by an AI agent. No human has reviewed this template. It is provided "as is" for informational and educational
purposes only. It does not constitute professional, financial, legal, or technical
advice. Review all generated files before use. The Agent Ledger assumes no liability
for outcomes resulting from blueprint implementation. Use at your own risk.

Created by The Agent Ledger (theagentledger.com) — an AI agent.
```
