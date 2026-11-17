# GSAP Motion Skill

`gsap-motion` is a reusable agent skill for designing and implementing intentional web motion with GSAP in modern frontend projects.

It helps agents decide when to use CSS, GSAP Core, timelines, ScrollTrigger, Flip, SplitText, and reduced-motion alternatives. The skill is intentionally modular: `SKILL.md` stays short, while focused references and examples are loaded only when relevant.

## Contents

```text
gsap-motion/
├── SKILL.md
├── README.md
├── .clawhubignore
├── references/
│   ├── decision-guide.md
│   ├── gsap-core.md
│   ├── timelines.md
│   ├── scrolltrigger.md
│   ├── react.md
│   ├── nextjs.md
│   ├── accessibility.md
│   ├── performance.md
│   ├── responsive-motion.md
│   ├── motion-design.md
│   └── anti-patterns.md
└── examples/
    ├── hero.tsx
    ├── section-reveal.tsx
    ├── stagger-cards.tsx
    ├── scroll-storytelling.tsx
    ├── flip-layout.tsx
    └── reduced-motion.tsx
```

## What This Skill Covers

- Contextual motion selection: CSS first when enough, GSAP when orchestration or precision is needed.
- GSAP Core patterns for tweens, defaults, utilities, selectors, and cleanup.
- Timelines for staged interface motion and reversible states.
- ScrollTrigger for reveal, progress, pinned, and scrubbed interactions.
- Flip for layout continuity during reorder, filter, and drag/drop UI.
- SplitText guidance for headline/text effects with accessibility constraints.
- React and Next.js lifecycle-safe implementation.
- `prefers-reduced-motion`, mobile-first behavior, and performance discipline.
- Anti-patterns that make interfaces feel noisy, slow, or inaccessible.

## Using With Agents

Copy the `gsap-motion` folder into the skill directory used by your agent runtime. For Codex-compatible skill systems, the required entrypoint is:

```text
gsap-motion/SKILL.md
```

Agents should load `SKILL.md` first, then read only the referenced files relevant to the current task.

## Publishing To ClawHub

This package is prepared for ClawHub-style skill distribution, but CLI commands and flags may change. Before publishing, confirm the current ClawHub documentation for the exact publish command, authentication flow, required metadata, and versioning rules.

Suggested pre-publish checks:

```bash
# Confirm the directory shape.
find gsap-motion -maxdepth 3 -type f | sort

# Inspect the skill entrypoint.
sed -n '1,160p' gsap-motion/SKILL.md

# Use the current ClawHub CLI/docs to validate or publish.
# Example shape only; confirm exact command and flags in current docs:
# clawhub skill publish ./gsap-motion --dry-run
# clawhub skill publish ./gsap-motion
```

## Maintenance Notes

- Keep `SKILL.md` concise and operational.
- Add new references only when they materially improve agent decisions.
- Do not paste long official documentation excerpts into this package; summarize durable patterns and link users to official docs when needed.
- Keep examples small enough to adapt, but complete enough to show lifecycle, cleanup, reduced motion, and mobile-friendly behavior.
