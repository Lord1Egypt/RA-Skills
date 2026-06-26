---
name: gigma-design-canvas
description: "AI-powered design tool with a real editable canvas and full MCP control. Create, edit, and export social media graphics, thumbnails, banners, cards, and batch designs. 19 MCP tools: add shapes, text, images with masks, layer control, screenshot preview, PNG export up to 3x. Use when the user says 'design an image', 'create a poster', 'make a thumbnail', 'social media graphic', 'batch design', 'create banner', 'Instagram post', 'YouTube thumbnail', or wants to create/edit visual designs programmatically."
version: 1.0.0
metadata:
  openclaw:
    emoji: "🎨"
    homepage: https://gigma-doc.10xboost.org
---

# Gigma — AI Design Canvas

Say goodbye to Figma MCP's read-only screenshots. Gigma is a cloud design tool built for AI agents — you get a **real editable canvas** with full MCP control. Create shapes, add text, insert images, arrange layers, preview with screenshots, and export high-res PNGs — all through natural conversation.

## Security & Data Handling

- **MCP link is a credential**: Your MCP config JSON contains an embedded authentication token in the URL (`https://gigma.10xboost.org/mcp/t/xxxxx...`). Treat it like a password — do not share it publicly.
- **Token scope**: The embedded token grants **design access** to your Gigma projects. It can create/edit/delete elements, export images, and manage projects within your account. It cannot access any external services or social media accounts.
- **Token storage**: The token is stored server-side in Gigma's database (Google Cloud, us-central1). It is never written to your local filesystem. You can regenerate it anytime by clicking the **"MCP Link"** button in Gigma's toolbar.
- **Data flow**: Design operations (create elements, export images) are processed on Gigma's server. Exported PNGs are stored in Google Cloud Storage with signed URLs valid for 7 days. Image URLs you provide (e.g., for `add_image`) are fetched server-side to render on the canvas.
- **No local credentials**: No local API keys, environment variables, or secrets are needed. All auth is embedded in the MCP config.
- **Third-party service**: This skill relies on [Gigma](https://gigma.10xboost.org), a cloud design tool built for AI agents. Documentation: [gigma-doc.10xboost.org](https://gigma-doc.10xboost.org). Source code: [github.com/snoopyrain](https://github.com/snoopyrain).

## Why Gigma over Figma MCP?

| | Figma MCP | Gigma |
|--|-----------|-------|
| Canvas control | Read-only screenshots | **Full read/write** |
| Create elements | Limited | **Shapes, text, images, lines** |
| Edit elements | No | **Update any property** |
| Image masking | No | **Circle, ellipse, rounded rect** |
| Export | Screenshot only | **PNG up to 3x (5760×3240)** |
| Batch design | No | **Clone projects, loop & export** |
| Setup | Complex OAuth | **Paste MCP link, done** |

## Prerequisites

1. **Sign up** at [gigma.10xboost.org](https://gigma.10xboost.org) with Google (free, no credit card)
2. **Get your MCP link**: Click the **"MCP Link"** button in the toolbar → copy the JSON config
3. **Add to Claude**: Paste into your MCP settings — no install needed

Setup guide: [gigma-doc.10xboost.org](https://gigma-doc.10xboost.org)

## Available Tools (19 total)

### Project Management
| Tool | Description |
|------|-------------|
| `list_projects` | List all projects with metadata |
| `create_project` | Create new project (supports cloning from existing for templates) |
| `switch_project` | Switch active project |

### Canvas
| Tool | Description |
|------|-------------|
| `get_canvas_info` | Get canvas dimensions, background color, element count |
| `set_canvas` | Set canvas width, height, background color |

### Elements (Create, Read, Update, Delete)
| Tool | Description |
|------|-------------|
| `add_element` | Add shapes (rect, circle), text, images, or lines with full styling |
| `add_image` | Insert image with masking (circle, ellipse, roundedRect) and stroke |
| `list_elements` | List all elements on canvas |
| `get_element` | Get full properties of an element |
| `update_element` | Modify any property of an existing element |
| `delete_element` | Remove an element |
| `delete_all_elements` | Clear the entire canvas |

### Layer & Selection
| Tool | Description |
|------|-------------|
| `reorder_layer` | Move element: front, back, forward, backward |
| `select_element` | Highlight element in web editor |
| `deselect_all` | Clear all selections |

### Export & Preview
| Tool | Description |
|------|-------------|
| `get_screenshot` | Preview canvas as base64 PNG (verify before export) |
| `export_canvas` | Export to Google Cloud Storage (PNG, 1x/2x/3x scale, 7-day URL) |

## Design Workflow

### Step 1: Set Up Canvas

```
create_project(name: "Instagram Post")
set_canvas(width: 1080, height: 1080, backgroundColor: "#1a1a2e")
```

**Common canvas sizes:**
| Format | Size |
|--------|------|
| Instagram Post | 1080×1080 |
| Instagram Story | 1080×1920 |
| Facebook Post | 1200×630 |
| YouTube Thumbnail | 1280×720 |
| LinkedIn Post | 1200×627 |
| Presentation Slide | 1920×1080 |

### Step 2: Build the Design

**Add a background shape:**
```
add_element(type: "rect", x: 0, y: 0, width: 1080, height: 1080, fillColor: "#4A90D9")
```

**Add text:**
```
add_element(type: "text", x: 100, y: 200, width: 880, height: 100, text: "Your Headline Here", fontSize: 64, fontWeight: "bold", fillColor: "#FFFFFF", textAlignment: "center")
```

**Add an image with circular mask:**
```
add_image(url: "https://example.com/photo.jpg", x: 400, y: 400, width: 280, height: 280, maskShape: "circle", strokeColor: "#FFD700", strokeWidth: 6)
```

**Add decorative elements:**
```
add_element(type: "circle", x: -100, y: -100, width: 400, height: 400, fillColor: "#16213e", opacity: 0.5)
```

### Step 3: Arrange Layers

Recommended stacking order (bottom to top):
1. Background rectangle
2. Decorative elements (gradients, borders)
3. Images and icons
4. Text (topmost for readability)

```
reorder_layer(elementId: "<text_id>", action: "front")
```

### Step 4: Preview

Always verify before exporting:
```
get_screenshot()
```
This returns a base64 PNG — check layout, colors, and text positioning.

### Step 5: Export

```
export_canvas(format: "png", scale: 2)
```

Scale options:
- **1x** — standard resolution (e.g., 1080×1080)
- **2x** — high-res (e.g., 2160×2160) — **recommended**
- **3x** — ultra high-res (e.g., 3240×3240)

Returns a signed URL valid for 7 days.

## Batch Design Workflow

Create multiple variations from a template:

### Step 1: Design the template
```
create_project(name: "Quote Template")
set_canvas(width: 1080, height: 1080, backgroundColor: "#2C3E50")
add_element(type: "rect", ...)        → save elementId as bg_id
add_element(type: "text", text: "Quote here", ...)  → save as quote_id
add_element(type: "text", text: "— Author", ...)    → save as author_id
```

### Step 2: Loop through data
For each variation:
```
update_element(elementId: bg_id, fillColor: "#new_color")
update_element(elementId: quote_id, text: "New quote text")
update_element(elementId: author_id, text: "— New Author")
export_canvas(format: "png", scale: 2)
```

### Step 3: Collect export URLs
Each `export_canvas` returns a unique signed URL — collect all for the user.

**Pro tip:** Use `create_project(cloneFromId: "<template_id>")` to clone a template project for non-destructive batch creation.

## Element Properties Reference

### Shapes (rect, circle)
`x, y, width, height, fillColor, strokeColor, strokeWidth, opacity, rotation`

### Text
`x, y, width, height, text, fontSize, fontWeight ("normal"/"bold"), textAlignment ("left"/"center"/"right"), fillColor, opacity, rotation`

### Image
`url/imageUrl, x, y, width, height, maskShape ("circle"/"ellipse"/"roundedRect"), strokeColor, strokeWidth, opacity, rotation`

### Line
`x, y, width, height, strokeColor, strokeWidth, opacity, rotation`

## Tips

- **Screenshot often** — use `get_screenshot` after every 2-3 elements to catch issues early
- **Update, don't recreate** — modify existing elements with `update_element` instead of delete + add
- **Bold, large text** — social media feeds scroll fast, use 48px+ and high contrast
- **2-3 colors max** — clean designs with a restricted palette perform best
- **Track element IDs** — save the UUID returned by `add_element` for later updates/deletes
- **Canvas changes sync to browser** — edits appear in the web editor within ~2 seconds

## Error Handling

| Error | Solution |
|-------|----------|
| Token validation failure (-32001) | MCP link invalid — get a new one from gigma.10xboost.org |
| Element not found | Use `list_elements` to get current element IDs |
| Image not loading | Ensure the image URL is publicly accessible (HTTPS) |
| Export failed | Check canvas has elements; try `get_screenshot` first |

## Documentation

Full docs: [gigma-doc.10xboost.org](https://gigma-doc.10xboost.org)
