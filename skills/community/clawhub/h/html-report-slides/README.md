# html-report-slides

A single-file HTML report generator with a dark tech-style aesthetic. Perfect for strategy presentations, architecture overviews, cost analyses, and roadmap slides.

## Features (v2.0)

- **CSS Variables System** — All colors, spacing, and typography centralized in `:root`
- **Dark + Light Theme** — Toggle with `body.light` class for projector-friendly mode
- **Navigation** — Right-side dot nav + top progress bar + keyboard arrows/space
- **Entrance Animations** — IntersectionObserver-driven fadeInUp with staggered delays
- **Responsive** — Adapts from 1280px slides down to tablet/laptop viewports
- **Print/PDF Ready** — Complete print stylesheet + one-click export button
- **10 Component Snippets** — Copy-paste HTML fragments for common slide patterns

## Quick Start

1. Copy `components/base-template.html` as your new report file
2. Replace all `__PLACEHOLDER__` values with your content
3. Pick components from `components/` directory and paste them into your slides
4. Open in browser — done!

## Directory Structure

```
html-report-slides/
├── SKILL.md                    # AI skill definition (triggers, workflow)
├── components/
│   ├── base-template.html      # Full starter template (CSS vars + nav + animation)
│   ├── cover-slide.html        # Title/cover page
│   ├── svg-architecture.html   # Multi-layer architecture diagram
│   ├── storylines.html         # Strategy paths / storylines
│   ├── decision-cards.html     # A/B decision comparison
│   ├── next-steps.html         # Timeline / action items
│   ├── cost-cards.html         # KPI metric cards
│   ├── metric-table.html       # Data comparison table
│   ├── budget-timeline.html    # Budget progress bars
│   ├── future-cards.html       # Now vs Next planning
│   ├── placeholder-slide.html  # Placeholder for TBD content
│   └── README.md               # Component index
├── references/
│   ├── design-system.md        # Color, typography, spacing specs
│   └── svg-architecture-rules.md  # SVG layout principles
└── examples/
    ├── report.html             # Strategy overview example
    └── cost-report.html        # Cost analysis example
```

## Design System Highlights

| Element | Value |
|---|---|
| Background | `#0a0e1a` (dark) / `#f5f7fa` (light) |
| Title Gradient | `#ffffff → #7cacff → #a78bfa` |
| Slide Size | 1280×720px (responsive) |
| Font | Inter + PingFang SC fallback |
| Accent Colors | Blue `#5070ff` · Purple `#7c3aed` · Green `#10b981` · Orange `#f59e0b` |

## Trigger Phrases (for AI assistants)

- "Make a report page / presentation"
- "Create an HTML slide deck"
- "Tech-style dark presentation"
- "Architecture overview slide"
- "Cost analysis report"

## Installation

### As a WorkBuddy/Claw Skill
```bash
clawhub install html-report-slides
```

### Manual
Clone this repo and copy `components/base-template.html` to start.

## License

MIT-0 (No attribution required)
