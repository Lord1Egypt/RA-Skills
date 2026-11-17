<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 9: Component Library Definition

## Purpose

Define every UI component — its classification, variants, states, interactions, responsive behavior, accessibility requirements, and token usage. This is the implementation-ready specification that AI-DWG and developers consume.

---

## Depth Adaptation

| Depth | Component Output |
|-------|-----------------|
| **Minimal** | 10-15 core components (atoms + key molecules); states defined but not every variant |
| **Standard** | Full library (20-40 components); all variants, states, interactions, accessibility |
| **Comprehensive** | Full library + pattern compositions + interaction specifications + usage guidelines per component |

---

## Steps

### Step 1: Identify Components from Wireframes

Extract all unique UI elements from the screen inventory (Stage 7):

| Component | Level | Category | Screens Where Used |
|-----------|-------|----------|-------------------|
| Button | Atom | Action | All |
| Input Field | Atom | Input | Forms, Search |
| Card | Molecule | Display | Dashboard, List |
| Data Table | Organism | Display | Reports, Admin |
| Header | Organism | Navigation | All |
| Modal | Organism | Feedback | Confirmation, Edit |
| ... | ... | ... | ... |

### Step 2: Classify by Atomic Design

Organize into the hierarchy:

**Atoms** (indivisible elements):
- Button, Input, Label, Icon, Badge, Avatar, Checkbox, Radio, Toggle, Tooltip, Divider, Skeleton

**Molecules** (functional groups of atoms):
- Form Field (label + input + helper + error), Search Bar (input + button), Menu Item (icon + label + shortcut), Breadcrumb Item, Tab

**Organisms** (complex sections):
- Header, Footer, Navigation Drawer, Data Table, Card, Modal/Dialog, Toast/Notification, Form Section, Sidebar

### Step 3: Define Each Component

For EACH component, produce a specification following this structure:

```markdown
# Component: {Name}

## Classification
| Property | Value |
|----------|-------|
| Level | Atom / Molecule / Organism |
| Category | Navigation / Input / Display / Feedback / Layout / Action |
| Usage frequency | High / Medium / Low |

## Variants
| Variant | Use Case | Visual Distinction |
|---------|----------|-------------------|
| Primary | Main/prominent action | Solid fill, brand color |
| Secondary | Supporting action | Outlined, muted |
| Ghost/Tertiary | In-context, minimal | Text-only, no border |
| Destructive | Irreversible action | Red/danger color |

## Sizes
| Size | Token | Use Case |
|------|-------|----------|
| Small | `component.{name}.size.sm` | Dense UI, tables |
| Medium | `component.{name}.size.md` | Default |
| Large | `component.{name}.size.lg` | Touch-primary, CTAs |

## States (MANDATORY — all interactive components)
| State | Visual Change | Trigger | Token |
|-------|--------------|---------|-------|
| Default | Baseline appearance | Page load | `{component}.bg.default` |
| Hover | {change} | Mouse enter | `{component}.bg.hover` |
| Focus | {change} + focus ring | Tab / click | `{component}.border.focus` |
| Active | {change} | Mouse down / Enter | `{component}.bg.active` |
| Disabled | Reduced opacity, no pointer | Programmatic | `{component}.bg.disabled` |
| Loading | Spinner / skeleton | Async in progress | — |
| Error | Error color + message | Validation fail | `color.feedback.error` |
| Empty | Placeholder content | No data | — |
| Skeleton | Animated placeholder | Initial load | `color.skeleton` |

## Interactions
| Trigger | Behavior | Animation |
|---------|----------|-----------|
| Click/Tap | {action} | {transition description} |
| Hover | {state change} | {duration + easing} |
| Focus | {focus ring appears} | Immediate |
| Keyboard | {key → action mapping} | — |
| Long press | {if applicable} | — |

## Responsive Behavior
| Breakpoint | Adaptation |
|------------|-----------|
| Mobile (<640px) | {how component changes} |
| Tablet (640-1024px) | {changes if any} |
| Desktop (>1024px) | {default appearance} |

## Accessibility (MANDATORY)
| Property | Value |
|----------|-------|
| Role | `{ARIA role}` |
| Keyboard | `{key interactions: Tab, Enter, Space, Escape, Arrow keys}` |
| Screen reader | `{announcement pattern}` |
| Focus indicator | `{description — must meet 3:1 contrast}` |
| Touch target | `{minimum 44x44px}` |

## Content Constraints
| Property | Value |
|----------|-------|
| Character limit | {min-max or "no limit"} |
| Overflow behavior | Truncate with ellipsis / Wrap / Scroll |
| Required content | {what must always be present} |
| Optional content | {what can be omitted} |

## Token Usage
| Property | Token |
|----------|-------|
| Background | `{component}.bg.{state}` |
| Text | `{component}.text.{state}` |
| Border | `{component}.border.{state}` |
| Radius | `radius.{value}` |
| Padding | `spacing.{value}` |
| Shadow | `shadow.{value}` |

## Usage Guidelines
- **DO:** {correct usage pattern}
- **DO:** {another correct usage}
- **DON'T:** {common misuse}
- **DON'T:** {another misuse}
```

### Step 4: Define Interaction Patterns (Cross-Component)

Beyond individual components, define shared patterns:

| Pattern | Components Involved | Behavior |
|---------|--------------------|---------| 
| **Disclosure** | Button + Panel | Progressive reveal (expand/collapse) |
| **Selection** | List + Checkbox/Radio | Single or multi-select with feedback |
| **Drag & Drop** | Card/Item + Drop Zone | Reorder or categorize |
| **Infinite Scroll** | List + Loading | Load more on scroll threshold |
| **Optimistic Update** | Any mutable | Show success immediately, revert on failure |
| **Skeleton Loading** | Any data-dependent | Show structure before content |

### Step 5: Map Components to Flows

Cross-reference: which components appear in which flows?

| Flow | Key Components Used |
|------|-------------------|
| {flow name} | Button (Primary), Form Field, Modal, Toast |
| {flow name} | Data Table, Filter Bar, Pagination, Empty State |

This validates completeness: every flow step maps to defined components.

### Step 6: Present for Approval

Present:
- Complete component inventory (count per level)
- Sample full specifications (2-3 key components in detail)
- Interaction patterns list
- Component-to-flow mapping summary
- Any components that seem redundant or could be consolidated

---

## Gate

**Approval required before proceeding to Stage 10 (or Stage 11 if Stage 10 is skipped).**

User must confirm:
- Component inventory is complete
- All states are defined for interactive components
- Accessibility requirements are specified
- Responsive behavior is clear
- Token usage is consistent with the design system (Stage 8)

---

## Log

Update `uxd-state.md`:
- Completed Stages: add Stage 9 with date and artifacts (`08_Component_Library/Component_Inventory.md`, etc.)
- Current Stage: 10 (or 11 if Multi-Brand not triggered)

---

## Transition

**If Multi-Brand Theming is active:**
```
Stage 9 complete. {N} components defined across {levels}.

Moving to Stage 10: Multi-Brand Theming. I'll now define how the
design system supports multiple brands or color modes (dark/light).
```
Load `design/multi-brand-theming.md`.

**If Multi-Brand Theming is NOT active:**
```
Stage 9 complete. {N} components defined across {levels}.
Stage 10 (Multi-Brand Theming) skipped — single brand, no color modes.

Moving to Stage 11: Accessibility Baseline. I'll now consolidate
all accessibility requirements into a governed baseline.
```
Load `validate/accessibility-baseline.md`.
