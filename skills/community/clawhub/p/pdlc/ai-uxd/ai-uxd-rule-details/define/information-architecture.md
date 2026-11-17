<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 5: Information Architecture

## Purpose

Define how the product's content, features, and functionality are organized, labeled, and navigated. The IA determines whether users can find what they need — it is the structural skeleton of the experience.

---

## Depth Adaptation

| Depth | IA Output |
|-------|-----------|
| **Minimal** | Site map + primary navigation model + key labels |
| **Standard** | Full 4-system IA (organization, labeling, navigation, search) + validation |
| **Comprehensive** | Full IA + taxonomy governance + cross-referencing strategy + content model |

---

## Steps

### Step 1: Define Organization System

How content is grouped and categorized:

| Scheme | Description | When to Use |
|--------|-------------|-------------|
| **Exact** | Alphabetical, chronological, geographic | Reference content, directories |
| **Ambiguous** | Topic, task, audience, metaphor | Most product UIs |
| **Hybrid** | Combination of schemes per section | Complex multi-use products |

Produce an organization map:
```markdown
## Organization System

| Section | Scheme | Rationale |
|---------|--------|-----------|
| {main area} | {scheme} | {why this organization} |
```

### Step 2: Build Site Map

Produce a hierarchical structure (max 3 levels deep for navigation):

```
├── {L1: Primary section}
│   ├── {L2: Sub-section}
│   │   ├── {L3: Page/feature}
│   │   └── {L3: Page/feature}
│   └── {L2: Sub-section}
├── {L1: Primary section}
│   └── {L2: Sub-section}
└── {L1: Utility section}
```

**Rules:**
- Max 5-7 items at any level (Miller's law: 7±2)
- Depth vs. breadth: prefer breadth (flat) over depth (nested) — users miss deep content
- Every leaf node maps to at least one user flow (Stage 6)

### Step 3: Define Labeling System

How things are named throughout the product:

```markdown
## Labeling System

### Navigation Labels
| Location | Label | Meaning | Alternatives Considered |
|----------|-------|---------|------------------------|
| Global nav | {label} | {what it contains} | {rejected alternatives + why} |

### Terminology Glossary
| Term | Definition | Context |
|------|-----------|---------|
| {product-specific term} | {plain definition} | {where it appears} |

### Labeling Rules
1. Use verbs for actions: "Create Report" not "Report Creation"
2. Use nouns for navigation: "Reports" not "View Reports"
3. Consistent plurality: always plural for collections, singular for items
4. {Project-specific rules}
```

### Step 4: Define Navigation Model

The visible structures users use to move through the product:

| Navigation Type | Content | Behavior |
|-----------------|---------|----------|
| **Global** | Primary sections (always visible) | Persistent across all pages |
| **Local** | Sub-sections within current area | Changes per section |
| **Contextual** | Related content/actions | Inline, context-sensitive |
| **Utility** | Account, settings, help, logout | Secondary, often top-right or footer |
| **Breadcrumb** | Location indicator | Shows hierarchy path |
| **Search** | Query-based finding | Scope-aware (global or section) |

For each type, specify:
- Visible items (what shows)
- Overflow behavior (what happens with too many items)
- Active state (how user knows where they are)
- Mobile adaptation (how it transforms on small screens)

### Step 5: Define Search Strategy

If the product warrants search (most do):

| Aspect | Decision |
|--------|----------|
| Scope | Global / Section / Both |
| Auto-suggest | Yes / No |
| Filters | {list available filters} |
| Empty state | {what shows for no results} |
| Relevance model | {how results are ranked} |

### Step 6: Validate Against Personas

For each primary persona, trace their top goal through the IA:
```markdown
## IA Validation

| Persona | Goal | Path Through IA | Steps | Issues |
|---------|------|-----------------|-------|--------|
| {name} | {goal} | {Nav > Section > Page} | {count} | {any friction?} |
```

If a persona's key goal requires more than 3 clicks/taps from entry → flag as a friction point and propose a shortcut (quick action, dashboard widget, contextual link).

### Step 7: Present for Approval

Present:
- Complete site map
- Navigation model (types + behavior)
- Labeling system with glossary
- Persona validation results
- Any friction points identified

---

## Gate

**Approval required before proceeding to Stage 6.**

User must confirm:
- Site map structure is complete and logical
- Navigation model is appropriate for the product
- Labels are clear and consistent
- Persona validation passes (all key goals reachable efficiently)
- Search strategy is defined (if applicable)

---

## Log

Update `uxd-state.md`:
- Completed Stages: add Stage 5 with date and artifact (`04_Information_Architecture.md`)
- Current Stage: 6

---

## Transition

After gate approval:
```
Stage 5 complete. Information architecture defined and validated.

Moving to Stage 6: User Flow Design. I'll now design the step-by-step
interaction flows for each key task — showing how users move through
the IA to accomplish their goals.
```

Load `define/user-flow-design.md`.
