<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: C4 Modules + Backlog + UX → rules/relevance-map.md (DISCOVERY)

## Purpose

Generates `rules/relevance-map.md` — the **code-area → reference-artifact** mapping that connects each code module to the specific backlog stories, wireframes, flows, and architecture references relevant to it. This is what turns "the files exist somewhere" into "when I work HERE, load THESE" — the input each platform adapter uses to wire contextual loading (Kiro fileMatch, Claude per-module `CLAUDE.md`, Cursor globs).

**Output:** `{workspace-root}/rules/relevance-map.md`

**Condition:** Generate IF ADLC present (needs C4 L3 module structure) AND at least one reference cluster (POLC or UXD) present. Without modules there's nothing to map from; without reference material there's nothing to map to.

**Cluster:** Cross-cutting (bridges ADLC module structure ↔ POLC/UXD reference material).

**Type:** Derived index — NOT a governed element. Auto-regenerated on re-baseline; manual `<!-- custom -->` refinements preserved.

---

## MANDATORY: Stage Sub-Role — Workspace Architect + Business Analyst

Workspace Architect (structure) layered with Business Analyst (matching intent to modules). ADDS a dimension — does NOT replace the primary role.

### Behavioral Shifts
- Match by meaning, not just string equality — `employee-onboarding` module ↔ `EPIC-001_Employee-Onboarding` ↔ `WF-01_Employee-Onboarding`
- When confident, auto-map; when unsure, mark `<!-- VERIFY -->` for human curation
- Preserve human refinements — never overwrite a `<!-- custom -->` mapping on re-baseline

### Anti-Patterns
- Do NOT force a mapping when naming doesn't align — flag it instead
- Do NOT overwrite manual curation
- Do NOT invent modules or artifacts not in the source

---

## Source Inputs

| Source | What to Extract | Used For |
|--------|-----------------|----------|
| AP `component-design.md` (C4 L3) | Module names + paths (`src/modules/{x}/`) | The "from" side (code areas) |
| PBP `epic-decomposition.md` + `backlog/epics/` | Epic IDs + titles + story files | The "to" side (backlog) |
| UXP wireframes / flows / personas | `WF-*`, `UF-*` names | The "to" side (UX) |
| AP ADRs + constraints | ADR IDs, constraint IDs | The "to" side (architecture) |

---

## Derivation Strategy (Auto-Map with Fallback)

### Step 1: Normalize names
Slugify module, epic, and wireframe names to a common form:
- `src/modules/employee-onboarding/` → `employee-onboarding`
- `EPIC-001_Employee-Onboarding` → `employee-onboarding`
- `WF-01_Employee-Onboarding` → `employee-onboarding`

### Step 2: Match by normalized name
When normalized names align across module ↔ epic ↔ wireframe → **auto-map** (high confidence).

### Step 3: Fallback for non-aligned
When a module has no clear epic/wireframe match (names don't align) → emit the row with a `<!-- VERIFY: manual curation needed -->` marker and best-guess candidates.

### Step 4: Preserve manual curation
On re-baseline, rows (or cells) marked `<!-- custom -->` are preserved verbatim — DWG re-derives only the non-custom rows.

---

## Target Structure: rules/relevance-map.md

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AP component-design.md (C4 L3) + backlog/ + ux/"
generatedOn: "{generation-date}"
ownership: hybrid
projectId: "{project-id}"
---
<!-- DWG-BASELINE: v{N} (confirmed v{N}) | {projectId} | {timestamp} -->

# Relevance Map

> When working in a code area, consult the mapped reference material.
> Auto-derived from C4 module structure + naming. Manual edits: mark `<!-- custom -->` to survive re-baseline.

| Code Area | Backlog | Wireframes | Flows | Architecture |
|-----------|---------|------------|-------|--------------|
| `src/modules/employee-onboarding/` | `backlog/epics/EPIC-001_stories/` | `ux/wireframes/WF-01_*.md` | `ux/user-flows/UF-01_*.md` | ADR-001, C-05 |
| `src/modules/payroll-processing/` | `backlog/epics/EPIC-002_stories/` | `ux/wireframes/WF-02_*.md` | `ux/user-flows/UF-02_*.md` | ADR-004 |
| `src/shared/auth/` <!-- VERIFY: manual curation needed --> | (no direct epic) | — | — | ADR-001 (security), C-07 |
| … | … | … | … | … |

## Global (applies everywhere)
- Security: `rules/security-rules.md` + `architecture/constraint-register.md` (C-05, C-07)
- Definition of Done: `backlog/DEFINITION_OF_DONE.md`
```

---

## How Adapters Consume This

The relevance map is the **source** each platform adapter reads to wire contextual loading:

| Platform | How it uses relevance-map |
|----------|---------------------------|
| Kiro | Each row → a `fileMatch` steering file (`fileMatchPattern: 'src/modules/{x}/**'`) surfacing the mapped refs |
| Claude Code | Each row → a `src/{module}/CLAUDE.md` listing the mapped refs (auto-loads on dir touch) |
| Cursor | Each row → a `.cursor/rules/{module}.mdc` with `globs: ['src/modules/{x}/**']` |
| Codex / Generic | Rendered as a table in `AGENTS.md` / `WORKSPACE_GUIDE.md` (manual lookup) |

DWG generates the relevance map ONCE (canonical, in `rules/`); adapters translate it per platform.

---

## Transformation Rules

### Rule 1: Auto-Map by Normalized Name
Module ↔ epic ↔ wireframe matched on slugified name. High-confidence matches are auto-filled.

### Rule 2: Flag Uncertain Rows
No clear match → `<!-- VERIFY: manual curation needed -->` + best-guess candidates. Never force a wrong mapping.

### Rule 3: Preserve `<!-- custom -->`
Manual refinements survive re-baseline. DWG re-derives only non-custom rows.

### Rule 4: Global Section for Cross-Cutting
Security, DoD, and other always-applicable refs go in the Global section, not per-module.

### Rule 5: Not a Governed Element
Auto-regenerated; GCE does not drift-scan it (derived index — see context-map-generation Governance Note).

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| ADLC absent (no modules) | SKIP — no "from" side; relevance map not generated |
| POLC + UXD both absent | SKIP — no "to" side |
| Module with no matching epic/wireframe | Emit row with `<!-- VERIFY -->` + candidates |
| Names don't follow any convention | Emit skeleton rows (all modules) with `<!-- VERIFY -->`; full manual curation |
| Re-baseline after manual curation | Preserve `<!-- custom -->` rows; re-derive the rest |

---

## Output Validation

- [ ] `rules/relevance-map.md` generated when ADLC + (POLC or UXD) present
- [ ] One row per C4 module
- [ ] High-confidence matches auto-filled; uncertain rows flagged `<!-- VERIFY -->`
- [ ] Global section covers cross-cutting refs
- [ ] `<!-- custom -->` rows preserved on re-baseline
- [ ] Baseline stamp present
- [ ] All referenced paths resolve
