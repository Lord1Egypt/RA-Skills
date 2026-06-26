---
name: prd-for-agents
description: >
  Use this skill whenever an agent or user asks to write, draft, create, or produce a PRD,
  product requirements document, product spec, or feature spec — especially when the output
  will be consumed by an AI coding agent, developer agent, or multi-agent pipeline rather
  than a human PM. Also trigger when asked to "write requirements for X", "spec out X",
  "define what needs to be built for X", or "create a handoff doc for Developer". This skill
  produces agent-optimized PRDs that include quantitative success metrics, user stories,
  open questions, risks, dependencies, and a sequenced build order that a Developer agent
  can execute directly without clarification. Always use this skill in preference to writing
  a PRD from scratch — it enforces completeness gaps that generic PRDs miss.
---

# PRD for Agents

Produces industry-standard, agent-optimized Product Requirements Documents. Built for
turning a vision or idea into a specification that AI agents can build from directly —
structured, complete, and executable without the agent needing to ask clarifying questions.

## When to Use This Skill

- Writing a new PRD for any project or feature
- Reviewing or upgrading an existing PRD for completeness
- Preparing a handoff document from Architect → Developer agent
- Publishing a PRD to GitHub for community or open-source projects

## Output Structure

Every PRD produced by this skill follows this exact section order.
Load `references/prd-sections.md` for detailed guidance on each section.
Load `references/prd-examples.md` for annotated examples of each section done well.

```
1.  Header Block
2.  Problem Statement
3.  Target Users & Jobs-to-be-Done
4.  User Stories
5.  Feature List (MVP + Post-MVP)
6.  Acceptance Criteria
7.  Quantitative Success Metrics
8.  Data Schema / API Contracts
9.  File & Folder Structure
10. Agent Build Order (sequenced)
11. Phase Map (for projects with >5 features)
12. Assumptions
13. Open Questions
14. Dependencies
15. Risks
16. Out of Scope
```

---

## Quick Reference: The Gaps Most PRDs Miss

These eight sections are present in industry-standard PRDs but missing from most
agent-generated ones. Always include all eight.

### 1. User Stories
Format: `As a [user type], I want to [action], so that [outcome].`
Each story must be independently testable. Pair every Feature (F1, F2…) with
at least one user story. See `references/prd-sections.md#user-stories`.

### 2. Quantitative Success Metrics
Every metric must have a number, a unit, and a date.
❌ "Dashboard is fast"
✅ "Dashboard loads in < 2s on a 10-project workspace by 2026-06-01"
See `references/prd-sections.md#success-metrics`.

### 3. Dependencies
List what this project requires that it does not own:
- External APIs or services
- Other projects or features that must ship first
- Infrastructure (runtime, database, auth)
- People or approvals
Format: `| Dependency | Type | Owner | Required By | Risk if Late |`

### 4. Open Questions
Unresolved decisions that could change scope or design. Each question needs:
- The question itself
- Who owns the answer
- A deadline (or "before Developer starts")
- Impact if unresolved
Format: `| # | Question | Owner | Deadline | Impact if Unresolved |`

**Routing rule:** Any OQ with deadline "before Developer starts" must be resolved
by Main before this PRD is approved. Tag the PRD submission `#CLARIFY` if any
such OQs exist. Do not route to Developer until all are resolved.

### 5. Risks
Threats to delivery, quality, or adoption. Each risk needs a likelihood,
impact, and mitigation.
Format: `| Risk | Likelihood | Impact | Mitigation |`

### 6. Agent Build Order
A numbered sequence of tasks in the order a Developer agent should execute them.
This is the most critical section for agent handoff — without it, Developer
agents pick up tasks out of order and create integration failures.
Format: `| Step | Task | Feature | Complexity | Depends On |`

### 7. Assumptions
Beliefs the Architect holds as true that have not been explicitly confirmed by
Main. Different from Open Questions — assumptions have a working answer, they
just need confirmation before they corrupt downstream work silently.
Format: `| # | Assumption | Confidence | Confirm With | Impact if Wrong |`

**Routing rule:** Any assumption with confidence < High, or any assumption whose
"Impact if Wrong" would change architecture or scope, must be confirmed by Main
before PRD approval. Tag the PRD submission `#CLARIFY` if any such assumptions exist.

### 8. Phase Map
Required for projects with more than 5 MVP features. Breaks the build into
phases so Developer works on Phase 1 only, while Main can validate that the
overall sequence makes sense before committing to Phase 1 architecture.
Format: `| Phase | Scope summary | Depends On | Target | Status |`

**Routing rule:** Main must validate the Phase Map before Developer starts Phase 1.
Key question Main must answer: "Does Phase 1 deliver standalone value, and would
Phase 2+ requirements change the Phase 1 architecture?" If yes — revise before build.

---

## PRD Completeness Checklist

Run this checklist before marking a PRD as ready for Developer handoff.
A PRD missing any ✅ item should be sent back to Architect.

### Structure
- [ ] Header block includes: Project, Version, Status, Author, Approved By, Date
- [ ] Problem statement supported by evidence or data, not just assertion
- [ ] Target users defined as roles with jobs-to-be-done, not just names
- [ ] Every MVP feature has at least one user story
- [ ] Every user story has a corresponding acceptance criterion
- [ ] Post-MVP items are explicitly listed (not just "future work")

### Metrics
- [ ] Every success metric has a numeric target
- [ ] Every success metric has a unit (seconds, %, count, etc.)
- [ ] Every success metric has a target date or milestone
- [ ] North Star metric is identified (the one metric that matters most)

### Handoff Readiness (Agent-Specific)
- [ ] Data schema or API contracts are defined (even if minimal)
- [ ] File and folder structure is specified
- [ ] Agent build order is present and sequenced
- [ ] No task in the build order depends on an unresolved open question
- [ ] All dependencies are listed with owners and risk flags

### Risk & Uncertainty
- [ ] Assumptions section present with confidence levels and impact if wrong
- [ ] Any assumption with confidence < High flagged for Main confirmation
- [ ] Open questions section present (state "None" explicitly if empty)
- [ ] Any OQ with deadline "before Developer starts" flagged with #CLARIFY
- [ ] Risks section present with mitigations
- [ ] If >5 MVP features: Phase Map present and validated by Main

### PRD Review Loop
When Main responds to #CLARIFY submissions, Architect must:
- **Confirms as-is** → mark resolved, no PRD change, continue to approval
- **Scoped correction** (changes specific sections) → update affected sections,
  increment version x.y, re-run checklist on changed sections, re-submit
- **Broad correction** (changes architecture, scope, or phase structure) →
  full PRD revision, increment version x+1.0, full re-submit
- **Max 3 loops** — if unresolved after 3 iterations, escalate to human operator

---

## Writing Principles

These principles apply regardless of project type or domain.

**Start with the problem, not the solution.**
The problem statement should be provable without the proposed solution existing.
If removing the feature list makes the problem statement collapse, rewrite it.

**Requirements describe what, not how.**
"The system sends a confirmation email" ✅
"The system uses SendGrid to send a confirmation email" ❌ (that's architecture)

**One requirement = one thing.**
If an acceptance criterion contains "and", split it into two criteria.

**Testability is mandatory.**
Every acceptance criterion must be verifiable by QA without human judgment.
"The UI is clean" is not testable. "All form fields have labels accessible to
screen readers" is testable.

**Metrics need baselines.**
A target without a baseline is unmeasurable. If no baseline exists, state
"Baseline to be established in first two weeks of development."

---

## Reference Files

| File | Load When |
|------|-----------|
| `references/prd-sections.md` | Writing or reviewing any PRD section in detail |
| `references/prd-examples.md` | Need annotated examples of well-written sections |

---

## Common Commands

```
# Draft a new PRD from a brief
"Write a PRD for [project/feature description]"

# Upgrade an existing PRD
"Review this PRD for completeness gaps" → run checklist above

# Handoff readiness check
"Is this PRD ready for Developer?" → run Handoff Readiness + Risk & Uncertainty checklists

# Clarify submission (when OQs or assumptions need Main resolution)
"Submit this PRD for clarification" → tag #CLARIFY, list unresolved items for Main

# Specific section help
"Write the user stories for this PRD" → load references/prd-sections.md#user-stories
"Write success metrics for this PRD" → load references/prd-sections.md#success-metrics
"Write the assumptions for this PRD" → load references/prd-sections.md#assumptions
"Write the phase map for this PRD"   → load references/prd-sections.md#phase-map
```
