# Pretext + Three.js Viral Frontend Agent Pack

A generic agent pack for building shareable, reactive, editorial, game-like, and physically expressive web interfaces with **Pretext**, **Three.js**, and **Canvas 2D**.

This pack is intentionally **project-agnostic**. It is for GitHub agents, ClawHub agents, Claude Code, OpenClaw, Hermes-style specialists, and other code agents that need a clear operational skill instead of vague design advice.

## Files

- `SKILL.md` — core knowledge: APIs, architectures, renderer choices, ecosystem patterns, and implementation guidance.
- `TASK.md` — generic mission brief for building viral Pretext + Three.js experiences.
- `CHECKLIST.md` — acceptance criteria and failure checks.
- `PROMPTS.md` — reusable prompts for different execution modes.
- `EXAMPLES.md` — compact starter patterns and implementation snippets.

## What changed in this version

This revision adds **clear ecosystem patterns** agents should borrow from:

- **Textura** — DOM-free layout engine pattern using Pretext + Yoga.
- **Pinch-Type** — mobile pinch-to-resize-text pattern.
- **Pretext Breaker variants** — word/glyph-as-brick game pattern.
- **Dokobot pretext-demo** — instant obstacle-aware relayout playground pattern.
- **Variable Typographic ASCII / editorial demos** — ambient rails, proportional ASCII, and magazine-like flow patterns.

## Best use

Use this pack when the goal is to build one of these:

- typographic hero scenes
- reactive particle or glyph formations
- physics-based text destruction / reconstruction
- spatial/editorial microsites
- launch pages with one unforgettable interaction
- mini-games that treat text as a physical material
- hybrid DOM + WebGL interfaces

## Non-goals

This pack is **not** for:

- standard marketing sites with no interaction ambition
- generic Tailwind-only UI work
- backend integration plans
- project-specific branding or business logic

## Recommended agent order

1. Read `SKILL.md`
2. Read `TASK.md`
3. Use `CHECKLIST.md` while building
4. Use `PROMPTS.md` to choose a mode
5. Copy patterns from `EXAMPLES.md`

## Ideal output style

Agents using this pack should produce:

- fast-loading experiences
- motion with clear hierarchy
- readable typography at rest
- dramatic interaction without losing usability
- mobile-safe fallbacks
- clean, modular code
