<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: UX Design Package (AI-UXD) → navigation-structure.md (UXD CLUSTER)

## Purpose

Transforms the **information architecture** produced by AI-UXD (`define/information-architecture.md` — site map, navigation model, taxonomy, search strategy) into a prescriptive `navigation-structure.md` steering file. This governs how the application's routes, navigation, and content hierarchy are built, so AI-DLC v1 scaffolds routing and nav components that match the designed IA instead of improvising structure.

**Output:** `rules/navigation-structure.md`

**Condition:** Generate IF `uxd-state.md` is present AND the UXP contains an information-architecture artefact.

**Cluster:** UX — belongs exclusively to the UXD input cluster.

---

## MANDATORY: Stage Sub-Role — UX Designer

During THIS activity, ALSO adopt the mindset of a **UX Designer**. ADDS a thinking dimension — does NOT replace your primary role.

### Behavioral Shifts
- Navigation is structure, not decoration — the IA is the skeleton routes hang from
- Taxonomy terms are the product's vocabulary — preserve labels verbatim (they appear in URLs, menus, breadcrumbs)
- A route hierarchy mirrors the site map — depth and grouping are deliberate
- Search strategy is part of IA — how content is found is as designed as how it is organized

### Anti-Patterns for This Activity
- Do NOT rename navigation labels or taxonomy terms — they are user-facing vocabulary
- Do NOT flatten a deliberately nested hierarchy
- Do NOT invent routes the IA does not define

---

## Source Inputs

**Primary source:** AI-UXD → UXP, via `uxd-state.md` marker.

| UXP Document | What to Extract | Maps to Section |
|---|---|---|
| Information Architecture (site map) | Page/section hierarchy | Route Hierarchy |
| Navigation model | Primary/secondary/utility nav, breadcrumb model | Navigation Rules |
| Taxonomy | Categories, tags, content types, labels | Taxonomy & Labels |
| Search strategy | Search scope, filters, facets, results model | Search Rules |
| User flows (`define/user-flow-design.md`) | Entry points, key paths | Route entry/guard notes |

### `uxd-state.md` Fields Used

| Field | Used For |
|-------|----------|
| `Completed Stages` | Confirm Phase 2 (Define) complete — IA produced |
| `Design Depth` | Minimal → primary nav only; Comprehensive → full taxonomy + search facets |
| `Project ID` | Correlation key |

---

## Target Structure: navigation-structure.md

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-UXD — define/information-architecture.md"
generatedOn: "{generation-date}"
ownership: generated
projectId: "{project-id}"
---

<!-- AI-DWG generated | source: AI-UXD Information Architecture | date: {generation-date} -->

# Navigation & Information Architecture Rules

## Route Hierarchy
<!-- begin: UXP-sourced -->
| Rule ID | Route | Label | Parent | Access | Notes |
|---------|-------|-------|--------|--------|-------|
| NAV-RT-01 | `/{route}` | {label} | {parent or —} | {public/auth} | {entry point / guard} |
| ... | ... | ... | ... | ... | ... |
<!-- end: UXP-sourced -->

## Navigation Rules
| Rule ID | Rule |
|---------|------|
| NAV-01 | Primary navigation MUST contain exactly: {items}. MUST NOT add unlisted top-level items without IA update. |
| NAV-02 | Breadcrumbs MUST reflect the route hierarchy above. |
| NAV-03 | {secondary/utility nav rules} |

## Taxonomy & Labels
| Rule ID | Term | Type (category/tag/content-type) | Usage |
|---------|------|----------------------------------|-------|
| NAV-TAX-01 | {term} | {type} | MUST use this exact label in UI, URLs, and metadata |

## Search Rules (IF search strategy present)
| Rule ID | Rule |
|---------|------|
| NAV-SR-01 | Search scope: {scope}. MUST index: {content types}. |
| NAV-SR-02 | Facets/filters MUST be: {facets}. |
```

---

## Transformation Rules

### Rule 1: Labels & Taxonomy Are VERBATIM
Navigation labels, route slugs, and taxonomy terms are copied exactly — they are user-facing vocabulary.

### Rule 2: Hierarchy Depth Is Preserved
The route table's `Parent` column reproduces the site-map nesting exactly.

### Rule 3: Prescriptive Nav Constraints
Every nav rule uses MUST/MUST NOT (e.g., "MUST NOT add unlisted top-level items").

### Rule 4: Search Section Is Conditional
Generate Search Rules only if the UXP defines a search strategy; otherwise omit with `<!-- UXP defined no search strategy -->`.

---

## Interaction with Other Mappings

| Related Mapping | Relationship |
|---|---|
| `containers-to-frontend.md` | `frontend-standards.md` governs HOW routes/components are coded; this file governs WHAT the route/nav structure is. No overlap. |
| `uxd-to-design-system.md` | Nav components reference design-system tokens; labels live here, styling there. |
| `components-to-structure.md` (ADLC) | If ADLC present, reconcile UXD route hierarchy with C4 frontend container structure; conflicts surface via the conflict gate. |

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| UXP present, no IA artefact | Skip; flag: "UXP lacks information architecture — navigation structure not generated" |
| IA defines content model but no routes | Generate Taxonomy + Search sections; mark Route Hierarchy `<!-- routes not specified -->` |
| Backend-only project (no UI) | Skip entirely (no nav surface) |
| IA conflicts with ADLC frontend containers | Cross-input conflict — surface, do not resolve |

---

## Output Validation

- [ ] Navigation labels & taxonomy terms verbatim
- [ ] Route hierarchy preserves IA nesting
- [ ] Every nav rule is prescriptive (MUST/MUST NOT)
- [ ] Search section present IFF UXP defines search strategy
- [ ] Provenance front-matter + projectId present
