# PinePaper Studio — AI Agent Skills Reference

> **What is PinePaper?** A professional web app for creating animated text, graphics, diagrams, and data visualizations on an infinite canvas. Powered by Paper.js vector math — everything is resolution-independent and exportable.
>
> **How AI agents use it:** Via MCP tools (`@pinepaper.studio/mcp-server`) or the Agent Mode JS API (`window.PinePaperAgent`).

---

## Table of Contents

- [Item Creation](#item-creation)
- [Animation](#animation)
- [Relations (Inter-Item Behaviors)](#relations)
- [Keyframe Animation](#keyframe-animation)
- [Text & Typography](#text--typography)
- [Diagrams & Flowcharts](#diagrams--flowcharts)
- [Maps & Geospatial](#maps--geospatial)
- [Masking & Reveal Effects](#masking--reveal-effects)
- [Visual Effects](#visual-effects)
- [Image Filters](#image-filters)
- [Rigging & Skeletal Animation](#rigging--skeletal-animation)
- [Blending & Compositing](#blending--compositing)
- [3D Projection](#3d-projection)
- [Background Generators](#background-generators)
- [Camera Control](#camera-control)
- [Export Formats](#export-formats)
- [Canvas & View Management](#canvas--view-management)
- [Selection & Queries](#selection--queries)
- [History](#history)
- [Agent Mode Quick Start](#agent-mode-quick-start)
- [MCP Tool Reference](#mcp-tool-reference)

---

## Item Creation

Create items with `app.create(type, params)`. All items are vector-based and infinitely scalable.

### Item Types

| Type | Key Parameters |
|------|---------------|
| `text` | `content`, `fontSize`, `fontFamily`, `fontWeight`, `color`, `x`, `y` |
| `circle` | `radius`, `fillColor`, `strokeColor`, `x`, `y` |
| `rectangle` | `width`, `height`, `fillColor`, `cornerRadius`, `x`, `y` |
| `ellipse` | `radiusX`, `radiusY`, `fillColor`, `x`, `y` |
| `triangle` | `radius`, `fillColor`, `x`, `y` |
| `star` | `radius`, `points`, `innerRadius`, `fillColor`, `x`, `y` |
| `polygon` | `radius`, `sides`, `fillColor`, `x`, `y` |
| `line` | `from`, `to`, `strokeColor`, `strokeWidth` |
| `path` | `segments`, `strokeColor`, `closed` |
| `arc` | `from`, `through`, `to`, `strokeColor` |

### Common Parameters (All Items)

```
x, y              — Position
fillColor         — Fill (hex, rgba, or gradient object)
strokeColor       — Stroke color
strokeWidth       — Stroke width
opacity           — 0-1
rotation          — Degrees
scale / scaleX/Y  — Uniform or axis scale
shadowColor       — Shadow color
shadowBlur        — Shadow blur radius
shadowOffset      — [dx, dy]
blendMode         — CSS blend mode string
label             — String or { content, position, fontSize, color }
```

### Gradient Colors

```javascript
fillColor: {
  type: 'linear',   // or 'radial'
  stops: [
    { color: '#ff0000', offset: 0 },
    { color: '#0000ff', offset: 1 }
  ],
  origin: [100, 100],
  destination: [500, 500]
}
```

### Batch Operations

```javascript
app.batchCreate([
  { type: 'text', params: { content: 'Hello', x: 200, y: 200 } },
  { type: 'circle', params: { radius: 50, x: 400, y: 300 } }
]);
```

---

## Animation

### Simple Animations

Apply via `app.animate(item, { animationType, animationSpeed })` or inline during creation.

| Type | Effect | Key Params |
|------|--------|-----------|
| `pulse` | Scale breathing | `speed`, `intensity` |
| `rotate` | Continuous spin | `speed` |
| `bounce` | Vertical bounce | `speed`, `intensity` |
| `fade` | Opacity pulse | `speed`, `intensity` |
| `wobble` | Side-to-side rock | `speed`, `intensity` |
| `shake` | Rapid jitter | `speed`, `intensity` |
| `swing` | Pendulum swing | `speed`, `intensity` |
| `jelly` | Elastic squash/stretch | `speed`, `intensity` |
| `typewriter` | Character-by-character reveal | `speed` |

### Inline Animation

```javascript
app.create('text', {
  content: 'Hello World',
  x: 400, y: 300,
  animationType: 'bounce',
  animationSpeed: 1.2,
  animationIntensity: 0.15
});
```

---

## Relations

Relations define persistent inter-item behaviors. Add with `app.addRelation(sourceId, targetId, type, params)`.

### Motion Relations

| Relation | Description | Key Params |
|----------|-------------|-----------|
| `orbits` | Circular motion around target | `radius`, `speed`, `direction`, `phase` |
| `follows` | Move toward target | `offset`, `smoothing`, `delay` |
| `attached_to` | Move with target | `offset`, `inherit_rotation` |
| `maintains_distance` | Stay fixed distance | `distance`, `strength` |
| `points_at` | Rotate to face target | `offset_angle`, `smoothing` |
| `mirrors` | Mirror position | `axis`, `center` |
| `parallax` | Depth-based movement | `depth`, `origin` |
| `bounds_to` | Stay within bounds | `padding`, `bounce` |
| `spring_follow` | Physics spring motion | `stiffness`, `damping`, `mass`, `maxDisplacement` |

### Animation Relations

| Relation | Description | Key Params |
|----------|-------------|-----------|
| `grows_from` | Scale in from zero | `origin`, `duration`, `delay`, `easing` |
| `staggered_with` | Staggered effect | `index`, `stagger`, `effect` |
| `indicates` | Highlight pulse | `scale`, `color`, `duration`, `repeat` |
| `circumscribes` | Draw shape around target | `shape`, `color`, `strokeWidth`, `fadeOut` |
| `wave_through` | Wave distortion | `amplitude`, `frequency`, `direction` |
| `morphs_to` | Shape morph | `duration`, `easing`, `morphColor`, `morphSize` |

### Camera Relations

| Relation | Description | Key Params |
|----------|-------------|-----------|
| `camera_follows` | View tracks item | `smoothing`, `offset`, `zoom`, `deadzone` |
| `camera_animates` | Keyframe camera | `keyframes`, `duration`, `loop` |

### Procedural Relations

| Relation | Description | Key Params |
|----------|-------------|-----------|
| `wiggle` | Noise-driven motion | `property`, `frequency`, `amplitude`, `seed` |
| `driven_by` | Property linking | `sourceProperty`, `targetProperty`, `multiplier` |
| `time_expression` | Math-based motion | `property`, `expression`, `baseValue` |

### Character Relations

| Relation | Description | Key Params |
|----------|-------------|-----------|
| `part_of` | Semantic child | `role` (e.g., `eye_left`, `mouth`) |
| `expresses` | Facial expression | `expression`, `interval`, `duration` |

### Convenience Methods

```javascript
app.addRelation(sourceId, targetId, type, params);
app.removeRelation(sourceId, targetId, type);
app.replaceRelation(sourceId, targetId, type, params);
app.getRelations(itemId);
app.hasRelation(sourceId, targetId, type);
app.addParts(parentId, { eye_left: id1, eye_right: id2 });
```

### Time-Scoped Relations

Any relation supports `startTime`, `endTime`, and `autoRemove` to limit when it's active during timeline playback.

---

## Keyframe Animation

Full timeline-based animation with per-property easing, spatial paths, and morphing.

```javascript
app.create('circle', {
  radius: 40, x: 100, y: 300,
  animationType: 'keyframe',
  keyframes: [
    { time: 0, properties: { x: 100, opacity: 0 }, easing: 'easeOut' },
    { time: 1, properties: { x: 500, opacity: 1 } },
    { time: 2, properties: { x: 500, y: 100, scale: 2 }, easing: 'bounce' }
  ]
});
```

### Animatable Properties

`x`, `y`, `position`, `scale`, `scaleX`, `scaleY`, `rotation`, `opacity`, `fillColor`, `strokeColor`, `fontSize`, `strokeWidth`, `shadowBlur`, `shadowOffsetX`, `shadowOffsetY`, `segments` (path morphing), `trimStart`, `trimEnd`, `trimOffset`

### Easing Functions

`linear`, `easeIn`, `easeOut`, `easeInOut`, `easeInCubic`, `easeOutCubic`, `easeInOutCubic`, `bounce`, `elastic`, or custom cubic bezier `[x1, y1, x2, y2]`

### Per-Property Easing

```javascript
{ time: 1, properties: { x: 500, y: 100 }, propertyEasings: { x: 'bounce', y: 'easeOut' } }
```

### Spatial Motion Paths

```javascript
{ time: 0, properties: { x: 100, y: 300 }, spatialHandles: { out: [50, -100] } },
{ time: 1, properties: { x: 500, y: 300 }, spatialHandles: { in: [-50, -100] } }
```

### Trim Paths (Line Draw Effect)

```javascript
app.create('path', {
  segments: [[100, 300], [700, 300]],
  strokeColor: '#3b82f6',
  animationType: 'keyframe',
  keyframes: [
    { time: 0, properties: { trimEnd: 0 } },
    { time: 2, properties: { trimEnd: 1 }, easing: 'easeOut' }
  ]
});
```

### Timeline Playback

```javascript
app.playKeyframeTimeline(duration, loop);
app.pauseKeyframeTimeline();
app.stopKeyframeTimeline();
app.seekKeyframeTimeline(time);
```

### Animation Presets Library

Import from `js/templates/_shared/animations.js`:

**Reveal:** `fadeInUp`, `fadeInDown`, `fadeInLeft`, `fadeInRight`, `fadeIn`
**Scale:** `popIn`, `explosivePop`, `scalePulse`, `breathe`
**Physics:** `gravityDrop`, `rubberBand`, `swing`, `elasticSnap`
**Paths:** `spiralIn`, `sineFloat`, `figureEight`, `circularOrbit`
**Glitch:** `glitchFlicker`, `motionBlurSnap`, `cyberScan`
**Exit:** `zoomOut`, `fadeOutDown`, `hingeDrop`, `shrinkAway`

---

## Text & Typography

### Letter Collage

Break text into individually styled/animated letters:

```javascript
const collage = app.letterCollage.create('HELLO', {
  style: 'tile',        // tile, magazine, paperCut, fold, gradient
  palette: 'neon',       // wordle, scrabble, candy, neon, rainbow, pastel, etc.
  fontSize: 48,
  x: 200, y: 150
});
```

**Tile Palettes:** `wordle`, `scrabble`, `candy`, `neon`, `rainbow`, `pastel`, `cotton`, `earth`, `ocean`, `forest`, `sunset`, `corporate`, `minimal`, `monochrome`, `christmas`, `halloween`, `valentines`, `magazine`, `ransom`, `newspaper`

**Gradient Palettes:** `rainbow`, `sunset`, `fire`, `gold`, `rose`, `ocean`, `ice`, `forest`, `midnight`, `cyberpunk`, `neonGlow`, `chrome`

### Staggered Letter Animation

```javascript
app.letterCollage.applyStaggeredAnimation(collageId, {
  effect: 'fadeSlideUp',   // fadeSlideDown, popIn, typewriter, wave
  staggerDelay: 0.1,
  duration: 0.5,
  sequence: 'linear'       // reverse, random, center, fibonacci, wave
});
```

### Cursive Handwriting

```javascript
app.createCursiveText('Hello World', {
  x: 200, y: 300, scale: 2,
  strokeColor: '#f59e0b', strokeWidth: 3,
  animate: true, duration: 3
});
```

### Font Studio

Create custom fonts from drawn glyphs:

```javascript
app.fontStudio.createGlyph(char, paperPath);
app.fontStudio.downloadFont('otf');
app.fontStudio.loadIntoDocument();
```

---

## Diagrams & Flowcharts

### Create Diagram Shapes

```javascript
app.diagramSystem.createShape('process', { position: new Point(x, y), label: 'Step 1' });
app.diagramSystem.createShape('decision', { position: new Point(x, y), label: 'Yes/No?' });
```

**Shape Types:** `process`, `decision`, `terminal`, `data`, `document`, `database`, `cloud`, `server`, `uml-class`, `uml-usecase`

**Comment Shapes:** `speech-bubble`, `speech-bubble-square`, `thought-bubble`, `comment-box`, `speech-bubble-pointed`, `double-bubble`, `quote-bubble`, `callout-box`

### Connect & Layout

```javascript
app.diagramSystem.connect(shape1, shape2);
await app.diagramSystem.applyLayout(null, 'hierarchical', { direction: 'TB' });
```

**Layout Algorithms:** `hierarchical`, `force-directed`, `tree`, `radial`, `grid`

### Mermaid Import/Export

```javascript
// Import Mermaid syntax
const result = app.importMermaid(`
  graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[End]
`);

// Export current diagram as Mermaid
const mermaid = app.exportMermaid({ direction: 'LR' });
```

### Arrow System

```javascript
app.arrowSystem.createArrow([point1, point2], {
  lineColor: '#333', lineWidth: 2,
  headStyle: 'stealth'   // classic, stealth, sharp, open, none
});
```

---

## Maps & Geospatial

### Load a Map

```javascript
const map = await app.mapSystem.loadMap('world', {
  projection: 'naturalEarth',
  quality: 'standard',
  interactive: true,
  showOcean: true
});
```

**Available Maps:** `world`, `worldHighRes`, `usa`, `usaCounties`, `canada`, `india`, `europe`

**Projections:** `naturalEarth`, `mercator`, `robinson`, `orthographic`, `equirectangular`, `albers`, `albersUsa`, `conicEqualArea`, `winkelTripel`

### Choropleth & Data Visualization

```javascript
app.mapSystem.applyDataColors(
  { 'USA': 90, 'CAN': 75, 'MEX': 60 },
  { colorScale: ['#f7fbff', '#08519c'], legend: true, legendTitle: 'Score' }
);
```

### Region Control

```javascript
app.mapSystem.highlightRegions(['USA', 'CAN'], { fill: '#ef4444' });
app.mapSystem.animateReveal('all', { duration: 1, stagger: 0.05, effect: 'fadeIn' });
```

### Markers & Labels

```javascript
app.mapSystem.addMarker(-122.4, 37.8, { shape: 'pin', label: 'San Francisco' });
app.mapSystem.addRegionLabel('USA', { content: 'United States', fontSize: 14 });
```

### Region Animation

```javascript
app.animateMapWave({
  duration: 10, loop: true,
  colors: ['#ef4444', '#fbbf24', '#22c55e', '#3b82f6'],
  waveDirection: 'horizontal'
});
```

### Import/Export

```javascript
app.mapSystem.exportSVG();
app.exportMapGeoJSON({ includeStyles: true });
app.exportMapRegionDataCSV();
await app.importCustomMap(geoJson);
```

---

## Masking & Reveal Effects

### Static Masks

```javascript
app.applyMask(item, 'circle', { radius: 100 });
app.applyMask(item, 'star', { points: 5, radius: 80 });
```

**Mask Types:** `rectangle`, `circle`, `ellipse`, `star`, `triangle`, `hexagon`, `heart`, `rounded`, `custom`

**Mask Modes:** `clip` (show inside), `subtract` (show outside), `intersect` (overlap only)

### Animated Mask Reveals

```javascript
app.applyAnimatedMask(item, 'wipeLeft', { duration: 0.8 });
```

**Preset Animations:** `wipeLeft`, `wipeRight`, `wipeUp`, `wipeDown`, `iris`, `irisOut`, `star`, `heart`, `curtainHorizontal`, `curtainVertical`, `cinematic`, `diagonalWipe`, `revealUp`, `revealDown`

### Mask Stacking

```javascript
app.maskingSystem.addMask(item, 'circle', { mode: 'clip' });
app.maskingSystem.addMask(item, 'rectangle', { mode: 'subtract' });
```

---

## Visual Effects

Apply particle/FX effects to items:

```javascript
app.applyEffect(item, 'sparkle', { color: '#ffd700', speed: 2 });
app.applyEffect(item, 'confetti', { colors: ['#ff0', '#f0f', '#0ff'], count: 50 });
```

**Effect Types:**

| Effect | Key Params |
|--------|-----------|
| `sparkle` | `color`, `speed`, `size` |
| `blast` | `color`, `radius`, `count`, `interval` |
| `fire` | `color`, `size`, `turbulence` |
| `smoke` | `color`, `size`, `drift` |
| `rain` | `color`, `count`, `speed`, `angle` |
| `snow` | `color`, `count`, `speed`, `spread` |
| `confetti` | `colors[]`, `count`, `gravity` |
| `ripple` | `color`, `maxRadius`, `ringCount` |
| `glow` | `color`, `speed`, `intensity` |
| `electric` | `color`, `boltCount`, `length` |

---

## Image Filters

GPU-accelerated filters for raster images:

```javascript
await app.applyImageFilter(raster, 'blur', { radius: 5 });

// Chain multiple filters
await app.applyImageFilterChain(raster, [
  { name: 'brightness', params: { value: 20 } },
  { name: 'contrast', params: { value: 15 } },
  { name: 'vignette', params: { intensity: 0.5 } }
]);
```

**Filters:** `grayscale`, `sepia`, `brightness`, `contrast`, `saturation`, `invert`, `posterize`, `hsl`, `colorTint`, `vignette`, `edgeDetect`, `blur`

### Cutout Style Presets

```javascript
await app.applyCutoutStyle(item, 'sticker');
```

**Presets:** `papercut`, `postcard`, `sticker`, `poster`, `monochromeCut`, `edgeSketch`, `warmGlow`, `coolTone`

---

## Rigging & Skeletal Animation

### Create a Skeleton

```javascript
const skeletonId = app.riggingSystem.createSkeleton('character', { x: 400, y: 500 });
const spine = app.riggingSystem.addBone(skeletonId, { name: 'spine', length: 100, angle: -90 });
const head = app.riggingSystem.addBone(skeletonId, { name: 'head', length: 40, angle: -90, parentBoneId: spine });
```

### Rig Presets

Apply a full preset skeleton in one call:

```javascript
const preset = getRigPreset('humanoid');
const { boneMap, chainIds } = applyRigPreset(app.riggingSystem, skeletonId, preset);
```

**Presets:** `humanoid` (20 bones), `quadruped` (13), `spider` (19), `bird` (15), `fish` (14), `hand` (17), `centaur` (29), `simple_arm` (3), `snake` (10), `chain` (5)

### IK Solvers

```javascript
app.riggingSystem.createIKChain(skeletonId, {
  name: 'left_arm', boneIds: [upperArm, lowerArm],
  solverType: 'two_bone'   // 'fabrik', 'two_bone', 'ccd'
});
```

### Poses & Shape Keys

```javascript
// Save/load poses
const poseId = app.riggingSystem.savePose(skeletonId, 'wave');
app.riggingSystem.loadPose(skeletonId, poseId);
app.riggingSystem.interpolatePoses(poseA, poseB, 0.5);

// Shape keys (blend shapes)
const blinkKey = app.riggingSystem.saveShapeKey(skeletonId, 'blink');
app.riggingSystem.loadShapeKey(skeletonId, blinkKey, 0.8);  // weight 0-1
```

### Expressions

Built-in facial expressions: `blink`, `smile`, `frown`, `surprise`, `wink`, `talk`

```javascript
app.addRelation(faceId, null, 'expresses', { expression: 'blink', interval: 3 });
```

### Path Skinning (2D LBS)

```javascript
app.riggingSystem.skinPath(skeletonId, itemId, { maxInfluences: 2 });
```

---

## Blending & Compositing

```javascript
app.blendingSystem.applyPreset(itemId, 'neon');
app.blendingSystem.transitionBlendMode(itemId, 'screen', { duration: 0.5 });
app.blendingSystem.setGroupBlendMode(groupId, 'multiply', { cascadeOpacity: true });
```

**Presets:** `ghost`, `neon`, `shadow`, `glow`, `xray`, `dreamy`, `vintage`

**Blend Modes:** `normal`, `multiply`, `screen`, `overlay`, `darken`, `lighten`, `color-dodge`, `color-burn`, `hard-light`, `soft-light`, `difference`, `exclusion`, `hue`, `saturation`, `color`, `luminosity`

### Interactive Blending

```javascript
app.blendingSystem.addInteractiveBlend(itemId, {
  event: 'hover',
  modes: ['normal', 'screen'],
  opacities: [1.0, 0.8]
});
```

---

## 3D Projection

Render 3D primitives onto the 2D canvas:

```javascript
app.createObject3D('cube', { size: 1.5, color: '#3b82f6', rotationY: 45 });
app.createObject3D('sphere', { radius: 1, color: '#ef4444' });
app.createGlossySphere({ x: 400, y: 300, radius: 60, color: '#F97316' });

app.setProjection3D('perspective', { fov: 60 });
app.setCamera3D({ position: { x: 3, y: 2, z: 5 }, target: { x: 0, y: 0, z: 0 } });
```

**Primitives:** `cube`, `sphere`, `cylinder`, `torus`, `cone`

**Projections:** `perspective`, `orthographic`, `isometric`, `cabinet`, `cavalier`

---

## Background Generators

Procedural animated backgrounds:

```javascript
app.executeGenerator('drawBokeh', { circleCount: 30, animated: true });
app.executeGenerator('drawConstellation', { animated: true });
app.executeGenerator('drawWaves', { waveCount: 8, fill: true, animated: true });
```

**Generators:**

| Name | Description |
|------|------------|
| `drawBokeh` | Depth-of-field circles |
| `drawGradientMesh` | Multi-color gradient blobs |
| `drawOrganicFlow` | Aurora/silk flowing layers |
| `drawWaves` | Flowing wave lines |
| `drawStarfield` | Animated starfield |
| `drawNeonGrid` | Glowing neon grid |
| `drawCircuit` | Circuit board with pulses |
| `drawConstellation` | Connected star points |
| `drawGrid` | Customizable animated grid |
| `drawSunburst` | Radiating rays |
| `drawFlowField` | Directional flow particles |
| `drawNoiseTexture` | Perlin noise texture |
| `drawKaleidoscope` | Kaleidoscope pattern |
| `drawTessellation` | Geometric tiling |
| `drawSunsetScene` | Animated sunset |
| `drawCosmosSpace` | Space scene |
| `drawFireflies` | Floating fireflies |
| `drawFallingPetals` | Falling petals |
| `drawGeometricAbstract` | Overlapping shapes |
| `drawMetaballs` | Organic blobs |
| `drawGoldenSpiral` | Golden ratio spiral |
| `drawPerspectiveGrid` | 3D perspective grid |

---

## Camera Control

```javascript
app.camera.zoomIn(2, 0.5);           // Zoom 2x over 0.5s
app.camera.panTo(200, 200, 0.5);     // Pan to point
app.camera.moveTo(200, 200, 2, 0.5); // Pan + zoom
app.camera.reset(0.5);               // Reset view

// Keyframe camera animation
app.addRelation('camera', null, 'camera_animates', {
  duration: 6, loop: true,
  keyframes: [
    { time: 0, zoom: 1, center: [400, 300] },
    { time: 3, zoom: 2, center: [600, 300], easing: 'easeInOut' },
    { time: 6, zoom: 1, center: [400, 300] }
  ]
});
```

---

## Export Formats

| Format | Method | Notes |
|--------|--------|-------|
| **WebM** | Export UI | VP9, best for animations |
| **MP4** | Export UI | H.264 via WebCodecs (Chrome 94+) |
| **GIF** | Export UI | Via gif.js Web Workers |
| **Animated SVG** | `app.exportAnimatedSVG()` | SMIL or CSS animations |
| **PNG** | Export UI | Up to 600 DPI |
| **PDF** | `app.exportPDF({ dpi })` | 300/600 DPI, bleed, trim marks |
| **Lottie** | `app.exportLottie({ fps, duration })` | JSON for any Lottie player |
| **GeoJSON** | `app.exportMapGeoJSON()` | Map data export |
| **Mermaid** | `app.exportMermaid()` | Diagram text export |

---

## Canvas & View Management

### Canvas Presets

```javascript
app.setCanvasSize('instagram-post');    // 1080x1080
app.setCanvasSize('youtube-thumbnail'); // 1280x720
app.setCanvasSize('tiktok');            // 1080x1920
app.setCanvasSize({ width: 1920, height: 1080 }); // Custom
```

**Presets:** `youtube-thumbnail`, `instagram-post`, `instagram-story`, `tiktok`, `a4-portrait`, `letter-portrait`, and more.

### View Control

```javascript
app.getCanvasSize();  // { width, height, preset }
app.expandCanvasToIncludeContent(20);  // Fit to content + padding
```

---

## Selection & Queries

```javascript
app.select(item);
app.deselect();
app.selectAll();
app.deselectAll();
app.getSelection();

// Registry
app.itemRegistry.getAll();
app.itemRegistry.getByType('text');
app.itemRegistry.getItem(itemId);

// Relation queries
app.hasRelation(sourceId, targetId, type);
app.queryNotRelation(type);        // Items without relation
app.queryIsolatedItems();          // Items with no relations
app.queryCompound([...conditions]);
app.queryRelationChain([...types]);
```

---

## History

```javascript
app.undo();
app.redo();
app.getHistoryState();  // { canUndo, canRedo, undoCount, redoCount }
app.clearCanvas();
```

---

## Agent Mode Quick Start

Activate via URL `?agent=1` or `?mode=agent`:

```javascript
const agent = window.PinePaperAgent;
await agent.configure({ mode: 'agent' });
await agent.waitForReady();

// Create content
const text = app.create('text', { content: 'Hello', x: 400, y: 300, fontSize: 48 });
app.animate(text, { animationType: 'pulse' });

// Export
const result = await agent.quickExport();

// Reset for new canvas
agent.reset({ canvas: 'tiktok' });
```

### Smart Export

```javascript
const rec = agent.getExportRecommendation();
// { format: 'webm', reason: 'Has animations, WebM gives best quality' }
```

---

## MCP Tool Reference

The MCP server (`@pinepaper.studio/mcp-server`) exposes these tools:

### Item Tools
- `pinepaper_create_item` — Create any item type
- `pinepaper_modify_item` — Modify item properties
- `pinepaper_batch_create` — Create multiple items

### Animation Tools
- `pinepaper_animate` — Apply simple animation
- `pinepaper_keyframe_animate` — Apply keyframe animation

### Relation Tools
- `pinepaper_add_relation` — Add relation between items
- `pinepaper_remove_relation` — Remove relation

### Diagram Tools
- `pinepaper_create_diagram_shape` — Create flowchart shape
- `pinepaper_connect` — Connect shapes
- `pinepaper_auto_layout` — Apply layout algorithm

### Map Tools
- `pinepaper_load_map` — Load geographic map
- `pinepaper_highlight_regions` — Highlight regions
- `pinepaper_apply_data_colors` — Choropleth coloring
- `pinepaper_add_marker` — Add map marker

### Rigging Tools
- `pinepaper_create_skeleton` — Create skeleton
- `pinepaper_add_bone` — Add bone
- `pinepaper_attach_item_to_bone` — Attach item
- `pinepaper_apply_rig_preset` — Apply preset
- `pinepaper_save_pose` / `pinepaper_load_pose` — Pose management
- `pinepaper_interpolate_poses` — Blend poses

### Blending Tools
- `pinepaper_apply_blend_preset` — Apply blend preset
- `pinepaper_transition_blend_mode` — Animated blend transition
- `pinepaper_add_interactive_blend` — Interactive blending
- `pinepaper_set_group_blend_mode` — Group blending

### Filter Tools
- `pinepaper_apply_image_filter` — Single GPU filter
- `pinepaper_apply_filter_chain` — Multi-filter chain

### Masking Tools
- `pinepaper_apply_cutout_style` — Apply cutout preset
- `pinepaper_get_cutout_styles` — List presets

### Lasso Tools
- `pinepaper_lasso_activate` — Activate lasso on image
- `pinepaper_lasso_apply` — Extract region

### View Tools
- `pinepaper_zoom` — Set zoom level
- `pinepaper_pan` — Pan view
- `pinepaper_fit_view` — Fit content in view
- `pinepaper_get_view_state` — Get current view

### Selection Tools
- `pinepaper_select` — Select item
- `pinepaper_select_all` — Select all
- `pinepaper_deselect_all` — Deselect all
- `pinepaper_get_selection` — Get selection
- `pinepaper_delete_selected` — Delete selected

### Transform Tools
- `pinepaper_nudge` — Move items
- `pinepaper_flip` — Flip items
- `pinepaper_reorder` — Change z-order

### Background Tools
- `pinepaper_set_background` — Set background
- `pinepaper_clear_background` — Clear background
- `pinepaper_get_background` — Get background

### History Tools
- `pinepaper_undo` / `pinepaper_redo` — Undo/redo
- `pinepaper_get_history_state` — Get history state
- `pinepaper_clear_canvas` — Clear canvas

### Query Tools
- `pinepaper_query_items` — Query items by criteria
- `pinepaper_get_item_by_id` — Get specific item
- `pinepaper_hit_test` — Hit test at point
- `pinepaper_is_empty` — Check if canvas empty

### Precomp Tools
- `pinepaper_create_precomp` — Create composition
- `pinepaper_add_to_precomp` — Add to composition
- `pinepaper_remove_from_precomp` — Remove from composition

### Playback Tools
- `pinepaper_play_timeline` — Play keyframe timeline
- `pinepaper_stop_timeline` — Stop playback
- `pinepaper_pause_timeline` — Pause playback
- `pinepaper_seek_timeline` — Seek to time

### Export Tools
- `pinepaper_export_svg` — Export as SVG
- `pinepaper_export_training_data` — Export training data

### Generator Tools
- `pinepaper_execute_generator` — Run background generator
- `pinepaper_list_generators` — List available generators

### Font Tools
- `pinepaper_font_create_glyph` — Create font glyph
- `pinepaper_font_export` — Export font file
- `pinepaper_font_status` — Get font creation status
