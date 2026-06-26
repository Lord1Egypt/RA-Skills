---
name: hierarchical-agent-memory
description: >-
  Scalable memory architecture with hybrid topic-based working memory and
  optional time-based episodic recall. Provides structured MEMORY.md routing
  table, topic files for active projects, contact files, and configurable
  daily/weekly/monthly/yearly distillation layers. Use when the agent needs
  durable, organized long-term memory that survives compaction and scales
  across projects, contacts, and time horizons. For per-channel session
  isolation, install the companion skill agent-session-state. Upgrading from
  v2.x? Existing files are preserved — the agent will guide you through
  adding topic-based working memory alongside your current structure.
license: MIT
compatibility: "OpenClaw 2026.4.x or later. Requires memory-core plugin."
metadata:
  openclaw: {"requires": {"bins": ["openclaw"]}}
  version: "3.1.0"
  clawhub: {"category": "memory", "tags": ["memory", "hierarchy", "topics", "distillation"]}
---

# Hierarchical Agent Memory v3.1.0

Agents that run across multiple projects, contacts, and time horizons need memory that scales. Without structure, memory files grow into a single bloated document that triggers lost-in-the-middle degradation. This skill organizes agent memory into a hybrid architecture: topic-based working memory for active projects, and optional time-based archival layers for episodic recall.

## Onboarding

When this skill is installed or updated, initiate a setup conversation with the user before applying any memory structure changes. Do not silently create directories or files.

**Step 1 — Greet and explain.** Tell the user this skill organizes agent memory into a hybrid structure with topic-based working memory and optional time-based archival layers. Keep it to 2-3 sentences.

**Step 2 — Ask about preset preference.** Present three presets:

- **minimal** — MEMORY.md routing table plus daily notes. Best for simple setups and single-project agents.
- **standard** (default) — Adds topic files and contact files. Best for multi-project agents and teams.
- **full** — Adds weekly, monthly, and yearly auto-distillation layers. Best for long-running agents needing historical recall. If the bundled `memory-wiki` plugin is enabled, prefer **standard** — `memory-wiki`'s `syntheses/` pages and `reports/` dashboards already cover the same ground.

If the user says "just use defaults," apply standard and move on.

Companion skills and plugins: For per-channel session isolation, install `agent-session-state`. For governance and provenance tracking, install `agent-provenance`. If the bundled `memory-wiki` plugin is enabled, it sits beside this skill and is complementary — this skill owns the always-loaded MEMORY.md routing table and `memory/topics/` active-project working memory; `memory-wiki` owns the compiled durable knowledge vault (structured claims, provenance, dashboards). All are independent.

**Step 3 — Ask targeted follow-up questions based on preset.**

For standard or full: ask whether to create starter topic files from existing MEMORY.md content, and whether the user also uses companion skills.

For full only: first check whether `memory-wiki` is enabled by inspecting `plugins.entries.memory-wiki.enabled` in `openclaw.json`. If it is, warn the user that wiki `syntheses/` and `reports/` overlap with time-based distillation and offer **standard** as the recommended alternative. If the user still wants `full`, ask what timezone distillation cron jobs should use (default: system timezone) and what time weekly synthesis should run (default: Sunday 2:00 AM).

**Step 4 — Apply configuration.** Create the directory structure and write configuration to the workspace. Confirm what was created. Offer to run an initial migration if existing MEMORY.md content should be split into topic files.

**Step 5 — On skill update (v2.x to v3.x).** If `memory/weekly/` or `memory/daily/` already exists, the user is upgrading from v2.x. Tell them v3 adds topic-based working memory alongside the existing structure. Offer to scan current MEMORY.md and daily notes to suggest topic files. Do NOT delete or reorganize existing files without explicit approval.

**Step 6 — On skill update (v3.0.x to v3.1.0).** If the workspace config already has `time_layers: true` (or an effective `full` preset) AND `plugins.entries.memory-wiki.enabled` is true in `openclaw.json`, surface the overlap: wiki `syntheses/` and `reports/` dashboards now cover the same ground as weekly/monthly/yearly distillation. Offer to set `time_layers: false` and leave the existing `memory/weekly/`, `memory/monthly/`, and `memory/yearly/` archive files untouched (they're historical content, not regeneratable cache). If the user declines, do nothing — both systems can coexist, they'll just produce parallel rollups. If `memory-wiki` is not enabled, make no changes and do not mention this step.

---

## Memory Architecture

### Layer 1: MEMORY.md — Routing Table

MEMORY.md is loaded into the system prompt every session. It must stay under 3KB to avoid lost-in-the-middle degradation. It contains:

- Active project pointers — one line each, linking to topic files
- Key contact pointers — linking to contact files
- Infrastructure pointers — linking to config/endpoint files
- Active constraints and hard stops — the ONLY "content" that belongs here

MEMORY.md is a routing table, not a summary. If you're tempted to write a paragraph in MEMORY.md, it belongs in a topic file instead.

**Security note:** MEMORY.md is injected into the model context every session. Never put secrets, API keys, passwords, or sensitive PII in MEMORY.md or any file it points to. Store credentials in environment variables or `.env` files (excluded from memory). Active Constraints entries (e.g., "do not raise X") are acceptable — they are behavioral directives, not sensitive data.

Example MEMORY.md:

```markdown
## Active Projects
- [BlueCat MCP Testing](topics/bluecat-mcp.md) — BDDS integration, Bug #21 open
- [RPZ Article](topics/rpz-article.md) — draft in progress

## Key Contacts
- [Jane Doe](contacts/jane-doe.md) — BlueCat UX

## Active Constraints
- DO NOT RAISE: attorney call issue
- Merge freeze after 2026-04-15
```

### Layer 2: Topic Files — Working Memory

`memory/topics/<name>.md` files are the primary working layer. Each file is the authoritative source for one project, workstream, or subject area.

Structure topic files with the most recent information at the top, dated entries within the file, and links to relevant daily notes for full context.

**When to create a new topic file:** a project spans more than 2-3 daily notes, you find yourself repeatedly searching for the same subject, or the user explicitly asks to track something.

**When to update a topic file:** new decisions or status changes, after distilling relevant content from daily notes, or when correcting outdated information (update in place, don't append).

### Layer 3: Contact Files

`memory/contacts/<name>.md` files store information about people — role, email, context for how you interact with them, and when you last interacted.

### Layer 4: Daily Notes — Intake Layer

`memory/daily/YYYY-MM-DD.md` is the raw capture layer. OpenClaw automatically loads today's and yesterday's daily notes at session start.

Daily notes are intake, not archive. Important information should be distilled into topic files when the topic is active. Daily notes remain available for historical reference and time-based queries.

### Layer 5 (Optional): Time-Based Archival Layers

When enabled, weekly, monthly, and yearly summaries provide episodic recall — the ability to answer "what happened during week 15?" or "what did we accomplish in March?"

These layers are generated, read-only archives. They don't drive day-to-day context — topic files do that. They exist for historical queries and long-term recall.

- `memory/weekly/YYYY-WNN.md` — weekly summary, generated Sunday night
- `memory/monthly/YYYY-MM.md` — monthly summary, generated 1st of month
- `memory/yearly/YYYY.md` — yearly summary, generated Jan 1

Distillation is chronological, not categorical. Weekly summaries summarize the week's daily notes in time order. Topic categorization happens in topic files, not here.

---

## Configuration

### Presets

Set a preset in your workspace configuration. Presets provide sensible defaults; individual settings can be overridden.

**minimal** enables the routing table only. Topics, contacts, and time layers are all disabled.

**standard** (default) enables the routing table, topics, and contacts. Time layers are disabled.

**full** enables everything including time layers with distillation schedules. Weekly synthesis defaults to Sunday 2:00 AM, monthly to the 1st of each month at 2:00 AM, yearly to January 1 at 2:00 AM. All times use the configured timezone (default: system timezone). **Caveat:** if the `memory-wiki` plugin is enabled, its `syntheses/` pages and `reports/` dashboards overlap with time-based distillation — prefer **standard** unless you specifically want chronological archives in addition to wiki syntheses. See `references/configuration.md` for the full JSON format and all individual settings.

### Key Settings

- **preset** (string, default "standard") — base preset: minimal, standard, or full
- **routing_table_max_kb** (number, default 3) — max size for MEMORY.md in KB
- **topics** (bool, default true) — enable topic-based working memory files
- **contacts** (bool, default true) — enable contact files
- **time_layers** (bool, default false) — enable weekly/monthly/yearly archival layers
- **distillation.weekly.schedule** (string, default "0 2 * * 0") — cron expression for weekly synthesis
- **distillation.monthly.schedule** (string, default "0 2 1 * *") — cron expression for monthly synthesis
- **distillation.yearly.schedule** (string, default "0 2 1 1 *") — cron expression for yearly synthesis
- **distillation.timezone** (string, default system tz) — IANA timezone for cron schedules

---

## Behavioral Rules

### MEMORY.md Discipline

Never let MEMORY.md exceed routing_table_max_kb (default 3KB). Never write paragraphs or detailed status into MEMORY.md. When adding a new project or contact, add a one-line pointer to MEMORY.md and write the detail in the appropriate topic or contact file. Remove pointers when a project is completed or archived.

### Topic File Maintenance

Update topic files when new decisions or status changes occur. Keep the most recent information at the top of the file. Link back to daily notes for full context rather than duplicating content. Archive completed topic files by moving them to `topics/archive/`.

### Daily Note Distillation

After a session with substantive decisions or progress, distill key points into the relevant topic files. Don't duplicate — link to the daily note from the topic file. Daily notes are permanent intake records; never delete them to "clean up."

### Companion Skills and Plugins

Session isolation is handled by `agent-session-state` (separate skill). If installed, topic files and session state complement each other — topic files hold the authoritative project state, session files hold per-channel runtime context.

Governance is handled by `agent-provenance` (separate skill). If installed, provenance headers and TTL enforcement apply to instruction files, not to topic or contact files managed by this skill.

Durable knowledge compilation is handled by the bundled `memory-wiki` plugin. If enabled, this skill still owns MEMORY.md as the always-loaded routing table and `memory/topics/` as active-project working memory; `memory-wiki` owns the compiled knowledge vault (`entities/`, `concepts/`, `syntheses/`, `sources/`, `reports/`) with structured claims and dashboards. Do not duplicate content between topic files and wiki pages — topic files are short-horizon action state, wiki pages are durable belief artifacts with provenance. When `memory-wiki` is enabled, disable `time_layers` (or pick the **standard** preset) to avoid generating chronological archives that compete with wiki syntheses.

### Time-Based Layers (when enabled)

Weekly, monthly, and yearly files are generated archives — don't manually edit them. Distillation cron jobs use OpenClaw's built-in `cron` tool — they run as isolated agent sessions within the OpenClaw sandbox. No OS-level schedulers (crontab, systemd, launchd) are created or modified. If a cron job fails, daily notes remain the source of truth and synthesis can be re-run.

---

## Integration with OpenClaw Dreaming

If the Dreaming feature is enabled alongside this skill:

- **Dreaming promotes to MEMORY.md** — ensure promoted entries are pointers or constraints, not detailed content. If Dreaming promotes a detailed entry, move the detail to the appropriate topic file and replace the MEMORY.md entry with a pointer.
- **Daily notes feed both systems** — daily notes are intake for both topic file distillation and Dreaming's signal collection. No conflict.
- **No duplication** — if Dreaming handles promotion to MEMORY.md, the time-based distillation cron jobs should focus on archival summaries only, not promotion.

---

## Migration from v2.x

If upgrading from hierarchical-agent-memory v2.x:

1. Existing daily, weekly, monthly, and yearly directories are preserved as-is
2. The new `memory/topics/` directory is created alongside them
3. Suggest splitting current MEMORY.md content into a lean routing table (stays in MEMORY.md), topic files for each active project, and contact files for people
4. Ask user approval before making any changes to existing files

## Migration from v3.0.x to v3.1.0

v3.1.0 adds awareness of OpenClaw's bundled `memory-wiki` plugin. There are no schema changes and no automatic file modifications.

1. Existing topic files, contact files, daily notes, and time-based archives are left untouched
2. On first session after upgrade, the agent checks whether `plugins.entries.memory-wiki.enabled` is true in `openclaw.json`
3. If memory-wiki is enabled AND `time_layers` is currently true, the agent surfaces the overlap and offers to set `time_layers: false`. Existing `memory/weekly/`, `monthly/`, and `yearly/` files are historical content and are never deleted as part of this migration
4. If memory-wiki is not enabled, nothing changes and no prompt is shown
5. Ask user approval before changing any configuration

---

## Related Skills

- **agent-session-state** — Per-channel session isolation, WAL protocol, and working buffer management
- **agent-provenance** — File authorship, review tracking, and governance
