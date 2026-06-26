# Dream Prompt

This is the instruction set sent to the isolated cron agent. It must be self-contained — the agent wakes up with no context and only this prompt + workspace access.

---

## The Prompt

```
AUTONOMOUS DREAM CYCLE — Memory consolidation.

You are running a memory consolidation cycle ("dreaming"). You have no prior context — read files to orient yourself.

IMPORTANT: You are an isolated agent. Do NOT message anyone. Do NOT announce anything. Just read, consolidate, write, and reply NO_REPLY.

## GATE CHECK (do this first)

Read memory/dreaming-log.md (if it exists). Find the most recent "## YYYY-MM-DD HH:MM" heading.
Parse the date. Calculate hours since that timestamp.
If the last dream was less than 6 hours ago, reply NO_REPLY and stop immediately.
If the file doesn't exist or has no entries, proceed (this is the first dream).

## PHASE 1: ORIENT

Read these files in order:
1. Read `MEMORY.md` — understand what's already in long-term memory
2. Run: `ls -lt memory/*.md | head -10` — identify recent daily logs
3. Run: `ls .learnings/*.md` — check what learning files exist
4. Read `dreaming-config.json` (workspace root) — get Obsidian vault path and settings
5. Read `memory/dreaming-log.md` — find the date of the last dream to know what's "new"

Record the last dream date. Everything after that date is "new signal."

## PHASE 2: GATHER SIGNAL

### 2a: Read daily logs since last dream
For each `memory/YYYY-MM-DD.md` file dated AFTER the last dream date, read it fully. Extract:
- New facts, decisions, preferences stated by the user
- People mentioned with new context (role, team, relationship)
- Projects with status changes (started, completed, blocked)
- Tools configured, installed, or discovered
- Corrections (things that were wrong and got fixed)
- New plans created or plan phases completed

### 2b: Grep session transcripts for corrections and decisions
Run these greps to find high-signal sessions — only read the MATCHED lines, not full files:

```bash
# Find sessions with corrections (highest value signal)
grep -l "actually\|no.*that's wrong\|not.*it's\|I meant\|that's outdated" ~/.openclaw/agents/main/sessions/*.jsonl 2>/dev/null | tail -5

# Find sessions with decisions
grep -l "let's do\|go with\|use.*instead\|we decided\|the plan is" ~/.openclaw/agents/main/sessions/*.jsonl 2>/dev/null | tail -5
```

For each file found, grep the specific pattern to extract just the relevant context line. Do NOT read entire session files.

### 2c: Check learnings
Read `.learnings/LEARNINGS.md` — note entries with `Status: pending` (especially `Priority: high`).
Read `.learnings/ERRORS.md` — note entries with `Status: pending`.

### 2d: Scan for plans
Run:
```bash
find ~/.openclaw/workspace -name "task_plan.md" -not -path "*/node_modules/*" -not -path "*/skills/*/task_plan.md" 2>/dev/null
```
Also check:
```bash
find ~/.openclaw/workspace/plans -name "task_plan.md" 2>/dev/null
```

For each task_plan.md found, read just the first 30 lines to get the plan name, status, and phase summary.

## PHASE 3: CONSOLIDATE

Update MEMORY.md with gathered signal. Rules:

1. **Don't duplicate** — if a fact already exists in MEMORY.md, skip it
2. **Resolve contradictions** — if new info contradicts old info, keep the newer version and delete the old
3. **Absolute dates** — convert any "yesterday", "today", "last week" to actual dates based on the source file's date
4. **Remove stale** — if something references a file that doesn't exist, a task that's done, or a tool that was replaced, remove it
5. **Promote learnings** — for each high-priority pending learning in .learnings/, add the key insight to the appropriate MEMORY.md section and update the learning's status to "promoted"
6. **Be surgical** — only edit sections that actually changed. Don't rewrite the whole file.
7. **Update Active Plans table** — if MEMORY.md has an "Active Plans" section, update it with current plan statuses from the task_plan.md files you scanned

## PHASE 4: SYNC TO OBSIDIAN

Read `dreaming-config.json` — check if `targets.obsidian.enabled` is `true`. If not, skip to the Dreaming Log section.

If enabled, read `targets.obsidian.vaultPath` to get the vault path.

### 4a: Plan Tracking (CRITICAL — this is the primary sync responsibility)

For EACH task_plan.md found in Phase 2d:

1. **Derive the plan name** from the parent directory:
   ```bash
   # Example: ~/.openclaw/workspace/shapes-machina/task_plan.md → "shapes-machina"
   # Example: ~/.openclaw/workspace/plans/memory-dreaming/task_plan.md → "memory-dreaming"
   dirname /path/to/task_plan.md | xargs basename
   ```

2. **Check if Obsidian note exists:**
   ```bash
   ls "<vaultPath>/Plans/<plan-name>.md" 2>/dev/null
   ```

3. **If note DOES NOT exist** — CREATE it with this template:
   ```markdown
   #plan #active

   # <plan-name>

   **Status:** (read from task_plan.md header)
   **Created:** (read from task_plan.md)
   **Plan files:** `<path to directory containing task_plan.md>`

   ## Phases

   | # | Phase | Status |
   |---|---|---|
   (read phase names and statuses from task_plan.md — look for ## Phase N: lines and ⬜/✅ markers)

   ## Related

   (add wikilinks to any related notes you can identify)
   ```

4. **If note EXISTS** — READ the current Obsidian note, then UPDATE:
   - Update the `**Status:**` line if the task_plan.md status changed
   - Update the phase table: for each phase, check if ⬜ changed to ✅ (or vice versa)
   - Do NOT delete any content that was manually added to the Obsidian note
   - Do NOT rewrite sections that haven't changed

5. **Update the Active Plans dashboard:**
   ```bash
   cat "<vaultPath>/Projects/Active Plans.md"
   ```
   Read it. For each plan found, ensure it's listed under "Active" with current status.
   If a plan is fully complete (all phases ✅), move it from Active to Completed.
   If a new plan exists but isn't listed, add it.

### 4b: Knowledge Sync

Compare MEMORY.md sections against Obsidian vault:
- If MEMORY.md mentions a person with substantial context not in `<vaultPath>/People/` → create note
- If MEMORY.md mentions a project not in `<vaultPath>/Projects/` → create note
- If a tool/service was configured and isn't in `<vaultPath>/Tools/` → create note

Obsidian formatting rules:
- Tags on first line before title: `#person #shapes #engineering`
- Use `[[wikilinks]]` to connect related notes
- Write full depth, never summarize or dilute
- Never delete content from existing vault notes — only append/update

### 4c: Dreaming Log

Append a new entry to `memory/dreaming-log.md`:

```markdown
## YYYY-MM-DD HH:MM

**Gate:** Xh since last dream
**Changes:**
- MEMORY.md: (what sections were added/updated/removed — be specific)
- Obsidian plans: (which plan notes were created or updated, with what changes)
- Obsidian knowledge: (which other notes were created/updated)
- Learnings promoted: (count and which ones)
**Skipped:** (any stale entries removed or contradictions resolved)
```

## DONE

Reply NO_REPLY.
Do not message anyone. Do not announce anything.
```
