# SKILL.md — Pretext + Three.js Viral Frontend Design

## Purpose

Use this skill to build web experiences where **text is a first-class physical material**, not just DOM content.

The goal is to combine:

- **Pretext** for fast, accurate text measurement and line layout
- **Three.js** for spatial rendering, particles, cards, and scene composition
- optional **Canvas 2D** for hot-path text games and destruction systems
- optional **React Three Fiber** when a React scene architecture is genuinely useful
- optional **Yoga/Textura-style layout engines** when you need DOM-free multi-region layout

This skill is for interfaces that need to feel:

- editorial but alive
- interactive but readable
- experimental but intentional
- viral without being random

---

## What Pretext is for

Pretext is a text layout engine for the browser that lets you measure and lay out text without using DOM layout as the hot path.

Use Pretext when you need:

- deterministic multiline text layout
- per-line or per-glyph positioning
- layout-driven animation and physics
- canvas/WebGL text systems that still wrap correctly
- custom editorial, ASCII, or obstacle-aware typography systems

### Core API shapes

Use these functions depending on the goal:

- `prepare()` → fast preparation for basic text measurement
- `layout()` → get multiline layout at a given width
- `prepareWithSegments()` → prepare text while exposing segment-aware detail for richer rendering
- `layoutWithLines()` → get explicit per-line layout output
- `layoutNextLine()` → incremental/manual line walking for custom layout flows
- `walkLineRanges()` → traverse ranges for custom pipelines

### Current implementation guidance

- Use `prepare()` as the opaque fast path for simple wrapped text.
- Use `prepareWithSegments()` when your render path needs manual line ranges, grapheme-aware effects, or custom glyph bodies.
- Use `layoutWithLines()` when you want the whole paragraph resolved at once.
- Use `layoutNextLine()` for editorial engines, streaming flows, custom pagination, and obstacle-aware relayout loops.
- Preserve the rich line model instead of flattening everything immediately.
- Cache prepared results and only re-run layout when width/font/content actually changes.
- Keep `homeX/homeY` separate from live positions in all animated systems.

### Docs

- Pretext repo: https://github.com/chenglou/pretext
- Demo gallery: https://chenglou.me/pretext/

---

## What Three.js is for

Three.js should be used for:

- 3D camera composition
- particle systems
- glyph or card instancing
- lighting and depth
- background space and atmospheric scenes
- morphing between readable forms and dynamic states

### Renderer choice

Use **WebGLRenderer** by default.

Use **WebGPURenderer** only when you know you need modern node-material / TSL workflows or future-facing experiments and you accept compatibility tradeoffs.

### Important performance primitives

- `InstancedMesh` for repeated glyph quads/cards/particles
- texture atlases or canvas-texture panels instead of one mesh per letter when possible
- pooled particles, not DOM spam
- one clear frame loop, not several competing loops
- typed arrays for large mutable systems

### Docs

- Three.js docs: https://threejs.org/docs/
- WebGLRenderer: https://threejs.org/docs/pages/WebGLRenderer.html
- WebGPURenderer: https://threejs.org/docs/pages/WebGPURenderer.html
- InstancedMesh: https://threejs.org/docs/pages/InstancedMesh.html
- TSL: https://threejs.org/docs/pages/TSL.html

---

## When to use Canvas 2D instead of Three.js

Do **not** force Three.js into every problem.

Use **Canvas 2D** when you need:

- brick-breaker / arcade mechanics
- lots of glyph sprites with simple forces
- direct pixel control
- fast text destruction / reconstruction
- text fire, embers, sparks, smoke, or heat states
- low-overhead prototypes

Use **Three.js** when you need:

- camera parallax
- depth cues
- mesh lighting
- object-space transitions
- layered foreground / midground / background choreography
- 3D cards, tunnels, floating panels, or typographic sculpture

Use **hybrid DOM + Canvas/Three.js** for most production-facing viral sites.

---

## Best architecture patterns

### 1. DOM shell + WebGL hero

Best default for launch pages.

- DOM handles navigation, sections, CTAs, and accessibility
- Three.js owns the hero and maybe one interlude section
- Pretext drives typographic layout for hero overlays or transition states

### 2. DOM shell + Canvas game interlude

Best for text-destruction toys.

- DOM handles content
- Canvas 2D runs a contained game scene
- Pretext provides line/glyph home positions and collision boxes

### 3. Canvas-first editorial scene

Best for bold experiments.

- one canvas
- all text measured once with Pretext
- render loop updates positions, particles, collisions, overlays

### 4. Textura-style DOM-free layout scene

Best when text must flow across regions without DOM layout.

- Pretext handles line measurement
- Yoga-style constraints handle block layout
- render target can be Canvas, DOM overlays, or Three.js cards
- useful for magazines, dashboards, split panels, shape-aware editorial pages, and reactive obstacle layouts

### 5. R3F scene modules inside React app

Best when the product already uses React and scene state should live inside the component graph.

Use R3F when:

- the team already builds in React
- scene state should react to app state
- composition benefits from reusable components

Avoid R3F when:

- the whole site is a single static HTML demo
- the agent needs the lowest-friction standalone output
- React adds more ceremony than value

### R3F notes

- `@react-three/fiber@8` pairs with React 18
- `@react-three/fiber@9` pairs with React 19
- current releases also show active v10 alpha work

Docs:

- https://r3f.docs.pmnd.rs/getting-started/introduction
- https://r3f.docs.pmnd.rs/getting-started/installation
- https://github.com/pmndrs/react-three-fiber/releases

---

## Ecosystem patterns agents should borrow

### A. Textura pattern — DOM-free multi-block layout

Borrow this when you need **real layout**, not just hero tricks.

Core idea:

- use Pretext for text measurement
- use Yoga-style constraints for block layout
- render without relying on DOM layout in the hot path

Good for:

- magazine layouts
- dashboards with precise columns
- spatial editorial spreads
- obstacle-aware cards and pull quotes
- future “AI-native” UI systems that reflow continuously

Agent rule:

- use this pattern when the challenge is **layout orchestration**
- do not reimplement CSS flexbox poorly unless you truly need DOM-free control
- preserve a separation between block layout and glyph animation

### B. Pinch-Type pattern — mobile text pinch resizing

Borrow this when the design depends on **large expressive text on phones**.

Core idea:

- intercept pinch behavior
- resize actual text metrics instead of browser page zoom
- re-run Pretext layout at the new font size
- keep copy crisp and readable instead of shrinking the whole scene

Good for:

- mobile hero wordmarks
- kiosk/editorial text pages
- reading-centric prototypes
- phone-first experimental microsites

Agent rule:

- do not rely on browser zoom for typographic experiences
- implement a controlled text-scale state and re-layout pipeline
- always clamp min/max sizes and preserve readability

### C. Breaker pattern — text as bricks

Borrow this when you need a **playable destruction mechanic**.

Core idea:

- words or glyph clusters become bricks
- Pretext provides exact bounds
- ball/projectile impacts break text apart
- particles and letters inherit force from the impact point

Good for:

- mini-games
- hero interludes
- reveal transitions
- promotional toys

Agent rule:

- keep the game contained
- destruction should recover or reset cleanly
- prefer Canvas 2D unless real depth is materially important

### D. Dokobot pattern — instant obstacle-aware relayout playground

Borrow this when you need to **prototype interaction rules quickly**.

Core idea:

- drag a blocking object or icon
- re-run layout immediately
- watch text wrap around moving constraints
- use it as a sandbox before building the final art direction

Good for:

- debugging line logic
- experimenting with collision regions
- building custom pull-quote systems
- testing text/icon swaps

Agent rule:

- make a fast playground first if layout complexity is unclear
- lock in layout rules before spending time on polish

### E. Variable Typographic ASCII pattern

Borrow this when you need **ambient systems** that feel alive but still typographic.

Core idea:

- sample a field or image
- choose characters based on brightness and measured width
- preserve shape in proportional type, not just monospace
- use it for rails, signals, masks, side panels, and decorative avatars

Good for:

- side rails
- terminal / signal panels
- ambient HUD systems
- mascots or symbols built from text primitives

Agent rule:

- keep ambient ASCII secondary to the main hero
- prefer sparse, legible, slow-moving systems over noisy spam

### F. Editorial / magazine-style flow around shapes

Borrow this when the experience should feel **useful and premium**, not just chaotic.

Core idea:

- text flows through multiple columns
- text avoids obstacles or shapes
- pagination or line-walking remains cheap
- 3D objects or masks influence layout without destroying readability

Good for:

- article pages
- campaign microsites
- creative docs
- product storytelling

Agent rule:

- use this pattern to add credibility and usefulness
- combine one experimental hero with one disciplined editorial section

---

## Modern high-value use cases

### 1. Typographic hero organism

A large wordmark or symbol made of glyphs/particles that:

- holds a readable resting state
- reacts to cursor proximity
- breaks under force
- reforms cleanly

### 2. Text-as-physics material

Every glyph becomes a body with:

- home position
- velocity
- rotation
- spring force
- collision response
- burn / damage / dissolve state

### 3. Variable typographic ASCII systems

Use Pretext to precisely lay out monospace or variable-width ASCII compositions, then animate opacity, depth, spacing, or replacement maps.

### 4. Shape-aware editorial layouts

Text flows around masks, cards, sprites, or 3D object projections without DOM measurement bottlenecks.

### 5. Breakout / arcade text systems

Words or glyphs become exact collision objects that can shatter, slide, ignite, and return.

### 6. Mobile text-resize experiences

Large hero text or reading views can resize responsively via intentional pinch handling, not browser zooming.

---

## Clear execution flows for agents

### Flow A — build a viral hero

1. Choose the calm readable form.
2. Measure text with Pretext.
3. Create glyph bodies or particle anchors.
4. Define one local interaction force.
5. Add spring recovery.
6. Add one stronger disruption mode.
7. Tune idle readability before tuning chaos.

### Flow B — build a breaker/game scene

1. Use Pretext to measure words or glyph groups.
2. Convert blocks into collision units.
3. Implement the ball/attacker logic.
4. Spawn particles only on impact.
5. Reset/reform after each run.
6. Keep it bounded and shareable.

### Flow C — build a DOM-free layout section

1. Use Pretext to prepare text.
2. Use Yoga/Textura-style constraints for block positions.
3. Materialize lines into regions.
4. Optionally render regions as Three.js cards or Canvas panels.
5. Reflow only on width/content/obstacle changes.

### Flow D — build a mobile-safe expressive text system

1. Define text scale state.
2. Clamp scale bounds.
3. Re-run Pretext layout on scale changes.
4. Keep visual effects lighter than desktop.
5. Do not let hero decoration block reading.

---

## Performance rules

- measure text once, animate many times
- never do DOM reads in the hot path if the point of the system is DOM-free text
- pool particles and effect sprites
- batch repeated geometry with `InstancedMesh`
- use Canvas 2D for dense collision-heavy glyph systems
- use WebGL for depth, staging, and atmosphere
- tune mobile density separately
- pause or reduce hidden/offscreen work

---

## Design rules

- text must be readable in a calm state
- use one dominant interaction, not five competing ones
- ambient systems should support the hero, not duplicate it
- premium motion is about recovery timing and hierarchy, not just force
- experimental sections need one stable counterweight
- do not let technical cleverness erase editorial clarity

---

## Common mistakes

- treating Pretext as a buzzword instead of the actual layout engine
- using Three.js for everything, including problems Canvas 2D handles better
- making every glyph an individual mesh when instancing or sprites would do
- duplicating hero copy everywhere as decoration
- making the entire page chaotic instead of containing disruption locally
- forgetting a readable idle state
- ignoring mobile density and gesture behavior

---

## Resource set agents should inspect first

### Core

- Pretext: https://github.com/chenglou/pretext
- Pretext demos: https://chenglou.me/pretext/
- Three.js docs: https://threejs.org/docs/
- Yoga: https://github.com/facebook/yoga

### Ecosystem references

- Textura repo: https://github.com/razroo/textura
- Textura demo: https://razroo.github.io/textura/
- Pinch-Type repo (inspect if available): https://github.com/lucascrespo23/pinch-type
- Dokobot demo repo: https://github.com/dokobot/pretext-demo
- Breaker demo variant: https://pretext-breaker.thedevbelowstairs.com
- Variable Typographic ASCII: https://chenglou.me/pretext/variable-typographic-ascii/
- Pagination demo reference: https://pretext-stuff.solarise.dev/pagination.html

---

## Preferred deliverables

A good agent using this skill should ship:

- a standalone HTML prototype, or
- a Vite + TypeScript prototype, or
- a focused React/R3F prototype when React state sharing is actually useful

The result should be:

- readable at rest
- dramatic under interaction
- performant enough for short screen recordings
- modular enough for another agent to extend quickly
