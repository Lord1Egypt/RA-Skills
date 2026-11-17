# 3D Industry-Evolution Graph — Pitfalls & Lessons (hard-won during the AI-history project)

The following are the "final correct" conclusions we reached after many iterations of getting this kind of graph right. **Do not "optimize" your way back to the old behavior** when reusing the template.

## 1. Hover card: hug the current node, do NOT add "avoidance" logic
- **Final correct baseline**: `placeCard(node)` uses `nodeScreenCenter(node)` to compute the node's screen center, then places the card `+14px` down-right of it — and only does viewport clamping (so it can't go off-screen).
- We once added logic like "pick the emptiest of 4 sides / expand toward screen center / soft-clamp", and the card got flung into a corner and drifted further away with every hover. The user rejected it every time.
- The real requirement is: "card hugs the currently hovered node, the node peeks out from the card edge, **it's fine if it covers other non-hovered nodes**" — NOT "card must be fully visible and not cover anything".
- **Lesson**: for spatial-layout needs that are hard to describe in words, send a reference screenshot — it's the most accurate spec. Once the user accepts a minimal baseline, reuse it; don't pile on complex logic.

## 2. Oldest node must be off the ground (AXIS_BASE > 0)
- If the time axis anchors at `Y=0` (the ground plane), the oldest year (e.g. 1943) only sits a hair above the floor, while the event tetrahedron has radius 4.2 and the person sprite half-height is ~4.5 — so it **pokes into / half-buries in the ground**, looking like it's "below the horizon".
- Fix: `yearToY` maps `YEAR_MIN -> AXIS_BASE` (e.g. 10) and `YEAR_MAX -> AXIS_H`; the axis vertical line also starts at `AXIS_BASE`. Verify the oldest node's center is well above the ground.

## 3. Hover-to-front: renderOrder + depthTest off
- When nodes are dense/collapsed, the hovered node gets occluded by nodes behind it and can't be clicked.
- Fix: `setNodeActive(obj, true)` sets `obj.renderOrder=1000`, `obj.material.depthTest=false`, `depthWrite=true`; the connecting line / spotlight use 999 / 998 respectively. Reset everything on leave.

## 4. Image inlining & source limits (sandbox / browser)
- Goal: the page must **open offline** → avatars / logos / map are base64-inlined at generation time.
- In the sandbox, **Wikimedia gets SIGKILL'd and is unreachable**, but the **Bing image CDN is reachable**; prefer Bing image links (or Sina / other reachable sources) for person avatars.
- SVG logos go in directly as `data:image/svg+xml;base64,` (PIL can't read SVG); bitmaps are cropped to a circle (avatar) / shrunk (logo/map) via PIL, then converted to PNG base64.
- At runtime, avatars use `texLoader.load(dataURI)` and logos use `Image()` + canvas drawn onto a rounded brand-colored background; both accept data URIs and don't taint the canvas.

## 5. Deploy: reuse the same CloudStudio sandbox to keep the URL stable
- `workbuddy_cloudstudio_deploy` with the same directory/sandbox reuses it, keeping the URL stable (avoids a new link every time).
- After changes, always `curl` the live source and grep for the key change to confirm it took effect before delivering.

## 6. Verification habit
- After spatial/visual changes, use a standalone node script to quantitatively verify at multiple screen positions (card-to-node distance, occlusion, visible ratio), or compare against a reference screenshot — more reliable than "eyeballing it".
