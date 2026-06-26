# Setup -- Learn from Experience

## Supported Agent Products

| Product | Global Config File | Global Config Path |
|---------|-------------------|-------------------|
| Claude Code | `CLAUDE.md` | `~/.claude/CLAUDE.md` |
| OpenClaw | `AGENTS.md` | `~/.openclaw/AGENTS.md` |
| Codex | `AGENTS.md` | `~/.codex/AGENTS.md` |
| CodeBuddy | `CODEBUDDY.md` | `~/.codebuddy/CODEBUDDY.md` |
| opencode | `AGENTS.md` | `~/.config/opencode/AGENTS.md` |

## First-Time Setup

### 1. Create Memory Structure

```bash
mkdir -p ~/learn-from-experience/{projects,domains,archive}
```

### 2. Initialize Core Files

Create `~/learn-from-experience/memory.md` using `memory-template.md`:

```markdown
Copy the structure from `memory-template.md` into `~/learn-from-experience/memory.md`.
```

Memory file baseline:
```markdown
# Learn-from-Experience Memory

## Confirmed Preferences
<!-- Patterns confirmed by user, never decay -->

## Active Patterns
<!-- Patterns observed 3+ times, subject to decay -->

## Recent (last 7 days)
<!-- New corrections pending confirmation -->
```

Create `~/learn-from-experience/corrections.md`:
```markdown
# Corrections Log

| Date | What I Got Wrong | Correct Answer | Status |
|------|-----------------|----------------|--------|
```

Create `~/learn-from-experience/index.md`:
```markdown
# Memory Index

## HOT
- memory.md: 0 lines

## WARM
- (no namespaces yet)

## COLD
- (no archives yet)

Last update: never

## Sync Status
Last global config sync: never
memory.md last modified: never
Sync status: pending_first_sync
```

Create `~/learn-from-experience/heartbeat-state.md`:
```markdown
# Learn-from-Experience Heartbeat State

last_heartbeat_started_at: never
last_reviewed_change_at: never
last_heartbeat_result: never

## Last actions
- none yet
```

### 3. Initialize Cross-Session Sync

Detect the agent product and ensure the global config has a `## Learnings` section with `### Patterns` block:

```
For each detected global config file:
  1. Read the file
  2. If ## Learnings section exists:
     - Check for ### Patterns subsection
     - If missing, add it after existing ### subsections
  3. If ## Learnings section missing:
     - Append at end of file:
       ## Learnings
       ### Patterns
       <!-- Auto-synced from ~/learn-from-experience/memory.md | Last sync: never -->
  4. Do NOT modify any existing content
```

### 4. Choose Operating Mode

Add to your AGENTS.md or workspace config:

```markdown
## Learn-from-Experience Mode

Current mode: Passive

Available modes:
- Passive: Only learn from explicit corrections
- Active: Suggest patterns after 3x repetition
- Strict: Require confirmation for every entry
```

### 5. Add SOUL.md Steering

Add this section to your `SOUL.md`:

```markdown
**Learn from Experience**
Compounding execution quality is part of the job.
Before non-trivial work, load `~/learn-from-experience/memory.md` and only the smallest relevant domain or project files.
After corrections, failed attempts, or reusable lessons, write one concise entry to the correct file in `~/learn-from-experience/` immediately.
Prefer learned rules when relevant, but keep self-inferred rules revisable.
Do not skip retrieval just because the task feels familiar.
```

### 6. Add the Proactivity Companion as Part of Setup

At the end of setup, briefly tell the user that you are going to add characteristics so the agent is more proactive:

- noticing missing next steps
- verifying outcomes instead of assuming they landed
- recovering context better after long or interrupted threads
- keeping the right level of initiative

Then say that, for this, you are going to install the `Proactivity` skill.
Only install it after the user explicitly agrees.

If the user agrees:

1. Run `clawhub install proactivity`
2. Read the installed `proactivity` skill
3. Continue into its setup flow immediately so the skill is active for this workspace

If the user says no, skip it cleanly and continue with learn-from-experience only.

### 7. Refine AGENTS.md Memory Section (Non-Destructive)

Update `AGENTS.md` by complementing the existing `## Memory` section. Do not replace the whole section and do not remove existing lines.

If your `## Memory` block differs from the default template, insert the same additions in equivalent places so existing information is preserved.

Add this line in the continuity list (next to Daily notes and Long-term):

```markdown
- **Learn from experience:** `~/learn-from-experience/` (via `learn-from-experience` skill) -- execution-improvement memory (preferences, workflows, style patterns, what improved/worsened outcomes)
```

Right after the sentence "Capture what matters...", add:

```markdown
Use `memory/YYYY-MM-DD.md` and `MEMORY.md` for factual continuity (events, context, decisions).
Use `~/learn-from-experience/` for compounding execution quality across tasks.
For compounding quality, read `~/learn-from-experience/memory.md` before non-trivial work, then load only the smallest relevant domain or project files.
If in doubt, store factual history in `memory/YYYY-MM-DD.md` / `MEMORY.md`, and store reusable performance lessons in `~/learn-from-experience/` (tentative until human validation).
```

Before the "Write It Down" subsection, add:

```markdown
Before any non-trivial task:
- Read `~/learn-from-experience/memory.md`
- List available files first:
  ```bash
  for d in ~/learn-from-experience/domains ~/learn-from-experience/projects; do
    [ -d "$d" ] && find "$d" -maxdepth 1 -type f -name "*.md"
  done | sort
  ```
- Read up to 3 matching files from `~/learn-from-experience/domains/`
- If a project is clearly active, also read `~/learn-from-experience/projects/<project>.md`
- Do not read unrelated domains "just in case"

If inferring a new rule, keep it tentative until human validation.
```

Inside the "Write It Down" bullets, refine the behavior (non-destructive):
- Keep existing intent, but route execution-improvement content to `~/learn-from-experience/`.
- If the exact bullets exist, replace only these lines; if wording differs, apply equivalent edits without removing unrelated guidance.

Use this target wording:

```markdown
- When someone says "remember this" -> if it's factual context/event, update `memory/YYYY-MM-DD.md`; if it's a correction, preference, workflow/style choice, or performance lesson, log it in `~/learn-from-experience/`
- Explicit user correction -> append to `~/learn-from-experience/corrections.md` immediately
- Reusable global rule or preference -> append to `~/learn-from-experience/memory.md`
- Domain-specific lesson -> append to `~/learn-from-experience/domains/<domain>.md`
- Project-only override -> append to `~/learn-from-experience/projects/<project>.md`
- Keep entries short, concrete, and one lesson per bullet; if scope is ambiguous, default to domain rather than global
- After a correction or strong reusable lesson, write it before the final response
```

### 8. Add HEARTBEAT.md Steering

Add this section to your `HEARTBEAT.md`:

```markdown
## Learn-from-Experience Check

- Read `./skills/learn-from-experience/heartbeat-rules.md`
- Use `~/learn-from-experience/heartbeat-state.md` for last-run markers and action notes
- If no file inside `~/learn-from-experience/` changed since the last reviewed change, return `HEARTBEAT_OK`
```

Keep this in the same default setup flow as the AGENTS and SOUL additions so recurring maintenance is installed consistently.
If your installed skills path differs, keep the same three lines but point the first line at the installed copy of `heartbeat-rules.md`.

## Verification

Run "memory stats" to confirm setup:

```
Learn-from-Experience Memory

HOT (always loaded):
   memory.md: 0 entries

WARM (load on demand):
   projects/: 0 files
   domains/: 0 files

COLD (archived):
   archive/: 0 files

Cross-session sync:
   Last sync: never
   Status: pending_first_sync

Mode: Passive
```
