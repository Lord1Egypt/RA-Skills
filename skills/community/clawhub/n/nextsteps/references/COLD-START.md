# Cold-Start Bootstrap Protocol

Run this when `.nextsteps/PREFERENCES.md` does not exist — indicating first activation for this project.

## Step 1 — Scan Project Context

Scan for project information to seed intelligent defaults:

- **README.md**: Project description, tech stack, features
- **package.json / Cargo.toml / pyproject.toml / go.mod**: Language, dependencies, project name
- **Recent files** (if available): What the user has been working on
- **git log** (last 10 commits, if available): Recent activity patterns

Extract: primary language, framework, project type (web app, CLI, library, etc.), active areas.

## Step 2 — Create PREFERENCES.md

Create `.nextsteps/PREFERENCES.md` with Schema Version 2 defaults:

```markdown
# NextSteps User Preferences
## Schema Version: 2
## Last Updated: [today's date]
## Total Interactions: 0
## Selection Rate: N/A

## User Configuration
- enabled: true
- display-count: 5
- min-count: 1
- max-count: 7
- preferred-categories: [all]
- excluded-categories: []
- format: standard
- show-footer: true
- include-backlog: true
- include-lateral: true

## Topic Affinities
[Seed from project scan — all MODERATE initially]

## Category Preferences
- direct-follow-up: MODERATE
- actionable-task: MODERATE
- deep-dive: MODERATE
- memory-recall: MODERATE
- lateral-jump: MODERATE
- quick-win: MODERATE

## Anti-Preferences
- ignored-topics: []
- ignored-types: []

## Behavioral Patterns
- learned-display-count: 5
- count-learning-confidence: LOW

## Gaps Detected
[none yet]
```

Seed Topic Affinities from the project scan. Example: a Node.js Express project gets `api: MODERATE`, `testing: MODERATE`, `deployment: MODERATE`.

## Step 3 — Create HISTORY.md

Create `.nextsteps/HISTORY.md`:

```markdown
# NextSteps Selection History
## Format: [DATE] [EVENT-TYPE] details
## Max entries: 50 (summarize oldest 25 when overflow)
## Event types: [SELECTED], [IGNORED], [CONFIG-CHANGE], [HYPOTHESIS], [EXPERIMENT], [DIAGNOSTIC], [DISABLED], [ENABLED]
```

## Step 4 — Create BACKLOG.md

Create `.nextsteps/BACKLOG.md`:

```markdown
# NextSteps Backlog
## Format: - [DATE] [STATUS] brief-description (context: where-mentioned)
## Statuses: OPEN, IN-PROGRESS, DONE, DISMISSED
## Max active items: 30 (archive DONE/DISMISSED items when overflow)
```

## Step 5 — Security Check

Check if `.gitignore` exists. If `.nextsteps/` is NOT listed:
- Include as a next step in the first activation: "Add `.nextsteps/` to .gitignore — it contains personal preferences that shouldn't be committed"

## Step 6 — Generate First Suggestions

For the first activation, generate a balanced set:
- 1 Direct Follow-up (from current conversation)
- 1 Actionable Task (from project scan — something useful to do)
- 1 Deep Dive (relevant to the project's tech stack)
- 1 Lateral (creative idea based on project type)
- 1 Quick Win (small improvement found during project scan)

Adjust the above if `display-count` is different from 5. The distribution should match the slot allocation rules from CATEGORIES.md.

## Schema Migration

Note: PREFERENCES.md has a hard limit of 120 lines. If it reaches this limit during normal operation, summarize the oldest Topic Affinities entries and remove low-value data.

## Schema Migration

If PREFERENCES.md exists but lacks a `## User Configuration` section (Schema Version 1), migrate:
1. Read existing content
2. Insert `## User Configuration` section with all defaults after the header
3. Update `## Schema Version: 2`
4. Preserve all existing data (topic affinities, category preferences, etc.)

If migration fails partway, preserve unmodified sections and retry on next activation.
