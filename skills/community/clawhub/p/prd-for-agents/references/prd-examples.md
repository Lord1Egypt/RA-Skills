# PRD Examples Reference

Annotated examples of each PRD section done well. Use these as models when writing or reviewing.
All examples use a fictional "Agent Ledger" project — a file-based PSA tracking system for multi-agent foundries.

---

## Problem Statement — Good Example

> The Product Foundry operates with multiple AI agents executing work across concurrent
> projects. Without a structured tracking layer, three compounding problems emerge.
>
> **Gap 1 — No operational record.** Agents start fresh each session with no shared
> awareness of what was done, by whom, or what comes next. In 3 of 5 observed sessions,
> Developer repeated work Architect had already completed. Estimated waste: 30–60 minutes
> per project per week.
>
> **Gap 2 — No cross-project visibility.** An agent starting a new session cannot
> understand what is happening across the Foundry — only within a single project folder.
> The operator has no aggregated readiness signal.
>
> **Gap 3 — No cost awareness.** Token costs accumulate with no attribution to projects
> or features. After a 4-hour session, the operator cannot answer "what did that cost and
> what was it for?"

**Why this works:**
- Three specific, named gaps (not one vague problem)
- Evidence: "3 of 5 observed sessions" — observable, not assumed
- Quantified impact: "30–60 minutes per project per week"
- Each gap is independently real — removing one doesn't invalidate the others

---

## User Stories — Good Examples

```markdown
### US-01 — Session Resumption
**As a** Developer Agent,
**I want to** read a Session Log entry that summarises what was done last session,
**so that** I can resume work in under 30 seconds without re-reading all task history.

**Acceptance:** Given a TRACKING.md with a Session Log entry, Developer can identify
the correct next task without reading any other section.
**Feature:** F8 — Session Handoff Notes
**Priority:** Must Have

---

### US-02 — Cross-Project Visibility
**As a** Product Owner (Human),
**I want to** open one file (DASHBOARD.md) and see the status of all active projects,
**so that** I can do a morning review in under 2 minutes without opening individual project folders.

**Acceptance:** DASHBOARD.md contains all active projects, each with current task status
and assigned agent, updated within the same session as the last status change.
**Feature:** F5 — Dashboard View
**Priority:** Must Have

---

### US-03 — Cost Attribution
**As a** Product Owner (Human),
**I want to** see how many hours each agent has logged against each project,
**so that** I can evaluate which projects are consuming the most agent time and adjust priorities.

**Acceptance:** Agent Summary table in TRACKING.md shows total hours per agent,
reconciling with the sum of individual time log entries (within ±0.1 hours).
**Feature:** F9 — Agent Summary
**Priority:** Should Have
```

**Why these work:**
- Role is specific ("Developer Agent" not just "user")
- "So that" states an outcome, not a feature
- Acceptance line is one sentence and binary (pass/fail)
- Each maps to a numbered feature

---

## Quantitative Success Metrics — Good Example

```markdown
| Metric | Baseline | Target | Target Date | Measurement Method |
|--------|----------|--------|-------------|-------------------|
| ⭐ Agent cold-start context time | ~5 min (re-read all files) | < 30 seconds | 2026-06-01 | Time from session start to first task action, measured across 10 sessions |
| Dashboard staleness (time since last update) | Not tracked | Same session as last status change | 2026-06-01 | Check Last Updated timestamp vs most recent TRACKING.md edit |
| Orphaned tasks (tasks with no parent capability) | Not tracked | 0 per project | 2026-06-01 | Count tasks without a `## Capability:` parent in TRACKING.md |
| Time log tables with correct Total rows | Not tracked | ≥ 95% | 2026-06-01 | Count tables with `\| **Total** \|` row / total tables |
| Dependency violations (blocked task started without clearing) | Not tracked | 0 per sprint | Per sprint review | QA flags during review; count in QA-REPORT.md |
```

**Why this works:**
- ⭐ marks the North Star metric
- Every metric has a number AND a unit AND a date
- Baselines are honest — "Not tracked" with a plan is fine
- Measurement method explains *how* to verify, not just what to measure
- Metrics are outcomes (agent behavior, system state), not outputs (features shipped)

---

## Dependencies — Good Example

```markdown
| Dependency | Type | Owner | Required By | Risk if Late |
|------------|------|-------|-------------|--------------|
| Ollama runtime (local) | Service | Developer machine | Step 1 | Developer agent cannot run local models; all builds fail |
| OpenClaw `read` and `edit` tools | API | OpenClaw gateway | Step 1 | Agents cannot read or write TRACKING.md; entire system non-functional |
| Python 3.x | Library | Developer machine | Step 6 (reporting scripts) | Post-MVP scripts cannot run; MVP unaffected |
| Main agent approval of PRD | Approval | Sanket Sao | Before Developer starts | Developer cannot begin; project stalls |
| `_template/` project scaffold | Feature | Architect (this project) | Step 2 | Developer cannot bootstrap new projects; must create files manually |
```

**Why this works:**
- Every dependency has an owner — no ambiguity about who's responsible
- "Required By" is specific (step number, not just "early")
- "Risk if Late" states the exact downstream impact on the build order

---

## Open Questions — Good Example

```markdown
| # | Question | Owner | Deadline | Impact if Unresolved |
|---|----------|-------|----------|----------------------|
| OQ-1 | Should DASHBOARD.md live at workspace root or inside projects/? Current ARCHITECTURE.md says workspace root but some agents have been writing to projects/DASHBOARD.md. | Architect | Before Developer starts Step 3 | Developer creates file in wrong location; all agents point to different paths |
| OQ-2 | Should the Agent Summary table be manually updated by Architect (current spec) or auto-calculated from time log totals by a script (post-MVP)? If script, should it run at session end as a hook? | Sanket Sao | Before Developer starts Step 7 | If script, adds Step 7a to build order and requires Python dependency |
| ~~OQ-3~~ | ~~Should `On Hold` projects appear in DASHBOARD.md?~~ — **Resolved:** Yes, in a separate section. 2026-04-29. | — | — | — |
```

**Why this works:**
- OQ-1 is specific: names the exact conflict and where it appears
- OQ-2 shows how an open question can branch the build order — critical for agents
- OQ-3 shows resolved format — keep resolved questions for traceability, but strike them through
- Every open question has a deadline tied to a build step, not a calendar date

---

## Risks — Good Example

```markdown
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Local model (gemma4, qwen3.5) fails to correctly format TRACKING.md table syntax | High | High | Include exact table format examples in Architect handoff notes; QA validates all tables in first pass |
| Two agent sessions write to TRACKING.md simultaneously, causing data loss | Low | High | Assign one task per agent at a time (enforced by DASHBOARD.md Active Agents block); Architect reviews for conflicts at session start |
| DASHBOARD.md becomes stale because Architect forgets to regenerate | High | Medium | Add DASHBOARD.md regeneration to Architect's session-end checklist in AGENTS.md; timestamp makes staleness visible |
| File grows too large for local model context window (>50 tasks in one TRACKING.md) | Low (MVP) | Medium | Document 50-task soft limit; post-MVP: split by capability into separate files |
| QA agent misidentifies a logic flaw as a bug, routing to Developer instead of Architect | Medium | Medium | Require QA to include PRD section reference in every escalation tag; Architect reviews all #BUG escalations that touch schema or data model |
```

**Why this works:**
- Risks are specific to *this* system and *these* agents — not generic
- Mitigations are concrete actions with an owner implied
- Likelihood × Impact framing helps prioritize which risks to address first
- Agent-specific risks (local model formatting failures, context window limits) are included

---

## Agent Build Order — Good Example

```markdown
| Step | Task | Feature | Complexity | Depends On |
|------|------|---------|------------|------------|
| 1 | Create `_template/` directory with blank TRACKING.md, PRD.md, VISION.md, MILESTONES.md, STATUS.md, CHANGELOG.md | F6 | S | — |
| 2 | Write TRACKING.md v2 schema with all required fields (Priority, Target Date, Owner, Blockers, Session, Total rows) | F1–F4 | M | Step 1 |
| 3 | Create DASHBOARD.md at workspace root with Foundry Summary, Active Agents, per-project, and Blocked Tasks sections | F5, F10 | M | Step 2 |
| 4 | Add Session Log section to TRACKING.md template (append-only, one row per session) | F8 | S | Step 2 |
| 5 | Add Agent Summary section to TRACKING.md template (per-agent hours + task counts) | F9 | S | Step 2 |
| 6 | Validate all v2 schema fields are present in TRACKING.md and DASHBOARD.md | F1–F5 | S | Steps 3–5 |
| 7 | Update CHANGELOG.md to document v2 schema upgrade | — | S | Step 6 |
| 8 | Update STATUS.md with completed tasks and session log entry | — | S | Step 7 |
```

**Why this works:**
- Foundation first: template scaffold (Step 1) before any content (Step 2+)
- Each step is completable in a single agent session (no multi-hour L tasks without reason)
- Dependencies are explicit — no guessing what must come first
- Steps 6–8 are housekeeping steps (validate, changelog, status) — included, not assumed
- Complexity is honest — M for files that touch multiple sections, S for single-section work
