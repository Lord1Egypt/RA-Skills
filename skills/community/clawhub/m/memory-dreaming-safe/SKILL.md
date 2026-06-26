---
name: memory-dreaming
description: "Autonomous memory consolidation for OpenClaw agents — like REM sleep. Periodically gathers signal from daily logs, session transcripts, and learnings; consolidates into MEMORY.md; syncs structured knowledge to an Obsidian vault (or any markdown knowledge base); tracks plans; prunes stale entries. Use when: (1) setting up periodic memory maintenance, (2) manually triggering a dream cycle, (3) configuring Obsidian vault sync, (4) agent memory is getting noisy/contradictory and needs consolidation."
---

# Memory Dreaming

Autonomous memory consolidation ("dreaming") for OpenClaw agents. Runs as a cron job, consolidates scattered daily notes into curated long-term memory, and syncs structured knowledge to an Obsidian vault.

## When to Use

Use this skill when the user asks OpenClaw to:
- Reflect on stored memories and identify patterns
- Summarize recurring themes from past interactions
- Extract lessons from daily logs, errors, or learnings
- Consolidate noisy or contradictory memory entries
- Configure or set up periodic memory maintenance (cron)
- Manually trigger a memory consolidation cycle
- Sync structured knowledge to an Obsidian vault or markdown knowledge base

Do not use this skill for:
- Direct editing, deletion, or rewriting of memory files unless explicitly requested
- Processing sensitive personal data (credentials, secrets, medical/financial details) without explicit user consent
- Running shell commands or accessing files outside the configured memory workspace

## Core Principles

- **Read before Write:** Always analyze and understand current state before proposing any changes.
- **Diff before Apply:** Never modify files without presenting the proposed changes first.
- **Explicit Confirmation:** The user must explicitly approve ("Ja", "OK", "Bestätigt") before any write operation.
- **Sensitive Data Protection:** Automatically exclude credentials, secrets, and personal data unless explicitly authorized.
- **Interpretation, Not Fact:** AI-generated summaries are labeled as interpretations, not authoritative facts.
- **Transparency:** Log all actions and proposed changes so the user can audit what happened.

## Quick Start

1. Install: `clawhub install oryanmoshe/memory-dreaming`
2. Configure your vault path (optional): edit `dreaming-config.json` in your workspace
3. Set up the cron: run `scripts/setup-cron.sh`
4. Done — the agent dreams automatically every 8 hours

⚠️ The dream cycle will only apply changes after presenting a diff and receiving your confirmation.

To trigger a dream manually, tell the agent: "Run a dream cycle now."

## Workflow

### Step 1: Orient
- Read current memory state — MEMORY.md, recent daily logs, learnings, dreaming log
- Build a map of what exists and when it was last touched
- **Safety:** Only read, never modify in this phase

### Step 2: Gather Signal
- Search for high-value information added since the last dream
- Sources: daily logs, learnings, session transcripts, plan files
- **Efficiency:** Grep narrowly for high-signal patterns. Don't read full transcripts.

### Step 3: Consolidate (Analysis)
- Identify: duplicates, contradictions, stale entries, high-priority learnings
- **Proposal stage:** Prepare proposed changes but DO NOT apply yet
- Changes include: merge duplicates, convert relative dates, mark contradictions, promote learnings

### Step 4: Present Diff (Confirmation Gate)
- **BEFORE writing anything:** Present the proposed changes to the user
- Show: what would be merged, deleted, promoted, or modified
- Ask explicitly: "Soll ich diese Änderungen übernehmen?" / "Apply these changes?"
- **NEVER skip this step** — this is the critical safety gate

### Step 5: Apply (Only After Confirmation)
- Update MEMORY.md with confirmed changes only
- Delete contradicted facts only if explicitly approved
- Remove stale entries only if explicitly approved
- Promote learnings only if explicitly approved

### Step 6: Sync (Only After Confirmation)
- Push consolidated knowledge to external targets (Obsidian, etc.)
- **Safety:** Create/update notes but never delete existing vault content without confirmation
- Write dreaming log to document what changed

### Step 7: Verify
- Confirm all changes were applied correctly
- Log completion and token usage

## How It Works

The dream cycle has 4 phases, inspired by biological REM sleep and Claude Code's AutoDream:

### Phase 1: Orient
Read current memory state — MEMORY.md, recent daily logs, learnings, dreaming log. Build a map of what exists and when it was last touched.

### Phase 2: Gather Signal
Search for high-value information added since the last dream:
- **Daily logs** (`memory/YYYY-MM-DD.md`) since last dream
- **Learnings** (`.learnings/*.md`) — pending corrections, errors, best practices
- **Session transcripts** — grep for corrections ("actually...", "no that's wrong"), decisions ("let's do X"), proper nouns, preferences
- **Plan files** — scan workspace for `task_plan.md` files

Key: grep narrowly for high-signal patterns. Don't read full transcripts — that burns tokens for marginal value.

### Phase 3: Consolidate
Update MEMORY.md with gathered signal:
- **Merge** duplicate entries (same fact from 3 sessions → one entry)
- **Absolute dates** — convert "yesterday" → "2026-03-25"
- **Delete** contradicted facts (if preference changed, remove old one)
- **Remove** stale entries (references to deleted files, completed tasks)
- **Promote** high-priority learnings from `.learnings/` to MEMORY.md

### Phase 4: Sync
Push consolidated knowledge to external targets:
- **Obsidian vault** (opt-in) — create/update notes with tags, wikilinks, full depth
- **Plan tracking** — ensure every `task_plan.md` has a corresponding `Plans/<name>.md` in the vault
- **Dreaming log** — write what changed, tokens used, duration

## Gate

The cron fires on schedule but the dream cycle only executes if **≥6 hours** have passed since the last dream (checked via `dreaming-log.md` timestamp). This prevents wasted runs when nothing has changed.

Even when the gate passes, the skill still requires user confirmation before modifying any files (see Workflow Step 4).

## Configuration

Create `dreaming-config.json` in your workspace root to customize. All fields are optional — sensible defaults are used.

See `assets/dreaming-config.json` for the full schema with defaults.

Key options:
- `schedule` — cron expression (default: `"0 */8 * * *"`)
- `model` — which model runs the dream (default: `"anthropic/claude-sonnet-4-6"`)
- `gate.minHours` — minimum hours between dreams (default: `6`)
- `obsidian.enabled` — enable vault sync (default: `false`)
- `obsidian.vaultPath` — absolute path to Obsidian vault
- `delivery.mode` — `"none"` or `"announce"` changes to a channel
- `safety.requireConfirmation` — require user confirmation before applying changes (default: `true`)
  ⚠️ NEVER set this to `false` in production. The confirmation gate is the primary safety mechanism.

## Obsidian Sync Details

When enabled, the sync phase:
1. Compares MEMORY.md sections against existing vault notes
2. Creates new notes in configured subfolders (`People/`, `Projects/`, `Plans/`, `Tools/`)
3. Updates existing notes with new information (appends, doesn't overwrite)
4. Follows formatting rules: tags on first line, `[[wikilinks]]` throughout, full depth content
5. Tracks plans: scans for `task_plan.md` files → creates/updates `Plans/<name>.md`

For detailed sync behavior, see `references/obsidian-sync.md`.

## Manual Dream

Tell the agent any of these:
- "Run a dream cycle"
- "Consolidate memory"
- "Dream now"
- "Sync to obsidian"

The agent reads this skill and executes the 4-phase cycle immediately, ignoring the gate. The confirmation gate (Workflow Step 4) still applies.

## Setup Script

```bash
# Creates the cron job in OpenClaw
bash scripts/setup-cron.sh
```

The script reads `dreaming-config.json` (or uses defaults) and creates an isolated agentTurn cron job. See `scripts/setup-cron.sh` for details.

## Architecture

For the detailed 4-phase architecture, design decisions, and how this compares to Claude Code AutoDream, see `references/architecture.md`.

## Safety & Boundaries

### NEVER
- Never write files without explicit user confirmation
- Never execute commands without explicit user confirmation
- Invent memories or treat inferred patterns as facts
- Delete, overwrite, or rewrite memory files without **explicit user confirmation**
- Store sensitive personal data (credentials, secrets, medical/financial details, private third-party information) unless the user **explicitly requests it and it is appropriate**
- Run shell commands or access files outside the configured memory workspace unless explicitly requested
- Auto-execute the dream cycle without the 6-hour gate check (cron only)
- Treat AI-generated summaries as authoritative facts without labeling them as interpretations

### ALWAYS
- Confirm before write: Always present proposed changes and ask for explicit user confirmation before applying
- Confirm before execute: Never run commands or scripts without user approval
- Present proposed changes as a diff or structured list before applying
- Ask for explicit confirmation: "Soll ich diese Änderungen übernehmen?"
- Label AI-generated content clearly ("Zusammenfassung", "Interpretation", "Vorschlag")
- Respect the 6-hour gate between automatic dream cycles
- Backup MEMORY.md before making changes (if possible)
- Log all changes in dreaming-log.md with timestamp and rationale

### WHEN IN DOUBT
- Prefer read-only analysis over automatic modification
- Ask the user before proceeding with uncertain changes
- Document uncertainty in the dreaming log

## Boundaries

This skill **MAY**:
- Summarize, cluster, and suggest improvements to memory content
- Identify contradictions or stale entries
- Propose structural improvements (better tagging, linking, organization)
- Sync structured knowledge to external vaults (after confirmation)

This skill **MUST NOT**:
- Autonomously modify long-term memory without user confirmation
- Create behavioral rules that override user intent or system/developer instructions
- Delete source files (daily logs, session transcripts)
- Modify source code or project files
- Access files outside the configured memory workspace
- Store or process sensitive data without explicit user consent

## Examples

### Example 1: Pattern Recognition (Read-Only)

**User:** *"Review my memories and tell me what patterns you notice."*

**Skill:**
1. Reads relevant memory notes (Phase 1-2)
2. Analyzes recurring themes, preferences, unresolved tasks
3. Labels each finding: **Fact** / **Pattern** / **Suggestion**
4. **Presents summary without modifying anything**
5. "Ich habe folgende Muster erkannt: [...] Soll ich diese als zusammenfassende Notiz speichern?"

**Safety:** This is read-only until the user explicitly asks to save.

### Example 2: Manual Consolidation (Write After Confirmation)

**User:** *"Run a dream cycle now."*

**Skill:**
1. Executes Phase 1-3: Orient, Gather, Consolidate (analysis only)
2. **Phase 4 (Confirmation Gate):** Presents proposed changes:
   - Merge 3 duplicate entries about GPU-Transkription
   - Update "Andreas bevorzugt Azure TTS" (alte Info, jetzt Coqui auch installiert)
   - Promote "Ansible auf macmini103 blockiert" aus Learnings
3. **Asks:** "Ich schlage folgende Änderungen vor: [...] Soll ich MEMORY.md aktualisieren?"
4. **On "Ja":** Applies changes (Phase 5-7)
5. **On "Nein":** Aborts, logs user rejection, suggests alternative

### Example 3: Sensitive Data Encountered

**User:** *"Review everything from last week."*

**Skill:**
1. Scans logs and finds: reference to `ansible_ssh_cred.xml`, password discussion
2. **Stops:** "Ich habe Hinweise auf Zugangsdaten in den Logs gefunden. Aus Sicherheitsgründen überspringe ich diese Abschnitte. Soll ich nur die nicht-sensiblen Teile zusammenfassen?"
3. **Proceeds only** after user confirmation with explicit scope

**Safety:** Sensitive data detection triggers automatic exclusion + user confirmation.

## What This Skill Does NOT Do

- Does not replace QMD indexing (QMD handles search, this handles consolidation)
- Does not delete source files (daily logs are never removed, only consolidated from)
- Does not modify source code or project files
- Does not run without explicit setup (cron must be created via setup script)
