---
name: gmira
description: Use when building, redesigning, or reviewing a website or web surface that must not look generated. Covers landing pages, e-commerce (PLP, PDP, cart, checkout), car and vehicle inventory sites, course and cohort school pages, portfolios, dashboards, and marketing sites. Handles visual direction, WebGL and canvas effects, shadcn registry components, scroll choreography, typography, color, motion, empty and error states, accessibility, performance budgets, and multi-viewport visual verification. Also use when a page came out bland, templated, or "AI-looking" and needs a real direction, or when an installed registry component renders wrong.
---

# Gmira

A library for building web surfaces nobody can tell were generated.

The problem this solves is not skill, it is **decision avoidance**. An agent that has not decided
reaches for the median, and the median rendered to HTML is the card grid, the gradient headline,
the eyebrow over every section, the centered hero with two buttons. Installing more impressive
components does not fix it, it relocates it: the rainbow WebGL blob now sits exactly where the
purple CSS gradient sat in 2021.

So this library forces the decision first, then supplies the material.

## Read this first, always

`references/DOCTRINE.md` is the shared law. Load it before any other file here. Everything below
assumes it. Do not restate it back to the user; act on it.

## The one sequence that matters

Direction before elements. Every time, including on "just fix the hero".

```
1  BRIEF      what is true, who it is for, what the content actually is
2  DIRECTION  the 5-block contract, written down, before anything is placed
3  BUILD      surfaces, using the arsenal, repaired and tamed
4  GATE       slop, a11y, perf, then eyes on real screenshots
```

Skipping step 2 is how pages come out generic. If the user asks for a build and no direction
exists, write the direction first and show it. It costs 150 words.

## Commands

Invoke a sub-skill directly, or let this router pick.

### Decide

| Skill | Use when |
|---|---|
| `gmira-brief` | Starting anything. Extracts product truth, mode, and the real content model. |
| `gmira-direction` | The 5-block direction contract, with the anti-default mechanics. Nothing gets built before this. |
| `gmira-palette` | The color world. Committed strategy, 30 to 60% surface coverage, measured contrast. |
| `gmira-typeset` | The typographic voice. Measure, scale, tracking, what mono is allowed to mean. |

### Build

| Skill | Use when |
|---|---|
| `gmira-hero` | The first viewport. Owns the effect budget and the frame-zero problem. |
| `gmira-scroll` | Scroll choreography: pinned sections, scrub, tilt, reveal. One authored moment. |
| `gmira-catalog` | Any set of things: inventory, products, courses, creative walls. The anti-card-grid skill. |
| `gmira-detail` | A single thing in depth: PDP, vehicle detail, course page. Spec tables and variant state. |
| `gmira-flow` | Multi-step: checkout, enrollment, finance calculator, booking, application. |
| `gmira-proof` | Testimonials, results, logos, case studies. Without inventing any of them. |
| `gmira-nav` | Header, command menu, footer, and the chrome that carries the world. |

### Craft

| Skill | Use when |
|---|---|
| `gmira-arsenal` | Installing any registry component. Runs the repair and taming pass. Not optional. |
| `gmira-canvas` | Authoring or auditing canvas and WebGL work. Owns the GPU floor. |
| `gmira-motion` | Choosing and building the one authored moment. |
| `gmira-states` | Hover, focus, disabled, loading, error, empty. The six that get skipped. |

### Gate

| Skill | Use when |
|---|---|
| `gmira-slop` | Auditing for the visual tells no detector catches. Run before showing the user. |
| `gmira-a11y` | Contrast, focus order, semantics, canvas fallback readability. |
| `gmira-perf` | Frame budget, bundle weight, DPR caps, GPU teardown. |
| `gmira-verify` | Playwright at five viewports, then read the screenshots with your own eyes. |
| `gmira-ship` | Build, stage, publish. Never deploys without an explicit go. |

### Playbooks

Loaded by the build skills, not invoked directly. `references/playbooks/`:
`car-shop.md`, `ecommerce.md`, `ai-school.md`, `gtm-ugc-school.md`, and `worlds.md`
(the material-world catalog the direction skill draws from).

## Routing

- A vague ask ("build me a site", "make this better") means start at `gmira-brief`.
- A named surface with a direction already committed goes straight to the matching build skill.
- "It looks generic / bland / AI" is `gmira-slop` first, to name what is wrong, then almost
  always `gmira-direction`, because the cause is upstream of the pixels.
- "This component looks broken / wrong colors / nothing renders" is `gmira-arsenal`.
- Anything touching a canvas or shader also loads `gmira-canvas`.
- Before handing anything back: `gmira-verify`. No exceptions, and read the images.

## Stack

Next 16 + React 19 + Tailwind v4 + shadcn v4. Seven registries are wired in `components.json`
(514 components): `@componentry`, `@canvas-ui`, `@bklit`, `@ncdai`, `@kibo-ui`, `@react-bits`,
`@soundcn`. The shadcn MCP is connected; `shadcn search` and `shadcn view` work against all seven.

Default install stays cheap: `framer-motion`, `lenis`, `lucide-react`. That reaches every
non-three.js component including all four raw-WebGL heroes. three.js costs roughly 600 KB and is
only justified when one specific component earns it.

## Three laws that override any component's own defaults

Proven by build, written up in `references/DOCTRINE.md` Part 1.

1. **A registry component is an engine, not a design.** Its defaults are tuned to win a five-second
   gallery GIF. Install then tame, in the same breath.
2. **The arsenal is broken on arrival.** 12 of 56 componentry components ship unresolvable `cn`
   imports and 10 have undeclared dependencies. Repair before writing any page.
3. **An effect must earn its place at frame 0, with no input.** Pointer-driven effects are invisible
   in the state most visitors see.

## Prose

Everything this library writes for a user to read, including page copy: no dashes as pause,
sachlich tone, no performative warmth. Compound hyphens are fine. Denylist and the structural
AI-tells are in the doctrine, Part 7.5.
