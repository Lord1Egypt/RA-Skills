# immersive-presentations

`immersive-presentations` is a Codex/OpenCode skill for turning topics, briefs, research, or technical material into cinematic, interactive web presentations.

Its core rule:

**DO NOT build a deck. BUILD AN EXPERIENCE THAT CAN BE PRESENTED.**

The skill treats the basic unit as a `scene`, not a `slide`. It helps an agent design narrative architecture, acts, scene systems, visual metaphors, object continuity, presentation camera moves, meaningful interactivity, presenter/debug modes, accessibility, responsive behavior, technical diagrams, and data storytelling.

## What It Creates

- Narrative web presentations and scrollytelling experiences.
- Technical explainers with animated diagrams.
- Business, strategy, education, science, and data presentations.
- Speaker-ready interactive microsites.
- Implementation plans for React, Next.js, Vite, GSAP, canvas, SVG, WebGL, or native web stacks.

## Package Structure

```text
immersive-presentations/
|-- SKILL.md
|-- README.md
|-- agents/
|   `-- openai.yaml
`-- references/
    |-- narrative-architecture.md
    |-- scene-system.md
    |-- motion-and-gsap.md
    |-- interaction-and-modes.md
    |-- accessibility-responsive-performance.md
    |-- diagrams-data-and-domains.md
    |-- anti-patterns-and-quality-bar.md
    |-- templates/
    |   |-- briefing-template.md
    |   |-- presentation-plan-template.md
    |   |-- scene-spec-template.md
    |   `-- prompt-pack.md
    `-- examples/
        |-- rag-vs-agents.md
        `-- climate-risk-boardroom.md
```

## Installation

Copy the `immersive-presentations` folder into your OpenCode/Codex skills directory, for example:

```bash
~/.codex/skills/immersive-presentations
```

Then invoke it naturally:

```text
Use $immersive-presentations to create an interactive presentation about RAG vs autonomous agents for executives.
```

## Recommended Pairing

This skill is designed to work above the user's existing `gsap-motion` skill:

- `immersive-presentations` defines the narrative, scenes, metaphors, pacing, interactivity, and presentation behavior.
- `gsap-motion` executes advanced motion: timelines, ScrollTrigger, Flip, SplitText, responsive animation, accessibility, and performance.

## Good Input

```text
Create an immersive web presentation about how retrieval-augmented generation compares with AI agents.
Audience: directors and product leaders.
Goal: help them decide when to use each architecture.
Tone: cinematic, practical, not hype.
Length: 8-10 minutes.
```

## Expected Output

The agent should produce an implemented web experience or an implementation-ready plan with:

- Acts and scenes.
- Visual metaphors.
- Persistent objects and transformations.
- Presenter controls.
- Debug mode.
- Responsive behavior.
- Accessibility and reduced-motion support.
- Concrete technical implementation notes.

