# Next.js

GSAP touches the DOM, so keep it inside client-side code.

## App Router

Components that use GSAP directly should begin with:

```tsx
"use client";
```

Import GSAP and plugins inside that client component or a client-only helper.

## SSR Boundaries

Do not access `window`, `document`, DOM refs, or layout measurements during server render.

Safe pattern:

```tsx
"use client";

import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(useGSAP);
```

The animation setup runs after the component has mounted.

## Dynamic Imports

For heavier or route-specific animation modules, use dynamic import or component splitting so static pages do not load unnecessary animation code.

```tsx
import dynamic from "next/dynamic";

const MotionHero = dynamic(() => import("./MotionHero"), { ssr: false });
```

Use this when the animated component is optional, heavy, or depends on browser-only plugins.

## Route Transitions

Use route-level motion only when it improves orientation. Avoid long transitions that make navigation feel slower.

If preserving layout continuity across routes, consider Flip, shared stable IDs, and a short fallback when source/target elements are not both present.

## Images And ScrollTrigger

Next.js images can affect layout after loading if dimensions are not reserved. Prefer explicit sizes, aspect ratios, or containers. Refresh ScrollTrigger after major dynamic layout changes.

## Reduced Motion

Read reduced-motion preference in client code. Keep server-rendered content visible and usable before animation code runs.

## Deployment Discipline

- Avoid debug markers in production.
- Do not register the same plugin repeatedly in many modules if a shared client boundary is available.
- Confirm hydration does not depend on animation-created DOM.
- Keep text and controls in the DOM in meaningful order; animation should not be the only structure.
