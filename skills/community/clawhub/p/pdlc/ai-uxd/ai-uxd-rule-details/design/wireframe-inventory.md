<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 7: Wireframe & Screen Inventory

## Purpose

Define the complete screen inventory (every unique screen/state from the flows) and produce low-fidelity wireframe specifications. This stage translates abstract flows into concrete layout decisions.

---

## Depth Adaptation

| Depth | Wireframe Output |
|-------|-----------------|
| **Minimal** | Screen inventory + layout zones for key screens (no individual wireframes) |
| **Standard** | Screen inventory + wireframe specs for all unique screens |
| **Comprehensive** | Full wireframes + responsive annotations + interaction notes + external prototype links |

---

## Steps

### Step 1: Build Screen Inventory

Consolidate all screens from Stage 6 flow-to-screen mapping:

```markdown
## Screen Inventory

| # | Screen Name | Primary Flow | Template Type | States |
|---|-------------|-------------|---------------|--------|
| 1 | {name} | {owning flow} | {dashboard/list/detail/form/wizard/modal} | {default, empty, loading, error} |
| 2 | ... | ... | ... | ... |
```

**Deduplication:** If multiple flows touch the same screen, list it once with all owning flows referenced.

**State variants:** Each screen may have multiple states (loaded, empty, loading, error). Each state that looks visually different = a wireframe variant.

### Step 2: Define Template Types

Group screens by layout pattern:

| Template | Layout Structure | Typical Screens |
|----------|-----------------|-----------------|
| **Dashboard** | Header + nav + cards/widgets grid | Home, Overview, Analytics |
| **List** | Header + filter/sort bar + item rows | Inbox, Search results, Registers |
| **Detail** | Header + content body + sidebar/actions | Profile, Item view, Article |
| **Form** | Header + field groups + actions | Create/Edit, Settings, Onboarding steps |
| **Wizard** | Progress indicator + step content + nav | Multi-step creation, Setup |
| **Modal/Dialog** | Overlay + content + actions | Confirmation, Quick edit, Alert |
| **Empty** | Illustration/icon + message + CTA | First-time, No results, Error |

### Step 3: Produce Wireframe Specifications

For each screen (or template type at Minimal depth):

```markdown
# Wireframe: {Screen Name}

## Metadata
| Field | Value |
|-------|-------|
| Template | {type} |
| Primary flow | {flow name} |
| Persona | {who sees this most} |
| Entry points | {how user arrives here} |
| Exit points | {where user goes from here} |

## Layout Zones
```
┌─────────────────────────────────────┐
│ HEADER (logo, global nav, utilities)│
├───────────┬─────────────────────────┤
│ SIDEBAR   │ MAIN CONTENT            │
│ (local    │                         │
│  nav)     │  ┌─────────────────┐   │
│           │  │ Primary Content │   │
│           │  └─────────────────┘   │
│           │  ┌─────────────────┐   │
│           │  │ Secondary       │   │
│           │  └─────────────────┘   │
├───────────┴─────────────────────────┤
│ FOOTER (links, legal, status)       │
└─────────────────────────────────────┘
```

## Content Priority (top = highest)
1. {Primary content — what the user came for}
2. {Primary action — what they need to do}
3. {Supporting context — helps them decide}
4. {Secondary content — nice to have}
5. {Tertiary / navigation to related}

## Interactive Elements
| Element | Component | Action | Notes |
|---------|-----------|--------|-------|
| {labeled element} | {component type} | {what happens on interaction} | {constraints} |

## States
| State | Visual Difference | Trigger |
|-------|-------------------|---------|
| Default (loaded) | Full content visible | Data available |
| Empty | {empty state design} | No data |
| Loading | {skeleton/spinner} | Data fetching |
| Error | {error message + recovery} | Load failure |

## Responsive Behavior
| Breakpoint | Layout Change |
|------------|--------------|
| Desktop (>1024px) | {as shown above} |
| Tablet (640-1024px) | {changes — sidebar collapse? columns reduce?} |
| Mobile (<640px) | {changes — stack? hide? drawer?} |
```

### Step 4: Reference External Prototypes (if available)

If the team has Figma/Sketch/XD prototypes:
- Link each wireframe to its prototype equivalent
- Note any discrepancies between wireframe spec and prototype
- The wireframe spec is GOVERNANCE; the prototype is IMPLEMENTATION

### Step 5: Organize by Atomic Design

Map the screen inventory to Atomic Design hierarchy:
- Screens = **Pages** (real content instances)
- Layout patterns = **Templates** (structural containers)
- Sections within layouts = **Organisms** (identified for Stage 9)

### Step 6: Present for Approval

Present:
- Complete screen inventory (count + template distribution)
- Key wireframes (at least the primary screens for each template type)
- Responsive strategy overview
- Any screens that surprised the team (weren't expected from flows)

---

## Gate

**Approval required before proceeding to Stage 8.**

User must confirm:
- Screen inventory is complete (no missing screens from flows)
- Layout decisions are sound
- Content priority is correct per screen
- Responsive strategy is viable
- Empty/error/loading states are defined

---

## Log

Update `uxd-state.md`:
- Completed Stages: add Stage 7 with date and artifacts (`06_Wireframe_Specifications/Screen_Inventory.md`, etc.)
- Current Stage: 8

---

## Transition

After gate approval:
```
Stage 7 complete. {N} screens inventoried, wireframe specifications produced.

Moving to Stage 8: Design System Foundation. I'll now define the visual
and verbal system — colors, typography, spatial grid, icons, and voice
& tone — that makes every screen consistent and maintainable.
```

Load `design/design-system-foundation.md`.
