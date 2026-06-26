---
name: presentation-by-html
description: Use when the user needs to create a technical sharing, presentation, or talk material. Triggered by requests like "prepare a sharing", "make slides", "build a presentation", or any scenario requiring structured visual storytelling for an audience.
---

# Presentation Builder

## Overview

Build presentation materials as HTML through a two-phase process: **brainstorm first, build second**. Never produce slides before the narrative structure is solid.

## Phase 1: Brainstorm

Conduct a structured dialogue before writing any code.

### Required Questions

**Audience & Format:**

- Who is the audience? Technical depth? Prior knowledge?
- Duration? Format constraints?

**Content Core:**

- What problem does this solve? What was the status quo before?
- What is the core capability / contribution?
- Current status (shipped / MVP / in-progress)?
- Demos, data, or real cases available?

**Narrative Intent:**

- What should the audience take away?
- Pitfalls, "aha moments", counter-intuitive insights?

### Structuring Principles

- **Effect before mechanism**: Show what it does before explaining how
- **Pitfalls are gold**: Real failures resonate more than polished success. Structure each as: phenomenon -> cause -> solution -> generalizable insight
- **Avoid cliché openings**: Prefer tension, paradox, or direct demo over "imagine it's 3am..."
- **Time-box sections**: Allocate minutes explicitly. Core insights deserve >40% of time
- **One takeaway per slide**: Two ideas = two slides

### Iterate Until Stable

Continue dialogue until:

- Framework covers all sections with time estimates
- Narrative arc is clear (hook -> problem -> solution -> lessons -> future)
- User confirms "framework OK"

## Phase 2: Build HTML

### File Structure

Separate concerns into three files for maintainability:

```
project/
  presentation.html    # Semantic structure only, no inline styles except layout-specific
  css/style.css        # All visual styling, animations, component patterns
  js/deck.js           # Navigation, interactions, TOC, expandable logic
  images/              # Screenshots, avatars, demo videos
```

### Interaction Patterns (Critical)

The presentation is NOT a static slide deck. It uses **interactive detail-on-demand** patterns:

**1. Tab Cards** — Clickable cards that switch a shared detail area below

```html
<div class="grid-3">
  <div class="card tab-card active" data-tab="topic-a">Summary A</div>
  <div class="card tab-card" data-tab="topic-b">Summary B</div>
</div>
<div class="tab-detail-area">
  <div class="tab-detail active" data-tab="topic-a">...full detail...</div>
  <div class="tab-detail" data-tab="topic-b">...full detail...</div>
</div>
```

Use when: Multiple sub-topics exist under one slide, each with rich detail.

**2. Expandable Details** — Cards that expand to reveal deeper content

```html
<div class="card expandable" data-expand-target="detail-id">Summary</div>
<div class="expand-content-full" id="detail-id">
  <div class="expand-inner">...detailed content...</div>
</div>
```

Use when: A slide has layered information — show summary by default, expand for evidence/examples. Supports `data-default-open` attribute.

**3. Left-Tab + Right-Detail Panel** — Vertical tab list with adjacent detail pane

Use when: Each tab has substantial content (code blocks, diagrams) that benefits from full-width display. Example: security isolation details.

### Visual Design System

| Component | CSS Class | Usage |
| --- | --- | --- |
| Cards | `.card .card-accent .card-{color}` | Discrete points, categorized items |
| Tags | `.tag .tag-{color}` | Labels, keywords, status badges |
| Grids | `.grid-2` `.grid-3` | Parallel comparisons |
| Quote | `.quote` | Key insights, memorable one-liners |
| Architecture boxes | `.arch-box .arch-box.primary` | System diagrams |
| Code blocks | `<pre>` with `.comment .keyword .string .func .op` spans | Syntax-highlighted dark code |
| Comparison | `.compare-box .compare-before .compare-after` | Before/after with positioned labels |
| Timeline | `.timeline .timeline-item` | Sequential events with time markers |
| Pitfall insight | `.pitfall-step .pitfall-insight` | Highlighted takeaway badges |
| Big numbers | `.big-number` | Metrics with placeholder `__` for pending data |

### Color System (Semantic)

```css
--primary: #1a73e8;       /* neutral/default/architecture */
--accent: #ea4335;        /* problem/danger/before */
--accent-green: #34a853;  /* solution/success/after */
--accent-yellow: #fbbc04; /* caution/intermediate */
--accent-purple: #9334e6; /* advanced/depth/evaluator */
```

### Animation Patterns

- **Fade-in with stagger**: `.fade-in .fade-in-d1` through `.fade-in-d6` for progressive reveal
- **Step-by-step flow**: `.anim-step` + `.anim-flow` container, revealed sequentially by JS
- **Flow diagram**: `.flow-node` + `.flow-connector` revealed node-by-node with delays
- **Tab transitions**: CSS `@keyframes tabFadeIn` for smooth panel switching

### Slide Types

1. **Title slide** (`.slide-title`): Gradient background, white text
2. **Section divider** (`.slide-section`): Large faded number + heading
3. **Content slide**: h2/h3 + interactive components
4. **Architecture slide**: CSS flex/grid layouts with `.arch-box` nodes
5. **Comparison slide**: `.compare-before` / `.compare-after` side-by-side
6. **Data slide**: `.big-number` with `__` placeholders for pending metrics
7. **Q&A slide**: Minimal title-slide style

### JS Engine Responsibilities

```
deck.js handles:
- Slide navigation (keyboard ←→/Space/PgUp/PgDn, touch swipe, ESC for TOC)
- Progress bar + counter update
- Tab card switching (click → toggle active class on cards and detail panels)
- Expandable toggle (click → open/close with accordion behavior)
- Security panel switching
- Animated flow triggering (reset + staggered reveal on slide enter)
- Default-open restoration on slide enter
- Expand state cleanup on slide leave
```

### Content Density Rules

- Body text: 16-22px; never smaller than 13px even in expand-inner
- Cards: max 3-4 per slide in top-level grid
- Detail areas can be denser (tables, code, smaller font) since they're opt-in
- One core idea per slide at the summary level; detail areas can go deeper
- Use `data-title` on section/key slides for TOC generation
- Lazy-load heavy media (video onclick pattern)

### Things to Avoid

- External CDN links (must work offline/intranet)
- Single-file HTML over 500 lines (split CSS/JS)
- Static walls of text (use expandable/tab patterns for density)
- Inline styles for reusable patterns (extract to CSS classes)
- Images for diagrams (use CSS flex/grid compositions)
