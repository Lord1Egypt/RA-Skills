---
name: project-methodology
description: >-
  Complete project lifecycle methodology for Hermes Agent sessions. A single,
  integrated workflow covering warmup → plan → build → recap → wrapup — with
  context loading, feature planning, recap drafting, handoff verification, and
  project scaffolding. Every session follows the same cycle; nothing falls
  through the cracks.
version: 1.0.0
author: Alejandro Del Villar
license: MIT
metadata:
  hermes:
    homepage: https://github.com/adelvillar1
    tags:
      [project-management, methodology, session-lifecycle, warmup, planning,
       recaps, wrapup, context-loading, continuity]
    related_skills:
      [project-knowledge-graph, codebase-survey, slim-claude-md,
       tech-stack-evaluation, init-project-structure]
triggers:
  - "warmup"
  - "where did we leave off"
  - "what.*open"
  - "continue from yesterday"
  - "pick up where we left off"
  - "plan.*feature"
  - "draft.*plan"
  - "write.*recap"
  - "wrap up"
  - "we.*done"
  - "sign off"
  - "close out"
  - "init.*project"
  - "scaffold.*project"
security:
  scope:
    persistence:
      - "Reads project memory files (e.g. .md), docs/recaps/*.md, docs/plans/*.md, docs/architecture/*.md, docs/features/*.md, TECHNICAL-DOCUMENTATION.md, FUNCTIONAL-SPECIFICATIONS.md"
      - "Reads git log and git status to verify post-recap work"
      - "Writes recap files to docs/recaps/ and plan files to docs/plans/"
      - "Modifies project memory file 'Today's state' section when stale"
      - "Modifies plan file frontmatter (status, updated date) on completion"
  safety:
    - "Never auto-commits — all file writes are explicitly reviewed by the user"
    - "Local env file (CLAUDE.local.md) requires explicit user approval before reading"
    - "Direct database or API queries require explicit user approval in the current turn"
    - "Plan files are markdown with frontmatter — no executable code"
    - "Recap content is human-readable session journaling, not automated data collection"
---

# Project Methodology

> A complete, battle-tested session lifecycle for Hermes Agent. Every session
> follows the same cycle: warm up → plan → build → recap → wrap up. This skill
> integrates all five stages into one workflow so nothing is forgotten and
> every session picks up exactly where the last one left off.

## The Cycle

```
warmup → plan → build → recap → wrapup → (next session) warmup → ...
```

| Stage | What it does | When |
|-------|-------------|------|
| **Warmup** | Load project context, check active plans, check knowledge graph | Session start |
| **Plan** | Draft a feature plan with acceptance criteria | Before non-trivial work |
| **Build** | Implement the plan (the actual work) | After plan is accepted |
| **Recap** | Walk acceptance criteria, draft session recap | Before wrapping up |
| **Wrapup** | Verify handoff, update docs, drift check | Session end |

---

## Stage 1: Warmup — Load Context

Use at session start. Loads project memory, recent recaps, active plans, and
knowledge graph health into one state summary.

### 1. Confirm methodology is in use

```bash
[ -f CLAUDE.md ] || [ -f PROJECT.md ] || echo "WARNING: no project memory file found"
[ -d docs/recaps ] && echo "OK: recaps" || echo "INFO: no recaps yet"
[ -d docs/plans ] && echo "OK: plans" || echo "INFO: no plans yet"
```

If no project memory file exists, suggest running `init-project-structure`
(see References) to scaffold the methodology.

### 2. Check project knowledge graph (if installed)

```bash
python3 ~/.hermes/scripts/project-knowledge-index.py doctor 2>/dev/null | head -10
```

If healthy, note the chunk count and project list. Cross-project knowledge is
available during the session. If not installed, skip — it's additive.

### 3. Read foundational files

Read in this order:

- **Project memory file** (CLAUDE.md) — hard rules, today's state, pointer index
- **Local env file** (CLAUDE.local.md) — credentials and URLs. **Do NOT read this file automatically.** Only read it when the user explicitly asks you to check a credential, connection string, or environment variable, and only after they confirm in the current turn. Never paste contents into chat output.

### 4. Read latest recaps

```bash
# Probe for recap directories
for dir in docs/recaps .hermes/recaps docs/daily-recaps; do
  [ -d "$dir" ] && ls -t "$dir"/*.md 2>/dev/null | head -3 && break
done
```

Read the most recent recap in full. Read the previous 1-2 in headlines only
(Summary, Plans worked on, Open questions).

### 5. Verify post-recap git activity

```bash
LATEST_RECAP=$(ls -t docs/recaps/SESSION-RECAP-*.md 2>/dev/null | head -1)
if [ -n "$LATEST_RECAP" ]; then
  RECAP_DATE=$(date -r "$LATEST_RECAP" "+%Y-%m-%d %H:%M")
  echo "Latest recap: $LATEST_RECAP ($RECAP_DATE)"
  echo "--- Post-recap commits ---"
  git log --since="$RECAP_DATE" --oneline -20
fi
```

Cross-reference commit messages against the recap's "Open questions" and
"Doc updates deferred" sections. If commits resolved listed items, mute them
in your state summary.

### 6. Find and read active plans

```bash
grep -rl '^status: active' docs/plans/*.md .hermes/plans/*.md 2>/dev/null
```

Read each active plan in full. Note acceptance criteria progress
(met/partial/unmet).

**Cross-reference against recaps:** If a recap claims a plan is completed
but the plan file still shows `status: active`, flag the discrepancy.
The plan file with its unchecked acceptance criteria is the source of truth.

### 7. Read contract doc tables of contents

```bash
grep -riE '^##? ' docs/technical-documentation.md docs/functional-specifications.md 2>/dev/null | head -20
```

Don't read the full files. Just know what sections exist.

### 8. Present state summary

Build and present:

```
## Last session: {date} — {one-line summary}
## Active plans: {list with criteria progress}
## Project knowledge graph: {healthy/unavailable}
## Deferred blockers: {schema drift, environment issues, etc.}
## Open follow-ups: {aggregated from recaps, minus what git resolved}
```

Then ask: **"What do you want to work on?"**

### Warmup Pitfalls

- **Running heavyweight warmup mid-session** — if already deep in work, use lightweight mode (just read the relevant doc silently)
- **Reading every file** — only read files matching the user's stated task
- **Pasting secrets** — never paste values from CLAUDE.local.md
- **Stale plan statuses** — before any response that enumerates plan statuses, re-read the plan files (not cached memory)
- **False-positive file finds** — `/opt/homebrew/CLAUDE.md` is Homebrew, not a project

---

## Stage 2: Plan — Draft a Feature Plan

Use before starting non-trivial work. Creates an ISO-date-prefixed plan file at
`docs/plans/YYYY-MM-DD-<slug>.md`.

### When to use

- Any feature or change that takes more than 15 minutes
- User says "plan this", "draft a plan for X", "before we build this"

### Skip for

- Typo fixes, single-line bug fixes, dependency bumps, trivial changes

### Plan structure

Each plan file has YAML frontmatter and the following sections:

```markdown
---
status: draft|active|completed|cancelled
created: YYYY-MM-DD
updated: YYYY-MM-DD
slug: feature-name
---

# Plan: Feature Name

## Context

Why this work exists. What problem does it solve? What's the user-facing or
system-facing gap? Include references to relevant docs, user feedback, or
observed behavior.

## Approach

How the feature will be built. Technical approach, key design decisions,
trade-offs made. Think-aloud rather than final spec.

## Acceptance Criteria

- [ ] Criterion 1 — verifiable, specific
- [ ] Criterion 2
- [ ] Criterion 3

## Files to be touched

- `path/to/file.ts` — what changes
- `path/to/new-file.ts` — new file

## Out of scope

- What this plan explicitly does NOT cover

## Verification

How to confirm it works. Manual steps, test commands, URL patterns.

## Linked artifacts

- `docs/features/X.md` — update with new behavior
```

### Plan pitfalls

- **Plans are contracts.** Don't scope-creep. If mid-implementation you
  discover something that should be part of the plan, pause and update the
  plan's ACs first.
- **Plan before building.** A 5-minute plan saves 30 minutes of rework.
- **Update plan status immediately.** When work is confirmed complete, set
  `status: completed` and bump `updated:` in the same turn as the final
  commit. Do not defer this to recap or wrapup.
- **Plan file is the source of truth** for whether work is done — not the
  recap, not memory.

---

## Stage 3: Build — Implementation

The actual work happens here. Methodology considerations during build:

### Before writing code

1. **Scan sibling projects** for existing patterns first
2. **Check the existing pipeline job registry** before writing ad-hoc scripts
3. **Prefer quick experiments** over verbose analysis when evaluating new tools
4. **Cross-environment baselines** — before reporting progress deltas, check
   both staging and production to establish the true baseline

### During implementation

- Update plan ACs as items are completed
- If blocked, note the blocker in the plan file with a `[BLOCKED]` tag
- Prefer batched writes over individual round-trips for data scripts
- Dry-run is mandatory for all data scripts before live execution

### Security rules during build

- **No production operations without explicit user approval in the current turn**
- **Destructive operations (DELETE, DROP, TRUNCATE) require explicit approval**
- **Never use `prisma db push`** for changes going to staging/production —
  use `prisma migrate dev` + `prisma migrate deploy`
- **Never paste credentials, API keys, or connection strings into chat output**

---

## Stage 4: Recap — Write Session Recap

Use at the natural end of a working session after implementation. Drafts a
structured recap at `docs/recaps/SESSION-RECAP-YYYY-MM-DD.md`.

### Recap structure

```markdown
# Session Recap — YYYY-MM-DD

## Summary

One-paragraph overview of what was accomplished.

## Plans worked on

For each plan touched this session:
- Plan name and status after session
- Acceptance criteria walk: met/partial/unmet with notes

## Commits

| Hash | Message |
|------|---------|
| `abc1234` | feat: description |

## What was added

New files, features, infrastructure. Describe what and why.

## What was fixed

Bugs found and fixed. Include root cause.

## Files changed

Organized by category (backend, frontend, scripts, docs).

## Doc updates applied

List contract docs updated inline this session.

## Doc updates deferred

List contract docs that need updates but were deferred.
These MUST be addressed before the next session on this area.

## Open questions / next steps

Unresolved issues, known follow-ups, items for the next session.
```

### Recap process

1. **Detect what changed** — `git log --oneline` for the session
2. **Walk acceptance criteria** — read each active plan, check off ACs with user
3. **Update plan statuses** — set completed plans to `status: completed`
4. **Propose doc updates** — identify which contract docs need updating
5. **Draft the recap** — present it to the user for review
6. **NEVER auto-commit** — the user approves all file writes

### Recap pitfalls

- **Recaps can be wrong.** A session that was "drifting and acting erratically"
  may produce an incorrect recap. Cross-reference against the plan file's
  unchecked ACs — if the recap says "✅ Completed" but ACs are unchecked,
  the plan file wins.
- **Never commit the recap** — leave it as an unstaged file for the user
- **Doc updates deferred are debts** — if you defer a doc update, it goes
  in the recap's deferred section. The next warmup surfaces it.

---

## Stage 5: Wrapup — Verify Handoff

Use at session end. Ensures the next session picks up cleanly.

### 1. Verify recap exists

```bash
ls -t docs/recaps/*.md 2>/dev/null | head -1
```

If no recap was written (trivial session), note it.

### 2. Check project memory file freshness

```bash
wc -l CLAUDE.md
```

If >300 lines, suggest a CLAUDE.md organization pass.

### 3. Check for uncommitted changes

```bash
git status --short | head -20
```

If uncommitted work exists, note it in the wrap-up. Never commit on the
user's behalf.

### 4. Verify plan statuses

```bash
grep -rl '^status: active' docs/plans/*.md 2>/dev/null
```

For any plan whose work was completed this session but still shows `active`,
flag the staleness. The recap should have handled this, but catch it here
as a safety net.

### 5. Check for deferred doc-update debt

Scan the recap's "Doc updates deferred" section. If any exist, they go
into the next session's warmup state summary as open follow-ups.

### 6. Index knowledge graph (if installed)

```bash
python3 ~/.hermes/scripts/project-knowledge-index.py index 2>/dev/null
```

This picks up the new recap, updated plans, modified project memory file content, and any
new or changed skills.

### 7. Drift checks

```bash
wc -l CLAUDE.md                     # should be ≤300
git status CLAUDE.local.md           # should be hidden by gitignore
```

### 8. Draft next-session preview

A one-paragraph summary of what the next session should pick up:
- Active plans and their next AC
- Open follow-ups
- Deferred doc debts

### Wrapup pitfalls

- **Don't auto-commit.** The user controls commits.
- **Don't skip drift checks.** A project memory file that grew to 400 lines or a
  local.md that accidentally became tracked will bite the next session.
- **Wrapup is lightweight.** If the user is done, a quick status check
  and the next-session preview is sufficient. Don't over-engineer it.

---

## Appendix: Quick Reference

### Common commands

```bash
# Find project root
find ~ -maxdepth 5 -name "CLAUDE.md" 2>/dev/null | head -5
search_files(path="~", pattern="CLAUDE.md", limit=10)
search_files(path="~", pattern="PROJECT.md", limit=10)

# Find active plans
grep -rl '^status: active' docs/plans/*.md .hermes/plans/*.md 2>/dev/null

# Find recent recaps
ls -t docs/recaps/*.md | head -3

# Check post-recap commits
git log --since="$(date -r docs/recaps/SESSION-RECAP-*.md '+%Y-%m-%d %H:%M')" --oneline -20

# Read contract doc sections
grep -riE '^##? ' docs/technical-documentation.md docs/functional-specifications.md 2>/dev/null | head -20

# Check git status
git status --short

# Check project memory file size
wc -l CLAUDE.md
```

### Plan status lifecycle

```
draft → active → completed
                   → cancelled
                        → (archived)
```

Transition rules:
- `draft → active`: User approves plan, work begins
- `active → completed`: All ACs confirmed met
- `active → cancelled`: Superseded by a newer plan or abandoned
- Never go `completed → active` — if work resumes, create a new plan

### File layout

```
project/
├── CLAUDE.md                    # Slim router — hard rules, pointers, today's state
├── CLAUDE.local.md              # Gitignored — credentials, URLs (never commit)
├── docs/
│   ├── recaps/                  # Session recaps — SESSION-RECAP-YYYY-MM-DD.md
│   ├── plans/                   # Feature plans — YYYY-MM-DD-slug.md
│   ├── architecture/            # Architecture docs
│   ├── features/                # Feature docs
│   └── operations/              # Operations and pipeline docs
├── TECHNICAL-DOCUMENTATION.md   # Technical contract
└── FUNCTIONAL-SPECIFICATIONS.md # Functional contract
```

### Pitfalls master list

1. **Stale plan statuses** — report from files, not memory. Re-read before
   any status enumeration.
2. **Production operations** — zero without explicit user approval in the
   current turn.
3. **Secret exposure** — never paste connection strings, API keys, or tokens
   into chat output.
4. **Feature hallucination** — verify features exist before creating any
   marketing copy, social posts, or demos.
5. **Missing project discovery** — scan all projects before claiming an
   incomplete portfolio picture.
6. **Over-engineering** — start with a representative sample, not a full
   sweep.
7. **Skipping dry-run** — mandatory for all data scripts before live
   execution.
8. **Deferred doc updates** — if you defer a doc update, it goes in the
   recap. The next warmup surfaces it.
9. **Plan file not updated on completion** — update status immediately in
   the same turn as the work.
10. **Cache over files** — never trust cached plan statuses from earlier in
    the session.

---

## References

- `references/stale-data-verification.md` — how to verify dynamic data against
  live sources instead of trusting snapshot files
- `references/project-scaffold.md` — complete instructions for
  init-project-structure and slim-claude-md workflows
- `templates/plan.md` — markdown template for feature plans
- `templates/recap.md` — markdown template for session recaps
