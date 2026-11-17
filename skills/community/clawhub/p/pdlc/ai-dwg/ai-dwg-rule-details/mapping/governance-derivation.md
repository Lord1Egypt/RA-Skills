<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Governance Context → PROJECT_INSTRUCTIONS.md + CONTRIBUTING.md + ONBOARDING.md + PR Template + backlog/po-charter.md + backlog/prioritization-register.md

## Purpose

Derives operational governance documents from multiple AP sources — methodology decisions, team context, and quality attributes. These are NOT steering files but root-level operational documents that guide team workflow. Also carries POLC governance reference documents (PO Charter, Prioritization Register) into the backlog folder for developer context.

**Outputs:**
1. `info/PROJECT_INSTRUCTIONS.md` — Master developer guide (single entry point)
2. `info/CONTRIBUTING.md` — Commit strategy, PR process, branching model
3. `info/ONBOARDING.md` — New developer checklist
4. `.github/pull_request_template.md` — PR checklist template
5. `backlog/po-charter.md` — PO authority/escalation reference (IF POLC)
6. `backlog/prioritization-register.md` — Build order rationale (IF POLC)

---

## MANDATORY: Stage Sub-Role — Automation Engineer

During THIS activity, ALSO adopt the mindset of an **Automation Engineer**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- PROJECT_INSTRUCTIONS.md is the single entry point — a new developer should go from zero to running in one read
- Write commands that are technology-specific and copy-pasteable — `npm install` not "install dependencies"
- Design the PR template checklist to mirror steering files — each checkbox traces to a specific enforceable rule
- Think about onboarding as progressive complexity — Day 1 is setup, Day 2 is architecture understanding, Day 3 is workflow, Day 4-5 is first real task
- CONTRIBUTING.md must be action-oriented — "do this" not "we believe in quality"

### Anti-Patterns for This Activity
- Do NOT write generic governance docs that could apply to any project — commands, module names, and steering references must be specific to THIS workspace
- Do NOT make the PR template so long it gets ignored — focus on high-impact checks that match the steering rules
- Do NOT forget that these are operational docs (for humans) not enforcement docs (for AI-GCE) — they guide, not block

### Quality Check
A good output from this activity sounds like:
- "PROJECT_INSTRUCTIONS Quick Start: 6 steps from clone to running (clone → .env → docker compose → install → dev → verify). Key commands table with exact commands for this stack."
- "PR template checklist: Module boundaries (module-structure.md), domain terms (domain-context.md), error handling (error-handling.md), no sensitive data in logs (observability-sensitive.md)."

---

## Source

**From multiple AP artifacts:**
- Architecture Vision (system name, vision statement)
- Technology Stack (development tools, test runners)
- Infrastructure & Deployment (CI/CD, environments)
- Component Design (modules, ownership)
- All steering files already generated (referenced in PROJECT_INSTRUCTIONS)

---

## Target 1: info/PROJECT_INSTRUCTIONS.md

### Role

The ONE document every developer reads first. Points to everything else. Answers: "How do I work on this project?"

### Structure

```markdown
<!-- AI-DWG generated | source: Multiple AP artifacts | date: {generation-date} -->

# Project Instructions — {System Name}

## Quick Start

1. Clone the repository
2. Copy `.env.example` to `.env` — fill in local values
3. Run `docker compose up -d` — starts infrastructure
4. Run `{install command}` — installs dependencies
5. Run `{dev command}` — starts development server
6. Open `{URL}` — verify it works

## Architecture at a Glance

{2-3 sentences from Architecture Vision — what this system is}

**Stack:** {primary tech from tech-stack.md}
**Modules:** {list from module-structure.md}
**Style:** {architecture style — monolith/modular/microservices}

## Development Rules (Must Read)

All development rules are in `rules/`. Key files:

| File | Governs |
|------|---------|
| `workspace-rules.md` | Golden rules — read this first |
| `coding-standards.md` | Code patterns and conventions |
| `module-structure.md` | Module boundaries (what can depend on what) |
| `api-standards.md` | API conventions |
| `database-rules.md` | Schema and query rules |
| `git-workflow.md` | Branching and commit conventions |
| `testing-strategy.md` | What to test and how |

## How to Contribute

See [CONTRIBUTING.md](./CONTRIBUTING.md) for PR process, commit format, and review standards.

## New to the Team?

See [ONBOARDING.md](./ONBOARDING.md) for your first-week checklist.

## Key Commands

| Command | Purpose |
|---------|---------|
| `{install}` | Install dependencies |
| `{dev}` | Start dev server |
| `{test}` | Run tests |
| `{lint}` | Run linter |
| `{build}` | Production build |
| `docker compose up -d` | Start infrastructure |
| `{migrate}` | Run database migrations |

## Architecture Decisions

Architecture Decision Records (ADRs) document why things are the way they are:
- Located in: `{ADR path — from AP or separate repo}`
- Read when: you question a design choice or want to change an approach
```

---

## Target 2: info/CONTRIBUTING.md

### Structure

```markdown
<!-- AI-DWG generated | source: Infrastructure & Deployment + Team Context | date: {generation-date} -->

# Contributing

## Workflow

1. Pick a task from the backlog
2. Create branch: `{type}/{ticket}-{description}` (see git-workflow.md)
3. Implement with tests
4. Open PR using the template
5. Address review feedback
6. Merge after approval + CI pass

## Commit Messages

Format: `{type}({scope}): {subject}` (Conventional Commits)

See `rules/git-workflow.md` for full commit convention.

## Pull Requests

- Use the PR template (auto-loaded from `.github/pull_request_template.md`)
- Keep PRs focused — one concern per PR
- Maximum size: {from git-workflow.md — e.g., 400 lines}
- Required approvals: {from git-workflow.md}
- CI must pass before merge

## Code Standards

All coding standards are enforced via `rules/` files. Key requirements:
- Follow module boundaries (see `module-structure.md`)
- Use domain language (see `domain-context.md`)
- Handle errors per `error-handling.md`
- Log per `observability-logging.md`
- Test per `testing-strategy.md`

## Review Standards

When reviewing, check:
- [ ] Follows module boundaries
- [ ] Uses correct domain terminology
- [ ] Tests included for new behavior
- [ ] Error handling follows patterns
- [ ] No sensitive data in logs
- [ ] Tenant scoping applied (if multi-tenant)
```

---

## Target 3: info/ONBOARDING.md

### Structure

```markdown
<!-- AI-DWG generated | source: Multiple AP artifacts | date: {generation-date} -->

# Onboarding — New Developer Checklist

## Week 1

### Day 1: Setup
- [ ] Get repository access
- [ ] Clone repository
- [ ] Follow Quick Start in PROJECT_INSTRUCTIONS.md
- [ ] Verify local environment runs

### Day 2: Understand the Architecture
- [ ] Read `info/PROJECT_INSTRUCTIONS.md` completely
- [ ] Read `rules/workspace-rules.md` (golden rules)
- [ ] Read `rules/module-structure.md` (what depends on what)
- [ ] Read `rules/domain-context.md` (domain vocabulary)
- [ ] Review the Architecture Vision document (from AP)

### Day 3: Understand the Workflow
- [ ] Read `info/CONTRIBUTING.md`
- [ ] Read `rules/git-workflow.md`
- [ ] Read `rules/coding-standards.md`
- [ ] Make a trivial change (typo fix) → full PR cycle (branch, commit, PR, review, merge)

### Day 4-5: First Real Task
- [ ] Pick a small task (labeled "good first issue" or equivalent)
- [ ] Implement following all steering rules
- [ ] Write tests per testing-strategy.md
- [ ] Submit PR, receive feedback, iterate

## Key Documents

| Document | What You Learn |
|----------|---------------|
| PROJECT_INSTRUCTIONS.md | How to run the project |
| workspace-rules.md | Non-negotiable rules |
| module-structure.md | Architecture boundaries |
| domain-context.md | Correct terminology |
| coding-standards.md | How to write code here |
| git-workflow.md | How to use git here |
| DEFINITION_OF_DONE.md | When is your work "done" |

## Questions?

- Architecture questions → {team lead / architect}
- Process questions → {team lead / PM}
- Domain questions → {domain expert / product owner}
```

---

## Target 4: .github/pull_request_template.md

### Structure

```markdown
## Summary

{Brief description of what this PR does}

## Type

- [ ] Feature (`feat`)
- [ ] Bug fix (`fix`)
- [ ] Refactor (`refactor`)
- [ ] Documentation (`docs`)
- [ ] Tests (`test`)
- [ ] Chore (`chore`)

## Related

- Ticket: {PROJ-XXX}
- Related PRs: {if any}

## Changes

- {Change 1}
- {Change 2}

## Checklist

- [ ] Code follows steering rules (workspace-rules.md)
- [ ] Module boundaries respected (module-structure.md)
- [ ] Domain terminology correct (domain-context.md)
- [ ] Tests added/updated for new behavior
- [ ] Error handling follows error-handling.md
- [ ] No sensitive data in logs (observability-sensitive.md)
- [ ] Tenant scoping applied where applicable
- [ ] API changes follow api-standards.md
- [ ] Database changes include migration
- [ ] Documentation updated if needed

## Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing done for: {describe}

## Screenshots (if UI changes)

{Before/After or N/A}
```

---

## Transformation Rules

| AP Source | Output |
|----------|--------|
| System name + vision statement | PROJECT_INSTRUCTIONS header |
| Technology Stack (commands) | Quick Start commands |
| Module list from C4 L3 | Architecture at a Glance |
| Git workflow from Infrastructure | CONTRIBUTING workflow |
| Team context (review standards) | CONTRIBUTING review checklist |
| All steering file names | Onboarding reading list |
| Quality attributes + security rules | PR template checklist items |

---

## Key Rules

1. **PROJECT_INSTRUCTIONS is the entry point** — everything else is referenced from here
2. **Commands are technology-specific** — `npm install` vs `pip install` vs `dotnet restore`
3. **PR template checklist mirrors steering files** — each checkbox traces to a specific steering rule
4. **Onboarding is week-by-week** — progressive complexity, not everything at once
5. **CONTRIBUTING is action-oriented** — "do this", not "we follow these principles"


---

## Target 5: backlog/po-charter.md (IF POLC)

### Purpose

The PO Charter answers "who decides what gets built and how escalation works." Essential developer context when questions arise about priority, scope trade-offs, or acceptance disputes.

### Source

**From:** AI-POLC → PBP governance (`governance/po-charter.md` or equivalent role-definition document).

### Transformation

**Copy with provenance** — this is a reference document, not a steering file. DWG copies the PBP's PO Charter verbatim and adds provenance front-matter. No distillation, no summarization.

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-POLC — governance/po-charter.md"
generatedOn: "{generation-date}"
ownership: generated
projectId: "{project-id}"
---

{verbatim PO Charter content from PBP}
```

### Condition

Generate IF `polc-state.md` is present AND the PBP contains a PO Charter or equivalent authority/role document. If no such document exists in PBP, SKIP — do not fabricate.

---

## Target 6: backlog/prioritization-register.md (IF POLC)

### Purpose

The Prioritization Register answers "why this build order" — the rationale behind which epics/stories are higher priority. Developers need this when questioning why they're working on Feature A before Feature B.

### Source

**From:** AI-POLC → PBP governance (`governance/prioritization-register.md` or `strategy/value-prioritization.md` with full register).

### Transformation

**Copy with provenance** — reference document, not steering. DWG copies the register verbatim and adds provenance front-matter.

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-POLC — governance/prioritization-register.md"
generatedOn: "{generation-date}"
ownership: generated
projectId: "{project-id}"
---

{verbatim Prioritization Register content from PBP}
```

### Condition

Generate IF `polc-state.md` is present AND the PBP contains a prioritization register or equivalent ordering-rationale document. If no such document exists, SKIP — the ordering in `backlog/epics-and-backlog.md` already carries the rank (but not the full rationale).

---

## Key Rules (Targets 5 & 6)

1. **Reference documents, not steering** — these do NOT influence AI behavior per code change; they are human-readable governance context
2. **Copy verbatim** — do not paraphrase, summarize, or restructure POLC's content
3. **Provenance front-matter only** — the only DWG addition is the metadata header
4. **Skip if absent** — do NOT fabricate governance docs that POLC didn't produce
5. **Location: `backlog/`** — these are product governance, not operational docs; they live with the backlog they govern
