# PROMPTS.md — Reusable Agent Prompts

## 1. Full prototype build

Build a viral frontend prototype using Pretext and Three.js.

Requirements:
- one signature hero interaction
- one controlled text destruction mechanic
- one stable readable zone
- one ambient side/rail/tunnel/signal system
- readable at rest, dramatic on interaction
- fast enough for screen recording and sharing
- mobile simplification and reduced-motion fallback

Use Pretext for real text layout and glyph home positions.
Use Three.js only where spatial rendering is valuable.
Use Canvas 2D for contained game-like destruction if needed.
Choose one ecosystem pattern explicitly: Textura, Pinch-Type, Breaker, Dokobot playground, editorial flow, or variable typographic ASCII.
Output clean working code.

---

## 2. Hero-only mode

Build only the hero section.

Goal:
Create a typographic hero organism that starts readable, reacts to cursor movement, breaks apart under force, and reforms elegantly.

Rules:
- use Pretext for layout
- preserve readability at rest
- use one dominant visual form
- avoid decorative copy duplication
- keep code modular for later page integration

Optional pattern:
- variable typographic ASCII silhouette
- text-built mascot
- signal rails flanking the hero

---

## 3. Text destruction mode

Build a contained text-destruction scene.

Goal:
Turn a block of text into independent glyph or word bodies with home positions, velocity, rotation, spring return, and damage state.

Interaction:
- cursor blast, hold-to-burn, or moving destroyer object
- local destruction first, not full-screen chaos immediately
- pooled particles only
- graceful reconstruction or round reset

Prefer Canvas 2D unless real 3D depth materially improves the result.
Use Breaker-style bounds if the text is game-like.

---

## 4. Ambient system mode

Build a side rail / signal / tunnel ambient layer that supports a main hero without competing with it.

Requirements:
- sparse but alive
- slow flowing motion
- occasional glow or pulse
- mobile-safe density
- no exact duplication of hero copy

Use variable typographic ASCII ideas if useful.

---

## 5. DOM-free layout mode

Build a layout-driven prototype where text flows through multiple regions without relying on browser layout in the hot path.

Requirements:
- use Pretext for line measurement
- use a Textura/Yoga-style block layout approach
- support reflow when container widths or obstacles change
- keep rendering decoupled from layout logic
- show at least one obstacle-aware or multi-column layout behavior

---

## 6. Mobile text scaling mode

Build a phone-first typographic prototype where pinch gestures resize the text system instead of zooming the entire page.

Requirements:
- define a text-scale state
- clamp min/max sizes
- re-run Pretext layout on scale changes
- keep the main scene readable at all scales
- maintain a calm rest state

---

## 7. Playground mode

Build an obstacle-aware playground where a draggable object or icon causes text to reflow in real time.

Requirements:
- immediate feedback
- stable wrap logic
- clear visual obstacle region
- easy-to-edit content blocks
- use this as a proving ground before building the final art direction

---

## 8. Refactor mode

Refactor this Pretext + Three.js prototype for maintainability.

Goals:
- separate layout code from scene code
- centralize tuning values
- remove dead code
- reduce unnecessary allocations
- keep visuals unchanged unless they improve readability or performance

---

## 9. Viral polish mode

Take the existing prototype and make it more memorable without making it more chaotic.

Improve:
- silhouette clarity
- interaction payoff
- recovery timing
- hierarchy
- screen-recording appeal

Do not:
- add random effects
- animate every surface
- harm readability
- merge multiple ecosystem demos unless they fit one coherent system
