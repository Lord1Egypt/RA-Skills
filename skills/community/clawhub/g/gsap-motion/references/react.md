# React

React animation should respect component lifecycle, cleanup, remounts, concurrent rendering, and user state.

## Preferred Setup

Use `@gsap/react` when available:

```ts
import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(useGSAP);
```

Then scope animations to a root element:

```ts
const root = useRef<HTMLElement | null>(null);

useGSAP(
  () => {
    gsap.from("[data-card]", { opacity: 0, y: 16, stagger: 0.05 });
  },
  { scope: root },
);
```

Scoped selectors reduce accidental cross-component animation.

## Event Handlers

Wrap delayed or event-driven GSAP code with `contextSafe` so cleanup still works:

```ts
const { contextSafe } = useGSAP({ scope: root });

const onEnter = contextSafe((event: React.PointerEvent<HTMLButtonElement>) => {
  gsap.to(event.currentTarget, { scale: 1.04, duration: 0.18, overwrite: "auto" });
});
```

## Dependencies

Use dependencies intentionally. If an animation should rerun when data changes, include the relevant dependency and use `revertOnUpdate` when needed:

```ts
useGSAP(
  () => {
    gsap.from("[data-result]", { opacity: 0, y: 12, stagger: 0.04 });
  },
  { scope: root, dependencies: [items.length], revertOnUpdate: true },
);
```

Avoid rerunning entrance animations for unrelated state changes.

## Refs

For dynamic lists, data attributes plus scoped selectors are often simpler than managing an array of refs. Use explicit refs when the interaction targets a specific element or needs measurement.

## State And Animation

Let React own semantic state. Let GSAP own transient visual interpolation. Do not store every frame or transform value in React state.

Good split:

- React: selected item, expanded state, list order, modal open.
- GSAP: opacity, transform, timeline progress, transition between layouts.

## Cleanup Rules

- Create animations inside `useGSAP` when possible.
- Kill timelines created outside the hook.
- Remove listeners added manually.
- Use `contextSafe` for callbacks that create animations after the initial setup.
- Avoid global selectors and global mutable timelines unless deliberately app-level.
