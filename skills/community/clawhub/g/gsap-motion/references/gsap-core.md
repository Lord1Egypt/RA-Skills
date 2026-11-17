# GSAP Core

GSAP Core is best for precise DOM animation, especially transforms, opacity, coordinated states, and values that are difficult to express cleanly with CSS alone.

## Core Patterns

Use `gsap.to` for animating from the current state:

```ts
gsap.to(element, { opacity: 1, y: 0, duration: 0.45, ease: "power2.out" });
```

Use `gsap.from` for entrance motion:

```ts
gsap.from(element, { opacity: 0, y: 16, duration: 0.4, ease: "power2.out" });
```

Use `gsap.fromTo` when the start and end states must be explicit:

```ts
gsap.fromTo(
  element,
  { opacity: 0, scale: 0.96 },
  { opacity: 1, scale: 1, duration: 0.35, ease: "power2.out" },
);
```

## Defaults

Set local defaults inside a timeline or scoped setup instead of relying on global defaults for component code:

```ts
const tl = gsap.timeline({
  defaults: { duration: 0.35, ease: "power2.out" },
});
```

Global defaults can be useful for a whole app only when the team intentionally centralizes motion tokens.

## Easing

Use restrained eases for product UI:

- `power2.out` for entrances and state changes.
- `power2.inOut` for transitions between two stable states.
- `power3.out` for more expressive reveals.
- `back.out(...)` sparingly for playful feedback.

Avoid elastic or bounce eases for routine UI because they can feel slow and distract from content.

## Selectors And Scope

Prefer refs and scoped selectors in component systems. Avoid global selectors that can accidentally animate unrelated elements.

```ts
const items = gsap.utils.toArray<HTMLElement>("[data-card]", scope);
```

When using React, prefer `useGSAP` with a `scope` ref and `contextSafe` handlers. See `references/react.md`.

## Interruption

Kill or overwrite animations when the same target can be animated repeatedly:

```ts
gsap.to(target, {
  x: 0,
  opacity: 1,
  duration: 0.25,
  overwrite: "auto",
});
```

For high-frequency pointer effects, use `gsap.quickTo` or `gsap.quickSetter` rather than creating new tweens continuously.

## Cleanup

Every component-level animation should have a cleanup path:

- Revert GSAP context.
- Kill timelines created outside context.
- Kill ScrollTriggers created manually.
- Remove event listeners.
- Revert matchMedia registrations.

## Practical Defaults

For interface work:

- Keep most durations between `0.18` and `0.6` seconds.
- Use shorter durations for repeated items.
- Stagger lists lightly, usually `0.03` to `0.08` seconds.
- Avoid delaying primary controls.
- Never block reading or input with decorative entrance motion.
