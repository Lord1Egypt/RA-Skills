---
name: excalidraw
description: "Hand-drawn Excalidraw JSON diagrams — architecture, flow, sequence. Generate clean, well-laid-out charts with consistent box sizing, meaningful colors, and zero line crossings."
version: 2.1.0
author: Hermes Agent
license: MIT
dependencies: ["cryptography"]
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Excalidraw, Diagrams, Flowcharts, Architecture, Visualization, JSON]
    related_skills: [excalidraw-diagram-workflow]

---

# Excalidraw Diagram Skill

Create `.excalidraw` files that can be drag-dropped onto [excalidraw.com](https://excalidraw.com) or shared via URL. No account, no API keys, just JSON.

## When to use

Architecture diagrams, flowcharts, sequence diagrams, concept maps, process maps — any visual you want to communicate clearly.

## Workflow

1. **Load this skill** (you already did)
2. **Design the layout** (read the Layout Rules section first — this is where most bad diagrams fail)
3. **Write the elements JSON** — follow the Layout Rules strictly
4. **Pre-flight check** — verify all box widths and arrow lengths against Rule 6 before saving
5. **Save** as `.excalidraw` via `write_file`
6. **Upload** for a shareable link via `scripts/upload.py` in `terminal`
7. **Verify with screenshot** — check for overflow issues, fix and re-upload if needed

---

## Layout Rules (MOST IMPORTANT SECTION)

Bad diagrams fail for 4 reasons: **inconsistent box sizes**, **meaningless colors**, **crossing lines**, **disorganized arrangement**. Fix all four with these rules:

### Rule 1 — Use a Grid

Never place elements ad-hoc. Design on a virtual grid:
- **Column width**: 200–240px per logical column
- **Row height**: 100–120px per logical row
- **Gap between boxes**: minimum 30px horizontal, 25px vertical
- **X positions**: 0, 240, 480, 720, 960 (every 240px)
- **Y positions**: 0, 120, 240, 360, 480, 600 (every 120px)

### Rule 2 — Consistent Box Sizing

All boxes in the same logical row or category **MUST have identical dimensions**. Use one size for all level-1 nodes, another for all level-2 nodes. Only vary size for intentional hierarchy.

| Role | Width | Height |
|------|-------|--------|
| Level-1 node (main step) | 200 | 70 |
| Level-2 node (sub-step) | 180 | 60 |
| Title banner | 400 | 50 |
| Footer / badge | 160 | 40 |

### Rule 3 — Meaningful Color Coding

Colors must communicate **semantics**, not decorate. Pick ONE role per diagram:

**Role A — Flow / Process (arrows show direction):**
| Meaning | Fill Color | Hex |
|---------|-----------|-----|
| Start / Input | Light Blue | `#a5d8ff` |
| Step / Action | Light Blue | `#a5d8ff` |
| Decision | Light Yellow | `#fff3bf` |
| Success / Output | Light Green | `#b2f2bb` |
| External / Pending | Light Orange | `#ffd8a8` |
| Error / Alert | Light Red | `#ffc9c9` |

**Role B — Layered Architecture (zones show grouping):**
| Meaning | Fill Color | Hex |
|---------|-----------|-----|
| UI / Frontend layer | Blue zone | `#dbe4ff` |
| Logic / Agent layer | Purple zone | `#e5dbff` |
| Data / Tool layer | Green zone | `#d3f9d8` |

**Role C — Comparison (side-by-side):**
| Meaning | Fill Color | Hex |
|---------|-----------|-----|
| This side | Light Blue | `#a5d8ff` |
| That side | Light Purple | `#d0bfff` |

**Pick ONE role per diagram. Do NOT mix Role A and Role B colors in the same diagram.**

### Rule 4 — No Crossing Lines

Arrows must never cross other content. Techniques:
- **Sequential flow (left→right)**: all arrows point in one direction, use vertical spacing to separate rows
- **Vertical stacking**: if 3+ arrows would cross, stack them vertically with 15px gaps
- **L-shapes**: use `points: [[0,0],[dx,0],[dx,dy]]` to route around obstacles
- **Start/end bindings**: use `startBinding`/`endBinding` with `fixedPoint` so arrows snap to shape edges cleanly

### Rule 5 — Meaningful Arrangement

Layout must match the conceptual model:
- **Flowchart**: strict left→right or top→bottom. No boxes above arrows.
- **Layers**: background zones drawn FIRST (behind everything), then nodes inside each zone
- **Comparison**: left vs right, never diagonal
- **Title at top**, footer/result at bottom

### Rule 6 — Content Must Fit Inside Boxes

This is the #1 reason diagrams look broken after upload. Text that overflows its container makes the diagram unreadable. Prevent it with these rules:

**Minimum box widths by text length** (fontSize 16, Virgel font):

| Characters in label | Minimum box width |
|--------------------|-------------------|
| 1–8 chars | 120 px |
| 9–14 chars | 160 px |
| 15–20 chars | 200 px |
| 21–28 chars | 240 px |
| 29+ chars | split into two lines or reduce fontSize |

**Width formula**: `box_width >= text_length * 9.5` (at fontSize 16, Virgel = ~9.5px per character)

**Arrow label width**: The arrow must be at least `label_chars * 9.5 + 40` px long to fit the label clearly. If the flow is too short, stack arrows vertically rather than making them short.

**Text length hard limits**:
- Box labels: max 28 characters per line. Use `line1\nline2` for longer text (max 2 lines).
- Arrow labels: max 30 characters. Keep them short.
- Standalone text: no hard limit but prefer brevity.

**What to check before saving**:
1. Count the longest label in each row
2. Verify the box width >= that count × 9.5
3. Verify arrow length >= its label length × 9.5 + 40
4. If any box has width < 120px, widen it — no exceptions

**Warning signs of overflow**:
- Text looks squished or overlaps box edges → box too narrow
- Arrow label clips into the arrow line or bleeds outside → arrow too short
- Text trails off the right edge of a box → width is insufficient
- Multi-word label on one line but box is narrow → split with `\n` or widen box

---

## Element Format Reference

### Required Fields (all elements)
`type`, `id` (unique string), `x`, `y`, `width`, `height`

### Defaults (applied automatically — skip these)
- `strokeColor`: `"#1e1e1e"`
- `backgroundColor`: `"transparent"`
- `fillStyle`: `"solid"`
- `strokeWidth`: `2`
- `roughness`: `1` (hand-drawn look)
- `opacity`: `100`

### Element Types

**Rectangle**:
```json
{ "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 70 }
```
- `roundness: { "type": 3 }` for rounded corners
- `backgroundColor: "#a5d8ff"`, `fillStyle: "solid"` for filled

**Ellipse**:
```json
{ "type": "ellipse", "id": "e1", "x": 100, "y": 100, "width": 150, "height": 150 }
```

**Diamond**:
```json
{ "type": "diamond", "id": "d1", "x": 100, "y": 100, "width": 150, "height": 150 }
```

**Labeled shape (container binding)** — do NOT use `"label": { "text": "..." }` on shapes:
```json
{
  "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 70,
  "roundness": { "type": 3 }, "backgroundColor": "#a5d8ff", "fillStyle": "solid",
  "boundElements": [{ "id": "t_r1", "type": "text" }]
},
{
  "type": "text", "id": "t_r1", "x": 105, "y": 118, "width": 190, "height": 25,
  "text": "Start", "fontSize": 18, "fontFamily": 1, "strokeColor": "#1e1e1e",
  "textAlign": "center", "verticalAlign": "middle",
  "containerId": "r1", "originalText": "Start", "autoResize": true
}
```
- Works on rectangle, ellipse, diamond
- Text is auto-centered by Excalidraw when `containerId` is set
- The text `x`/`y`/`width`/`height` are approximate — Excalidraw recalculates them on load
- `originalText` must match `text`
- Always include `fontFamily: 1` (Virgil/hand-drawn font)

**Labeled arrow** — same container binding approach:
```json
{
  "type": "arrow", "id": "a1", "x": 300, "y": 135, "width": 200, "height": 0,
  "points": [[0,0],[200,0]], "endArrowhead": "arrow",
  "boundElements": [{ "id": "t_a1", "type": "text" }]
},
{
  "type": "text", "id": "t_a1", "x": 370, "y": 118, "width": 60, "height": 25,
  "text": "goes to", "fontSize": 14, "fontFamily": 1, "strokeColor": "#1e1e1e",
  "textAlign": "center", "verticalAlign": "middle",
  "containerId": "a1", "originalText": "goes to", "autoResize": true
}
```

**Standalone text** (titles and annotations only — no container):
```json
{
  "type": "text", "id": "t1", "x": 150, "y": 138, "text": "Hello",
  "fontSize": 24, "fontFamily": 1, "strokeColor": "#1e1e1e",
  "originalText": "Hello", "autoResize": true
}
```
- `x` is the LEFT edge
- Do NOT rely on `textAlign` or `width` for positioning

**Arrow**:
```json
{
  "type": "arrow", "id": "a1", "x": 300, "y": 135, "width": 200, "height": 0,
  "points": [[0,0],[200,0]], "endArrowhead": "arrow"
}
```
- `points`: `[dx, dy]` offsets from element `x`, `y`
- `endArrowhead`: `null` | `"arrow"` | `"bar"` | `"dot"` | `"triangle"`
- `strokeStyle`: `"solid"` (default) | `"dashed"` | `"dotted"`

### Arrow Bindings

```json
{
  "type": "arrow", "id": "a1", "x": 300, "y": 135, "width": 150, "height": 0,
  "points": [[0,0],[150,0]], "endArrowhead": "arrow",
  "startBinding": { "elementId": "r1", "fixedPoint": [1, 0.5] },
  "endBinding": { "elementId": "r2", "fixedPoint": [0, 0.5] }
}
```

`fixedPoint` coordinates: `top=[0.5,0]`, `bottom=[0.5,1]`, `left=[0,0.5]`, `right=[1,0.5]`

### Drawing Order (z-order)

Array order = z-order (first = back, last = front).
**Emit progressively**: background zones → shape → its bound text → its arrows → next shape.

- BAD: all rectangles, then all texts, then all arrows
- GOOD: bg_zone → shape1 → text_for_shape1 → arrow1 → shape2 → text_for_shape2 → ...
- Always place the bound text element immediately after its container shape

### Sizing Guidelines

**Font sizes:**
- `fontSize: 20` for titles and headings
- `fontSize: 16` for body text, labels, descriptions
- `fontSize: 14` for secondary annotations only (sparingly)
- NEVER use `fontSize` below 14

**Element sizes:**
- Minimum shape size: 120x60 for labeled rectangles/ellipses
- Leave 20-30px gaps between elements minimum
- Prefer fewer, larger elements over many tiny ones

**MANDATORY: Pre-check text fit before finalizing**
1. List every box's label text and count characters
2. Apply the Rule 6 minimum-width table — if any box is narrower than required, widen it first
3. For every arrow with a label, verify arrow width >= `label_chars × 9.5 + 40`
4. If text in a box feels even slightly cramped, add 20px of extra width

---

## Color Palette

### Pastel Fills (for shape backgrounds)
| Use | Fill Color | Hex |
|-----|-----------|-----|
| Primary / Input | Light Blue | `#a5d8ff` |
| Success / Output | Light Green | `#b2f2bb` |
| Warning / External | Light Orange | `#ffd8a8` |
| Processing / Special | Light Purple | `#d0bfff` |
| Error / Critical | Light Red | `#ffc9c9` |
| Notes / Decisions | Light Yellow | `#fff3bf` |
| Storage / Data | Light Teal | `#c3fae8` |
| Analytics | Light Pink | `#eebefa` |

### Background Zones (opacity 30-35 for layered diagrams)
| Use | Fill Color | Hex |
|-----|-----------|-----|
| UI / Frontend layer | Blue zone | `#dbe4ff` |
| Logic / Agent layer | Purple zone | `#e5dbff` |
| Data / Tool layer | Green zone | `#d3f9d8` |

### Text Contrast Rules
- **On white backgrounds**: minimum text color is `#757575`. Default `#1e1e1e` is best.
- **Colored text on light fills**: use dark variants (`#15803d` not `#22c55e`, `#2563eb` not `#4a9eed`)
- **White text**: only on dark backgrounds (`#9a5030` not `#c4795b`)
- **Never**: light gray (`#b0b0b0`, `#999`) on white — unreadable

---

## Saving & Uploading

### Saving a Diagram

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "hermes-agent",
  "elements": [ ...elements... ],
  "appState": { "viewBackgroundColor": "#ffffff" }
}
```

Save with `write_file` to any path, e.g. `~/diagrams/my_diagram.excalidraw`.

### Uploading for a Shareable Link

```bash
python ~/.hermes/skills/creative/excalidraw/scripts/upload.py ~/diagrams/my_diagram.excalidraw
```

This encrypts client-side (AES-GCM), embeds the key in the URL fragment, and uploads to excalidraw.com. Each upload gets a unique URL — **avoids the "file already exists" confirmation prompt**. No account needed.

Requires: `pip install cryptography`

---

## Common Mistakes to Avoid

1. **TEXT OVERFLOWS THE BOX** (the most common failure mode):
   - Causes: box too narrow for its label, arrow too short for its label, multi-line text crammed into one line
   - Symptom: text bleeds outside box edges, labels get clipped, arrows show "..." inside them
   - Fix: always use the Rule 6 minimum-width table to pre-calculate box widths. Make arrows at least `label_chars × 9.5 + 40` px long
   - Rule of thumb: if text feels "tight", the box is too small — add 40px of breathing room

2. **Do NOT use `"label"` on shapes** — this is NOT a valid Excalidraw property. It will be silently ignored, producing blank shapes. Always use container binding (`containerId` + `boundElements`).

2. **Every bound text needs both sides linked** — the shape needs `boundElements: [{"id": "t_xxx", "type": "text"}]` AND the text needs `containerId: "shape_id"`.

3. **Elements overlap when y-coordinates are close** — always check that text, boxes, and labels don't stack on top of each other.

4. **Arrow labels overflow short arrows** — keep labels short or make arrows wider.

5. **Center titles relative to the diagram** — estimate total width and center the title text over it.

6. **Draw decorations LAST** — sun, stars, icons should appear at the end of the array so they're on top.

7. **Color without meaning** — every color choice must map to a concept in the diagram. Random color assignment is noise.

---

## Verify with Screenshot (Required Step)

After uploading, always verify the result with a real screenshot. This catches layout problems that JSON inspection can't.

### Option A — PinchTab (preferred, uses your real Chrome)

Requires PinchTab Chrome extension installed:

```bash
# 1. Navigate to the Excalidraw URL
curl -X POST http://localhost:9867/navigate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://excalidraw.com/#json=<FILE_ID>,<KEY>"}'

# 2. Wait for render
sleep 4

# 3. Screenshot
curl -X POST http://localhost:9867/screenshot \
  -H "Content-Type: application/json" \
  -d '{"format": "jpeg", "quality": 85}' \
  --output ~/diagrams/my_diagram.jpg
```

Then load the screenshot with `vision_analyze` to verify layout quality.

### Option B — Chrome CDP (manual Chrome required)

The user must first start Chrome manually with debug port:
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-screenshot &
```

Then use the screenshot script:
```bash
python ~/work/ai/omnimcp-opencli/scripts/chrome_screenshot.py \
  "https://excalidraw.com/#json=<FILE_ID>,<KEY>" \
  ~/diagrams/my_diagram.jpg
```

### What to Check on the Screenshot

1. **Box sizes** — all boxes in same row same size? Text fits inside?
2. **Color coding** — does color map to a consistent meaning across the whole diagram?
3. **Arrow crossings** — no line crosses through any box or other line
4. **Content** — all key information visible and readable
5. **Arrangement** — does layout match the conceptual model (flow left→right, layers stacked)?

If problems found: patch the JSON and re-upload. Iterate until 8+/10.

---

## Complete Examples

See `references/examples.md` for copy-pasteable complete diagrams covering:
- Two connected labeled boxes (minimal flowchart)
- Photosynthesis process diagram (multi-node with background zones)
- MCP sequence diagram (actors, dashed lifelines, message arrows)

See `references/skill-selection-model.md` for the 3-layer skill selection architecture (Hermes/OpenClaw model) — useful when designing skill catalogs or building workflow diagrams about agent behavior.