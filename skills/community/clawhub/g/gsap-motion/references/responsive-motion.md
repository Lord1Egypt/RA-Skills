# Responsive Motion

Design motion mobile-first. Small screens, touch input, and short viewports change how motion feels.

## Mobile Defaults

On mobile:

- Use shorter travel distances.
- Keep durations tight.
- Avoid wide lateral motion that pushes content off-screen.
- Avoid pinned scroll scenes unless central to the experience.
- Prefer direct feedback near the user's touch target.
- Keep bottom navigation and primary controls stable.

## Desktop Enhancements

Desktop can support:

- Larger spatial transitions.
- More layered depth.
- Cursor-responsive hover effects.
- Wider staggered compositions.
- More ambitious scroll storytelling.

Treat these as enhancements, not requirements.

## Breakpoint-Aware Motion

Use GSAP matchMedia or CSS media queries to adjust behavior:

```ts
const mm = gsap.matchMedia();

mm.add("(min-width: 768px)", () => {
  gsap.from("[data-panel]", { x: 40, opacity: 0, stagger: 0.06 });
});

mm.add("(max-width: 767px)", () => {
  gsap.from("[data-panel]", { y: 18, opacity: 0, stagger: 0.04 });
});

return () => mm.revert();
```

## Input Modes

Do not rely on hover for essential interactions. Pair hover polish with tap/click/focus behavior.

Use pointer checks when needed:

```css
@media (hover: hover) and (pointer: fine) {
  .card:hover {
    transform: translateY(-2px);
  }
}
```

## Resizing

When animation depends on layout:

- Use responsive units and stable dimensions.
- Recalculate after resize if necessary.
- Let ScrollTrigger refresh positions.
- Prefer Flip for layout transitions caused by breakpoint changes.

## Content Variability

Design for long names, localized text, missing images, and dynamic counts. Motion must not hide overflow problems or make them worse.
