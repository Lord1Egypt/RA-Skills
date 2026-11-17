# Finding 02: pointer-driven effects have no idle state, and drag fights the DOM

Date: 2026-07-25. Screenshots in `proofs/finding-02/`.

Component under test: `@canvas-ui/liquid-react`, a real Navier-Stokes fluid solver that uses the
experimental html-in-canvas (`drawElement`) API to displace live DOM. Chrome 140+ behind
`chrome://flags/#canvas-draw-element`; everywhere else it falls back to a WebGL overlay.

This component is genuinely well built, which is why its failure modes are the interesting ones.
What it gets right, and what the library should copy verbatim:

- `useSyncExternalStore(emptySubscribe, supportsHtmlInCanvas, () => false)` for SSR-safe feature
  detection. The server snapshot returns `false`, so it never hydration-mismatches.
- The fallback renders `children` as **real DOM**, so text stays selectable, copyable, and
  reachable by a screen reader on every browser. The effect degrades, the content never does.
- The output canvas is `aria-hidden` with `pointerEvents: "none"`.
- `LiquidInstance` exposes an explicit `destroy()` that releases GPU resources, and `resize()`.

## Defect 1: nothing renders at frame 0

A fluid sim only paints where momentum has been injected. On first paint the hero is an empty
dark rectangle (`01-frame-zero-empty.png`). Every visitor sees that frame. Many see only that
frame: they land, read, and leave without ever dragging.

This generalizes past this component. Any effect keyed to pointer input (fluid, image-trail,
text-repel, cursor-driven particle typography, magnet-lines) is **invisible in the state that
matters most**. A gallery GIF never shows this because the person recording the GIF is already
moving the mouse.

**Law:** an effect must earn its place in the composition at frame 0, with no input. Either seed
it (inject splats on mount along a designed path), give it autonomous idle motion, or accept it
is a reward for interaction and design a hero that is already complete without it.

The React wrapper here makes seeding impossible: `createLiquid` returns an instance with a public
`splat(x, y, dx, dy)`, and `Liquid` keeps it in a private ref with no forwarded handle. Using it
as a hero requires patching the wrapper to expose the instance. That is the same install-then-tame
practice as Finding 01.

## Defect 2: drag selects text instead of driving the effect

The component's own framing is "drag across it". In the fallback path the children are real DOM,
so a drag is a **text selection**. `03-real-drag-selects-text.png` shows the headline highlighted
in blue with only faint fluid behind it. The interaction the component advertises and the
interaction the browser performs are different interactions.

The two correct resolutions, pick per surface:

- Drive from `pointermove` with no button held, so hovering is the gesture and drag stays
  selection. Right for text-bearing surfaces.
- Keep drag, and set `user-select: none` on the content. Only acceptable where the text is
  decorative, never on a headline someone might want to copy.

Shipping neither, which is the default, means the marquee interaction of the hero is broken on
the exact surface the component was built for.

## Defect 3: restrained settings make the effect invisible, loud settings make it slop

Defaults are `intensity: 2`, `blend: 5`, `distortion: 0.4`. Toned to `intensity: 1.1`,
`blend: 2.4` for a dark automotive palette, the fluid is barely perceptible even mid-drag.

This is the central tension of the whole arsenal and it does not have a settings answer. Turning
an effect down until it is tasteful usually turns it down until it is pointless, and the reflex
fix is to turn it back up until it is loud, which is where the gallery demo already was.

**Law:** the answer is compositional, not parametric. Give the effect a bounded region where it
can run at full strength (a panel, a card, a masked band, a single figure) instead of a
full-bleed backdrop that must stay quiet to keep text legible. Full strength inside a boundary
reads as intent. Half strength everywhere reads as a filter someone left on.

## Method note for the verify skill

Synthetic `new PointerEvent(...)` carries `movementX = 0`, and fluid solvers derive splat velocity
from movement deltas, so a dispatched event injects zero force and nothing renders
(`02-synthetic-events-nothing.png`). GL context was alive the whole time, so a "does it work"
check built on synthetic events reports a false negative.

**Any verify step for a pointer-driven effect must use the real mouse** (`page.mouse.move`,
`locator.dragTo`, `hover`), never `dispatchEvent`. Worth encoding in the verify skill, since it
is exactly the kind of check that silently passes or silently fails for the wrong reason.
