---
name: product-ux-workflow
version: "0.2.0"
license: Apache-2.0
description: "End-to-end product UX lifecycle methodology — four-stage workflow from requirements research and user scenario modeling to information architecture, low-fidelity wireframing, and developer handoff. Focuses on macro product UX: user journey maps, content hierarchy, IA, and design system alignment. Use when: planning product UX from 0 to 1, drafting user journey flows, defining PRD user scenarios, structuring information architecture, or creating low-fidelity wireframe prototypes. Keywords: 产品设计, UX流程, 用户旅程, 需求分析, 流程图, 低保真线框图, 原型规划, 体验设计, user journey, wireframe, user flow, information architecture, product UX, PRD."
metadata:
  openclaw:
    emoji: 📋
---

# Product UX Workflow — Four-Stage Product Lifecycle Process

A complete UI/UX product lifecycle methodology covering web and app from zero to one. Design philosophy: usability > beauty. Every pixel has a reason. Every click should be effortless.

> [!NOTE]
> **System Collaboration Guidelines**:
> - **Micro Interaction Resilience**: For pre-coding defensive state checklists (empty, error, loading, skeletons, destructive action confirmation), pair with `interaction-design-sop`.
> - **Component Implementation**: For headless component specs (HIG/Fluent/Material), refer to `custom-ui-spec`; for pre-built libraries (Ant Design, Element Plus, Arco, etc.), refer to `ui-framework-spec`.



---

## Stage 1: Requirements Research & Understanding

Before opening any design tool, establish a solid foundation of WHAT and WHY.

### Define Product Goals
- What user problem does this interface/feature solve?
- What is the business metric being measured?
- Success criteria: how do we know when it's working?

### User Scenario Analysis
- Who is the user? (Role, tech literacy, context of use)
- When and where do they use this? (Mobile vs desktop, casual vs urgent)
- Core task flow: what is the single most important action?

### Competitive Research
- Analyze 3 similar products' interaction patterns
- Note what works (borrow) and what doesn't (avoid)
- Identify UX gaps in the market

### Constraints Checklist
- **Technical**: Framework limitations, API availability, performance budget
- **Brand**: Design system compliance, tone of voice
- **Platform**: iOS HIG, Android Material Design, Web standards
- **Timeline**: MVP scope vs. future iterations

---

## Stage 2: Information Architecture & UX Design

Structure content and design the interaction logic before any visual styling.

### User Flow Diagrams
Map the complete journey:
- **Happy path**: The optimal flow with zero errors
- **Branch paths**: Alternative decisions the user might make
- **Edge cases**: What happens when things go wrong?

Design each path step-by-step. Every screen must answer: "What does the user do here, and where do they go next?"

### Content Hierarchy
- **Information Architecture Diagram**: Page/section relationships, navigation structure
- **Priority ordering**: What's most important on each screen goes first (top-left bias)
- **Labeling**: Clear, concise, user-centric terminology
- **AI-Native & Editorial UX (Anthropic / OpenAI / ArtCraft Paradigms)**: Read `references/editorial-ux-patterns.md` to choose between **Anthropic Editorial Broadsheet UX** (Cream & Ink band pacing, asymmetric sticky wayfinding splits, `60ch–70ch` reading measure, archive index rows), **OpenAI Conversational & Gallery UX** (Prompt-first hero entry with starter pills, persistent left navigation rail, borderless Pearl Gray bento surfaces, and atmospheric horizon media carousels), and **ArtCraft Studio Blueprint UX** (3-tier sunken `16:9` viewport proof cells with corner `.tick` crosshairs, exposed `1px` zero-radius CAD grid, binary `.invert-block` hover states, and multi-app color wayfinding).

### Wireframes (Low-Fidelity)
Focus on layout and information priority. No colors, no typography, no real content.
- Block out major content areas
- Define element grouping and spacing
- Establish visual hierarchy through size and position only

### Interaction Specifications — Every State
For every component/system state:
| State | Description |
|-------|-------------|
| **Normal** | Default appearance when data is loaded and ready |
| **Loading** | Content is being fetched — skeleton, spinner, shimmer |
| **Empty** | No data available — helpful message + CTA to populate |
| **Error** | Something went wrong — clear error message + recovery action |
| **Edge** | Boundary conditions — long text, many items, rapid clicks |

---

## Stage 3: Visual Design (UI)

Apply visual treatment to the approved wireframes.

### Design System Alignment
- **If a Design System exists**: Use existing components and tokens strictly. Do not invent new patterns without justification.
- **For headless components (shadcn/ui, Radix)**: Follow `custom-ui-spec` (aligning with Apple HIG, Microsoft Fluent, Google Material, Anthropic Editorial, OpenAI Modernist, or ArtCraft Blueprint).
- **For pre-built component libraries (Ant Design, Element Plus, Arco, TDesign, Semi)**: Follow `ui-framework-spec`.
- **If building from scratch**: Start with tokens (foundation), then components, then patterns (see Design System Building below).


### Page Layout
- **Grid system**: 4px or 8px base unit, consistent column math
- **Spacing scale**: Use a defined ratio (e.g., 4, 8, 12, 16, 24, 32, 48, 64)
- **Content zoning**: Primary content, secondary content, tertiary actions — clear visual weight distribution

### Component Design
For each core component:
- Button (primary, secondary, tertiary, ghost, danger, icon-only)
- Form elements (input, select, checkbox, radio, switch, date picker)
- Cards (content card, action card, image card)
- Modal / Dialog (confirmation, form, full-screen)
- Navigation (tab bar, sidebar, breadcrumb, pagination)
- Feedback (toast, alert, progress bar, skeleton, badge)

### Visual Detail
- Icon style (outline/filled/duotone, stroke weight, corner radius)
- Corner radius hierarchy (default = 8px, card = 12px, modal = 16px)
- Shadow/elevation levels (card = subtle, modal = prominent, toast = floating)
- Color usage (primary for actions, semantic for status, neutral for content)

### Responsive Adaptation
| Breakpoint | Layout | Behavior |
|------------|--------|----------|
| Desktop (≥1024px) | Multi-column, full navigation | Full feature set |
| Tablet (768-1023px) | 2-column condensed | Collapsed sidebar, simplified cards |
| Mobile (<768px) | Single column, bottom nav | Full-width, stacked, touch-optimized |

---

## Stage 4: Prototype & Delivery

Convert designs into developer-ready deliverables.

### High-Fidelity Prototype
- Interactive with real transitions and micro-interactions
- Connected flow: tap through the complete happy path + key edge cases
- Annotated with interaction notes

### Specification Annotations
For every element, specify:
- Dimensions: width, height, padding, margin
- Typography: font-family, size, weight, line-height, letter-spacing
- Color: hex/rgba values for fill, stroke, text, background
- Spacing: exact pixel values between elements
- States: hover, active, disabled, focus, error

### Design Decision Document
Record the rationale behind each significant choice:
- Why this layout? (Content hierarchy reasoning)
- Why this component? (Pattern matching or novel solution)
- Why this color? (Emotional strategy or accessibility)
- Alternatives considered and why they were rejected

### Developer Handoff Package
```
handoff/
├── designs/           # Figma file / screenshots with annotations
├── assets/            # Exported icons, images, illustrations
├── specs/             # Dimension and behavior specs
├── tokens.css         # Design token CSS variables
└── prototypes/        # Interactive prototype link
```

---

## Design System Building (From Scratch)

Build in layers, bottom-up.

### Layer 1: Design Tokens
| Token Category | Items |
|---------------|-------|
| **Color** | Primary, secondary, accent, neutral, semantic (success/warning/error/info) + dark mode equivalents |
| **Typography** | Font family (primary, mono), weight scale, type scale (h1-h6, body, caption), line-height scale |
| **Spacing** | 4px base grid → 4/8/12/16/24/32/48/64/96 spacing scale |
| **Shadows** | Elevation levels (0=flat, 1=card, 2=dropdown, 3=modal, 4=toast) |
| **Radius** | None(0), sm(4), md(8), lg(12), xl(16), full(9999) |
| **Breakpoints** | Mobile(375), tablet(768), desktop(1024), wide(1440) |

### Layer 2: Components
- **Basic**: Button, Input, Select, Checkbox, Radio, Switch, Badge, Avatar
- **Complex**: Form, Table, Card, Modal, Dropdown, Tabs, Accordion, Drawer, DatePicker
- **Feedback**: Toast, Alert, Progress, Skeleton, EmptyState, ErrorBoundary

### Layer 3: Patterns
- **Navigation**: List → Detail, Tab-based, Dashboard with drill-down
- **Form**: Inline edit, Wizard (multi-step), Full-page form, Modal form
- **Search & Filter**: Search bar + facets, Filter drawer, Sort dropdown
- **Error & Recovery**: Offline banner, Retry pattern, Graceful degradation

---

## Output Standard

Every deliverable must contain:

```markdown
## [Component/Screen Name]

### Design Asset
- [Figma / Screenshot / Wireframe]

### Interaction Specs
- Normal: [description]
- Hover/Focus: [description]
- Loading: [description]
- Empty: [description]
- Error: [description]

### Design Decision
- Why this layout/component/color: [reason]
- Design system compliance: [yes/no, if no explain why]
- Alternatives considered: [list with rejection reasons]

### Dev Annotations
- Key dimensions: [width/height/spacing]
- Responsive behavior: [breakpoint rules]
- Animation: [duration/easing]
```

## ⚠️ Hard Rules (STRICT — Violations cause production issues)

1. **MUST complete wireframes (Stage 2) before any visual design (Stage 3)**. Visual design without verified information architecture always results in rework.
2. **MUST define all interaction states** (loading, empty, error, hover, focus, disabled, active) for every component. Missing states are the #1 source of development handoff issues.
3. **MUST NOT use "approximately" or "close enough" in any annotation**. All dimensions, spacing, and alignment must be specified at the pixel level.
4. **MUST trace at least one complete user flow from entry to completion** before considering any stage done. Partial flows hide edge cases.
5. **MUST reference existing design system components before creating new ones**. Every new component must include a justification for why existing ones don't suffice.
6. **MUST NOT use subjective taste as a design justification**. Every decision must reference: user research data, usability heuristics (Nielsen's 10), platform conventions, or technical constraints.
7. **MUST deliver annotations that a frontend developer can implement without follow-up questions**. If a developer would need to ask "what about this state?", the deliverable is incomplete.
8. **MUST NOT start responsive adaptation before the primary breakpoint design is approved**. Premature responsive work multiplies changes across all breakpoints simultaneously.

## Critical Anti-Patterns

1. **Function before form**: Wireframe must be approved before visual design begins. Never skip this gate.
2. **Never forget empty states**: No data is the most common first-time experience. Design it.
3. **Reuse before create**: Use existing components unless there is a clear justification for a new one.
4. **Precise annotations only**: No "approximately" or "close enough". Px-level precision.
5. **Design for handoff**: Deliverables must be implementable by a frontend developer without follow-up questions.
6. **Complete interaction loops**: Every action → every state → every error. Trace one complete path before starting another.
