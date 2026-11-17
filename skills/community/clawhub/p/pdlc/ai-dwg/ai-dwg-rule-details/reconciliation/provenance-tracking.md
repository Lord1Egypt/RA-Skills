<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Provenance Tracking — Marking AP-Sourced vs. Team-Added Content

## Purpose

Defines how AI-DWG marks generated content to distinguish architecture-sourced rules from team additions. This enables future reconciliation to know what it can update and what it must preserve.

---

## MANDATORY: Stage Sub-Role — Workspace Architect

During THIS activity, ALSO adopt the mindset of a **Workspace Architect**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Provenance markers are the reconciliation contract — every marker pair you place determines what future diff/merge can touch
- Think about the file's evolution over time: starts as 100% AP-sourced, gradually teams add content outside markers — the architecture matures organically
- The reconciliation log is the institutional memory — append-only history of what changed, why, and who approved or rejected
- Ensure marker placement is granular — one pair per logical section, not one giant pair around the whole file
- File-level provenance headers establish traceability — every generated file must link back to its AP source artifact

### Anti-Patterns for This Activity
- Do NOT nest markers (begin inside begin) — this breaks reconciliation parsing
- Do NOT place team-intended content inside AP markers — it will be overwritten on next reconciliation
- Do NOT skip provenance headers on any generated file — without them, the file is orphaned from its AP source

### Quality Check
A good output from this activity sounds like:
- "File structure: provenance header → AP-sourced section (rules table) → team section (custom overrides) → second AP-sourced section (anti-patterns). Team content between markers is untouchable."
- "Reconciliation log entry: 2026-06-10 — API-RATE-02 modified (1000→2000 req/min), approved. AUTH-02 modification rejected (team prefers 15min). resilience-standards.md generated (microservices extension now active)."

---

## Provenance Markers

### File-Level Marker (Header)

Every AI-DWG generated file includes a provenance header as the FIRST content after front-matter:

```markdown
<!-- AI-DWG generated | source: {AP artifact name} | date: {YYYY-MM-DD} -->
```

**Fields:**
| Field | Value | Purpose |
|-------|-------|---------|
| `source` | Name of the primary AP artifact that drove this file's generation | Traceability |
| `date` | Date of generation or last reconciliation | Versioning |

**Examples:**
```markdown
<!-- AI-DWG generated | source: Security & Identity Architecture | date: 2026-06-10 -->
<!-- AI-DWG generated | source: Component Design (C4 L3) | date: 2026-06-10 -->
<!-- AI-DWG generated | source: Multiple AP artifacts | date: 2026-06-10 -->
```

---

### Section-Level Markers (Content Boundaries)

Within each file, AP-sourced content is wrapped in markers:

```markdown
<!-- begin: AP-sourced -->
{Content derived from Architecture Package — reconciliation may update this}
<!-- end: AP-sourced -->
```

**Rules for marker placement:**
1. Place markers around EACH logical section that comes from the AP
2. A file can have MULTIPLE marker pairs (one per section)
3. Content BETWEEN different marker pairs (gap content) is team-owned
4. Content AFTER the last marker pair is team-owned
5. Content BEFORE the first marker pair (after the file header) is team-owned

---

### Example: Annotated Steering File

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: API Architecture | date: 2026-06-10 -->

# API Standards                              ← Team can rename/adjust heading

## API Identity                              ← Team can add intro text here

<!-- begin: AP-sourced -->
**Style:** REST (resource-oriented)
**Format:** JSON only
**Base path:** /api/v1
<!-- end: AP-sourced -->

## URL Conventions

<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| API-URL-01 | Use kebab-case for URL paths |
| API-URL-02 | Resources are plural nouns |
| API-URL-03 | Nested resources for parent-child |
<!-- end: AP-sourced -->

## Team-Specific URL Notes               ← TEAM SECTION — never touched

We also follow these internal conventions:
- Admin endpoints use /admin/ prefix
- Internal endpoints use /internal/ prefix
(These are team decisions not from architecture)

## HTTP Methods

<!-- begin: AP-sourced -->
| Method | Usage | Idempotent |
|--------|-------|:----------:|
| GET | Retrieve | Yes |
| POST | Create | No |
...
<!-- end: AP-sourced -->

## Our Custom Rate Limit Exceptions      ← TEAM SECTION — never touched

The marketing API has special rate limits agreed with the client team:
- /api/v1/campaigns: 500 req/min (override)
```

---

## Reconciliation Log

After every reconciliation, append to a log file at workspace root:

### File: `.kiro/reconciliation-log.md`

```markdown
# Reconciliation Log

## {YYYY-MM-DD} — Reconciliation #{n}

**Trigger:** {what changed — e.g., "API Architecture updated rate limits"}
**AP artifacts read:** {list}
**Files affected:** {list}

### Changes Applied

| File | Change | Type | Approved |
|------|--------|:----:|:--------:|
| api-standards.md | API-RATE-02: 1000→2000 req/min | MODIFY | ✅ |
| api-standards.md | API-RATE-05: added burst limit rule | ADD | ✅ |
| error-handling.md | No changes needed | — | — |

### Changes Rejected

| File | Change | Type | Reason |
|------|--------|:----:|--------|
| security-rules.md | AUTH-02: 15min→10min token expiry | MODIFY | Team prefers 15min |

### Structural Changes

| Action | File | Reason |
|--------|------|--------|
| Generated | resilience-standards.md | Microservices extension now active |

---
```

---

## Provenance Rules

| # | Rule |
|---|------|
| 1 | EVERY file generated by AI-DWG MUST have the file-level provenance header |
| 2 | EVERY AP-derived section MUST be wrapped in `<!-- begin/end: AP-sourced -->` markers |
| 3 | Markers MUST NOT be nested (no begin inside begin) |
| 4 | Markers MUST be paired (every begin has exactly one end) |
| 5 | Team content MUST be outside markers — if team wants to override an AP rule, they add their version AFTER the AP section |
| 6 | If team modifies content INSIDE markers — it's a conflict during next reconciliation (their choice will be flagged) |
| 7 | The reconciliation log is append-only — history of all changes |
| 8 | Provenance date updates on EVERY reconciliation that touches the file |

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| File has no markers (externally created or markers stripped) | Treat as 100% team-owned — append-only mode for reconciliation |
| Team moved AP content outside markers (intentional override) | Respect — that content is now team-owned |
| Team deleted AP markers but kept content | Content is now team-owned — reconciliation adds new AP sections but doesn't update the unmarked content |
| Multiple AP sources for one file | Use `<!-- begin: AP-sourced ({specific source}) -->` for disambiguation |
| Reconciliation log becomes very large | Keep last 20 entries; archive older ones |

---

## Initial Generation (Mode 1) Provenance

During first generation, EVERYTHING is AP-sourced. The initial file looks like:

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: {AP artifact} | date: {date} -->

# {Title}

<!-- begin: AP-sourced -->
{All generated content}
<!-- end: AP-sourced -->
```

Over time, teams add content OUTSIDE the markers — the file naturally evolves from "100% AP" to "AP core + team extensions."
