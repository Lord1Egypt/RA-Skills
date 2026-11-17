<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-UXD
generatedVersion: "{version}"
source: "{upstream-doc-path}"
generatedOn: "{ISO-date}"
ownership: hybrid
---

# Component Inventory

## Summary

| Level | Count | Categories |
|-------|:-----:|-----------|
| Atoms | {N} | Action, Input, Display, Feedback |
| Molecules | {N} | Composed functional units |
| Organisms | {N} | Complex sections |
| **Total** | **{N}** | |

---

## Atoms

| # | Component | Category | Variants | States | Key Token |
|---|-----------|----------|:--------:|:------:|-----------|
| 1 | Button | Action | Primary, Secondary, Ghost, Destructive | 9 | `button.*` |
| 2 | Input | Input | Text, Number, Password, Search | 9 | `input.*` |
| 3 | Label | Display | Default, Required, Error | 3 | `typography.body.sm` |
| 4 | Icon | Display | — (per icon system) | 3 | `sizing.icon.*` |
| 5 | Badge | Display | Status, Count, Dot | 4 | `badge.*` |
| 6 | Avatar | Display | Image, Initials, Fallback | 3 | `sizing.avatar.*` |
| 7 | Checkbox | Input | Unchecked, Checked, Indeterminate | 6 | `checkbox.*` |
| 8 | Radio | Input | Unselected, Selected | 6 | `radio.*` |
| 9 | Toggle | Input | Off, On | 6 | `toggle.*` |
| 10 | Tooltip | Feedback | Top, Bottom, Left, Right | 2 | `tooltip.*` |
| 11 | Divider | Layout | Horizontal, Vertical | 1 | `color.border.default` |
| 12 | Skeleton | Feedback | Text, Circle, Rectangle | 1 | `color.skeleton` |
| {N} | {component} | {category} | {variants} | {states} | {token} |

---

## Molecules

| # | Component | Composed Of | Category | Variants | States |
|---|-----------|-------------|----------|:--------:|:------:|
| 1 | Form Field | Label + Input + Helper + Error | Input | Text, Select, Textarea | 6 |
| 2 | Search Bar | Input + Button + (Suggestions) | Input | Compact, Full | 5 |
| 3 | Menu Item | Icon + Label + Shortcut + Arrow | Navigation | Default, Destructive | 5 |
| 4 | Breadcrumb | Links + Separator | Navigation | — | 2 |
| 5 | Tab | Icon + Label + Badge | Navigation | — | 5 |
| 6 | Pagination | Buttons + Page numbers + Info | Navigation | Full, Compact | 3 |
| {N} | {component} | {atoms} | {category} | {variants} | {states} |

---

## Organisms

| # | Component | Composed Of | Category | Variants | States |
|---|-----------|-------------|----------|:--------:|:------:|
| 1 | Header | Logo + Nav + Search + Avatar + Utils | Navigation | Desktop, Mobile | 3 |
| 2 | Footer | Links + Legal + Social | Navigation | Full, Minimal | 1 |
| 3 | Navigation Drawer | Menu Items + Sections + Collapse | Navigation | Expanded, Collapsed | 3 |
| 4 | Data Table | Header + Rows + Sorting + Pagination | Display | Default, Selectable, Expandable | 5 |
| 5 | Card | Media + Content + Actions | Display | Default, Compact, Featured | 4 |
| 6 | Modal / Dialog | Overlay + Header + Body + Actions | Feedback | Alert, Confirmation, Form | 4 |
| 7 | Toast / Notification | Icon + Message + Action + Dismiss | Feedback | Success, Error, Warning, Info | 3 |
| 8 | Form Section | Heading + Description + Fields + Actions | Input | Default, Collapsible | 3 |
| {N} | {component} | {composition} | {category} | {variants} | {states} |

---

## Interaction Patterns (Cross-Component)

| Pattern | Components Involved | Behavior |
|---------|--------------------|---------| 
| Progressive Disclosure | Button/Link + Panel | Expand/collapse to reveal detail |
| Selection | List + Checkbox/Radio | Single or multi-select with feedback |
| Drag & Drop | Card/Item + Drop Zone | Reorder or categorize |
| Infinite Scroll | List + Skeleton + Trigger | Load more at scroll threshold |
| Optimistic Update | Any mutable component | Show success immediately, revert on fail |
| Skeleton Loading | Any data-dependent | Show structure shape before content |
| Confirmation | Trigger + Modal | Verify before destructive action |
| Auto-save | Form inputs | Save on blur/debounce, show status |

---

## Component-to-Flow Mapping

| Flow | Key Components Used |
|------|-------------------|
| {Flow 1} | {Button (Primary), Form Field, Modal, Toast} |
| {Flow 2} | {Data Table, Search Bar, Pagination, Empty State} |
| {Flow 3} | {Card, Navigation Drawer, Header, Breadcrumb} |

---

## Detailed Specifications

Each component has a full specification document at:
`08_Component_Library/Component_{Name}.md`

Full spec structure per component (see `design-standards.md`):
- Classification (level, category)
- Variants (with use cases)
- Sizes (with tokens)
- States (ALL — mandatory)
- Interactions (triggers + behaviors)
- Responsive behavior
- Accessibility (role, keyboard, screen reader, focus, touch target)
- Content constraints
- Token usage map
- Usage guidelines (DO / DON'T)
