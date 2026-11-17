# Decision Guide

Use motion only when it helps the user understand what changed, where they are, what can be interacted with, or what deserves attention.

## CSS First

Use CSS transitions or keyframes when animation is:

- A simple hover, press, focus, selected, disabled, or expanded state.
- A single-element opacity or transform change.
- Declarative and tied directly to class/state changes.
- Easy to express without measuring layout or sequencing multiple actors.

Good CSS candidates:

- Button press feedback.
- Card hover lift.
- Navigation active indicator.
- Tooltip fade/slide.
- Loading shimmer.
- Drawer overlay fade plus panel slide, if simple.

## Use GSAP Core

Use GSAP when the interface needs:

- Precise sequencing or orchestration.
- Interruptible animations that should not stack.
- Dynamic values computed at runtime.
- Coordinated movement across multiple elements.
- Physics-like easing, quick setters, or repeated controlled effects.
- Cleanup-safe imperative control inside component lifecycle.

## Use Timelines

Use a timeline when:

- Several animations belong to one experience.
- You need labels, offsets, nested timing, pause, resume, reverse, or restart.
- State changes should be replayable or reversible.
- A component has an entrance sequence with dependent parts.

## Use ScrollTrigger

Use ScrollTrigger when animation depends on scroll position:

- Section reveals.
- Pinned panels.
- Scroll progress indicators.
- Scrubbed storytelling scenes.
- Batch reveals of repeated content.

Avoid ScrollTrigger for ordinary viewport visibility if CSS or a lightweight Intersection Observer is enough.

## Use Flip

Use Flip when layout changes should feel continuous:

- Sorting a ranking.
- Filtering cards.
- Drag/drop reordering.
- Moving an item from grid to detail view.
- Changing from compact to expanded card layouts.

Flip is often better than manually calculating transforms because it derives the visual transition from before/after layout states.

## Use SplitText Carefully

Use SplitText when animated typography is important to the concept: hero headlines, editorial reveals, kinetic type, or brand moments.

Avoid it for body text, legal text, long paragraphs, frequently changing content, or text that must remain immediately readable. Preserve readable DOM semantics and provide a reduced-motion path.

## Selection Questions

Before choosing an implementation, answer:

- What user problem does this motion solve?
- Does CSS fully cover the behavior?
- Does the animation need sequencing, cleanup, or interruption control?
- Does it respond to scroll, layout changes, or user drag?
- How does it behave with reduced motion?
- What happens on narrow screens, touch input, slow devices, and long content?
