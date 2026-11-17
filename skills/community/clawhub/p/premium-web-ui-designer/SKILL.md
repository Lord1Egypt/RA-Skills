---
name: premium-web-ui-designer
description: Upgrade websites, web apps, dashboards, SaaS products, landing pages, portfolios, and interactive tools into polished, premium, modern interfaces. Use when the user asks for better frontend visual design, high-end UI, fashionable styling, layout refinement, component polish, responsive design, or design critique for HTML/CSS/React/Vue/Tailwind projects.
---

# Premium Web UI Designer

## Goal

Make frontend work feel designed, not merely assembled. Produce interfaces with clear hierarchy, confident spacing, restrained color, refined typography, strong interaction states, and responsive layouts that look production-ready.

## Design Workflow

1. Identify the product type before styling:
   - SaaS/dashboard: dense, calm, scannable, operational.
   - Portfolio/brand/product: editorial, image-led, distinctive.
   - Tool/editor: ergonomic controls, clear affordances, stable layout.
   - Landing page: strong first-viewport signal, credible narrative, clear action.
2. Choose one visual direction from `references/web-style-directions.md`. Do not blend many trends at once.
3. Define a small design system before editing:
   - typography scale
   - spacing rhythm
   - surface and border rules
   - color roles
   - icon/button/input states
4. Redesign structure before decoration. Fix hierarchy, alignment, density, and content grouping first.
5. Apply polish through purposeful details:
   - consistent 4/8 px spacing rhythm
   - meaningful contrast between primary, secondary, and muted content
   - restrained shadows and borders
   - professional hover, focus, selected, disabled, empty, loading, and error states
   - stable component dimensions so labels and dynamic content do not shift layout
6. Validate visually in desktop and mobile widths. Use screenshots when possible.

## Frontend Rules

- Prefer real product or content imagery over abstract decorative shapes when the subject matters.
- Do not make generic gradient-orb backgrounds, unless the user explicitly asks for that style.
- Do not overuse glassmorphism, purple-blue gradients, beige palettes, or oversized cards.
- Do not put cards inside cards.
- Use icons for compact controls when a common icon exists.
- Keep border radius controlled: usually 6-10 px for product UI, larger only for brand/editorial designs.
- Keep text readable and contained. Never let button labels, cards, or headings overflow.
- Make responsive behavior explicit with grids, flex rules, min/max widths, aspect ratios, and stable toolbars.
- For dashboards, avoid marketing hero layouts. Prioritize comparison, scanning, filters, tables, charts, and repeated workflows.

## Implementation Checklist

When editing code:

1. Inspect existing frameworks and styling conventions first.
2. Reuse current components and tokens when they exist.
3. Add only the CSS, assets, and dependencies needed for the redesign.
4. Keep semantic HTML and accessible labels intact.
5. Test with at least one desktop and one mobile viewport.
6. Capture screenshots and revise visible defects before final delivery.

## Output Standard

In the final response, summarize:

- visual direction used
- major layout and component changes
- responsive checks performed
- remaining limitations, if any

If the work is a design review instead of code editing, lead with the most important visual problems and give concrete fixes.
