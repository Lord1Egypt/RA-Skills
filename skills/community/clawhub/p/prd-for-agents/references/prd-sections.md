# PRD Sections Reference

Detailed guidance for every section in the prd-architect template.

## Table of Contents
1. [Header Block](#1-header-block)
2. [Problem Statement](#2-problem-statement)
3. [Target Users & Jobs-to-be-Done](#3-target-users--jobs-to-be-done)
4. [User Stories](#4-user-stories)
5. [Feature List](#5-feature-list)
6. [Acceptance Criteria](#6-acceptance-criteria)
7. [Success Metrics](#7-success-metrics)
8. [Data Schema & API Contracts](#8-data-schema--api-contracts)
9. [File & Folder Structure](#9-file--folder-structure)
10. [Agent Build Order](#10-agent-build-order)
11. [Dependencies](#11-dependencies)
12. [Open Questions](#12-open-questions)
13. [Risks](#13-risks)
14. [Out of Scope](#14-out-of-scope)

---

## 1. Header Block

Metadata that identifies the document and its state.

```markdown
# PRD — [Project Name]
**Project:** [Name]
**Version:** [1.0, 2.0, etc.]
**Status:** Draft | In Review | Approved | Superseded
**Author:** [Agent or person who wrote it]
**Approved By:** [Product Owner name — leave blank until approved]
**Date:** YYYY-MM-DD
**GitHub:** [repo URL if applicable]
```

**Rules:**
- Version increments on any structural change (new features, removed scope)
- Status must be `Approved` before Developer agent starts work
- Never delete old versions — use CHANGELOG.md to track changes

---

## 2. Problem Statement

The single most important section. Defines why this product exists.

**Structure:**
1. Current state (what is broken or missing today)
2. Impact (who is affected and how badly)
3. Evidence (data, observations, or user research that proves the problem)
4. Gap statement (what is missing that would solve it)

**Rules:**
- Must be provable without the proposed solution existing
- Must name specific users who experience the problem
- Should include at least one data point or observation as evidence
- Max 3 paragraphs — if you need more, the problem is not yet clear

**Anti-patterns:**
❌ "Users need a better way to track projects" (vague, no evidence)
❌ "We should build a dashboard because dashboards are useful" (solution-first)
✅ "Agents start each session with no shared awareness of project state.
   In 3 of 5 observed sessions, Developer repeated work that Architect had
   already completed, because there was no shared tracking file. This adds
   an estimated 30–60 minutes of redundant work per project per week."

---

## 3. Target Users & Jobs-to-be-Done

Who uses this and what they need to accomplish.

**Format:**
```markdown
| User | Job-to-be-Done | Frequency |
|------|----------------|-----------|
| [Role] | [When X, I need to Y, so I can Z] | Daily/Weekly/Per-project |
```

**Rules:**
- Use roles, not names ("Architect Agent", not "Alice")
- Jobs-to-be-done follow the format: "When [trigger], I need to [action], so I can [outcome]"
- Include frequency — it affects prioritization
- For agent-targeted PRDs, always include both agent users AND the human operator

---

## 4. User Stories

Testable expressions of requirements from the user's perspective.

**Format:**
```markdown
### US-01 — [Short Title]
**As a** [user role],
**I want to** [action or capability],
**so that** [outcome or value].

**Acceptance:** [one-line testable criterion that proves this story is done]
**Feature:** F[n] — links to feature list
**Priority:** Must Have | Should Have | Nice to Have
```

**Rules:**
- Every MVP feature (F1, F2…) must have at least one user story
- Each story must be independently testable
- "Acceptance" line is a one-sentence summary — full criteria go in Section 6
- Stories should describe outcomes, not UI specifics
- If a story requires more than 3 days of work, split it

**MoSCoW priority definitions:**
- **Must Have:** Product does not function without this
- **Should Have:** Significant value loss without this, but workarounds exist
- **Nice to Have:** Desirable but not delivery-blocking

---

## 5. Feature List

What the product does, organized by MVP and Post-MVP.

**Format:**
```markdown
### 🟢 MVP Scope

#### F1 — [Feature Name]
[2-3 sentence description of what this feature does and why it's needed]
- Sub-capability 1
- Sub-capability 2

### 🔵 Post-MVP (Out of Scope for V1)
- [Feature name] — [one-line rationale for deferral]
```

**Rules:**
- Features are numbered F1, F2… — referenced by user stories and acceptance criteria
- Each feature description answers: what does it do, not how it works
- Post-MVP items must be explicitly listed — "we'll add more later" is not acceptable
- If a feature has sub-capabilities, list them as bullets
- Complexity estimate (S/M/L) is optional but helpful for Developer agent

---

## 6. Acceptance Criteria

Testable conditions that define when each feature is complete.

**Format:**
```markdown
### F1 — [Feature Name]
- [ ] [Specific, testable condition]
- [ ] [Specific, testable condition]
```

**Rules:**
- Every criterion must be binary — pass or fail, no judgment calls
- Avoid "should" — use "must" or state the condition directly
- Each criterion covers exactly one thing (no "and")
- QA agent uses these as its test cases — write them for QA, not for humans
- If a criterion requires setup or context, add a note: `(requires project with 3+ tasks)`

**Testability test:** Can QA verify this criterion without asking a human what "good" looks like?
- ❌ "Dashboard looks clean and professional"
- ✅ "Dashboard renders without horizontal scroll on a 1280px viewport"
- ✅ "All table columns have header labels"

---

## 7. Success Metrics

How we know the product is working after it ships.

**Format:**
```markdown
| Metric | Baseline | Target | Target Date | Measurement Method |
|--------|----------|--------|-------------|-------------------|
| [What] | [Current state or "TBD — establish in week 1"] | [Number + unit] | [Date or milestone] | [How to measure] |
```

**Rules:**
- Every metric needs: a number, a unit, and a date
- Baseline is required — state "TBD" with a plan if it doesn't exist yet
- North Star metric must be identified (mark with ⭐)
- Metrics should be outcomes (user behavior, system performance), not outputs (features shipped)
- For agent-targeted products: include agent performance metrics, not just user metrics

**Metric categories to consider:**
- **Performance:** latency, throughput, uptime
- **Quality:** error rate, test coverage, defect escape rate
- **Adoption:** active users, feature usage rate, retention
- **Efficiency:** time-on-task, steps-to-complete, support tickets
- **Agent-specific:** cold-start context time, handoff accuracy, session continuity rate

---

## 8. Data Schema & API Contracts

The structure of data the product creates, reads, or exchanges.

**When to include:**
- Any time data is persisted (files, databases, APIs)
- Any time two agents or systems exchange structured data
- Any time a Developer agent needs to know what shape data takes

**Format for file-based schema:**
```markdown
### [File or Record Name]
\`\`\`markdown
**Field:** Value type and constraints
**Field:** Value type and constraints
\`\`\`
```

**Format for API contracts:**
```markdown
### POST /endpoint
**Request:**
\`\`\`json
{ "field": "type — description" }
\`\`\`
**Response:**
\`\`\`json
{ "field": "type — description" }
\`\`\`
**Errors:** 400 if X, 404 if Y
```

**Rules:**
- Define allowed values for enum fields explicitly
- Note which fields are required vs optional
- For file-based systems, show a complete example, not just field names
- Version the schema if it may change (Schema v1, v2…)

---

## 9. File & Folder Structure

The layout of files and directories the Developer agent will create.

**Format:**
```markdown
\`\`\`
project-root/
├── src/
│   ├── [file] — [purpose]
│   └── [file] — [purpose]
├── [file] — [purpose]
└── [file] — [purpose]
\`\`\`
```

**Rules:**
- Every file listed must have a one-line purpose description
- Distinguish between files the Developer creates vs files that already exist
- For agent foundry projects, include workspace files (TRACKING.md, PRD.md) in the tree
- If structure is large, show only the top 2 levels and describe subdirectories

---

## 10. Agent Build Order

The sequence in which a Developer agent should implement features.

**This is the most important section for agent handoff.** Without a build order,
Developer agents pick up tasks in the wrong sequence and create integration failures
that QA cannot resolve without design escalation.

**Format:**
```markdown
| Step | Task | Feature | Complexity | Depends On |
|------|------|---------|------------|------------|
| 1 | [Specific task description] | F[n] | S/M/L | — |
| 2 | [Specific task description] | F[n] | S/M/L | Step 1 |
```

**Complexity definitions:**
- **S (Small):** < 1 hour, single file, no integration
- **M (Medium):** 1–4 hours, multiple files, some integration
- **L (Large):** 4+ hours, cross-cutting concern, significant integration

**Rules:**
- Foundation before features (data models before UI, schema before logic)
- Independent tasks before dependent ones
- Each step should be completable in a single agent session
- If a step depends on an unresolved open question, flag it: `⚠ blocked by OQ-[n]`
- Total steps should map to a realistic session count for the Developer agent

---

## 11. Dependencies

External things this project requires that it does not own.

**Format:**
```markdown
| Dependency | Type | Owner | Required By | Risk if Late |
|------------|------|-------|-------------|--------------|
| [Name] | API / Library / Service / Approval / Feature | [Owner] | [Step or date] | [Impact] |
```

**Dependency types:**
- **API:** External service the product calls (Anthropic, Ollama, GitHub, etc.)
- **Library:** npm/pip package the code imports
- **Service:** Running infrastructure (gateway, database, auth)
- **Approval:** Human sign-off required before proceeding
- **Feature:** Another project feature that must ship first
- **Data:** Dataset or seed data required for the feature to function

**Rules:**
- If a dependency has no owner, escalate to Main before Developer starts
- Note the version or API version where relevant
- "Risk if Late" should be specific: "Developer cannot start Step 4" not just "delay"

---

## 12. Open Questions

Unresolved decisions that could change scope or design.

**Format:**
```markdown
| # | Question | Owner | Deadline | Impact if Unresolved |
|---|----------|-------|----------|----------------------|
| OQ-1 | [Question] | [Role] | [Date or "before Dev starts"] | [What changes] |
```

**Rules:**
- Every open question needs an owner — questions without owners never get answered
- Deadline should be "before Developer starts Step N" for agent-pipeline clarity
- If an open question is resolved, update to: `~~OQ-1~~ — Resolved: [answer] ([date])`
- A PRD with unresolved OQs that affect build order is NOT ready for Developer handoff
- If there are no open questions, state explicitly: `No open questions as of [date]`

---

## 13. Risks

Threats to delivery, quality, or adoption.

**Format:**
```markdown
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Risk description] | High/Med/Low | High/Med/Low | [Specific action to reduce risk] |
```

**Risk categories to consider:**
- **Technical:** Model capability limits, tool call failures, file conflicts
- **Scope:** Feature creep, unclear requirements, changing priorities
- **Dependency:** External API changes, library deprecations, blocked approvals
- **Agent-specific:** Local model tool-call failures, streaming bugs, context window limits
- **Adoption:** Users not understanding the system, poor documentation

**Rules:**
- Mitigation must be a specific action, not "monitor closely"
- High likelihood + High impact risks should block Developer start until mitigated
- For agent foundry projects, always include a risk for local model capability limits

---

## 14. Out of Scope

Explicit list of things this version does NOT include.

**Format:**
```markdown
- [Item] — [one-line rationale]
```

**Rules:**
- List things that were considered and explicitly deferred, not just random exclusions
- This section protects against scope creep — if it's not listed, it's open to debate
- Reference Post-MVP features here so they're findable in one place
- For agent-targeted PRDs, explicitly state infrastructure constraints:
  "No database, server, or API layer — file-based storage only"
