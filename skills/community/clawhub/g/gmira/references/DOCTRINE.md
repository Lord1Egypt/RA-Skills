# The Gmira doctrine

Every skill in this library loads this file. It is the shared law. Skills add technique on top;
none of them contradict what is here.

Sources: `impeccable.md` (design engine), `componentry.md` (56 components), `canvas-ui.md`,
`bklit-ui.md`, `chanhdai.md`, `CATALOG.md` (514 components across 7 registries), and two findings
proven by build in `proofs/`.

---

## Part 0. The one-paragraph thesis

Generic output is not a talent problem, it is a **decision-avoidance** problem. An agent that has
not decided reaches for the median, and the median rendered to HTML is the card grid, the gradient
headline, the eyebrow over every section, the centered hero with two buttons. Installing more
impressive components does not fix this. It relocates it: in 2026 the rainbow WebGL blob sits
exactly where the purple CSS gradient sat in 2021. The arsenal raises the ceiling and does nothing
to the floor. **Gmira forces the decision first, then supplies material to execute it.**

---

## Part 1. Three laws proven by build, not by reading

These came out of installing the arsenal and looking at what rendered. They are the reason this
library exists rather than a list of nice components.

### Law 1. A registry component is an engine, not a design

Its defaults are tuned to win a five-second gallery GIF, and the gallery GIF is the new generic.

Evidence: `@componentry/dither-prism-hero` given a near-black / deep-green / gold palette rendered
a rainbow smear with a blown-out white disc welded to the center. Cause: a 9-layer shader that sets
the palette at layer 2 and then **adds** prism, iridescence, and a `vec3(1.0, 0.8, 1.0)` glow at
roughly +1.84 per channel before clamp. The glow's position and intensity were hardcoded in the
uniform block **and re-set every frame**, with no prop to reach them. Full writeup:
`FINDING-01-tame-the-arsenal.md`.

Practices, mandatory in every build skill:

1. **Install then tame, in the same breath.** shadcn copies source into your repo precisely so you
   can edit it. An unedited registry component is an unfinished one.
2. **Grep for welded constants before use.** Numeric literals assigned inside `useFrame`, uniform
   `useMemo` blocks, or render loops. The specific smell: a prop exists for a thing and a hardcoded
   value elsewhere overrides it.
3. **Additive effect stacks cannot honor a dark palette.** More than two `col += ...` without
   renormalizing trends to white. Verify by comparing rendered pixels against the source hexes,
   never by trusting prop names.
4. **Use the `children` slot, never the component's own `title` props.** Those ship banned
   patterns: `dither-prism-hero`'s default headline class is
   `text-transparent bg-clip-text bg-gradient-to-b ...`, gradient text, which the craft floor bans.

### Law 2. The arsenal is broken on arrival, and repair is part of install

Measured across componentry's 56 components:

| Breakage | Count | Fix |
|---|---|---|
| `cn` imported from `@workspace/ui/lib/utils`, a leaked monorepo alias | 10 | rewrite to `@/lib/utils` |
| `cn` imported from `../lib/utils`, resolves wrong | 2 | rewrite to `@/lib/utils` |
| Undeclared runtime dep, so `shadcn add` never installs it | 10 | 7 need framer-motion, 2 gsap, 1 lucide-react |
| Over-declared dep never imported | 1 | `testimonial-marquee`, drop it |
| Tailwind keyframes referenced but never shipped | 1 | `shimmer-button`, define them |
| Remote assets hardcoded in default props | 7 | swap for local, or add to `next.config` `images.remotePatterns` |

Named broken imports: `circuit-board`, `cursor-driven-particle-typography`, `hyper-text`,
`letter-cascade`, `scroll-based-velocity`, `scroll-choreography`, `scrub-input`, `spotlight-card`,
`testimonial-marquee`, `text-repel`, `hero-geometric`, `liquid-chrome`.

Also: every animated component imports `framer-motion`, the pre-v11 name, not `motion`. Alias or
find-and-replace.

**Every build skill runs a repair pass immediately after `shadcn add`, before writing any page.**

### Law 3. An effect must earn its place at frame 0, with no input

Any effect keyed to pointer input is invisible in the state that matters most. Visitors land, read,
and leave without ever moving the mouse across the hero. A gallery GIF never shows this because the
person recording it is already dragging.

Applies to: fluid sims, `image-trail`, `text-repel`, `cursor-driven-particle-typography`,
`magnet-lines`, `eye-tracking`, spotlight cards.

Three permitted resolutions, pick one explicitly:
- **Seed it.** Inject motion on mount along a designed path.
- **Give it autonomous idle motion** that pointer input then perturbs.
- **Accept it is a reward for interaction** and design a composition already complete without it.

Two corollaries from the same build:

- **Drag-driven effects fight the DOM.** When content is real DOM, a drag is a text selection, not
  an effect gesture. Drive from `pointermove` with no button held, or set `user-select: none` and
  only on text nobody would want to copy.
- **Restrained settings make effects invisible; loud settings make them slop. The answer is
  compositional, not parametric.** Give the effect a bounded region where it runs at full strength
  (a panel, a masked band, one figure) instead of a full-bleed backdrop that must stay quiet to keep
  text legible. Full strength inside a boundary reads as intent. Half strength everywhere reads as a
  filter someone left on.

Full writeup: `FINDING-02-effects-need-an-idle-state.md`.

---

## Part 2. Decide before you build

### 2.1 Mode, per surface

Adopted from impeccable. Mode names what the visitor's success looks like **on the surface in
hand**, not on the project. A tool's landing page is Persuade even though the product is Operate.

| Mode | Visitor success | Typical surfaces |
|---|---|---|
| **Persuade** | decides and acts; design is the product | landing, campaign, pricing |
| **Operate** | completes a task | app UI, dashboard, checkout, admin, filters |
| **Read** | understands something | docs, curriculum, guides, changelog |
| **Experience** | is inside the work itself | portfolio, gallery, showcase, creative wall |

Mode sets the effect budget. **Persuade and Experience can spend; Operate and Read cannot.** A
checkout with a fluid background is a bug. Effect intensity in Operate is near zero and the budget
goes to state coverage and input latency instead.

### 2.2 The direction contract, written before any element is placed

Five blocks, 150 words total, committed to `.gmira/surfaces/<slug>.md` **and** emitted as an
HTML comment in the built markup so the finishing review can audit it promise by promise.

```
THESIS         one sentence: what this surface argues
OWN-WORLD      the material world it borrows from, named specifically
STORY          what changes between first viewport and last
FIRST VIEWPORT what is on screen before any scroll, in nouns
FORM           the structural decision: how the page is built, not how it feels
```

**Falsifiability test: if a block reads like a mood, the direction is not decided yet.** "Premium
and modern" is a mood. "A 1970s Porsche parts catalogue: monospace part numbers, hairline rules,
photographs on a neutral card, no rounded corners anywhere" is a direction.

### 2.3 Anti-default mechanics

The reason "be original" fails is that a model's own ranking is a deterministic function of its
priors. Ranking harder cannot beat the prior. Only an **external assignment** can.

1. **Externalized dice.** Draw the material world from `playbooks/worlds.md` by an outside index,
   not by picking a favorite. Assign, do not choose.
2. **Name the rut, exclude it, and exclude its opposite.** Write down what the category's default
   looks like, then exclude it. Then write down the obvious contrarian move and exclude that too.
   Predictable contrarianism is also a prior. **If someone could guess the aesthetic from the
   category alone, or from category-plus-avoidance, rework until neither answer is obvious.**
3. **Seven candidates spanning at least three material families**, then fuse the two strongest and
   judge the fusion on exactly two axes. Fewer than seven and the prior wins.
4. **The standing exit.** The safe conventional option is always available to the user and the agent
   may never recommend it or weigh it. Preserves user agency without letting agent risk aversion win.

### 2.4 The specificity test

**Could an unrelated product use this page unchanged?** If yes, nothing was decided. Applied per
section, not just per page.

---

## Part 3. The craft floor: numbers, not intentions

Each is a check on the built result. Read computed values, do not assume.

### 3.1 Type
- Body measure **65 to 75ch**. Display max **6rem**. Tracking floor **-0.04em**, and -0.02 to
  -0.03em usually reads better.
- Functional text floor **11px**. Scale ratio **1.25** (1.125 to 1.2 for Operate).
- Real copy at every breakpoint. Zero overflow, zero clipping. Balanced headings.
- Mono carries metadata only: file names, part numbers, measurements, code. **Never mono as a
  costume for "technical".**

### 3.2 Color
- Body and placeholder text **>= 4.5:1**, large text **>= 3:1**, measured.
- On colored surfaces tint secondary text from that hue or the foreground. **Never gray.**
- Committed color strategy means the accent covers **30 to 60% of the surface**, not one button.
- No gradient text. Emphasis comes from weight or size.

### 3.3 Depth and shape
- Shadows carry **an offset and a soft blur**. A zero-offset colored halo is decoration.
- **Declare elevation once**: border or shadow, not both. A 1px border under a wide soft shadow is
  the ghost card.
- Card radii **12 to 16px**. Pills are for small controls only.

### 3.4 Layout
- Spacing base **4 units**. Tight groups, generous separation, **more space above a heading than
  below it**.
- Squint test: at 10% zoom the page still has a structure.

### 3.5 Motion
- **One authored moment**, not scattered effects, and not one identical entrance on every section.
- Durations **100 to 800ms**. Exponential ease-out from an already-visible default:
  `cubic-bezier(0.16, 1, 0.3, 1)`.
- Never `transition: all`. Reduced motion is a **total kill switch**, not a slowdown.
- Material palette reaches past transform and opacity: blur, backdrop-filter, clip-path, mask,
  shadow, and on the GPU tier displacement, flow fields, feedback buffers, SDF morphs, particle
  advection.

### 3.6 States, content, copy
- Every interactive surface ships **hover, focus, disabled, loading, error, empty**. Six, always.
- Real content model. **Zero invented metrics, testimonials, logos, or client names.** Truth binds
  claims, not demonstrations: an illustrative value is fine when labeled as one.
- Controls name their action. Errors name the problem **and** the recovery.

---

## Part 4. The GPU floor (this library's original contribution)

Impeccable's own gap analysis names this as missing: it has numeric floors for type, color, layout,
and motion, and none for GPU work. These are ours.

| Check | Floor |
|---|---|
| Frame budget | 16.7ms total at 60fps. **The effect layer gets at most 8ms**, leaving headroom for layout, paint, and the app. Measure, do not estimate. |
| Pixel ratio | Cap at **1.5 for full-bleed backgrounds, 2.0 for bounded surfaces**. Never pass raw `devicePixelRatio`; a DPR-3 phone renders 9x the pixels for no visible gain. |
| Shader precision | `highp` desktop, **`mediump` on mobile**. Declare it, never rely on the default. |
| Simulation grids | Sim grid <= 128, dye or display texture <= 512 for full-bleed. Double them only inside a bounded region. |
| Context loss | A `webglcontextlost` listener is **mandatory**, with `preventDefault()` and a restore path. Without it a backgrounded tab returns to a dead black rectangle. |
| Teardown | Every effect exposes and calls an explicit `destroy()`: cancel the RAF, delete textures, framebuffers, programs, and buffers, disconnect observers, remove listeners. A route change must not leak a GPU context. Browsers cap live contexts at roughly 16; leaking hits the cap and every later canvas silently fails. |
| Offscreen | Pause the loop when the canvas leaves the viewport (IntersectionObserver) and when the tab hides (`visibilitychange`). Battery and thermals are visible to the user as a hot phone. |
| Reduced motion | `prefers-reduced-motion` freezes the effect at a **deliberately chosen still frame**. The still frame must look composed, so pick its time value, do not let it land at t=0. |
| Failure readability | **Everything the page says must remain readable and operable with the canvas removed.** Test by deleting the canvas element, not by trusting a fallback branch. |
| First frame | The effect must not delay first contentful paint. Mount after content, never block on shader compile. |
| Weight | three.js is roughly 600 KB. **Only justified when the specific component earns it.** Raw WebGL costs nothing; four of the strongest heroes in the arsenal are raw WebGL with zero dependencies. |

**Performance is a design material here, not only a constraint.** Load time, first-frame time, and
thermal behavior have visible consequences, so they are decisions, not overheads.

---

## Part 5. Visual tells no detector catches

Impeccable ships this list for prose and explicitly lacks it for design. This is the design
analogue of "uniform paragraph length". None of these are individually wrong; all of them are
signatures of assembly rather than design.

1. **Uniform section rhythm.** Every section the same vertical padding, so the page has no
   emphasis, only a queue.
2. **The three-column reflex.** Any set of things becomes three columns regardless of what the set is.
3. **One crop ratio everywhere.** Every image the same aspect, so nothing is featured.
4. **Single accent color applied everywhere,** so it stops meaning anything.
5. **Every section entering identically on scroll.** Fade-up, 0.6s, stagger 0.1, forever.
6. **Icon-plus-heading-plus-two-lines** as the answer to every group of items.
7. **Sentence-case everything, or title-case everything,** with no distinction earned by hierarchy.
8. **The full-bleed effect that must stay quiet.** Turned down so far it reads as a filter left on.
9. **Perfectly even card heights** achieved by truncating real content to fit the grid.
10. **The centered column with nothing to its left or right,** at every breakpoint, so the desktop
    layout is only the mobile layout with more air.
11. **Chrome standing in for content**: sparklines, progress rings, and soft-shadowed rounded
    rectangles where the actual data should be.
12. **Effects that all come from one registry,** so the page inherits that registry's house style
    instead of the brief's.

### The category defaults to refuse

Not bans; the brief's own words can earn any of them. Reaching for one when the axis is free means
you were not deciding.

- Same-size cards of icon + heading + text as the page structure. Nested cards are always wrong.
- The hero-metric template: big number, small label, supporting stats, accent.
- A tracked uppercase eyebrow over every section. One named kicker is a system.
- Section numbers 01 / 02 / 03 unless the sequence carries information the reader needs.
- A modal for a task needing neither interruption nor protected focus.
- Glass and blur as decoration rather than as a specific effect.
- A colored `border-left` above 1px on cards, list items, callouts, alerts.
- Light or dark picked by category rather than from the use scene.

### Components to refuse by default

The most-cloned primitives, present in a dozen registries and on every AI-assembled landing page:
`border-beam`, `shimmer-button`, `pulsating-button`, `interactive-hover-button`, `text-animate`,
`hyper-text`, `scroll-based-velocity`. Use one at most, restyled.

Also: `matrix-rain` on anything AI-adjacent, `particle-galaxy` as a generic backdrop, `liquid-blob`
(reads as 2021 Dribbble).

**Underused and worth reaching for**, because almost nobody ships them: `circuit-board`,
`split-flap-display`, `ascii-effect`, `dithered-logo`, `scrub-input`, `orbit-card-stack`,
`silk-aurora`.

---

## Part 6. Choosing components

### 6.1 The cheap stack

```
framer-motion   unlocks 29 of 56 componentry components
lenis           unlocks 2 more, both best-in-class scroll
lucide-react    icons
```

This reaches **every non-three.js component**, including all four raw-WebGL heroes (`silk-aurora`,
`webgl-liquid`, `liquid-chrome`, `closing-plasma`), because raw WebGL needs no library. Skip
`three`, `@react-three/fiber`, `drei`, `gsap`, `opentype.js` unless one specific component earns it.

Fourteen components are genuinely dependency-free and import-clean, and that set alone covers a
hero, a background, a gallery, and buttons at zero install cost: `animated-gradient`, `ascii-effect`,
`dither-gradient`, `dithered-logo`, `gradient-hero-01`, `hyper-text`, `infinite-image-field`,
`matrix-rain`, `noise-texture`, `pixel-canvas`, `pulsating-button`, `shimmer-button`, `silk-aurora`,
`split-flap-display`.

### 6.2 Canvas text is invisible

Anything that renders text to canvas is invisible to search engines, screen readers, and
`Ctrl+F`. **Never on commerce, pricing, or any page with an SEO job.** That rules out
`cursor-driven-particle-typography` and `infinite-image-field` for product surfaces regardless of
how good they look. Prefer DOM-text effects (`text-repel`, `kinetic-text-reveal`) which keep the
text real.

### 6.3 Per-vertical picks

Full tables with reasoning in `componentry.md` section 5. Headlines:

- **Car shop:** `liquid-chrome` (literal liquid metal, zero deps), `ripple-transition`,
  `scroll-tilted-grid`, `spotlight-card`, `split-flap-display` for spec figures, `noise-texture`.
  Avoid `matrix-rain`, `circuit-board`, `particle-galaxy`.
- **E-commerce:** `dither-gradient` (3.5 KB, safe on every page), `ripple-transition` on variant
  switch, `spotlight-card` (stays a real link), `testimonial-marquee` (pure CSS), `scrub-input` as a
  real filter primitive. Avoid every canvas-text component.
- **AI school:** `circuit-board` is the standout, a real node-and-edge diagram primitive with
  per-node status, used to draw the actual pipeline. Plus `silk-aurora`, `ascii-effect`,
  `github-calendar`, `mac-keyboard`, `split-flap-display`. **Avoid `matrix-rain` and
  `particle-galaxy`**: using the two most exhausted "we do AI" cliches undercuts the exact
  credibility the page is buying.
- **GTM / UGC school:** `webgl-liquid` hero, `scroll-tilted-grid` for the creative wall,
  `letter-cascade`, `sticky-scroll-cards` for the offer stack, `testimonial-marquee`, `text-repel`.
  Avoid anything heavy: page weight is revenue on paid traffic.

---

## Part 7. Method

### 7.1 Anchoring quarantine

The best idea in impeccable and it generalizes. **When you have both a deterministic checker and a
judgment pass, run judgment first, in isolation.** Otherwise the checker's output becomes the
ceiling of the judgment: the reviewer stops looking once the machine's list is satisfied.

Concretely: the taste read of a screenshot completes and is written down **before** detector output,
console logs, or lint results enter the same context. For GPU work this means judging the feel
before reading the frame-time trace.

### 7.2 Loud degradation

Any skill with an optional-but-preferred path announces when it took the lesser one, as a mandatory
first line: `WARNING DEGRADED: <reason>`. "Unavailable" never includes "inconvenient".

### 7.3 Bounded verification budget

**Two screenshot rounds, fixes batched between them.** Not a per-tweak loop. Round one collects all
findings across all viewports; round two confirms the batch. A third round means the direction was
wrong, not the details, so go back to Part 2.

### 7.4 Named failure modes beat checklists

Named failures are findable failures. Build the vocabulary before the checklist. Ours so far: the
welded constant, the gallery-GIF default, the frame-zero void, the filter left on, the assembled
page.

### 7.5 Prose

No dashes as pause anywhere the skill writes user-facing text. Compound hyphens are fine. Sachlich
tone, no performative warmth. Denylist inherited: `seamless`, `robust`, `delve`, `elevate`,
`empower`, `pivotal`, `tapestry`, `data-driven`, `in today's`, `gone are the days`,
`whether you're`, `let's dive in`, `in summary`, `in conclusion`, `moreover`, `furthermore`.

The structural tells no validator catches: the negation pivot ("It is not just X, it is Y"), triadic
auto-pilot (everything in threes), uniform paragraph rhythm, hollow confidence.

---

## Part 8. The gates

A surface ships only when all ten are green, checked on the built result.

| Gate | Check |
|---|---|
| **G1 Direction** | The 5-block contract exists in writing, was written before any element was placed, and the built page traces to it block by block |
| **G2 Refusals** | Zero category defaults and zero refused components present, unless the brief's words earned one and it is logged |
| **G3 Contrast** | Body and placeholder >= 4.5:1, large >= 3:1, measured from computed styles |
| **G4 Type** | Measure 65 to 75ch, tracking >= -0.04em, real copy at every breakpoint, zero overflow |
| **G5 Motion** | One authored moment, no identical per-section entrance, reduced motion is a total kill switch |
| **G6 States** | Hover, focus, disabled, loading, error, empty present for every interactive surface |
| **G7 Content** | Real content model, zero invented metrics, testimonials, logos, or client names |
| **G8 GPU** | Every canvas surface passes Part 4: DPR cap, precision, context loss, destroy, offscreen pause, reduced motion, readable with the canvas deleted |
| **G9 Console** | Zero console errors at 1920x1080, 1440x900, 1024x768, 834x1112, 390x844 |
| **G10 Eyes** | The screenshots were read by the agent and findings written down. Three regressions in the predecessor project were caught only this way |

Plus two mechanical preconditions that are not judgment calls:

- **G0a Repair.** Every installed component passed the Law 2 repair pass.
- **G0b Idle.** Every pointer-driven effect declares which Law 3 resolution it took.
