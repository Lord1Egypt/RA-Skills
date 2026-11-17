## Template Architecture

This section describes the complete structure of an Orshot template for MCP tools and AI agents.

### Template Structure

An Orshot template consists of **pages**, each containing a **canvas** and **elements**.

```
Template
├── id: number | string
├── name: string
├── description: string
├── width: number
├── height: number
├── pages_data: Array
    └── Page
        ├── id: string (UUID)
        ├── name: string
        ├── canvas: CanvasConfig
            ├── width: number
            ├── height: number
            ├── backgroundColor: string
            ├── backgroundImage: string
        ├── elements: Element[]
        ├── modifications: Modification[] (API parameters)
            ├── id: string
            ├── type: string
            ├── element: Element
            ├── description: string
        └── thumbnail_url: string | null
```

### Canvas Configuration

| Property          | Type   | Default         | Description                               |
| ----------------- | ------ | --------------- | ----------------------------------------- |
| `width`           | number | 800             | Canvas width in pixels (max: 5000)        |
| `height`          | number | 800             | Canvas height in pixels (max: 5000)       |
| `backgroundColor` | string | "#ffffff"       | Background color (hex, rgba, or gradient) |
| `backgroundImage` | string | ""              | URL to background image                   |
| `borderWidth`     | number | 0               | Border width in pixels                    |
| `borderColor`     | string | "rgba(0,0,0,1)" | Border color                              |
| `borderStyle`     | string | "solid"         | Border style (solid, dashed, etc)         |

### Canvas Size Presets

| Name                 | Dimensions | Use Case                        |
| -------------------- | ---------- | ------------------------------- |
| Square               | 1080×1080  | Instagram posts, general social |
| Instagram Story      | 1080×1920  | Stories, Reels, TikTok          |
| Slide/Presentation   | 1920×1080  | Presentations, slides           |
| YouTube Thumbnail    | 1280×720   | Video thumbnails                |
| Twitter Post         | 1600×900   | X/Twitter posts                 |
| Open Graph           | 1200×630   | Link previews, Facebook         |
| Pinterest Pin        | 1000×1500  | Pinterest                       |
| A4 Document          | 2480×3508  | Print documents                 |
| App Store Screenshot | 1290×2796  | iOS app screenshots             |

### Universal Element Properties

All elements share these base properties:

| Property            | Type    | Description                                  |
| ------------------- | ------- | -------------------------------------------- |
| `id`                | string  | Unique identifier (UUID)                     |
| `name`              | string  | Display name in layer list (was `layerName`) |
| `type`              | string  | "text", "image", "shape", "video"            |
| `position`          | object  | `{ x: number, y: number }` from top-left     |
| `dimensions`        | object  | `{ width: number, height: number }`          |
| `rotation`          | number  | Rotation in degrees (0-360)                  |
| `zIndex`            | number  | Layer order (higher = on top)                |
| `aspectRatioLocked` | boolean | Lock aspect ratio during resize              |
| `isHidden`          | boolean | Hide element from render                     |
| `skewX`             | number  | Horizontal skew angle                        |
| `skewY`             | number  | Vertical skew angle                          |

### Text Element

**Content Types:**

- **Plain text**: `"Hello World"` - Standard text string
- **Multi-line**: Use `\n` for line breaks: `"Line 1\nLine 2"`
- **Dynamic via API**: Use `.prompt` modifier for AI-generated text

```javascript
{
  type: "text",
  content: string,          // Plain text string
  layerName: string,        // Display name
  zIndex: number,
  rotation: number,
  position: { x: number, y: number },
  dimensions: { width: number, height: number },
  style: {
    // Typography
    fontFamily: string,     // e.g., "Inter", "Prata", "SF Pro"
    fontSize: string,       // e.g., "48px"
    fontWeight: string | number, // "400", "700", 700
    fontStyle: string,      // "normal", "italic"
    lineHeight: number,     // e.g., 1.2
    letterSpacing: string,  // e.g., "0px", "2px"

    // Appearance
    fill: string,           // Color or gradient
    color: string,          // Hex or rgba
    opacity: number,        // 0-1
    stroke: string,         // Stroke color
    strokeWidth: string,    // e.g., "0px"

    // Alignment & Layout
    textAlign: string,      // "left", "center", "right"
    verticalAlign: string,  // "flex-start", "center", "flex-end"
    textTransform: string,  // "none", "uppercase"
    textDecoration: string, // "none", "underline"
    textMode: string,       // "overflow", "fit"
    paddingX: string,
    paddingY: string,

    // Borders & Backgrounds
    borderColor: string,
    borderWidth: string,
    borderRadius: string,
    textBackgroundColor: string,
    textBackgroundRadius: string,
    textStrokeColor: string,
    textStrokeWidth: string,

    // Effects
    minFontSize: string,    // For "fit" mode
    filter: string,         // e.g., "blur(0px)"
    mixBlendMode: string,   // "normal", "multiply", etc.
    boxShadowX: string,
    boxShadowY: string,
    boxShadowBlur: string,
    boxShadowColor: string,
    dropShadowX: string,
    dropShadowY: string,
    dropShadowBlur: string,
    dropShadowColor: string
  },
  // Parameterization
  parameterizable: boolean,
  parameterId: string,
  parameterType: "text"
}
```

**Gradient text:**

```javascript
color: "linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 100%)";
```

### Image Element

**Content Types:**

- **URL** (recommended): `"https://example.com/image.png"` - Best for dynamic content
- **Base64**: `"data:image/png;base64,iVBORw0KGgo..."` - For embedded images
- **Binary**: Raw binary data (API upload only)

```javascript
{
  type: "image",
  content: string,          // URL (preferred), base64, or binary
  isSvg: boolean,
  layerName: string,
  style: {
    // Sizing & Positioning
    objectFit: string,      // "contain", "cover", "fill"
    objectPosition: string, // "center", "top left"

    // Appearance
    opacity: number,
    fill: string,           // Background fill
    stroke: string,         // Border stroke

    // Borders
    borderRadius: string,   // "0px", "12px", "50%"
    borderWidth: string,
    borderColor: string,

    // Effects
    filter: string,         // "blur(2px)", "grayscale(100%)"
    mixBlendMode: string,
    boxShadowX: string,
    boxShadowY: string,
    boxShadowBlur: string,
    boxShadowColor: string,
    dropShadowX: string,
    dropShadowY: string,
    dropShadowBlur: string,
    dropShadowColor: string,

    svgColor: string        // Recolor monochrome SVGs
  },
  parameterType: "imageUrl"
}
```

### Shape Element

```javascript
{
  type: "shape",
  shapeType: string,        // "rectangle", "circle", "arrow"
  layerName: string,
  style: {
    // Fill & Stroke
    fill: string,           // Color or gradient
    stroke: string,
    strokeWidth: string,    // e.g. "0px"

    // Dimensions
    borderRadius: string,   // Rectangle only
    borderWidth: string,
    borderColor: string,
    borderStyle: string,

    // Appearance
    opacity: number,
    filter: string,
    mixBlendMode: string,

    // Shadows
    boxShadowX: string,
    boxShadowY: string,
    boxShadowBlur: string,
    boxShadowColor: string,
    dropShadowX: string,
    dropShadowY: string,
    dropShadowBlur: string,
    dropShadowColor: string
  },
  parameterType: "fill"
}
```

**Gradient fills:**

```javascript
fill: "linear-gradient(180deg, rgba(0,0,0,0.7) 0%, transparent 100%)";
fill: "radial-gradient(circle at center, #FF6B6B 0%, #4ECDC4 100%)";
```

### Video Element

**Content Types:**

- **URL** (required): `"https://example.com/video.mp4"` - Must be a publicly accessible URL
- Supported formats: MP4, WebM, MOV
- For best results, use MP4 with H.264 codec

```javascript
{
  type: "video",
  content: string,          // Video URL (must be publicly accessible)
  videoOptions: {
    loop: boolean,
    muted: boolean,
    trim_start_time: string,
    trim_end_time: string,
    duration: number | null
  },
  style: {
    // Sizing & Positioning
    objectFit: string,      // "contain", "cover", "fill"
    objectPosition: string,

    // Appearance
    opacity: number,
    filter: string,
    mixBlendMode: string,

    // Borders & Shadows
    borderRadius: string,
    borderWidth: string,
    borderColor: string,
    elementBoxShadowX: string,
    elementBoxShadowY: string,
    elementBoxShadowBlur: string,
    elementBoxShadowColor: string
  },
  parameterType: "videoUrl"
}
```

### Parameterization Best Practices

When creating or updating templates, **always ensure all text, image, and video elements are parameterizable** with unique IDs. This enables dynamic content replacement via the API.

#### Required Setup

Every dynamic element MUST have:

```javascript
{
  parameterizable: true,
  parameterId: "unique_id",  // Unique across template, lowercase with underscores
  parameterType: "text" | "imageUrl" | "videoUrl"
}
```

#### Naming Conventions

| Element Type | parameterId Examples                        | parameterType |
| ------------ | ------------------------------------------- | ------------- |
| Text         | `headline`, `subtitle`, `cta_text`, `price` | `"text"`      |
| Image        | `product_image`, `logo`, `background_image` | `"imageUrl"`  |
| Video        | `hero_video`, `background_video`            | `"videoUrl"`  |

#### Best Practices

1. **Use descriptive IDs:** `product_title` not `text1`
2. **Be consistent:** Use snake_case across all templates
3. **Unique per template:** No duplicate parameterIds on same page
4. **Group logically:** Related elements share naming prefix (e.g., `card_title`, `card_image`)

#### Validation Checklist

Before finalizing any template update:
- [ ] All text elements have `parameterizable: true` and unique `parameterId`
- [ ] All image elements have `parameterizable: true` and unique `parameterId`
- [ ] All video elements have `parameterizable: true` and unique `parameterId`
- [ ] No duplicate parameterIds exist on the same page
- [ ] parameterIds are descriptive and follow snake_case convention

### Design Best Practices

#### Typography Guidelines
- **Font limit:** Use 2-3 fonts maximum per template
- **Hierarchy:** Headings should be 1.5-2x larger than body text
- **Minimum size:** 24px for social media readability
- **Weights:** Headings 600-900 (bold), Body 400-500 (regular)

**Popular font pairings:**
- `Prata` + `Inter`
- `Instrument Serif` + `DM Sans`
- `Playfair Display` + `Lato`
- `Montserrat` + `Open Sans`

**Platform-specific fonts:**
- iOS: `SF Pro Display`, `SF Pro Text`
- Android: `Google Sans`, `Roboto`

#### Color Guidelines
**Luxury/Gold palette:**
- Gold: `#D4AF37`
- Dark gold: `#B8860B`
- Light gold: `#F5E7A3`

**iOS system colors:**
- Blue: `#007AFF`
- Gray: `#8E8E93`
- Background: `#F5F5F7`

**Professional dark:**
- Navy: `#0F172A`
- Slate: `#1E293B`, `#334155`
- Muted: `#64748B`, `#94A3B8`

**Best practices:**
- Ensure 4.5:1 minimum contrast for text readability
- Use gradients sparingly for premium effects
- Consistent color palette (3-5 colors max)

#### Layout Guidelines
- **Edge padding:** 40-60px from canvas edges
- **Element spacing:** 20-40px between elements
- **Alignment:** Center for formal, left for modern
- **Visual flow:** Guide eye with size, color, position

**zIndex ordering:**
- Background images/colors: 1
- Overlay shapes: 2-3
- Text elements: 4-6
- Interactive elements: 7+

#### Common Operations (Design Automation)

**Add text element:**
```javascript
addElement("text", {
  content: "Hello World",
  fontFamily: "Inter",
  fontSize: 48,
  fontWeight: "700",
  color: "#FFFFFF",
  x: 100,
  y: 100,
  width: 400,
  height: 60,
});
```

**Add shape backdrop:**
```javascript
addElement("rectangle", {
  fill: "rgba(0,0,0,0.5)",
  width: 1080,
  height: 200,
  x: 0,
  y: 800,
  borderRadius: "0px",
});
```

**Batch update multiple elements:**
```javascript
batchUpdate([
  {
    elementId: "heading",
    type: "ORSHOT_UPDATE_ELEMENT",
    updates: { style: { fontSize: 72 } },
  },
  {
    elementId: "subtitle",
    type: "ORSHOT_UPDATE_ELEMENT",
    updates: { style: { color: "#94A3B8" } },
  },
  { type: "ORSHOT_UPDATE_CANVAS", updates: { backgroundColor: "#0F172A" } },
]);
```

