---
name: gsap-motion
description: Design and implement intentional web motion with GSAP, React, Next.js, ScrollTrigger, Flip, SplitText, accessibility, performance, and responsive behavior. Use when animation or interaction polish is part of a frontend task.
metadata:
  short-description: Intentional GSAP motion for modern frontends
---

# GSAP Motion

Use this skill to add motion that clarifies state, hierarchy, navigation, storytelling, or direct manipulation in modern web interfaces.

Prefer the simplest durable tool:

- Use CSS transitions or keyframes for simple hover, focus, opacity, transform, and one-off state changes.
- Use GSAP Core for precise sequencing, interruption control, complex transforms, and animation that must be coordinated across elements.
- Use timelines when multiple animations need shared timing, labels, pause/resume, or reversal.
- Use ScrollTrigger for scroll-linked reveals, pinned sections, progress, and scroll storytelling.
- Use Flip for layout reordering, drag/drop transitions, masonry changes, filters, and route-level layout continuity.
- Use SplitText only when text animation is central to the experience and accessibility/fallbacks are handled.

## Operating Rules

- Motion must serve a product purpose: orientation, feedback, emphasis, continuity, or delight.
- Keep motion mobile-first and fast. Default to shorter durations, clear easing, and fewer moving parts on small screens.
- Respect `prefers-reduced-motion`; provide meaningful reduced or disabled motion paths.
- Animate `transform` and `opacity` whenever possible. Avoid animating layout-heavy properties in high-frequency motion.
- In React, scope animations to component lifecycles and clean up all GSAP instances, triggers, media queries, and observers.
- In Next.js, keep GSAP code on the client side and avoid server-side access to `window`, `document`, or DOM refs.
- Avoid decorative motion that competes with reading, decision-making, forms, navigation, or primary content.

## Routing

Read only what is relevant to the current task:

- For choosing CSS vs GSAP and selecting a pattern, read `references/decision-guide.md`.
- For GSAP basics, tweens, eases, utilities, cleanup, and defaults, read `references/gsap-core.md`.
- For sequencing, labels, shared control, and reversible UI motion, read `references/timelines.md`.
- For scroll reveals, pinned sections, scrubbed scenes, and responsive scroll behavior, read `references/scrolltrigger.md`.
- For React component integration, refs, `useGSAP`, context, and cleanup, read `references/react.md`.
- For Next.js App Router, client components, dynamic import, SSR boundaries, and route transitions, read `references/nextjs.md`.
- For accessibility, reduced motion, focus, vestibular safety, and text animation caveats, read `references/accessibility.md`.
- For rendering performance, layout thrash, GPU compositing, and testing, read `references/performance.md`.
- For breakpoints, input modes, resize behavior, and mobile-first defaults, read `references/responsive-motion.md`.
- For motion strategy, hierarchy, personality, and microinteractions, read `references/motion-design.md`.
- For common mistakes and when not to animate, read `references/anti-patterns.md`.

Use examples only as adaptation references, not as fixed templates:

- `examples/hero.tsx` for staged hero entrances.
- `examples/section-reveal.tsx` for progressive section reveals.
- `examples/stagger-cards.tsx` for card grids and ranking lists.
- `examples/scroll-storytelling.tsx` for ScrollTrigger scenes.
- `examples/flip-layout.tsx` for layout reorder/filter transitions.
- `examples/reduced-motion.tsx` for reduced-motion handling.

## Delivery Checklist

Before finishing a frontend motion task:

- Confirm motion still works when content length changes.
- Confirm cleanup prevents duplicated animations after remounts or route changes.
- Confirm keyboard and screen-reader flows remain usable.
- Confirm reduced-motion behavior is present.
- Confirm mobile and desktop timing, spacing, and trigger points feel appropriate.
- Confirm no important text or controls are obscured during animation.
