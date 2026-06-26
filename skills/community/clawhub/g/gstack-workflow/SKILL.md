---
name: dev-workflow
description: Structured development workflow inspired by Garry Tan's gstack. Use when the user wants to build a feature, start a project, do a code review, or ship code with a disciplined Think → Plan → Build → Review → Test → Ship process. Triggers on phrases like "start a project", "build a feature", "dev workflow", "ship code", "code review workflow", "plan and build", "structured development". Also useful when the user wants to run a disciplined development process with role-based subagents for analysis, design, review, QA, and release.
---

# Dev Workflow — Structured Development Sprint

A 6-phase development process that turns a vague idea into shipped code. Each phase has a clear role, a defined output, and feeds into the next. Run phases sequentially or skip ahead when context is clear.

## Phases

| # | Phase | Role | Output |
|---|-------|------|--------|
| 1 | **Think** | YC Office Hours Coach | `DESIGN.md` |
| 2 | **Plan** | Eng Manager | `PLAN.md` |
| 3 | **Build** | Implementer | Code + Tests |
| 4 | **Review** | Staff Engineer | Review Report |
| 5 | **Test** | QA Lead | Bug Report + Fixes |
| 6 | **Ship** | Release Engineer | PR / Deploy |

## How to Use

### Full Sprint (recommended for new features)

```bash
# Start from scratch
"I want to build X" → run all 6 phases

# Or ask me:
"Run dev-workflow on [feature description]"
```

I will walk through each phase, spawning a focused subagent per phase with the right model and prompt.

### Partial Sprint

Skip phases when you already have context:

- "Skip think, I have DESIGN.md" → start from Plan
- "Just review and ship this branch" → run Review → Test → Ship
- "I need a design review" → run Phase 2 (Plan) only

### Single Phase

Any phase can run standalone:

- `/think` — Reframe the problem, challenge assumptions, write DESIGN.md
- `/plan` — Architecture, data flow, test strategy, write PLAN.md
- `/build` — Implement from PLAN.md
- `/review` — Code review with auto-fix for obvious issues
- `/test` — Browser testing, regression tests, bug reports
- `/ship` — Sync, test, push, open PR

## Phase Details

### Phase 1: Think (YC Office Hours)

**Goal:** Reframe the problem before writing code.

Spawn a subagent (Sonnet) with the Think prompt from `references/prompts.md`. It will:

1. Ask 6 forcing questions about the real pain, not the feature request
2. Challenge the framing — "You said X but you actually need Y"
3. Generate 3 implementation approaches with effort estimates
4. Recommend the narrowest wedge to ship tomorrow
5. Write `DESIGN.md` with the distilled product vision

**Key rule:** Listen to the pain, not the feature request. The user says "daily briefing app" but means "personal chief of staff AI."

### Phase 2: Plan (Eng Manager)

**Goal:** Lock architecture before building.

Spawn a subagent (Sonnet) with the Plan prompt. It reads `DESIGN.md` and produces `PLAN.md` containing:

1. Architecture diagram (ASCII)
2. Data flow and state machines
3. File structure and module boundaries
4. Test strategy and failure modes
5. Milestone breakdown (what ships first)

**Key rule:** No code until the plan is approved. Challenge scope ruthlessly.

### Phase 3: Build (Implementer)

**Goal:** Write code from PLAN.md.

Use the main session or spawn a subagent (Haiku for simple, Sonnet for complex). It reads `PLAN.md` and:

1. Implements each milestone in order
2. Writes tests alongside code (aim for >80% coverage)
3. Commits atomically per milestone
4. Updates PLAN.md with implementation notes

**Key rule:** Follow the plan. If the plan is wrong, update PLAN.md first, then code.

### Phase 4: Review (Staff Engineer)

**Goal:** Find bugs that pass CI but blow up in production.

Spawn a subagent (Sonnet) with the Review prompt. It:

1. Reads the diff against main/develop
2. Catches logic errors, race conditions, edge cases
3. Auto-fixes obvious issues (formatting, unused imports)
4. Flags completeness gaps and security concerns
5. Writes a review report

**Key rule:** Be paranoid. Assume the code will be hit by edge cases tomorrow.

### Phase 5: Test (QA Lead)

**Goal:** Test like a user, not like a developer.

Spawn a subagent (Sonnet) with the Test prompt. It:

1. Opens the app in a real browser (use `browser` tool)
2. Clicks through every user flow
3. Tests edge cases and error states
4. Reports bugs with reproduction steps
5. Auto-fixes and generates regression tests

**Key rule:** The user doesn't read code. Click the buttons. Break things.

### Phase 6: Ship (Release Engineer)

**Goal:** One command to production.

Run in main session:

1. Sync with remote (git pull/rebase)
2. Run full test suite
3. Audit test coverage
4. Push and open PR
5. Update project docs

**Key rule:** If tests fail, don't ship. Fix first.

## Model Selection

| Phase | Model | Why |
|-------|-------|-----|
| Think | Sonnet | Needs judgment to reframe problems |
| Plan | Sonnet | Architecture decisions need reasoning |
| Build | Haiku/Sonnet | Simple features → Haiku, complex → Sonnet |
| Review | Sonnet | Bug detection needs deep analysis |
| Test | Sonnet | Browser interaction needs context |
| Ship | Haiku | Mechanical execution |

## Parallel Sprints

For large projects, run multiple sprints on different branches:

1. Create feature branches for each sprint
2. Spawn subagents per branch
3. Each subagent works in isolation
4. Review and merge sequentially

Max practical parallelism: 3-5 sprints (limited by context management).

## Output Files

All phase outputs go to the project root:

- `DESIGN.md` — Product vision from Think phase
- `PLAN.md` — Architecture and milestones from Plan phase
- Review reports are written to stdout (capture in conversation)
- Test reports are written to stdout

Clean up output files after shipping if not needed long-term.
