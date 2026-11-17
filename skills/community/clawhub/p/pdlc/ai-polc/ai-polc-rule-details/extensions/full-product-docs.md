<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: Full Product Docs (Full Rules)

**Stage:** 12 (Product Documentation)
**Adds:** PRD template, feature brief template, product wiki governance, API change communication

---

## Additional Steps (extend Stage 12)

### Step 12.E1: PRD Template

Product Requirement Document — used to communicate a feature/epic to stakeholders before build:

```markdown
# PRD: {Feature/Epic Name}

## Problem Statement
{What problem does this solve? Who has this problem? How bad is it?}

## Proposed Solution
{What are we building? How does it solve the problem?}

## Scope
### In Scope
- {item 1}
- {item 2}

### Out of Scope
- {item 1 — and why it's out}

## Success Metrics
| Metric | Baseline | Target | Measurement |
|--------|----------|--------|------------|
| {metric} | {current} | {goal} | {how measured} |

## User Stories (Summary)
{List of key stories or link to Tier 2 output}

## Dependencies
- {Technical dependencies}
- {Business dependencies}
- {External dependencies}

## Timeline (Estimated)
- Design: {duration}
- Build: {duration}
- Test: {duration}
- Release: {target}

## Risks
{Key risks from risk register relevant to this feature}

## Stakeholder Sign-Off
| Role | Name | Status |
|------|------|:---:|
| PO | {name} | ✅ |
| Sponsor | {name} | Pending |
| Tech Lead | {name} | Pending |
```

### Step 12.E2: Feature Brief Template

Shorter than a PRD — for communicating upcoming work:

```markdown
# Feature Brief: {Name}

**Epic:** EPIC-{NNN}
**Priority:** {rank}
**Target Release:** R{N}
**Status:** {Planned | In Progress | Shipped}

## One-Liner
{What this feature does in one sentence}

## Why Now
{Why this is prioritized for this release — value justification}

## What Users Get
{User-facing description — what changes for them}

## What's NOT Included
{Explicit scope boundaries}

## Success Looks Like
{1-2 measurable outcomes}
```

### Step 12.E3: Product Wiki Governance

For teams maintaining a product knowledge base:

| Aspect | Rule |
|--------|------|
| Structure | Mirror roadmap themes as top-level sections |
| Ownership | PO owns structure; team owns technical content |
| Update cadence | Per release (minimum); per sprint (recommended) |
| Archive policy | Move shipped feature docs to "Released" section |
| Versioning | Match product version numbering |

### Step 12.E4: API Change Communication

For developer-facing products:

```markdown
# API Change Notice: {version}

## Breaking Changes
| Endpoint | Change | Migration Path | Deadline |
|----------|--------|---------------|----------|
| {endpoint} | {what changed} | {how to migrate} | {date} |

## New Endpoints
| Endpoint | Purpose | Availability |
|----------|---------|:---:|
| {endpoint} | {what it does} | {date} |

## Deprecations
| Endpoint | Replacement | Removal Date |
|----------|------------|:---:|
| {old} | {new} | {date} |
```

---

## Additional Output

When active, Stage 12 produces:
- PRD template (reusable for future epics)
- Feature brief template
- Wiki governance rules
- API change notice template (if developer-facing product)

All stored in the PBP output alongside `release-notes-governance.md`.
