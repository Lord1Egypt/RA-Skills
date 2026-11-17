---
name: immersive-presentations
description: Create cinematic, narrative, interactive web presentations from a topic or briefing. Use when the user wants an immersive presentable experience rather than a conventional slide deck.
metadata:
  short-description: Build immersive narrative web presentations
---

# Immersive Presentations

Use this skill when creating, planning, reviewing, or improving a web-based presentation that should feel like a guided interactive experience: cinematic, didactic, visual, narrative, and presentable live.

Core maxim:

**DO NOT build a deck. BUILD AN EXPERIENCE THAT CAN BE PRESENTED.**

The basic unit is a `scene`, not a `slide`. A scene has a purpose, a beat in the story, a visual state, continuity with surrounding scenes, interaction rules, pacing, and a transition. Avoid treating the output as a sequence of static screens with decorative animation.

## Operating Model

Start by turning the user's topic or briefing into a narrative system:

1. Identify the audience, promised transformation, central tension, and takeaway.
2. Shape the story into acts and scenes.
3. Select visual metaphors and persistent objects that can transform across scenes.
4. Define the presentation camera: framing, movement, focus, zoom, reveal, and spatial continuity.
5. Design interaction as meaningful exploration, not decoration.
6. Implement as a responsive web experience with presenter and debug modes.
7. Verify motion, readability, keyboard flow, reduced-motion behavior, and mobile framing.

Whenever possible, demonstrate concepts visually instead of explaining them only with text. Replace bullet lists with transformations, diagrams, timelines, maps, simulations, comparisons, annotated objects, and progressive reveals.

## Read Relevant References

Read only the references needed for the current task:

- For story structure, acts, scene beats, pacing, and continuity, read [references/narrative-architecture.md](references/narrative-architecture.md).
- For scene archetypes, visual metaphors, object permanence, and anti-deck composition, read [references/scene-system.md](references/scene-system.md).
- For animation strategy and delegation to the user's `gsap-motion` skill, read [references/motion-and-gsap.md](references/motion-and-gsap.md).
- For presenter mode, debug mode, keyboard/scroll control, and interaction design, read [references/interaction-and-modes.md](references/interaction-and-modes.md).
- For responsive design, accessibility, performance, and QA expectations, read [references/accessibility-responsive-performance.md](references/accessibility-responsive-performance.md).
- For technical diagrams, data storytelling, technical topics, business, science, and education, read [references/diagrams-data-and-domains.md](references/diagrams-data-and-domains.md).
- For things to avoid and final acceptance criteria, read [references/anti-patterns-and-quality-bar.md](references/anti-patterns-and-quality-bar.md).
- For reusable prompts and output templates, read files in [references/templates](references/templates) as needed.
- For examples of complete narrative plans, read [references/examples](references/examples) only when examples would improve the result.

## Required Deliverables For New Presentations

When asked to create a presentation, produce or implement:

- A concise `presentation-plan.md` or equivalent planning section with audience, objective, thesis, narrative arc, acts, scene list, recurring objects, interaction model, and motion intent.
- A web implementation or implementation-ready spec where each scene has a clear `scene id`, role in the narrative, visual metaphor, key objects, transition in/out, interaction, accessibility notes, and presenter notes.
- Presenter controls: previous/next, progress, keyboard support, and an option for presenter notes or speaker view when practical.
- Debug controls for development: scene jump, motion/reduced-motion toggle, layout safe-area overlay, and state reset when practical.
- Responsive layouts for desktop and mobile that preserve the narrative rather than merely stacking slide-like content.

## Design Rules

- Use scenes, acts, camera moves, object transformations, and spatial continuity.
- Keep important visual objects alive across transitions when they represent the same idea.
- Prefer annotated diagrams, simulated systems, comparative canvases, timelines, maps, or data scenes over large text blocks.
- Use text as narration, labels, captions, and punchlines. Do not use text as the whole experience.
- Use typography, position, scale, light, and motion to guide attention.
- Make interactions reveal causality, tradeoffs, sequence, or structure.

## Forbidden Defaults

Do not create a conventional deck by default. Avoid:

- Title-and-bullets slides.
- Repeated fade-in/fade-out transitions.
- Card grids masquerading as storytelling.
- SaaS dashboard aesthetic unless the content is literally an operational product interface.
- Gratuitous glassmorphism, gradient blobs, neon panels, or decorative particle fields.
- Static screenshots with animated captions as the primary experience.
- Walls of bullet points, tiny labels, or dense paragraphs.
- Motion that does not teach, reveal, compare, transform, or focus attention.

## Integration With `gsap-motion`

If the user's `gsap-motion` skill is available, use it for motion execution after this skill has defined the narrative, scene structure, motion intent, accessibility constraints, and interaction behavior. This skill decides what the experience should communicate and how scenes relate; `gsap-motion` helps implement timelines, ScrollTrigger, Flip, SplitText, responsive motion, performance, and reduced-motion behavior.

If `gsap-motion` is not available, implement motion directly with the project's existing stack while preserving the same intent and quality bar.
