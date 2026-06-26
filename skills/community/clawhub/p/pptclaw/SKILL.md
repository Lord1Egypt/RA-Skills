---
name: pptclaw
description: >
  Create and edit presentations by writing slide JSON files directly. Use this skill whenever the user wants to
  create a presentation, build slides, design a deck, add or modify slide elements, or work with the pptclaw CLI.
  Covers deck format, element schemas, theme colors, layout conventions, and CLI commands.
---

# PPTClaw Skill Reference

PPTClaw is a local-first presentation editor. Decks are JSON files on disk — you create and edit them directly, and the editor syncs changes live via WebSocket.

## Setup

If `pptclaw` is not installed, install it globally:
```bash
pnpm add -g pptclaw    # or: npm install -g pptclaw
```

## Deck Format

A deck is a folder with this structure:

```
my-deck/
├── manifest.json           # Title, theme, viewport, slide order
├── slides/
│   ├── 001-abc123.json     # Slide files: <NNN>-<id>.json
│   ├── 002-def456.json
│   └── ...
└── assets/                 # Images and other media
    ├── hero.jpg
    └── ...
```

### manifest.json

```json
{
  "title": "My Presentation",
  "format": "1",
  "viewport": { "width": 1920, "ratio": 0.5625 },
  "theme": {
    "primary": "#2563eb",
    "secondary": "#7c3aed",
    "tx1": "#1e293b",
    "accents": ["#2563eb", "#7c3aed", "#5b9bd5", "#ff6b6b", "#4ecdc4", "#95e1d3"],
    "fontHeading": "YouSheBiaoTiHei",
    "fontBody": "Microsoft YaHei"
  }
}
```

- `viewport.ratio` is height/width (0.5625 = 16:9, giving 1920x1080)
- `theme.accents` is an array of 6 colors used sequentially for chart series, infographic items, etc.

### Slide JSON

Each slide file contains one slide object:

```json
{
  "id": "abc123",
  "elements": [ /* PPTElement objects */ ],
  "background": { "type": "solid", "color": "#ffffff" },
  "remark": "Speaker notes text",
  "type": "content"
}
```

- `type`: "cover", "contents", "transition", "content", "end"
- `elements`: array of typed element objects (see below)
- `background`: optional, defaults to white
- `remark`: optional speaker notes (plain text)

## Canvas

- Size: **1920 x 1080 pixels**
- Origin: top-left corner (0, 0)
- All position/size values are in pixels

## Base Element Fields

Every element shares these fields:

```ts
id: string        // Unique element ID
left: number      // X position (px from left edge)
top: number       // Y position (px from top edge)
width: number     // Element width (px)
height: number    // Element height (px)
rotate: number    // Rotation in degrees, default 0
lock?: boolean    // Lock element from editing
groupId?: string  // Elements with same groupId form a group
name?: string     // Display name
link?: { type: 'web' | 'slide', target: string }
```

Exception: `line` elements omit `height` and `rotate` — they use start/end points instead.

## Theme Colors

Use CSS variable references instead of hardcoded hex values to stay consistent with the deck's theme:

| Variable | Purpose |
|----------|---------|
| `var(--primary)` | Primary brand color |
| `var(--secondary)` | Secondary/accent color |
| `var(--tx1)` | Text color |
| `var(--accent1)` to `var(--accent6)` | Chart/emphasis colors |

**Brightness variants** — append a suffix to any theme variable:
- `var(--primary-plus-50)` — lighter (+50 brightness)
- `var(--primary-minus-25)` — darker (-25 brightness)
- Works for all theme colors: secondary, tx1, accent1-6

**Theme fonts:**
- `var(--font-heading)` — for titles, subtitles, headers
- `var(--font-body)` — for body text, content, items

## Common Style Types

### Outline (border)
```ts
{ style?: 'solid' | 'dashed' | 'dotted', width?: number, color?: string }
```

### Shadow
```ts
{ offset: number, angle: number, blur: number, color: string, alpha: number }
// offset: 0-100, angle: 0-359, blur: 0-100 (pt), alpha: 0-100 (0=transparent)
```

### Gradient
```ts
{
  type: 'linear' | 'radial',
  colors: [{ pos: number, color: string, alpha?: number }],  // pos: 0-100%
  rotate?: number,
  radialStart?: 'center' | 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right'
}
```

## Text Element (Inline Reference)

Text is the most common element type, so its full schema is included here. For other element types, run `pptclaw element-docs <type>`.

```ts
interface PPTTextElement extends PPTBaseElement {
  type: 'text'
  content: string           // ProseMirror HTML
  defaultColor: string      // Fallback color (overridden by inline HTML styles)
  fill?: string             // Background fill color
  lineHeight?: number       // Line height multiplier, default 1.5
  wordSpace?: number        // Letter spacing, default 0
  paragraphSpace?: number   // Paragraph spacing (px), default 5
  opacity?: number          // 0-1, default 1
  vertical?: boolean        // Vertical text mode
  outline?: Outline
  shadow?: Shadow
  textType?: 'title' | 'subtitle' | 'content' | 'item' | 'itemTitle' | 'notes' | 'header' | 'footer'
}
```

### HTML Content Format

The `content` field uses ProseMirror HTML with inline styles:

```html
<p style="font-size: 72px; font-family: var(--font-heading); font-weight: bold;">Title Text</p>
<p style="font-size: 36px; font-family: var(--font-body);">Body paragraph</p>
```

Supported inline styles: `font-size` (px), `color`, `font-weight`, `font-style`, `text-decoration`, `text-align`, `font-family`.

### Font Size Rules

Font sizes in HTML are in **px**, which equals **2x the PowerPoint pt value**. This matters because presentations are viewed on large screens — small text becomes unreadable.

| Role | Pt | Px | Notes |
|------|----|----|-------|
| Title | 36pt | 72px | Minimum for slide titles |
| Subtitle | 24pt | 48px | |
| Body | 18pt | 36px | Recommended 36-40px |
| Minimum | 16pt | 32px | Nothing smaller than this |

Common mistake: using web-scale sizes like 14px, 16px, 18px — these are too small for presentations.

## Slide Background

```json
{
  "background": {
    "type": "solid",
    "color": "var(--primary-plus-80)"
  }
}
```

Types: `"solid"` (with `color`) or `"gradient"` (with `gradient` object). Set backgrounds on the slide object, not by creating a full-canvas shape.

## Layout Conventions

### Standard Content Page
- **Title**: left: 80, top: 80, font-size: 72px, bold
- **Content area**: left: 80, top: 200, width: 1760, height: 800
- Large elements (charts, infographics, tables) should fill the content area when shown alone

### Centering
To horizontally center an element: `left = (1920 - width) / 2`

Note: `left: 960` does NOT center — it places the element's left edge at the midpoint, pushing it right.

### Layout Self-Check

Before finalizing element positions, verify:
1. **No overlap** — element rectangles don't unintentionally intersect
2. **Readable text** — all font sizes >= 32px, content fits within element bounds
3. **Edge margins** — elements stay >= 60px from canvas edges
4. **Element spacing** — >= 20px gap between elements
5. **Consistency** — use 20px card gap and 10px border-radius across all slides

## Element Types

Beyond the text element documented above, PPTClaw supports these element types:

| Type | Description | Key Fields |
|------|-------------|------------|
| `image` | Image with cover/fill, clipping, masking | imageSource, fit, clipShape, mask |
| `shape` | Vector shape with optional inner text | shapeId, fill, gradient, text |
| `line` | Line/arrow/connector (no height/rotate) | start, end, points, width (stroke) |
| `chart` | Data visualization (8 chart types) | chartType, data, color |
| `table` | Grid table with styled cells | data (2D TableCell), colWidths, theme |
| `icon` | SVG icon by keyword search | keyword, color |
| `artText` | Decorative wave text (cover pages only) | content, style, defaultColor |
| `infographic` | Template-based infographic/diagram | template, data, color |

Get the full schema for any type:
```bash
pptclaw element-docs <type>           # e.g., pptclaw element-docs image
pptclaw element-docs chart table      # multiple types at once
pptclaw element-docs                  # list all types
```

## CLI Reference

All commands support `-p, --port <port>` (default: 3059).

### pptclaw serve [deck]
Start the editor server as a background daemon. Optionally open a deck immediately.
```bash
pptclaw serve                    # start server
pptclaw serve ./my-deck          # start and open deck
pptclaw serve --port 4000        # custom port
```
Exit code: 0 on success, 1 if server fails to start.

### pptclaw open \<path\>
Open a deck folder in the running editor.
```bash
pptclaw open ./my-deck
pptclaw open ./my-deck --session custom-id
```
Output: session ID, path, slide count.

### pptclaw validate \<path\>
Validate a deck folder structure and content. Returns JSON with `valid`, `errors`, `warnings`.
```bash
pptclaw validate ./my-deck
```
Exit code: 0 if valid, 1 if errors found. Requires running server.

### pptclaw list-decks
List active sessions (open decks) with slide counts.
```bash
pptclaw list-decks
```

### pptclaw status
Show server status, auth state, and active sessions as JSON.

### pptclaw init
Copy the PPTClaw skill file to `.claude/skills/pptclaw/SKILL.md` in the current directory.

### pptclaw element-docs [type...]
Print element type documentation.
```bash
pptclaw element-docs              # list available types
pptclaw element-docs image        # print image element docs
pptclaw element-docs chart table  # print multiple
```

### pptclaw search-images \<query\>
Search Unsplash images. Returns JSON array of results with id, description, dimensions.

### pptclaw download-image \<url\> --deck \<path\>
Download an image to a deck's assets folder.

## Workflows

### Create a New Deck

1. Create the folder structure:
   ```bash
   mkdir -p my-deck/slides my-deck/assets
   ```

2. Write `manifest.json` with title, theme, and viewport

3. Create slide files in `slides/` (numbered: `001-<id>.json`, `002-<id>.json`, ...)

4. Validate:
   ```bash
   pptclaw validate ./my-deck
   ```

5. Open in editor:
   ```bash
   pptclaw serve ./my-deck
   ```

### Edit an Existing Slide

1. Read the slide JSON file
2. Modify the `elements` array — add, update, or remove elements
3. Write the file back — the editor picks up changes automatically via file watcher
4. Validate if needed: `pptclaw validate ./my-deck`

### Add Images

1. Search for images:
   ```bash
   pptclaw search-images "mountain landscape"
   ```
2. Download to deck assets:
   ```bash
   pptclaw download-image <url> --deck ./my-deck
   ```
3. Reference in slide JSON via `imageSource` field on an image element
