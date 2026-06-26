# Obsidian Assistant (黑曜石助手)

An AI-powered Obsidian knowledge management companion that learns your vault's structure, habits, and workflows — then helps you maintain, optimize, and extract value from your second brain.

---

## What It Does

Obsidian Assistant is a WorkBuddy skill designed for **serious Obsidian users** who want more than generic advice. It works in four modes:

| Mode | Trigger | Output |
|------|---------|--------|
| **Habit Discovery** | First use, or "tell me about my vault" | Fills in your personal profile (`habit-patterns.md`) |
| **Q&A** | Any specific Obsidian question | Personalized, habit-aware answers with copy-paste code |
| **Pattern Extraction** | "Help me automate this", "create a template" | Templates, Dataview queries, QuickAdd macros, SOPs |
| **Vault Health Check** | "My vault is messy", "Inbox is backed up" | Diagnostic report + actionable fixes |

---

## How It Works

### Profile Memory

The skill maintains a persistent `references/habit-patterns.md` — a living profile of your vault that grows with every conversation. It remembers:

- Your vault path and sync method (iCloud, Git, Obsidian Sync...)
- Directory structure and organizing logic (PARA, Zettelkasten, custom...)
- Tag conventions and naming patterns
- Installed plugins and workflow habits
- High-frequency operation patterns

You never repeat yourself. The assistant reads your profile first, then answers.

### Four Work Modes

**1. Habit Discovery**
Proactively maps your vault via the Obsidian CLI (`obsidian vaults`, `obsidian tags`, `obsidian orphans`, etc.), analyzes your directory layout, and builds your profile through natural conversation — no interrogation, just a few targeted questions over time.

**2. Q&A**
Gives specific, actionable answers grounded in your actual setup:
- "How do I set up a Zettel workflow?" → answered using your existing plugins and folder conventions
- Dataview queries are written for your schema, not a generic one

**3. Pattern Extraction**
Turns observed habits into reusable artifacts:
- **Note templates** → written to `assets/templates/`, ready to drop into your Obsidian template folder
- **Dataview queries** → packaged with field explanations
- **QuickAdd macros** → JSON output with install instructions
- **Workflow SOPs** → numbered steps ready to paste into a note

**4. Vault Health Diagnosis**
Diagnoses across four dimensions:
- Inbox backlog (count + avg. dwell time)
- Orphan notes (no backlinks)
- Tag consistency and redundancy
- Stale/unresolved tasks

---

## File Structure

```
obsidian-assistant/
├── SKILL.md                        # Core instructions for the AI
├── references/
│   ├── habit-patterns.md           # User profile (auto-built over time)
│   └── obsidian-concepts.md        # Obsidian internals reference
└── assets/templates/
    ├── daily-note.md               # Daily journal template
    ├── project-note.md             # Project kickoff template
    └── book-note.md                # Book reading notes template
```

---

## Built-in Templates

Three templates are included and ready to use:

### Daily Note (`daily-note.md`)
Timestamped log entries with sections for focus, tasks, inbox processing, and tomorrow's plan.

### Project Note (`project-note.md`)
Goal / background / milestones / key links / log — structured for project kickoff and tracking.

### Book Note (`book-note.md`)
Core thesis / key concepts / notable quotes / personal reflections / actions / related notes.

---

## Dataview Quick Reference

Common queries pre-written and ready to copy into your vault:

```dataview
// All inbox files, oldest first
LIST FROM "0-Inbox" SORT file.ctime ASC

// Notes created today
LIST WHERE file.cday = date(today)

// Active projects
TABLE date, status FROM "1-Projects" WHERE status = "active"

// Unfinished tasks, cross-note
TASK WHERE !completed

// Orphan notes (no outgoing links)
LIST WHERE length(file.outlinks) = 0 AND file.folder != "templates"
```

---

## Interaction Principles

- **Memory first** — always reads the profile before responding
- **Personalized** — advice adapts to your existing structure, never imposes foreign conventions
- **Incremental** — builds understanding through natural conversation, not a一次性 interrogation
- **Actionable** — every suggestion includes copy-pasteable steps and code
- **Profile-driven** — new habits get written back to the profile automatically

---

## Requirements

- **Obsidian 1.12+** (for CLI support)
- **Obsidian CLI enabled** — Settings → General → Enable CLI
- **PATH configured**:
  ```bash
  # macOS
  export PATH="$PATH:/Applications/Obsidian.app/Contents/MacOS"
  # Linux (Flatpak)
  alias obsidian='flatpak run md.obsidian.Obsidian'
  ```

---

## Extending the Skill

The skill ships with empty profile files. As you use it, your `habit-patterns.md` accumulates real data about your vault. This makes the assistant progressively smarter — it starts with zero knowledge of your vault and builds a detailed, actionable model over time.

To add new templates, drop `.md` files into `assets/templates/` and they become available for the assistant to customize and deploy.

---

## Philosophy

This skill is built on a single idea: **the AI should remember what the user shouldn't have to repeat**.

Most AI interactions about knowledge management stay surface-level because the AI has no context. Obsidian Assistant changes that by maintaining a persistent, structured profile of your vault — your organizing logic, your tag conventions, your workflow habits — and using that profile to deliver answers that are actually tailored to you.
