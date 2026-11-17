# Timelines

Use timelines to make related motion behave like one controlled sequence.

## When To Use

Use a timeline when:

- Multiple elements animate as one interaction.
- Timing relationships matter.
- A sequence needs labels or overlaps.
- The animation should be paused, resumed, reversed, or restarted.
- You need predictable cleanup for several tweens.

## Structure

Keep timelines local to the component or interaction.

```ts
const tl = gsap.timeline({
  defaults: { duration: 0.35, ease: "power2.out" },
});

tl.from("[data-kicker]", { opacity: 0, y: 10 })
  .from("[data-title]", { opacity: 0, y: 18 }, "-=0.15")
  .from("[data-card]", { opacity: 0, y: 20, stagger: 0.05 }, "-=0.1");
```

## Labels

Labels make complex sequences easier to read and adjust:

```ts
tl.addLabel("intro")
  .from(title, { opacity: 0, y: 18 }, "intro")
  .from(media, { opacity: 0, scale: 0.96 }, "intro+=0.08");
```

## Reversible UI

For menus, drawers, detail panels, and preview states, create paused timelines and play or reverse them:

```ts
const menuTl = gsap.timeline({ paused: true })
  .to(panel, { xPercent: 0, duration: 0.28, ease: "power2.out" })
  .to(backdrop, { opacity: 1, duration: 0.2 }, "<");

menuTl.play();
menuTl.reverse();
```

Ensure the initial visual state exists in CSS so the page is usable before JavaScript runs.

## Nested Timelines

Use small timeline factories for repeated motion patterns:

```ts
function cardIntro(card: HTMLElement) {
  return gsap.timeline()
    .from(card.querySelector("[data-rank]"), { scale: 0.8, opacity: 0 })
    .from(card.querySelector("[data-cover]"), { y: 16, opacity: 0 }, "<");
}
```

Avoid over-abstracting timelines when a direct sequence is clearer.

## Timing Discipline

- Overlap related animations with `"<"` or `"-=..."`.
- Keep repeated-item staggers tight.
- Let important content arrive early.
- Avoid long chained entrances that make the user wait.
- Use `clearProps` only when returning control to CSS is important.
