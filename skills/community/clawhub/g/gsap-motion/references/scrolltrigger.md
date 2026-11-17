# ScrollTrigger

Use ScrollTrigger when animation depends on scroll position, viewport entry, pinned storytelling, or scroll progress.

## Registration

Register plugins once in a client-side module or component boundary:

```ts
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);
```

In Next.js, this belongs in a client component or dynamically imported client-only module.

## Reveals

Use modest reveal distances and trigger points. Content should not feel hidden for too long.

```ts
gsap.from(items, {
  opacity: 0,
  y: 24,
  duration: 0.45,
  ease: "power2.out",
  stagger: 0.05,
  scrollTrigger: {
    trigger: section,
    start: "top 75%",
    once: true,
  },
});
```

## Scrubbed Motion

Use `scrub` when visual state should map to scroll progress. Avoid scrubbed text readability effects unless the text remains legible.

```ts
gsap.to(panel, {
  scale: 0.94,
  opacity: 0.75,
  scrollTrigger: {
    trigger: section,
    start: "top top",
    end: "bottom top",
    scrub: true,
  },
});
```

## Pinning

Pinned sections can be powerful but expensive on mobile. Use them when they support storytelling or comparison, not as default page decoration.

Consider disabling or simplifying pinned scenes on narrow screens:

```ts
ScrollTrigger.matchMedia({
  "(min-width: 768px)": () => {
    // pinned desktop scene
  },
  "(max-width: 767px)": () => {
    // simpler mobile reveal
  },
});
```

## Refresh And Dynamic Content

Call refresh after images, fonts, route transitions, or dynamic layout changes that affect trigger positions:

```ts
ScrollTrigger.refresh();
```

Prefer stable image dimensions and reserved layout space so refreshes are less likely to cause visible jumps.

## Cleanup

When using `useGSAP`, triggers created inside context are reverted with the context. For manual setup, kill triggers on cleanup:

```ts
const trigger = ScrollTrigger.create({ trigger: el, start: "top center" });
trigger.kill();
```

## Practical Rules

- Use `once: true` for ordinary reveal animations.
- Avoid animating every section in the same way.
- Do not hide essential content until scroll JavaScript runs.
- Test touch devices and short screens.
- Avoid pinned scroll hijacking.
- Keep debug markers out of production.
