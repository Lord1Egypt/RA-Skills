# Memory Operations

## User Commands

| Command | Action |
|---------|--------|
| "What do you know about X?" | Search all tiers, return matches with sources |
| "Show my memory" | Display memory.md contents |
| "Show [project] patterns" | Load and display specific namespace |
| "Forget X" | Remove from all tiers, confirm deletion |
| "Forget everything" | Full wipe with export option |
| "Recent changes?" | Show last 20 corrections |
| "Export memory" | Generate downloadable archive |
| "Memory stats" | Show tier sizes, last compaction, sync status |
| "Sync memory" | Trigger cross-session sync now |


## Automatic Operations

### On Session Start
1. Load memory.md (HOT tier)
2. Check index.md for context hints and sync status
3. If sync status is `stale` -> detect agent product -> run global config sync
4. If project detected -> preload relevant namespace

### On Correction Received
```
1. Parse correction type (preference, pattern, override)
2. Check if duplicate (exists in any tier)
3. If new:
   - Add to corrections.md with timestamp
   - Increment correction counter
4. If duplicate:
   - Bump counter, update timestamp
   - If counter >= 3: ask to confirm as rule
5. Determine namespace (global, domain, project)
6. Write to appropriate file
7. Update index.md line counts
8. If written to Confirmed Preferences -> trigger global config sync
```

### On Pattern Match
When applying learned pattern:
```
1. Find pattern source (file:line)
2. Apply pattern
3. Cite source: "Using X (from memory.md:15)"
4. Log usage for decay tracking
```

### Weekly Maintenance (Cron)
```
1. Scan all files for decay candidates
2. Move unused >30 days to WARM
3. Archive unused >90 days to COLD
4. Run compaction if any file >limit
5. Update index.md
6. Generate weekly digest (optional)
7. Check sync status -> if stale, run global config sync
```

## Global Config Sync Operation

### Trigger Conditions
- Correction promoted to Confirmed Preferences
- memory.md promote/demote/compact completed
- User says "sync memory"
- Session end with new confirmed rules

### Agent Detection
```
Check in order (first existing path wins):
1. ~/.claude/CLAUDE.md              (Claude Code)
2. ~/.openclaw/AGENTS.md            (OpenClaw)
3. ~/.codex/AGENTS.md               (Codex)
4. ~/.codebuddy/CODEBUDDY.md        (CodeBuddy)
5. ~/.config/opencode/AGENTS.md     (opencode)
If multiple exist, sync to all of them.
```

### Sync Procedure
```
1. Read ~/learn-from-experience/memory.md
2. Extract ## Confirmed Preferences section
3. For each entry "### title | confidence [| priority]":
   - Derive tag from title (snake_case, abbreviated)
   - Compile to: "- [tag] one-line core description"
   - If priority is HIGH, mark for retention during truncation
4. Detect agent product(s) -> locate global config file(s)
5. For each global config file:
   a. Read the file
   b. Locate ### Patterns block under ## Learnings
      - If ## Learnings not found: create it at the end of the file
      - If ### Patterns not found: create it after the last ### under ## Learnings
   c. Replace content between ### Patterns header and next ###/## header
      - Preserve the comment line with updated timestamp
      - Write compiled entries (max 30 lines)
      - If > 30 entries: keep HIGH priority first, then by confidence desc
6. Update ~/learn-from-experience/index.md:
   - Set "Last global config sync:" to today
   - Set "Sync status: in_sync"
7. Confirm to user: "Synced N entries to global config"
```

### Stale Detection
```
On skill activation:
1. Read ~/learn-from-experience/index.md
2. Compare "Last global config sync" vs "memory.md last modified"
3. If memory.md is newer -> set "Sync status: stale"
4. If stale -> auto-sync and notify user
```

### Safety Guards
- ONLY modify ### Patterns block; never touch other global config content
- Before write: verify old content was correctly located (check surrounding headers)
- After write: count lines in ### Patterns block; if > 30, truncate and warn
- If global config read fails: skip sync, log warning, do not block session

## File Formats

### memory.md (HOT)
```markdown
# Learn-from-Experience Memory

## Confirmed Preferences
- format: bullet points over prose (confirmed 2026-01)
- tone: direct, no hedging (confirmed 2026-01)

## Active Patterns
- "looks good" = approval to proceed (used 15x)
- single emoji = acknowledged (used 8x)

## Recent (last 7 days)
- prefer SQLite for MVPs (corrected 02-14)
```

### corrections.md
```markdown
# Corrections Log

## 2026-02-15
- [14:32] Verbose explanation -> bullet summary
  Type: communication
  Context: Chat response
  Confirmed: pending (1/3)

## 2026-02-14
- [09:15] Use SQLite not Postgres for MVP
  Type: technical
  Context: database discussion
  Confirmed: yes (said "always")
```

### projects/{name}.md
```markdown
# Project: my-app

Inherits: global, domains/code

## Patterns
- Use Tailwind (project standard)
- No Prettier (eslint only)
- Deploy via GitLab CI

## Overrides
- semicolons: yes (overrides global no-semi)

## History
- Created: 2026-01-15
- Last active: 2026-02-15
- Corrections: 12
```

## Edge Case Handling

### Contradiction Detected
```
Pattern A: "Use tabs" (global, confirmed)
Pattern B: "Use spaces" (project, corrected today)

Resolution:
1. Project overrides global -> use spaces for this project
2. Log conflict in corrections.md
3. Ask: "Should spaces apply only to this project or everywhere?"
```

### User Changes Mind
```
Old: "Always use formal tone"
New: "Actually, casual is fine"

Action:
1. Archive old pattern with timestamp
2. Add new pattern as tentative
3. Keep archived for reference ("You previously preferred formal")
```

### Context Ambiguity
```
User says: "Remember I like X"

But which namespace?
1. Check current context (project? domain?)
2. If unclear, ask: "Should this apply globally or just here?"
3. Default to most specific active context
```

### Multiple Agent Products
```
User has both Claude Code and CodeBuddy installed.

Action:
1. Sync writes to ALL detected global config files
2. memory.md remains the single source of truth
3. Each product reads its own global config independently
```
