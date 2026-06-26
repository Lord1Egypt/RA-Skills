# MindStudio Interface Designer Skill

A master Claude Code skill for building production-grade React interfaces inside the [MindStudio Interface Designer](https://university.mindstudio.ai/docs/building-ai-agents/interface-designer).

Drop this skill into your Claude Code project via the MindStudio local tunnel and Claude will interview you before writing a single line of code, commit to a bold aesthetic direction, wire all inputs to your MindStudio workflow variables correctly, and deliver a component that compiles and hands off to the next block without breaking.

---

## What This Skill Does

- **Interviews first, builds second.** Claude asks focused discovery questions about purpose, audience, tone, brand, and variable names before any design or code work begins.
- **Maps inputs to MindStudio variables.** Every field gets a confirmed variable name. State keys match exactly. A comment block at the top of every component documents what the workflow receives.
- **Wires the bridge correctly.** Uses `submit()` and `useIsRunning()` from `./bridge` — the only correct way to advance a MindStudio workflow. Never uses `window.MindStudio.submit`.
- **Commits to a real aesthetic direction.** Chooses from 10 defined archetypes (Refined Minimal, Dark Technical, Glassmorphic, Luxury Editorial, etc.) and executes fully — no generic AI aesthetics.
- **Ships accessible, performant code.** WCAG AA contrast, keyboard navigation, `prefers-reduced-motion`, React performance patterns, and a 30-point pre-delivery checklist enforced on every build.

---

## Setup

### Requirements

- [MindStudio](https://www.mindstudio.ai) account with Interface Designer access
- Claude Code installed and running
- MindStudio local tunnel connected to Claude Code

### Installation

1. Clone or download this repository
2. Copy `SKILL.md` into your Claude Code skills directory (typically `.claude/skills/mindstudio-interface-designer-skill/SKILL.md`)
3. Open your MindStudio project and add a **User Input** block to your workflow
4. In the block's Optional Settings, switch **Interface** to **Custom (Beta)**
5. Click **Configure Interface** to open the Interface Designer
6. Start the dev environment and connect via the local tunnel to Claude Code
7. Describe your interface — Claude will handle the rest

---

## How It Works

The skill follows a 12-phase process:

| Phase | What Happens |
|-------|-------------|
| 1. Discovery | Claude interviews you — one question at a time — about purpose, user, tone, brand, and variable names |
| 2. Aesthetic Direction | Claude commits to one of 10 archetypes and identifies the one unforgettable design moment |
| 3. Design System | Typography, color tokens, spacing, and z-index scale established before any code |
| 4. Component Architecture | MindStudio bridge wired correctly — `submit()`, `useIsRunning()`, variable state keys |
| 5. Visual Craft | Motion, backgrounds, depth, shadows, and glassmorphism patterns applied |
| 6. Interaction Design | Hover states, focus rings, loading states, form validation, touch targets |
| 7. Accessibility | ARIA labels, keyboard nav, contrast, `prefers-reduced-motion` |
| 8. React Performance | No waterfalls, no barrel imports, memoization, stable callbacks |
| 9. Light/Dark Mode | Both modes production-ready if theming is required |
| 10. Layout Patterns | Responsive layouts for forms, wizards, and dashboards |
| 11. Industry Guidance | SaaS, healthcare, fintech, beauty, creative — context-specific design direction |
| 12. Pre-Delivery Checklist | 30-point checklist covering visual, interaction, layout, accessibility, performance, and MindStudio compatibility |

---

## The MindStudio Bridge

The most critical piece. Every component this skill generates imports from `./bridge` — MindStudio's runtime connector between your React UI and the workflow engine.

```tsx
import { submit, useIsRunning } from './bridge'

export default function Interface() {
  const isRunning = useIsRunning()

  const handleSubmit = () => {
    submit({ topic, tone, keywords }) // advances to next workflow block
  }

  return (
    <button onClick={handleSubmit} disabled={isRunning}>
      {isRunning ? 'Processing...' : 'Submit'}
    </button>
  )
}
```

The skill enforces that `window.MindStudio.submit` and manual `setTimeout` loading patterns are never used — both fail silently in production.

---

## Aesthetic Archetypes

| Archetype | Best For |
|-----------|----------|
| Refined Minimal | SaaS, B2B, professional tools |
| Luxury Editorial | Portfolios, premium services |
| Dark Technical | Developer tools, AI products, fintech |
| Warm & Approachable | Consumer apps, health, education |
| Bold Brutalist | Fashion, art, provocative brands |
| Glassmorphic | Modern SaaS, dashboards |
| Bento Grid | Dashboards, feature showcases |
| Retro-Futuristic | AI tools, tech demos |
| Claymorphic | Consumer apps, games |
| Organic/Natural | Wellness, food, sustainability |

---

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | The skill itself — loaded by Claude Code |
| `README.md` | This file |
| `EXAMPLES.md` | Real prompt examples with expected variable output |
| `skill.json` | Skill metadata for registries and tooling |

---

## License

MIT
