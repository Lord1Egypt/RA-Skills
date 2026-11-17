---
name: hierarchical-agent-memory
description: >-
  Scalable memory architecture with hybrid topic-based working memory and
  optional time-based episodic recall. Keeps MEMORY.md a lean routing table,
  adds topic files for active projects and contact files for people, and
  distills OpenClaw's daily notes into them. Use when the agent needs durable,
  organized long-term memory that survives compaction and scales across
  projects, contacts, and time horizons. Run /hierarchical_agent_memory status
  to check the current layout. For per-channel session notes, install the
  companion skill agent-session-state. Upgrading from v3.1 or earlier? The
  agent will offer to move memory/daily/ notes to where OpenClaw reads them.
license: MIT-0
compatibility: "OpenClaw 2026.4.x or later. Requires the memory-core plugin."
user-invocable: true
metadata:
  openclaw:
    requires:
      bins: ["openclaw"]
    paths:
      write: ["MEMORY.md", "memory/"]
      read: ["MEMORY.md", "USER.md", "memory/"]
  version: "3.2.0"
  clawhub: {"category": "memory", "tags": ["memory", "hierarchy", "topics", "distillation"]}
---

# Hierarchical Agent Memory v3.2.0

Agents that run across multiple projects, contacts, and time horizons need memory that scales. Without structure, MEMORY.md grows into a single bloated document that is truncated at the bootstrap budget and triggers lost-in-the-middle degradation long before that. This skill organizes agent memory into a hybrid architecture: a lean MEMORY.md routing table, topic-based working memory for active projects, contact files for people, and optional time-based archival layers for episodic recall.

## At a glance

OpenClaw already provides the memory runtime. It injects `MEMORY.md` and `USER.md` at the start of eligible private sessions, keeps daily notes at `memory/YYYY-MM-DD.md`, preloads today's and yesterday's notes on a bare `/new` or `/reset`, indexes everything under `memory/` for `memory_search` and `memory_get`, runs a silent memory flush before compaction, and, from 2026.8.1, runs a nightly dreaming sweep that promotes durable items from daily notes into `MEMORY.md`. If your MEMORY.md is small and you work on one or two things, that is enough and you do not need this skill.

This skill adds the curation discipline that the runtime does not: a rule that MEMORY.md stays a routing table of pointers and constraints, a topic file per active project that holds the authoritative state, a contact file per person, and a distillation habit that moves decisions out of daily notes into those files. Nothing here replaces search, flush, dreaming, or the wiki. The skill tells the agent where things belong and keeps the always-loaded file small.

## Slash commands

The skill is user-invocable. Where your channel registers skill commands natively (`commands.nativeSkills`, on by default where supported), the command is the skill name with characters outside letters, digits, and underscores replaced, so it appears as `/hierarchical_agent_memory`. The generic form `/skill hierarchical-agent-memory <command>` always works. Skill commands route through the model, so the agent follows the matching section of this file. Supported commands:

- `status` (default when no argument is given) reports the current preset, the size of MEMORY.md against `routing_table_max_kb`, the number of topic and contact files, the newest daily note, and whether `memory/daily/` still holds unmigrated notes.
- `setup` starts or repeats the onboarding conversation below.
- `migrate` runs the daily-note migration described under Migration from v3.1.x, with approval.
- `distill` reads today's and yesterday's daily notes plus any session file for this conversation and proposes updates to topic and contact files. Nothing is written until the user approves.
- `archive <topic>` moves `memory/topics/<topic>.md` to `memory/topics/archive/` and removes its pointer from MEMORY.md, after confirmation.

## Onboarding

When this skill is installed or updated, initiate a setup conversation with the user before applying any memory structure changes. Do not silently create directories or files. See `references/onboarding-guide.md` for the full script.

**Step 1: Greet and explain.** Tell the user this skill organizes agent memory into a hybrid structure with topic-based working memory and optional time-based archival layers. Keep it to 2-3 sentences.

**Step 2: Ask about preset preference.** Present three presets:

- **minimal** keeps MEMORY.md as a routing table and uses OpenClaw's daily notes as they are. Best for simple setups and single-project agents.
- **standard** (default) adds topic files and contact files. Best for multi-project agents and teams.
- **full** adds weekly, monthly, and yearly distillation layers. Only for agents that need chronological archives in addition to what OpenClaw already keeps. If the bundled `memory-wiki` plugin is enabled, or if dreaming is on (the default from 2026.8.1), prefer **standard**: wiki `syntheses/` and dreaming's phase reports under `memory/dreaming/` already cover the same ground.

If the user says "just use defaults," apply standard and move on.

Companion skills and plugins: for per-conversation decision notes, install `agent-session-state`. For file authorship and review tracking, install `agent-provenance`. If the bundled `memory-wiki` plugin is enabled, it sits beside this skill: this skill owns the always-loaded MEMORY.md routing table and `memory/topics/` working memory; `memory-wiki` owns the compiled knowledge vault. All are independent.

**Step 3: Ask targeted follow-up questions based on preset.** For standard or full: ask whether to create starter topic files from existing MEMORY.md content, and whether the user also uses companion skills. For full only: first check whether `memory-wiki` is enabled by inspecting `plugins.entries.memory-wiki.enabled` in `openclaw.json`. If it is, warn about the overlap and offer **standard**. If the user still wants `full`, ask what timezone distillation jobs should use (default: system timezone) and what time weekly synthesis should run (default: Sunday 2:00 AM).

**Step 4: Apply configuration.** Create the directory structure and write configuration to the workspace. Confirm what was created. Offer to run an initial migration if existing MEMORY.md content should be split into topic files.

**Step 5: On update from v2.x.** If `memory/weekly/` exists but `memory/topics/` does not, the user is upgrading from v2.x. Tell them v3 adds topic-based working memory alongside the existing structure. Offer to scan MEMORY.md and daily notes to suggest topic files. Do NOT delete or reorganize existing files without explicit approval.

**Step 6: On update from v3.0.x.** If the workspace config has `time_layers: true` AND `plugins.entries.memory-wiki.enabled` is true, surface the overlap and offer to set `time_layers: false`, leaving existing archive files untouched. If `memory-wiki` is not enabled, say nothing.

**Step 7: On update from v3.1.x or earlier.** If `memory/daily/` exists, the daily notes are in a directory OpenClaw does not read. Explain this in two sentences and offer the migration under Migration from v3.1.x. Do not move anything until the user approves.

---

## Memory Architecture

### Layer 1: MEMORY.md, the routing table

OpenClaw injects MEMORY.md into the system prompt of the main, private session only. Subagent, cron, group, and channel sessions omit it. The runtime truncates the injected copy at `bootstrapMaxChars` (20,000 characters by default), but lost-in-the-middle degradation sets in far earlier, so this skill keeps the hand-maintained part under `routing_table_max_kb` (3KB by default). It contains:

- Active project pointers, one line each, linking to topic files
- Key contact pointers, linking to contact files
- Infrastructure pointers, linking to config or endpoint files
- Active constraints and hard stops, the ONLY "content" that belongs here

MEMORY.md is a routing table, not a summary. If you're tempted to write a paragraph in MEMORY.md, it belongs in a topic file instead.

**Dreaming-managed entries.** From OpenClaw 2026.8.1, dreaming is on by default and promotes qualified items into MEMORY.md. Its entries carry trailing markers such as `<!-- trigger: … -->`, `<!-- importance: N -->`, and a `Source: path#Lx-Ly` reference, and the deep phase may rewrite them during consolidation. Treat those entries as machine-managed: never edit, reword, or delete them by hand, and do not count them toward `routing_table_max_kb`. If a promoted entry duplicates something a topic file already holds, leave the entry alone and make sure the topic file is the richer of the two. If dreaming entries push the whole file toward the bootstrap budget, tell the user and offer two choices: keep dreaming and accept a larger MEMORY.md, or set `plugins.entries.memory-core.config.dreaming.enabled: false` so this skill's distillation is the only promotion path. Do not change that setting yourself.

**Security note:** MEMORY.md is injected into the model context of every main session. Never put secrets, API keys, passwords, or sensitive PII in MEMORY.md or any file it points to. Store credentials in environment variables or `.env` files (excluded from memory). Active Constraints entries such as "do not raise X" are acceptable; they are behavioral directives, not sensitive data.

Example MEMORY.md:

```markdown
## Active Projects
- [BlueCat MCP Testing](memory/topics/bluecat-mcp.md) — BDDS integration, Bug #21 open
- [RPZ Article](memory/topics/rpz-article.md) — draft in progress

## Key Contacts
- [Jane Doe](memory/contacts/jane-doe.md) — BlueCat UX

## Active Constraints
- DO NOT RAISE: attorney call issue
- Merge freeze after 2026-04-15
```

### Layer 2: Topic files, the working memory

`memory/topics/<name>.md` files are the primary working layer. Each file is the authoritative source for one project, workstream, or subject area. They are never injected at session start; the agent reads them when MEMORY.md points at them, and `memory_search` indexes them because they live under `memory/`.

Structure topic files with the most recent information at the top, dated entries within the file, and links to relevant daily notes for full context.

**When to create a new topic file:** a project spans more than 2-3 daily notes, you find yourself repeatedly searching for the same subject, or the user explicitly asks to track something.

**When to update a topic file:** new decisions or status changes, after distilling relevant content from daily notes, or when correcting outdated information (update in place, don't append).

If the work happens inside a Git repository and your OpenClaw version annotates project-scoped memory (`<!-- project: … -->` trailing comments), keep that annotation on entries you copy into a topic file so ranking still favors them in that repository.

### Layer 3: Contact files

`memory/contacts/<name>.md` files store information about people: role, email, context for how you interact with them, and when you last interacted. OpenClaw has no native equivalent. Relationship facts that change how the *user* should be assisted belong in `USER.md` as directives, not here; contact files describe third parties.

### Layer 4: Daily notes, the intake layer

Daily notes are OpenClaw's own files at `memory/YYYY-MM-DD.md`, directly under `memory/`. This skill does not relocate them, because every native reader and writer expects them there: the first-turn preload on a bare `/new` or `/reset` reads only that directory, the pre-compaction memory flush appends there, the bundled `session-memory` hook writes `memory/YYYY-MM-DD-HHMM.md` beside them, and dreaming ingests dated files from there. Versions before v3.2 of this skill used `memory/daily/`; see Migration from v3.1.x.

Daily notes are intake, not archive, and they are not loaded all the time. Only today's and yesterday's notes are preloaded, and only on a fresh session; everything older is reachable through `memory_search` and `memory_get`. That is the point: history you can refer to, without paying for it on every turn. Important information should be distilled into topic files while the topic is active. Never delete daily notes to "clean up"; they are the permanent intake record and dreaming's source material.

Slugged same-day files written by the `session-memory` hook count as daily notes for distillation. Dreaming phase reports under `memory/dreaming/` are generated output and are not intake.

### Layer 5 (optional): Time-based archival layers

When enabled, weekly, monthly, and yearly summaries provide episodic recall: "what happened during week 15?" or "what did we accomplish in March?"

- `memory/weekly/YYYY-WNN.md`, generated Sunday night
- `memory/monthly/YYYY-MM.md`, generated on the 1st of the month
- `memory/yearly/YYYY.md`, generated January 1

These layers are generated, read-only archives. They don't drive day-to-day context; topic files do that. Distillation is chronological, not categorical. Be aware of two native overlaps before enabling them: `memory-wiki` produces `syntheses/` pages and `reports/` dashboards, and dreaming produces per-phase daily reports under `memory/dreaming/` plus a diary in `DREAMS.md`. Most users on 2026.8.1 or later do not need this layer.

### Where things belong

OpenClaw now defines a split between files, and this skill follows it. A stable preference, communication-style rule, relationship fact, or active-project fact that changes how the user should be assisted goes in `USER.md`, written as a dated imperative directive in OpenClaw's own format (see the User model docs). A durable non-profile fact, decision, or constraint goes in MEMORY.md as a one-line pointer or constraint, with the detail in a topic file. Running context and observations go in today's daily note. An event-conditioned future action ("when someone mentions the launch, remind me to…") goes to the `intent` tool where your version provides it, not to Active Constraints. An exact-time or recurring action goes to `automations` (named `cron` before 2026.8.1). Active Constraints in MEMORY.md are for standing prohibitions and hard stops only.

---

## Configuration

### Presets

Set a preset in your workspace configuration. Presets provide sensible defaults; individual settings can be overridden.

**minimal** enables the routing table only. Topics, contacts, and time layers are all disabled.

**standard** (default) enables the routing table, topics, and contacts. Time layers are disabled.

**full** enables everything including time layers with distillation schedules. Weekly synthesis defaults to Sunday 2:00 AM, monthly to the 1st of each month at 2:00 AM, yearly to January 1 at 2:00 AM, all in the configured timezone (default: system timezone). See `references/configuration.md` for the full JSON format and all individual settings.

### Key Settings

- **preset** (string, default "standard"): base preset: minimal, standard, or full
- **routing_table_max_kb** (number, default 3): max size of the hand-maintained part of MEMORY.md in KB, excluding dreaming-managed entries
- **topics** (bool, default true): enable topic-based working memory files
- **contacts** (bool, default true): enable contact files
- **time_layers** (bool, default false): enable weekly/monthly/yearly archival layers
- **distillation.weekly.schedule** (string, default "0 2 * * 0"): cron expression for weekly synthesis
- **distillation.monthly.schedule** (string, default "0 2 1 * *"): cron expression for monthly synthesis
- **distillation.yearly.schedule** (string, default "0 2 1 1 *"): cron expression for yearly synthesis
- **distillation.timezone** (string, default system tz): IANA timezone for schedules

There is deliberately no setting for the daily-note directory. OpenClaw owns that path.

---

## Behavioral Rules

### MEMORY.md Discipline

Never let the hand-maintained part of MEMORY.md exceed routing_table_max_kb. Never write paragraphs or detailed status into MEMORY.md. When adding a new project or contact, add a one-line pointer to MEMORY.md and write the detail in the appropriate topic or contact file. Remove pointers when a project is completed or archived. Leave dreaming-managed entries untouched. Use `/context detail` or `openclaw doctor` to see raw versus injected sizes when checking the budget.

### Topic File Maintenance

Update topic files when new decisions or status changes occur. Keep the most recent information at the top of the file. Link back to daily notes for full context rather than duplicating content. Archive completed topic files by moving them to `memory/topics/archive/`.

### Daily Note Distillation

After a session with substantive decisions or progress, distill key points into the relevant topic files. Don't duplicate; link to the daily note from the topic file. When writing to today's daily note during the pre-compaction memory flush, append only new text; recent releases reject replayed paragraphs during the flush.

### Companion Skills and Plugins

Per-conversation notes are handled by `agent-session-state`. If installed, topic files and session files complement each other: topic files hold the authoritative project state, session files hold what one conversation decided.

Governance is handled by `agent-provenance`. If installed, provenance headers and review cadence apply to instruction files; topic and contact files are agent-authored and need only the staleness check that skill provides.

Durable knowledge compilation is handled by the bundled `memory-wiki` plugin (available since 2026.4.7, must be enabled). This skill still owns MEMORY.md and `memory/topics/`; `memory-wiki` owns the compiled vault. Do not duplicate content between topic files and wiki pages. When `memory-wiki` is enabled, keep `time_layers` off.

### Time-Based Layers (when enabled)

Weekly, monthly, and yearly files are generated archives; don't manually edit them. Distillation jobs use OpenClaw's built-in `automations` tool (named `cron` before 2026.8.1) and run as isolated agent sessions within the OpenClaw sandbox. No OS-level schedulers are created or modified. Each job is created only after the user agrees, is named `hierarchical-agent-memory <weekly|monthly|yearly> synthesis`, and can be listed, disabled, or removed with `openclaw automations list|disable|remove` (`openclaw cron` on releases before 2026.8.1). If a job fails, daily notes remain the source of truth and synthesis can be re-run.

---

## Integration with OpenClaw Dreaming

Dreaming is opt-in on releases before 2026.8.1 and on by default from 2026.8.1 (`plugins.entries.memory-core.config.dreaming.enabled`). When it runs alongside this skill:

- **Dreaming promotes to MEMORY.md and only there.** Its entries are machine-managed (see Layer 1). The agent does not reword them, move them into topic files, or delete them. If the user wants a promoted entry gone, point them to `openclaw memory forget` (2026.8.1 or later) or to editing the file themselves.
- **Daily notes feed both systems.** Daily notes are intake for this skill's distillation and for dreaming's signal collection. No conflict, provided the notes are at `memory/YYYY-MM-DD.md`.
- **Topic files stay richer than promoted entries.** When dreaming promotes something a topic file covers, the topic file remains the authoritative source; the MEMORY.md entry is a hint, not a duplicate to reconcile.
- **Time layers are redundant with dreaming reports.** Dreaming writes `memory/dreaming/<phase>/YYYY-MM-DD.md` and `DREAMS.md`. Prefer **standard** over **full** when dreaming is on.

---

## Version notes

This skill is written for whichever OpenClaw release the user actually runs, including the monthly extended-stable lines (`2026.N.35`). Check `openclaw --version` once per session when a version-dependent instruction matters.

- On every supported release, daily notes live at `memory/YYYY-MM-DD.md`, MEMORY.md and USER.md are bootstrap files with the limits above, and user-invocable skill commands work.
- From 2026.8.1: dreaming is on by default, the scheduler tool and CLI are `automations` (`cron` remains an alias), transcripts live in SQLite, and `openclaw memory forget` exists.
- Before 2026.8.1: dreaming is opt-in, the scheduler is `cron`, and `HEARTBEAT.md` and `TOOLS.md` are still live workspace files.
- On recent mainline releases the `intent` tool (standing intents), the `goal` command, and the directive-based USER.md format exist. Detect them by presence rather than by version: if the `intent` tool is not in the tool list, keep event-conditioned reminders in a topic file with a review date.

---

## Migration from v2.x

If upgrading from hierarchical-agent-memory v2.x, see `references/migration-v2-to-v3.md`. Existing weekly, monthly, and yearly directories are preserved; `memory/topics/` is created alongside them; MEMORY.md is split into a routing table with user approval.

## Migration from v3.0.x to v3.1.0

v3.1.0 adds awareness of the bundled `memory-wiki` plugin. No schema changes and no automatic file modifications. If `memory-wiki` is enabled and `time_layers` is true, the agent surfaces the overlap and offers to set `time_layers: false`; archive files are never deleted.

## Migration from v3.1.x to v3.2.0

v3.2.0 moves daily notes from `memory/daily/` to OpenClaw's own location, `memory/YYYY-MM-DD.md`. Until they are moved, the preload on `/new`, the memory flush, the session-memory hook, and dreaming all operate on a directory that has nothing in it, while the skill's notes sit where nothing native reads them.

1. Detect: `memory/daily/` exists and contains `YYYY-MM-DD.md` files.
2. Propose: list how many files would move, and whether any date already has a note at `memory/YYYY-MM-DD.md`. Get approval before touching anything.
3. Move each `memory/daily/YYYY-MM-DD.md` to `memory/YYYY-MM-DD.md`. If the workspace is a git repository, use `git mv` so history follows the file. If a root note for the same date already exists, append the `memory/daily/` content to the root note under a `## Migrated from memory/daily/` heading rather than overwriting either one, then delete the source.
4. Leave `memory/daily/` in place if it still holds anything else; remove it once empty, with confirmation.
5. Update any pointers in MEMORY.md, topic files, or AGENTS.md that reference `memory/daily/`. If AGENTS.md tells the agent to read `memory/daily/YYYY-MM-DD.md` at startup, tell the user that line is now wrong and show the replacement; do not edit AGENTS.md without approval.
6. Re-run `/hierarchical_agent_memory status` to confirm the newest daily note is at the root.

Nothing is loaded that was not loaded before: older notes remain on-demand through `memory_search`, and only today's and yesterday's notes are preloaded, and only on a fresh session.

---

## Related Skills

- **agent-session-state**: per-conversation decision notes with a Write-Ahead Log protocol
- **agent-provenance**: file authorship, review tracking, and governance
