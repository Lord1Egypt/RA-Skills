# Design Reference Library — Installation & Usage

**Installed:** June 1 2026
**Location:** `~/.hermes/references/design/`
**Index:** `~/.hermes/references/design/INDEX.md`

## Glitch aesthetic (your home base)

Your glitch design language lives at `design/glitch-aesthetic/`:
- `web-glitch-effects.md` — main reference (character corruption, chromatic aberration, weather-reactive colors, syslog panel, scroll-driven effects)
- `keyframes-and-css.md` — keyframe animations, glitch wrapper CSS, weather-to-color mapping
- `telemetry-bleed.md` — visitor telemetry harvester, three-mode bleed engine
- `syslog-panel.md` — syslog panel layout, typing animation, entry lifecycle

Created: May 27 2026. Moved from `<fs-root>/references/creative/` to `~/.hermes/references/design/glitch-aesthetic/` on June 1 2026.

This is separate from the four reference repos below. Use these when the project calls for polished, established design languages. Use your glitch aesthetic when that's the right fit.

## What's here

Four repos + one enforcement skill system, ~1,550 files, ~32MB of design system specs:

| Repo | Content |
|------|---------|
| `design.md/` (Google) | The DESIGN.md format spec — token schema, CLI (lint/diff/export), canonical section order |
| `awesome-design-md/` (VoltAgent) | 72 real-world brand design systems — Stripe, Linear, Spotify, Apple, Nike, Vercel, BMW, etc. |
| `awesome-design-skills/` (TypeUI) | 67 named aesthetic styles — Glassmorphism, Brutalism, Neobrutalism, Claymorphism, Cosmic, Editorial, etc. |
| `awesome-ios-design-md/` (Meliwat) | 200 top iOS app design systems, each with 4 flavors (SwiftUI, Expo/RN, Jetpack Compose, framework-neutral) |
| `taste-skill/` (Leonxlnx) | Anti-slop frontend enforcement for AI agents. Dials system (variance/motion/density), brief inference protocol, hard layout rules, pre-flight checklist. Stack-agnostic anti-pattern reference. |
| `responsive-design/` (wshobson) | Modern responsive CSS layouts — container queries, fluid typography with clamp(), CSS Grid/Flexbox patterns, mobile-first breakpoints, responsive nav/images/tables. 4 reference files with worked CSS/TSX examples. |

## When to use (triggers)

- Building any web app, site, or UI component
- Writing a DESIGN.md for a project
- Choosing a visual direction / aesthetic for a product
- Building a mobile app (iOS, Android, React Native, Flutter)
- User says "make it look like X" or "use the design from Y"
- Any task where you'd otherwise default to generic/aesthetic-free UI choices
- **Responsive CSS:** building fluid layouts, container queries, breakpoint strategies, responsive typography → use `responsive-design/references/` for worked CSS/TSX patterns
- **Preventing AI-slop:** output looks generic, templated, or has common AI design tells → use `taste-skill/anti-slop-rules.md` and `anti-slop-preflight.md`
- **Redesigning existing UI:** auditing and upgrading an existing frontend → use `taste-skill/` redesign-skill
- **Frontend quality gate:** before shipping any UI, run the pre-flight checklist at `taste-skill/anti-slop-preflight.md`

## How to use

**For web/SaaS projects:**
1. Browse `awesome-design-md/` entries in INDEX.md for the closest brand match
2. Fetch the DESIGN.md from getdesign.md (URLs in the repo README)
3. Drop it in project root, tell your agent to build against it

**For aesthetic direction:**
1. Browse `awesome-design-skills/` for the style (e.g., "glassmorphism", "brutalism")
2. Preview at https://typeui.sh/design-skills
3. Pull: `npx typeui.sh pull <slug>`

**For mobile apps:**
1. Find the closest app in `awesome-ios-design-md/design-md/<category>/<app>/`
2. Pick the flavor matching your stack
3. Drop next to AGENTS.md / CLAUDE.md

**For responsive CSS layouts:**
1. Read `responsive-design/SKILL.md` for the overview and best practices
2. For worked examples, go to `responsive-design/references/`:
   - `details.md` — container queries, fluid typography, CSS Grid, responsive nav/images/tables (CSS + TSX)
   - `breakpoint-strategies.md` — mobile-first breakpoint scales, content-based breakpoints
   - `container-queries.md` — container query syntax, units (cqi/cqw/cqh), style queries
   - `fluid-layouts.md` — clamp() patterns, fluid spacing systems, viewport units (dvh/svh/lvh)

## Reference file path convention

Reference files for design live under `~/.hermes/references/design/`. This is the current convention. If you find design references at old paths like `<fs-root>/references/creative/`, migrate them here.

Responsive-design skill references live under `$HERMES_HOME/../indigo/skills/responsive-design/references/`.

## Updating

```bash
cd ~/.hermes/references/design/<repo> && git pull
```

For the responsive-design skill (installed via agentskill.sh CLI):
```bash
npx @agentskill.sh/cli@latest install @wshobson/responsive-design
cp -r ~/.hermes/skills/responsive-design $HERMES_HOME/../indigo/skills/responsive-design
```