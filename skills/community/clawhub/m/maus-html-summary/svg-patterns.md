# SVG Skeleton Patterns

Geometric base skeletons for the eight metaphor types referenced in
`SKILL.md` Stage 3. These are starting points, not finished art.

**How to use:** pick a skeleton matching your idea's metaphor type,
paste into the card, then adapt:

- Labels and text content (the most important adaptation)
- Number of boxes / nodes / steps (match the real structure)
- Colors (stay within the warm muted palette; use the page accent colors)
- Proportions if needed

**What not to change:** the basic geometry — these were drawn to render
correctly across viewport sizes. Don't randomize coordinates.

The default palette used below: `#ffcd55` (warm yellow), `#ffd6ca`
(soft coral), `#cde4ff` (light blue), `#d7f0de` (mint green), `#1f2430`
(dark ink). Pick 2 – 3 per SVG; don't use all five.

---

## 1. Layer stack

For: layered concepts, abstraction levels, stacked components,
hierarchies where higher layers depend on lower ones.

```html
<svg viewBox="0 0 240 200" width="100%" style="max-width:240px;height:auto" role="img" aria-label="Layer stack">
  <rect x="20" y="36" width="200" height="34" rx="6" fill="#ffd6ca" stroke="#1f2430" stroke-width="1.5"/>
  <text x="120" y="58" text-anchor="middle" font-family="system-ui,sans-serif" font-size="13" font-weight="600" fill="#1f2430">Layer 3 (Label)</text>
  <rect x="20" y="78" width="200" height="34" rx="6" fill="#cde4ff" stroke="#1f2430" stroke-width="1.5"/>
  <text x="120" y="100" text-anchor="middle" font-family="system-ui,sans-serif" font-size="13" font-weight="600" fill="#1f2430">Layer 2 (Label)</text>
  <rect x="20" y="120" width="200" height="34" rx="6" fill="#d7f0de" stroke="#1f2430" stroke-width="1.5"/>
  <text x="120" y="142" text-anchor="middle" font-family="system-ui,sans-serif" font-size="13" font-weight="600" fill="#1f2430">Layer 1 (Label)</text>
</svg>
```

Adapt: number of layers (2 – 5 work), label text, color order
(top-down or bottom-up depending on the concept).

---

## 2. Pipeline / conveyor belt

For: sequential processes, transformations, data/material flow, ordered
steps with arrows.

```html
<svg viewBox="0 0 320 100" width="100%" style="max-width:320px;height:auto" role="img" aria-label="Pipeline">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#1f2430"/>
    </marker>
  </defs>
  <rect x="10" y="30" width="70" height="40" rx="8" fill="#ffcd55" stroke="#1f2430" stroke-width="1.5"/>
  <text x="45" y="55" text-anchor="middle" font-family="system-ui,sans-serif" font-size="12" font-weight="600" fill="#1f2430">Step 1</text>
  <path d="M 85 50 L 105 50" stroke="#1f2430" stroke-width="2" marker-end="url(#arr)"/>
  <rect x="110" y="30" width="70" height="40" rx="8" fill="#ffd6ca" stroke="#1f2430" stroke-width="1.5"/>
  <text x="145" y="55" text-anchor="middle" font-family="system-ui,sans-serif" font-size="12" font-weight="600" fill="#1f2430">Step 2</text>
  <path d="M 185 50 L 205 50" stroke="#1f2430" stroke-width="2" marker-end="url(#arr)"/>
  <rect x="210" y="30" width="70" height="40" rx="8" fill="#d7f0de" stroke="#1f2430" stroke-width="1.5"/>
  <text x="245" y="55" text-anchor="middle" font-family="system-ui,sans-serif" font-size="12" font-weight="600" fill="#1f2430">Step 3</text>
</svg>
```

Adapt: number of stages (2 – 5; if more than 5, wrap to a second row
or use Funnel instead), step labels, vertical version if it fits the
card better. The `marker id` must be unique per page if multiple
pipelines appear — use `arr1`, `arr2`, ...

---

## 3. Cross-section

For: showing what is inside something — anatomy, internal structure,
nested concepts. Concentric circles read as "core surrounded by layers".

```html
<svg viewBox="0 0 240 220" width="100%" style="max-width:240px;height:auto" role="img" aria-label="Cross-section">
  <circle cx="120" cy="110" r="90" fill="#fffaf2" stroke="#1f2430" stroke-width="1.5"/>
  <circle cx="120" cy="110" r="60" fill="#cde4ff" stroke="#1f2430" stroke-width="1.5"/>
  <circle cx="120" cy="110" r="32" fill="#ffcd55" stroke="#1f2430" stroke-width="1.5"/>
  <text x="120" y="115" text-anchor="middle" font-family="system-ui,sans-serif" font-size="12" font-weight="700" fill="#1f2430">Core</text>
  <text x="120" y="65" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" font-weight="600" fill="#1f2430">Middle layer</text>
  <text x="120" y="30" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" font-weight="600" fill="#1f2430">Outer</text>
</svg>
```

Adapt: number of rings (2 – 4), labels, color order. For asymmetric
internals, use a single circle with internal partitioning lines
instead.

---

## 4. Before / after

For: change, transformation, improvement, before/after states.

```html
<svg viewBox="0 0 320 150" width="100%" style="max-width:320px;height:auto" role="img" aria-label="Before after">
  <defs>
    <marker id="arr-vn" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#1f2430"/>
    </marker>
  </defs>
  <text x="60" y="22" text-anchor="middle" font-family="system-ui,sans-serif" font-size="13" font-weight="700" fill="#5d6678" letter-spacing="0.05em">BEFORE</text>
  <rect x="15" y="38" width="90" height="90" rx="14" fill="#ffd6ca" stroke="#1f2430" stroke-width="1.5"/>
  <text x="60" y="88" text-anchor="middle" font-family="system-ui,sans-serif" font-size="12" font-weight="600" fill="#1f2430">State A</text>
  <path d="M 120 83 L 200 83" stroke="#1f2430" stroke-width="2.5" marker-end="url(#arr-vn)"/>
  <text x="260" y="22" text-anchor="middle" font-family="system-ui,sans-serif" font-size="13" font-weight="700" fill="#5d6678" letter-spacing="0.05em">AFTER</text>
  <rect x="215" y="38" width="90" height="90" rx="14" fill="#d7f0de" stroke="#1f2430" stroke-width="1.5"/>
  <text x="260" y="88" text-anchor="middle" font-family="system-ui,sans-serif" font-size="12" font-weight="600" fill="#1f2430">State B</text>
</svg>
```

Adapt: state labels (the boxes should say what the state IS, not just
"A" and "B"); optionally add a small caption above the arrow with the
mechanism that drove the change.

---

## 5. Node graph

For: networks, relationships, dependencies, hub-and-spoke patterns.

```html
<svg viewBox="0 0 280 200" width="100%" style="max-width:280px;height:auto" role="img" aria-label="Node graph">
  <line x1="60" y1="50" x2="140" y2="100" stroke="#1f2430" stroke-width="1.5"/>
  <line x1="220" y1="50" x2="140" y2="100" stroke="#1f2430" stroke-width="1.5"/>
  <line x1="140" y1="100" x2="60" y2="160" stroke="#1f2430" stroke-width="1.5"/>
  <line x1="140" y1="100" x2="220" y2="160" stroke="#1f2430" stroke-width="1.5"/>
  <circle cx="60" cy="50" r="22" fill="#cde4ff" stroke="#1f2430" stroke-width="1.5"/>
  <text x="60" y="55" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" font-weight="700" fill="#1f2430">A</text>
  <circle cx="220" cy="50" r="22" fill="#cde4ff" stroke="#1f2430" stroke-width="1.5"/>
  <text x="220" y="55" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" font-weight="700" fill="#1f2430">B</text>
  <circle cx="140" cy="100" r="28" fill="#ffcd55" stroke="#1f2430" stroke-width="1.5"/>
  <text x="140" y="105" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" font-weight="700" fill="#1f2430">Center</text>
  <circle cx="60" cy="160" r="22" fill="#d7f0de" stroke="#1f2430" stroke-width="1.5"/>
  <text x="60" y="165" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" font-weight="700" fill="#1f2430">C</text>
  <circle cx="220" cy="160" r="22" fill="#d7f0de" stroke="#1f2430" stroke-width="1.5"/>
  <text x="220" y="165" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" font-weight="700" fill="#1f2430">D</text>
</svg>
```

Adapt: node labels (single letters become real names — "Codex",
"Gateway", "Senox" — never leave as "A/B/C"), number of peripheral
nodes (3 – 5), edge directions (add markers if directed).

---

## 6. Funnel

For: filtering, narrowing-down, conversion, "many in → few out".

```html
<svg viewBox="0 0 240 220" width="100%" style="max-width:240px;height:auto" role="img" aria-label="Funnel">
  <polygon points="20,30 220,30 170,100 70,100" fill="#cde4ff" stroke="#1f2430" stroke-width="1.5"/>
  <polygon points="70,100 170,100 145,160 95,160" fill="#ffcd55" stroke="#1f2430" stroke-width="1.5"/>
  <polygon points="95,160 145,160 130,205 110,205" fill="#ffd6ca" stroke="#1f2430" stroke-width="1.5"/>
  <text x="120" y="65" text-anchor="middle" font-family="system-ui,sans-serif" font-size="12" font-weight="600" fill="#1f2430">Many inputs</text>
  <text x="120" y="133" text-anchor="middle" font-family="system-ui,sans-serif" font-size="12" font-weight="600" fill="#1f2430">Filter</text>
  <text x="120" y="192" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" font-weight="700" fill="#1f2430">Output</text>
</svg>
```

Adapt: stage labels (be concrete: "100 applications", "20 interviews",
"3 hires" beats generic "input/filter/output"). 2 or 4 stages work
too if you adjust the polygons.

---

## 7. Growth curve

For: growth, decay, trends over time, exponential or linear
trajectories.

```html
<svg viewBox="0 0 280 180" width="100%" style="max-width:280px;height:auto" role="img" aria-label="Growth curve">
  <line x1="40" y1="150" x2="260" y2="150" stroke="#1f2430" stroke-width="1.5"/>
  <line x1="40" y1="150" x2="40" y2="20" stroke="#1f2430" stroke-width="1.5"/>
  <path d="M 40 145 Q 130 140 180 100 T 250 30" fill="none" stroke="#ff7a59" stroke-width="3" stroke-linecap="round"/>
  <circle cx="40" cy="145" r="4" fill="#1f2430"/>
  <circle cx="140" cy="120" r="4" fill="#1f2430"/>
  <circle cx="250" cy="30" r="4" fill="#1f2430"/>
  <text x="36" y="168" text-anchor="end" font-family="system-ui,sans-serif" font-size="11" fill="#5d6678">Start</text>
  <text x="146" y="138" font-family="system-ui,sans-serif" font-size="11" fill="#5d6678">Turn</text>
  <text x="250" y="22" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" font-weight="700" fill="#1f2430">Goal</text>
  <text x="150" y="172" text-anchor="middle" font-family="system-ui,sans-serif" font-size="10" fill="#5d6678">Time -></text>
  <text x="28" y="85" text-anchor="middle" font-family="system-ui,sans-serif" font-size="10" fill="#5d6678" transform="rotate(-90 28 85)">Growth →</text>
</svg>
```

Adapt: axis labels (be concrete: "MAU" or "GB" instead of "Growth";
"Q1 -> Q4" instead of "time"), curve shape (use straight `L` segments
for linear, current `Q`/`T` curves for exponential, decay version with
descending curve).

---

## 8. Circuit / logic flow

For: logical wiring, if/then chains, switches, conditional flow.

```html
<svg viewBox="0 0 320 180" width="100%" style="max-width:320px;height:auto" role="img" aria-label="Circuit logic flow">
  <defs>
    <marker id="arr-sb" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#1f2430"/>
    </marker>
  </defs>
  <rect x="20" y="65" width="70" height="50" rx="10" fill="#ffcd55" stroke="#1f2430" stroke-width="1.5"/>
  <text x="55" y="95" text-anchor="middle" font-family="system-ui,sans-serif" font-size="12" font-weight="600" fill="#1f2430">Input</text>
  <polygon points="120,90 155,55 190,90 155,125" fill="#cde4ff" stroke="#1f2430" stroke-width="1.5"/>
  <text x="155" y="95" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" font-weight="700" fill="#1f2430">If?</text>
  <path d="M 90 90 L 118 90" stroke="#1f2430" stroke-width="2" marker-end="url(#arr-sb)"/>
  <rect x="225" y="30" width="80" height="45" rx="10" fill="#d7f0de" stroke="#1f2430" stroke-width="1.5"/>
  <text x="265" y="57" text-anchor="middle" font-family="system-ui,sans-serif" font-size="12" font-weight="600" fill="#1f2430">Yes path</text>
  <path d="M 175 75 L 225 55" stroke="#1f2430" stroke-width="2" marker-end="url(#arr-sb)"/>
  <text x="195" y="55" font-family="system-ui,sans-serif" font-size="10" fill="#5d6678">yes</text>
  <rect x="225" y="105" width="80" height="45" rx="10" fill="#ffd6ca" stroke="#1f2430" stroke-width="1.5"/>
  <text x="265" y="132" text-anchor="middle" font-family="system-ui,sans-serif" font-size="12" font-weight="600" fill="#1f2430">No path</text>
  <path d="M 175 105 L 225 125" stroke="#1f2430" stroke-width="2" marker-end="url(#arr-sb)"/>
  <text x="195" y="128" font-family="system-ui,sans-serif" font-size="10" fill="#5d6678">no</text>
</svg>
```

Adapt: replace generic labels ("Input", "Yes path") with the actual
input and outcome from the source. Chain two diamonds for multi-step
conditionals.

---

## When to use which

| Concept | Pattern |
|---|---|
| Things built on top of each other | Layer stack |
| One thing turns into another, step by step | Pipeline |
| What's hidden inside something | Cross-section |
| State changed because of X | Before / after |
| Things connected to each other | Node graph |
| Many things become few things | Funnel |
| Something grows or shrinks over time | Growth curve |
| Decision splits the flow | Circuit / logic flow |

If no row fits, the idea is probably too abstract or too small to
deserve its own card. Fold it into a neighbor.
