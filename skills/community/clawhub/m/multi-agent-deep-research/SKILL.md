---
name: openclaw-deep-research
description: Coordinate deep, source-verifiable research projects in OpenClaw using AgentSkills-compatible folders, local artifact tracking, and explicit evidence ledgers. Use when the user wants a high-quality report or investigation that spans many sources, needs auditable claims, benefits from delegation, or must manage context-window limits by writing project state to local files during an OpenClaw workflow.
---

# OpenClaw Deep Research

Run research as a file-backed production workflow, not as a chat-only exercise. Optimize for source traceability, narrow ownership, compact handoffs, and a final report that distinguishes facts, interpretations, comparisons, and forecasts.

## Platform notes

- Install this skill under `~/.openclaw/skills/openclaw-deep-research/` for user-wide use or `skills/openclaw-deep-research/` inside a workspace when using OpenClaw local skills.
- Keep the actual research directory under the active workspace so report artifacts remain close to the task.
- Assume delegation is optional. Use subagents only if the current OpenClaw setup exposes them and the user explicitly wants parallel work.

## Quick start

1. Freeze the topic, audience, report shape, and research cutoff date before collecting sources.
2. Create one canonical project root in the current workspace and treat it as the single source of truth.
3. Persist project memory immediately: status, task board, source ledger, claim ledger, fact-check log, handoffs, and draft report.
4. If the user explicitly wants multi-agent work, split the project into bounded roles with disjoint write scopes. Otherwise use the same workflow locally without delegation.
5. Collect sources first, write claims second, draft only from verified claims, and end with a QA pass that checks dates, comparability, and unsupported conclusions.

## Non-negotiables

- Keep exactly one canonical project directory.
- Write project memory to local files; do not rely on chat history as durable state.
- Prefer primary sources for unstable or high-stakes facts.
- Give every substantive claim a `claim_id` and at least one `source_id`.
- Put absolute dates on fast-moving facts and on the report cutoff.
- State the comparison metric and time window whenever comparing countries, companies, models, markets, or policies.
- Separate `hard_fact`, `reported_fact`, `interpretation`, `comparison`, and `forecast`.
- Do not let multiple agents edit the same files unless the user explicitly wants that tradeoff.

## Workflow

### 1. Freeze scope

- Clarify the research question, target reader, deliverable format, and report cutoff date.
- Prefer dimensional comparison over a single headline ranking when the topic is structurally uneven.
- Record the scope and stop conditions before searching.

For a starter layout, load `references/project-layout.md`.

### 2. Create the file-backed workspace

- Create the project root and a minimal scaffold for workflow, sources, claims, checks, handoffs, and deliverables.
- Record current phase, next actions, and open questions in a short status file.
- Update these files every round so a later agent can resume without replaying chat.

For copy-paste starter files, load `references/templates.md`.

### 3. Decide the delegation pattern

- Only use OpenClaw subagents when the user explicitly asks for multi-agent or delegation work and the current setup supports them.
- Use one agent per bounded responsibility or per independent research slice.
- Assign each agent one objective, one read set, one write scope, one cutoff date, and one handoff target.
- Keep the PM/orchestrator role local whenever possible so synthesis and quality control stay centralized.

For role options and handoff contracts, load `references/delegation-patterns.md`.

### 4. Collect sources

- Build the source ledger before building the narrative.
- Prioritize primary sources: official documents, filings, company docs, papers, model cards, release notes, government pages, and original datasets.
- Use high-quality secondary sources for synthesis and triangulation when primary material is incomplete.
- Record enough metadata that another reviewer can reopen the source later.

For evidence rules and claim classes, load `references/evidence-standards.md`.

### 5. Build claims

- Convert source notes into atomic claims.
- Attach `source_id`, claim class, confidence, date range, and comparability notes.
- Mark unsupported or unresolved claims as `draft`, `blocked`, `contested`, or equivalent; do not quietly promote them into the report.

### 6. Normalize comparisons

- Build a comparison matrix when the report compares two or more entities.
- Explicitly mark rows as `comparable`, `partial`, or `not_comparable`.
- If two sources use different units, populations, definitions, or time windows, say so instead of forcing a clean ranking.

### 7. Draft the report

- Put the research cutoff date near the top.
- Draft from verified claims only.
- Keep the main text readable, but make the evidence chain auditable through source and claim ledgers.
- Include a methods section, limits section, and open questions or future watchpoints section.

### 8. QA the report

- Recheck every numerical claim, dated statement, and leadership claim.
- Downgrade or remove statements that are true only under narrow assumptions.
- Ensure the final report does not blur facts and inference.
- Confirm that every citation in the report resolves back to the local ledgers.

## Delegation rules

- Keep agent ownership disjoint by file path or by work package.
- Require every handoff to include: `done`, `verified`, `open`, `next`, and changed files.
- Do not ask scouts to write synthesis if their job is evidence collection.
- Do not ask drafters to invent facts or fill gaps from memory.
- Route conflicts back to the source layer, not to a rhetorical compromise.

## Writing rules

- Prefer direct, dated language: "As of 2026-03-21..." over relative timing.
- Use cautious wording for vendor claims, self-reported performance, and fast-moving policy changes.
- Avoid totalizing conclusions like "X is winning overall" unless the evidence really supports that scope.
- End with what is still uncertain and what could change the conclusion.

## Reference map

- `references/project-layout.md` -> canonical directory structure and when to create each artifact.
- `references/delegation-patterns.md` -> role menu, handoff contract, and anti-duplication rules.
- `references/evidence-standards.md` -> source hierarchy, claim classes, and QA gates.
- `references/templates.md` -> compact starter templates for ledgers, status files, and handoffs.
- `references/platform-notes.md` -> OpenClaw specific installation and usage notes.
