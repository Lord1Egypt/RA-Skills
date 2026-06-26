# Materials Library

What's available to you. Use what the content needs. Ignore the rest.
The best slide is often built with none of these — just CSS and a strong idea.
If external fonts or libraries fail to load, the core text and structure must still remain readable.

---

## Icons

**Lucide** — clean, consistent, ~1500 icons on a 24px grid. Covers UI actions, arrows,
data, communication, files, nature, people, shapes. Good default for structural and
functional icons. Available via CDN or as inline SVG copied from lucide.dev.
CDN: `https://unpkg.com/lucide@0.469.0/dist/umd/lucide.min.js` — load via `<script>`, then call `lucide.createIcons()`.

**Phosphor** — ~9000 icons in 6 weights (thin / light / regular / bold / fill / duotone).
Better for expressive, editorial, or illustrative use. Duotone and fill weights work well
as decorative hero elements.
CDN: `https://unpkg.com/@phosphor-icons/web@2.1.1/src/regular/style.css`

Use icons to anchor meaning, not to decorate. An icon earns its place when it makes
the content faster to understand — not when it makes the slide look less empty.

---

## Charts and Data Visualization

**Chart.js** — bar, line, doughnut, radar, scatter, bubble. Good default for most data
needs. Straightforward API, responsive by default. Style to match your palette: remove
default borders, use transparent backgrounds, match colors to your accent variables.
CDN: `https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js`

**ECharts** — richer visualization types: treemaps, sankey, sunburst, geographic maps,
parallel coordinates. Better CJK font support and more animation control than Chart.js.
Reach for it when Chart.js can't cleanly handle the visualization you need.
CDN: `https://cdnjs.cloudflare.com/ajax/libs/echarts/5.4.3/echarts.min.js`

**Pure CSS** — for simple proportional comparisons (3–6 items, no interactivity), a
hand-coded CSS bar chart is often cleaner and faster than loading a library. Animated
with `transform: scaleX()` from a `transform-origin: left` baseline.

Don't reach for a chart library just because there's a number in the content. A single
large number styled as display type is often more powerful than a chart.

---

## Diagrams

**Mermaid** — renders text-defined diagrams: flowchart, sequenceDiagram, classDiagram,
stateDiagram, erDiagram, gantt, pie, mindmap, timeline. Good when the content has a
process, decision tree, or system relationship that's fundamentally about connections.
CDN: `https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js`
Initialize with `mermaid.initialize({ startOnLoad: true, theme: 'dark' })` (or 'default' for light).

**Hand-coded SVG** — when you need pixel-perfect control over layout, positioning, or
animation that Mermaid's auto-layout can't give you. Best for simple diagrams (2–5 nodes)
where writing it by hand is faster than fighting the layout algorithm.

---

## Animation

**CSS transitions + IntersectionObserver** — the right default for scroll-snap reveals.
No library needed. Implement with a class toggle (e.g. `.reveal` → `.visible`) triggered
by IntersectionObserver on each slide. Key detail: IntersectionObserver won't fire for
elements already in the viewport on page load — always add a `setTimeout` fallback to
trigger the first slide's reveals immediately.

**GSAP** — when CSS transitions aren't enough: complex sequenced animations, precise
scroll-triggered timing, physics-based motion, coordinated multi-element choreography.
CDN: `https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js`

---

## Atmosphere (pure CSS, no library)

**Ambient blobs** — absolutely positioned elements with `border-radius: 50%`,
`filter: blur(80–120px)`, low opacity, and a slow looping `@keyframes` drift. Vary
animation duration per blob to avoid synchronized movement. Best on dark backgrounds.

**Grid lines** — `background-image` with two perpendicular `linear-gradient` layers at
a fixed `background-size`. Opacity 0.02–0.04 — felt, not seen. Signals precision and
structure.

**Noise texture** — inline SVG `feTurbulence` filter applied as a `background-image`
data URI at 2–4% opacity. Adds tactile quality to flat surfaces.

All atmosphere effects: `position: absolute; pointer-events: none` inside the slide,
with content above via `position: relative; z-index: 1`.

---

## CSS Patterns With Exactly One Correct Form

These are kept here because getting them wrong produces silent failures — the code runs
but doesn't work in all browsers, or breaks in a non-obvious way.

**Gradient text** — requires all three properties in this order:

```css
background: linear-gradient(...);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;
```

Missing `-webkit-text-fill-color: transparent` causes the gradient to be invisible on
some browsers. The `-webkit-` prefixed properties must come before the unprefixed ones.

**Scroll-snap container** — the snap behavior lives on the scroll container, not the slides:

```css
html {
  scroll-snap-type: y mandatory;
  scroll-behavior: smooth;
}
.slide {
  scroll-snap-align: start;
}
```

`scroll-snap-type` on the wrong element (e.g. `body` when `html` is the scroller) silently
does nothing on some browsers.

---

## What's Also Possible

Beyond the above — things worth knowing exist that aren't listed here:

- CSS `@property` for animating custom properties (gradients, colors)
- `backdrop-filter: blur()` for frosted glass effects on surface elements
- CSS `clip-path` for non-rectangular slide layouts and reveal animations
- `mix-blend-mode` for layered color effects between elements
- CSS `counter()` for auto-numbered elements without JavaScript
- `scroll-driven animations` (newer CSS) for effects tied directly to scroll position
- Canvas API for generative or particle-based backgrounds
- Web Animations API as a lighter alternative to GSAP for sequenced animations
- Variable fonts for expressive weight/width transitions within a single typeface
- SVG `<animate>` and `<animateTransform>` for self-contained animated diagrams
