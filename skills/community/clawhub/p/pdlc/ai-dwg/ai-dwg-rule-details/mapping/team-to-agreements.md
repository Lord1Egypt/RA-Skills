<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Team Context → TEAM_AGREEMENTS.md + role-isolation.md + coding-standards.md + naming-conventions.md + testing-strategy.md + session-governance.md + project-governance.md + scope-and-risks.md

## Purpose

Derives team operational rules, role definitions, coding conventions, and governance steering from team context, methodology decisions, quality attributes, and scope information across the AP.

**Outputs:**
1. `info/TEAM_AGREEMENTS.md` — Operating rules (root document)
2. `rules/role-isolation.md` — Who does what in AI-DLC v1 workflow
3. `rules/coding-standards.md` — Code patterns and conventions
4. `rules/naming-conventions.md` — File/folder/class/method naming
5. `rules/testing-strategy.md` — Test types, coverage, patterns
6. `rules/session-governance.md` — AI-DLC v1 session rules
7. `rules/project-governance.md` — Sprint cadence, DoD, gates
8. `rules/scope-and-risks.md` — Scope boundaries, risk awareness

---

## MANDATORY: Stage Sub-Role — Workspace Architect

During THIS activity, ALSO adopt the mindset of a **Workspace Architect**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Design for team self-sufficiency — governance docs should eliminate the need to ask "how do we work here?"
- Make role boundaries explicit and enforceable — unclear boundaries lead to architects coding and developers making architecture decisions
- Ensure coding-standards and naming-conventions are technology-specific, not generic — a TypeScript project gets different patterns than Java
- Write session-governance for AI-DLC v1 as guardrails — prevent the AI from going rogue during code generation sessions
- Cross-reference domain-context.md in naming conventions — domain terms override general technology conventions

### Anti-Patterns for This Activity
- Do NOT write generic coding standards that apply to "any language" — standards must match the AP's technology stack
- Do NOT make testing-strategy vague ("write tests") — specify targets, pyramid levels, and what NOT to test
- Do NOT generate role-isolation.md without considering the team's actual size and composition from config

### Quality Check
A good output from this activity sounds like:
- "coding-standards.md for NestJS: modules use DI decorators, services are injectable, controllers handle HTTP only, repositories own data access. Import via barrel files only."
- "SG-07 (Session Governance): Read domain-context.md before naming any entity, variable, or endpoint — AI MUST use exact terms from ubiquitous language."

---

## Sources

These outputs draw from MULTIPLE AP artifacts simultaneously:

| AP Source | Used For |
|-----------|----------|
| Architecture Vision (Quality Attributes) | Testing targets, quality gates |
| Technology Stack (language, framework) | Coding standards, naming conventions |
| Component Design (modules, patterns) | Coding patterns specific to the architecture |
| System Context (scope, externals) | Scope boundaries |
| Architecture Workbook (open items, risks) | Risk awareness |
| Infrastructure (CI/CD, environments) | Governance cadence |
| Team size (from config questions) | Operational doc depth |

---

## Target 1: TEAM_AGREEMENTS.md

### Role

Operating rules agreed by the team — how work is organized, reviewed, and communicated.

### Key Sections

```markdown
<!-- AI-DWG generated | source: Team context + AP methodology | date: {generation-date} -->

# Team Agreements

## Working Model
- Autonomy mode: {from config — Autopilot/Supervised}
- Review standard: {from AP — e.g., 1 peer + CODEOWNER}
- Ownership model: {from module-structure — collective / strong ownership per module}
- Pair/mob programming: {from AP — e.g., for complex tasks / not practiced}

## Communication
- Async-first: decisions documented in ADRs/tickets — not in chat
- Blockers: escalate within {hours}
- Questions about architecture: check steering files first, then ask architect

## Quality Standards
- "Done" means: passes DEFINITION_OF_DONE.md — no negotiation
- Tech debt: log as tickets — never ignore silently
- Refactoring: allowed in scope of current task — major refactors need ADR
```

---

## Target 2: role-isolation.md

### Role

Defines role boundaries for AI-assisted development — who does what, preventing role confusion.

### Key Sections

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Team Context + AP methodology | date: {generation-date} -->

# Role Isolation

## Roles in Development Workflow

| Role | Responsibilities | Boundaries (MUST NOT) |
|------|-----------------|----------------------|
| Architect | Define architecture, approve ADRs, review boundary changes | Write feature code, skip ADR for significant changes |
| Developer | Implement features per steering rules, write tests | Make architecture decisions without ADR, violate module boundaries |
| QA / Tester | Define test scenarios, verify acceptance criteria | Skip security testing, approve without running tests |
| Security | Review auth/authz changes, validate security rules | Block non-security PRs, override architect decisions |
| PM / Product | Define requirements, prioritize backlog, accept deliverables | Dictate technical approach, skip acceptance testing |

## AI-DLC v1 Role (When AI Implements Code)

| AI MUST | AI MUST NOT |
|---------|------------|
| Follow ALL steering files | Invent new patterns outside steering rules |
| Ask when steering is unclear | Assume intent when rules conflict |
| Produce code matching coding-standards.md | Use patterns from other projects/memory |
| Respect module boundaries | Create cross-module dependencies without flagging |
| Log decisions that deviate from patterns | Silently deviate and hope no one notices |

## Segregation of Duties

- Architecture decisions: Architect approves
- Code changes: Developer peer + CODEOWNER
- Security-sensitive changes: Security role reviews
- Steering file changes: Architect/Tech Lead only
- DoD exceptions: Tech Lead only (documented)
```

---

## Target 3: coding-standards.md

### Key Content (Technology-Specific)

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Technology Stack + Component Design | date: {generation-date} -->

# Coding Standards

## Language & Framework Conventions
{Derived from Technology Stack — specific to chosen language}

## File Organization
{Derived from Component Design — module/layer structure}

## Code Patterns
{Derived from Component Design — DI, repository pattern, service pattern}

## Import Rules
{Derived from module-structure.md — barrel imports, no deep imports}

## Error Handling Pattern
{Cross-reference to error-handling.md}

## Async Patterns
{From Technology Stack — promises/async-await/observables based on framework}
```

---

## Target 4: naming-conventions.md

### Key Content

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Technology Stack + Component Design + Domain Context | date: {generation-date} -->

# Naming Conventions

## Files & Folders
| Item | Convention | Example |
|------|-----------|---------|
| Module folder | kebab-case | `incident-management/` |
| Service file | {tech convention} | `incident.service.ts` |
| Controller file | {tech convention} | `incident.controller.ts` |
| Test file | {tech convention} | `incident.service.spec.ts` |

## Classes & Interfaces
{From technology conventions — PascalCase, I-prefix for interfaces, etc.}

## Functions & Methods
{From technology conventions — camelCase, verb-first for actions}

## Database (cross-ref database-rules.md)
{snake_case tables, columns — from DB rules}

## API (cross-ref api-standards.md)
{kebab-case URLs, camelCase JSON — from API rules}

## Domain Terms
{Cross-reference domain-context.md — use EXACT terms, never synonyms}
```

---

## Target 5: testing-strategy.md

### Key Content

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Quality Attributes + Technology Stack | date: {generation-date} -->

# Testing Strategy

## Test Pyramid

| Level | Scope | Speed | Coverage Target |
|-------|-------|:-----:|:---------------:|
| Unit | Single function/class | Fast | {from AP — e.g., 80%} |
| Integration | Module interactions, DB, API | Medium | {from AP — e.g., key flows} |
| E2E | Full user journey | Slow | {from AP — e.g., critical paths only} |

## Test Rules
- Unit tests: required for all business logic
- Integration tests: required for all API endpoints + DB interactions
- E2E tests: required for critical user journeys
- Test data: use factories/builders — never hardcoded
- Mocking: mock external dependencies — never mock the thing you're testing

## When NOT to Test
- Framework-generated boilerplate (module declarations, DI wiring)
- Simple getters/setters with no logic
- Third-party library behavior (they test their own code)
```

---

## Target 6: session-governance.md

### Key Content

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Methodology decisions | date: {generation-date} -->

# Session Governance (AI-DLC v1)

## Rules for AI-Assisted Development Sessions

| Rule | Description |
|------|-------------|
| SG-01 | NEVER write code without checking relevant steering files first |
| SG-02 | One task per session — complete before starting next |
| SG-03 | Verify against DEFINITION_OF_DONE.md before declaring task complete |
| SG-04 | If steering rules conflict or are unclear → ask, don't assume |
| SG-05 | Log any deviation from steering rules with justification |
| SG-06 | Read module-structure.md before creating files in any module |
| SG-07 | Read domain-context.md before naming any entity, variable, or endpoint |
```

---

## Target 7: project-governance.md

### Key Content

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Infrastructure (CI/CD) + Team Context | date: {generation-date} -->

# Project Governance

## Sprint Cadence
- Sprint length: {from AP/config — e.g., 2 weeks}
- Ceremonies: {planning, standup, review, retro}

## Quality Gates
- PR approval required before merge
- CI must pass (lint + test + build + security)
- DoD verified before task closure

## Escalation
- Blocker: escalate to tech lead within {hours}
- Architecture deviation needed: ADR required before implementation
- Security concern: flag immediately — don't proceed until resolved
```

---

## Target 8: scope-and-risks.md

### Key Content

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: System Context (C4 L1) + Architecture Workbook | date: {generation-date} -->

# Scope & Risks

## In Scope
{From C4 L1 — what's inside the system boundary}
- Module list from module-structure.md

## Out of Scope
{From Architecture Vision — explicitly excluded items}

## Known Risks
{From Architecture Workbook — open items, unresolved questions}
| Risk | Impact | Mitigation |
|------|--------|-----------|
| {risk from workbook} | {impact} | {current mitigation approach} |

## Assumptions
{From Architecture Workbook — assumptions that must hold}

## Constraints Reminder
Cross-reference: workspace-rules.md Constraints section
```

---

## Transformation Rules

| AP Source | Outputs |
|-----------|---------|
| Team size (config) | TEAM_AGREEMENTS depth, role-isolation detail |
| Technology Stack (language/framework) | coding-standards, naming-conventions |
| Quality Attributes (all) | testing-strategy targets, DoD criteria |
| Component Design (patterns) | coding-standards patterns |
| Domain Context (from C4 L3) | naming-conventions domain terms |
| Infrastructure (CI/CD, cadence) | project-governance |
| System Context (boundary) | scope-and-risks |
| Architecture Workbook (open items) | scope-and-risks risks/assumptions |
| Methodology decisions | session-governance |

---

## Key Rules

1. **coding-standards is technology-specific** — Node project gets different standards than Java project
2. **naming-conventions cross-references domain-context** — domain terms override general conventions
3. **testing-strategy has specific targets** — "write tests" is not a strategy; "80% unit coverage on business logic" is
4. **session-governance is for AI-DLC v1** — rules that prevent the AI from going rogue during code generation
5. **role-isolation prevents chaos** — clear boundaries stop architects from coding and developers from making architecture decisions
6. **scope-and-risks preserves awareness** — developers should know what's out of scope and what risks exist
