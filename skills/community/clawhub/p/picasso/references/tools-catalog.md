# Tools & Libraries Catalog

Consolidated reference for animation libraries, design tools, and utilities. Quick lookup when generating or recommending tools.

## Animation Libraries

### React Bits (reactbits.dev)
126 animated React components. 37.5K GitHub stars.
- **Text (23):** Split Text, Blur Text, Shiny Text, Gradient Text, Glitch Text, Scrambled Text, Count Up, etc.
- **Animations (28):** Electric Border, Glare Hover, Magnet Lines, Click Spark, Pixel Trail, Meta Balls, etc.
- **Components (36):** Magic Bento, Fluid Glass, Tilted Card, Dock, Gooey Nav, Elastic Slider, etc.
- **Backgrounds (39):** Liquid Ether, Silk, Aurora, Plasma, Hyperspeed, Iridescence, Balatro, etc.
- **Tools:** Background Studio, Shape Magic, Texture Lab

### Animate UI (animate-ui.com)
shadcn-registry-based animation components built on Motion (Framer Motion).
- Animated primitives (ported from Radix UI, Base UI, Headless UI)
- Components with baseline styles inspired by shadcn/ui
- Animated Lucide icons
- Install: follows shadcn pattern (copy source, customize)

### Cursify (cursify.ui-layouts.com)
11 React cursor animation effects:
Fairydust, Smooth Following, Canvas, Bubble, Character, Snowflake, Rainbow, Follow, Spotlight, Springy, Neural Glow.
Best for: portfolio sites, creative agencies, landing pages (not productivity tools).

### Motion (formerly Framer Motion)
React animation library with gesture support, spring physics, layout animations.
Use for: complex choreography, gesture-driven interactions, shared layout transitions.

### Torph (npm torph)
Character-level text morph animations. Dependency-free. React, Vue, Svelte, vanilla TS.

## Visual Effects

### Radiant Shaders (radiant-shaders.com)
80+ production-ready WebGL/Canvas shaders. 0 dependencies, MIT license. Copy source, integrate, ship. Similar to shadcn's approach but for visual effects.

## Layout & Interaction

### Hit Area Utilities (bazza.dev)
Tailwind classes expanding clickable areas without affecting visual layout.
Install: `npx shadcn@latest add https://bazza.dev/r/hit-area`
Classes: `hit-area-6`, `hit-area-x-4`, `hit-area-l-8`, `hit-area-debug`

### WebHaptics (npm web-haptics)
Haptic feedback for mobile web. React, Vue, Svelte, TypeScript.
Patterns: success, warning, error, light, medium, heavy, soft, rigid, selection.
```jsx
import { useWebHaptics } from "web-haptics/react";
const { trigger } = useWebHaptics();
```

### Pretext (@chenglou/pretext)
500x faster text measurement than DOM. Pure TypeScript, ~15KB.
Two-function API: `prepare()` (one-time) + `layout()` (hot path, pure arithmetic).
Universal: DOM, Canvas, SVG, WebGL, server-side. CJK, Arabic, Hebrew, Thai support.

## Design References

### Component Gallery (component.gallery)
60 interface components, 95 design systems, 2,676 examples.
Cross-reference the same component across 95+ design systems for naming conventions and patterns.

### Checklist Design (checklist.design)
56 design checklists:
- 13 page checklists (404, Login, Pricing, Sign Up, etc.)
- 24 component checklists (Button, Card, Modal, Table, Toast, etc.)
- 13 flow checklists (Adding to cart, Resetting password, etc.)
- 3 topic checklists (Responsiveness, Dark Mode, UX Copy)
- 3 brand checklists (Logo, Typography, Tone of Voice)
Also: Figma plugin for in-context checking.

## Design Tools

### Google Stitch (stitch.withgoogle.com)
AI design tool: text prompts -> high-fidelity UI designs with production code.
Features: AI canvas, voice interaction, DESIGN.md export, instant prototyping.
MCP server + SDK for coding agent integration. 350 free generations/month.

### Subframe (subframe.com)
Drag-and-drop visual editor connected to coding agents via MCP.
AI generates -> you visually refine -> clean code flows back.

### Variant (variant.com)
AI design generator with infinite scroll exploration. Enter idea, scroll for endless options.

## CSS & Font Tools
- **pyftsubset** / **glyphhanger** -- font subsetting
- **svgo** -- SVG optimization (`svgo --precision=1 --multipass`)
- **critical** (npm) / **critters** (webpack/vite) -- critical CSS extraction

## Sound & Haptics
- **soundcn** -- 700+ CC0 UI sounds
- **Kenney.nl** -- free CC0 UI sound packs
- **Freesound.org** -- CC0 filtered sounds
- **Tone.js** -- procedural runtime synthesis

## Utilities
- **facehash** -- deterministic avatar faces from any string (~3KB)
- **better-icons** -- 200K+ icons from 150+ icon sets
- **Lucide React** -- default icon library (tree-shakeable)
- **better-all** -- dependency-based parallel data fetching
