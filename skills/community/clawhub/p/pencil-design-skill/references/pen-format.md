# .pen File Format Reference

> **Applies to**: Mode A (Direct File Writing) + Mode B (MCP Tools)
> **Priority**: Core document — read before writing any `.pen` file
> **See also**: [design-tokens.md](design-tokens.md) · [overflow-prevention.md](overflow-prevention.md)

This document is the **single source of truth** for `.pen` file JSON format, distilled from all example files. **Do NOT read files in the `examples/` directory** unless debugging a specific format error.

## Top-Level Structure

```json
{
  "version": "2.8",
  "children": [ ... ],
  "themes": { ... },
  "variables": { ... }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `version` | Yes | Always `"2.8"` |
| `children` | Yes | Array of top-level nodes (frames, prompts, text) |
| `themes` | No | Theme axis definitions (for multi-theme support) |
| `variables` | No | Design token definitions |

## Node Types

All nodes have `type`, `id`, and optionally `name`.

| type | Description | Key Properties |
|------|-------------|----------------|
| `frame` | Container/layout node (the core building block) | layout, children, fill, stroke, cornerRadius, padding, gap |
| `text` | Text content | content, fontFamily, fontSize, fontWeight, lineHeight |
| `icon_font` | Icon from icon font library | iconFontName, iconFontFamily, fill |
| `ref` | Instance of a reusable component | ref (target component id), descendants |
| `rectangle` | Rectangle shape | fill, cornerRadius, stroke |
| `ellipse` | Ellipse/circle shape | fill, stroke |
| `line` | Line element | stroke |
| `prompt` | AI design prompt | content, model |

## ID Format

IDs are **5-character alphanumeric short codes**: `"MzSDs"`, `"PV1ln"`, `"6xhgh"`.
Use similar short random IDs when creating new nodes. Avoid descriptive IDs longer than ~12 chars.

## Frame Node (Most Important)

```json
{
  "type": "frame",
  "id": "abc12",
  "name": "Card",
  "clip": true,
  "reusable": true,
  "width": 360,
  "height": 200,
  "fill": "$--background",
  "cornerRadius": 6,
  "stroke": { ... },
  "effect": { ... },
  "opacity": 0.8,
  "enabled": true,
  "layout": "vertical",
  "gap": 16,
  "padding": [16, 24],
  "justifyContent": "center",
  "alignItems": "center",
  "children": [ ... ],
  "slot": ["child1", "child2"],
  "theme": { "Mode": "Dark" }
}
```

### Layout

| Value | Behavior |
|-------|----------|
| `"vertical"` | Children stack top-to-bottom (flex-column) |
| `"horizontal"` | Children flow left-to-right (flex-row). **This is the default when `layout` is omitted.** |
| `"none"` | Absolute positioning — children use `x`/`y` coordinates |

### Size

| Form | Example | Description |
|------|---------|-------------|
| number | `360` | Fixed pixel size |
| `"fill_container"` | — | Stretch to fill parent |
| `"fill_container(N)"` | `"fill_container(480)"` | Fill parent, default/fallback N px |
| `"fit_content"` | — | Shrink to content |
| `"fit_content(N)"` | `"fit_content(900)"` | Fit content, min-height N px |

### Padding

| Form | Example | Meaning |
|------|---------|---------|
| number | `16` | All sides equal |
| `[v, h]` | `[8, 16]` | Vertical, Horizontal |
| `[t, r, b, l]` | `[8, 6, 8, 32]` | Top, Right, Bottom, Left |

### Gap

```json
"gap": 16       // spacing between children (can be negative: -1)
```

### Alignment

| Property | Values |
|----------|--------|
| `justifyContent` | `"center"`, `"end"`, `"space_between"` |
| `alignItems` | `"center"` |

### Position (only in `layout: "none"` parent)

```json
"x": 200, "y": 100
```

## Fill

```json
// 1. Solid color (string)
"fill": "#0C0C0C"

// 2. Variable reference
"fill": "$--background"

// 3. Color object (with enabled toggle)
"fill": { "type": "color", "color": "$--white", "enabled": false }

// 4. Image fill
"fill": { "type": "image", "enabled": true, "url": "https://...", "mode": "fill" }

// 5. Gradient fill
"fill": {
  "type": "gradient",
  "gradientType": "linear",
  "enabled": true,
  "rotation": 135,
  "size": { "height": 1 },
  "colors": [
    { "color": "#FF5C00", "position": 0 },
    { "color": "#FF8C40", "position": 1 }
  ]
}

// 6. No fill
"fill": []
```

## Stroke

```json
"stroke": {
  "align": "inside",          // "inside" | "outside" | "center"
  "thickness": 1,             // uniform
  "fill": "$--border"         // stroke color (string or variable)
}

// Single-side stroke:
"stroke": {
  "align": "inside",
  "thickness": { "right": 1 }   // or "bottom", "top", "left"
}

// With join/cap:
"stroke": { "align": "inside", "thickness": 1, "join": "round", "cap": "round" }
```

## Corner Radius

```json
"cornerRadius": 6                                          // uniform
"cornerRadius": "$--radius-pill"                           // variable ref
"cornerRadius": [6, 0, 0, 6]                              // [topLeft, topRight, bottomRight, bottomLeft]
"cornerRadius": ["$--radius-pill", 0, 0, "$--radius-pill"] // mixed
```

## Effect (Shadow)

```json
// Single shadow
"effect": {
  "type": "shadow",
  "shadowType": "outer",
  "color": "#0000000d",
  "offset": { "x": 0, "y": 1 },
  "blur": 1.75,
  "spread": -1
}

// Multiple shadows
"effect": [ { ... }, { ... } ]

// No effects
"effect": []
```

## Text Node

```json
{
  "type": "text",
  "id": "txt01",
  "name": "Heading",
  "fill": "$--foreground",
  "content": "Hello World",
  "fontFamily": "Inter",               // or "$--font-primary"
  "fontSize": 14,
  "fontWeight": "normal",              // "normal" | "500" | "600" | "700"
  "lineHeight": 1.4285714285714286,    // multiplier
  "letterSpacing": -0.5,               // optional
  "textAlign": "center",               // "center" | "right" (default: left)
  "textAlignVertical": "middle",       // "middle" | "bottom"
  "textGrowth": "fixed-width",         // "fixed-width" | "auto"
  "width": "fill_container",           // use with textGrowth: "fixed-width"
  "textDecoration": "underline",       // optional
  "opacity": 0.6,                      // optional
  "maxLines": 2                        // optional, truncation
}
```

**Key rule**: For text inside auto-layout frames, always use `"width": "fill_container"` with `"textGrowth": "fixed-width"` to prevent overflow.

## Icon Font Node

```json
{
  "type": "icon_font",
  "id": "ico01",
  "width": 16,
  "height": 16,
  "iconFontName": "hexagon",        // Lucide icon name
  "iconFontFamily": "lucide",       // always "lucide"
  "fill": "$--foreground"
}
```

Common icon sizes: 12, 16, 20, 24. When inside `layout: "none"` parent, add `x`/`y`.

Common Lucide icons: `hexagon`, `plus`, `check`, `chevron-right`, `chevron-down`, `chevrons-up-down`, `search`, `x`, `ellipsis`, `mail`, `lock`, `eye`, `eye-off`, `github`, `arrow-right`, `star`, `heart`, `settings`, `user`, `home`, `menu`

## Ref Node (Component Instance)

```json
// Basic ref
{
  "type": "ref",
  "id": "ref01",
  "ref": "VSnC2",                    // ID of reusable: true component
  "x": 200, "y": 100                // position (in layout: "none" parent)
}

// Ref with overrides
{
  "type": "ref",
  "id": "ref02",
  "ref": "VSnC2",
  "reusable": true,                  // ref itself can be reusable
  "name": "Button/Primary",
  "width": "fill_container",
  "descendants": {
    "Tr3Fv": { "content": "Submit" },       // override text content
    "SlKX1": { "iconFontName": "check" },   // override icon
    "soROh": { "enabled": false }            // hide a child
  }
}

// Ref with children replacement (for slots)
{
  "type": "ref",
  "id": "ref03",
  "ref": "ctKFD",
  "children": [
    { "type": "icon_font", "id": "ico99", ... }
  ]
}
```

## Reusable Components

Mark a frame as reusable to make it available for `ref` instances:

```json
{
  "type": "frame",
  "id": "VSnC2",
  "name": "Button/Default",
  "reusable": true,
  ...
}
```

## Slot

Declare replaceable child positions in a frame:

```json
{
  "type": "frame",
  "slot": ["childId1", "childId2"],
  "children": [...]
}
```

## Variables

### Variable Types

| Type | Example Value |
|------|---------------|
| `"color"` | `"#fafafa"`, `"#09090b"` |
| `"number"` | `999`, `6`, `0` |
| `"string"` | `"Inter"`, `"Geist"` |

### Variable Reference Syntax

Prefix `$` before variable name: `"$--background"`, `"$--radius-pill"`, `"$--font-primary"`

Can be used in: `fill`, `stroke.fill`, `cornerRadius`, `fontFamily`

### Variable Definition

```json
"variables": {
  "--background": {
    "type": "color",
    "value": "#fafafa"
  },
  "--radius-pill": {
    "type": "number",
    "value": 999
  },
  "--font-primary": {
    "type": "string",
    "value": "Inter"
  }
}
```

### Themed Variables (multi-value)

```json
"--background": {
  "type": "color",
  "value": [
    { "value": "#fafafa" },
    { "value": "#09090b", "theme": { "Mode": "Dark" } },
    { "value": "#09090b", "theme": { "Mode": "Dark", "Base": "Zinc" } }
  ]
}
```

First entry without `theme` = default. Entries with `theme` = overrides for that theme combination.

## Themes

```json
"themes": {
  "Mode": ["Light", "Dark"],
  "Base": ["Neutral", "Gray", "Slate", "Stone", "Zinc"]
}
```

For simple Light/Dark only:
```json
"themes": {
  "Mode": ["Light", "Dark"]
}
```

Apply a theme to a frame:
```json
{
  "type": "frame",
  "theme": { "Mode": "Dark", "Base": "Zinc" }
}
```

## Shadcn Dark Zinc Variables (Default Template)

Use this complete variables block for the default Shadcn Dark style:

```json
"themes": {
  "Mode": ["Light", "Dark"]
},
"variables": {
  "--background":            { "type": "color", "value": [{ "value": "#fafafa" }, { "value": "#09090b", "theme": { "Mode": "Dark" } }] },
  "--foreground":            { "type": "color", "value": [{ "value": "#0a0a0a" }, { "value": "#fafafa", "theme": { "Mode": "Dark" } }] },
  "--card":                  { "type": "color", "value": [{ "value": "#fafafa" }, { "value": "#18181b", "theme": { "Mode": "Dark" } }] },
  "--card-foreground":       { "type": "color", "value": [{ "value": "#0a0a0a" }, { "value": "#fafafa", "theme": { "Mode": "Dark" } }] },
  "--popover":               { "type": "color", "value": [{ "value": "#fafafa" }, { "value": "#18181b", "theme": { "Mode": "Dark" } }] },
  "--popover-foreground":    { "type": "color", "value": [{ "value": "#0a0a0a" }, { "value": "#fafafa", "theme": { "Mode": "Dark" } }] },
  "--primary":               { "type": "color", "value": [{ "value": "#18181b" }, { "value": "#fafafa", "theme": { "Mode": "Dark" } }] },
  "--primary-foreground":    { "type": "color", "value": [{ "value": "#fafafa" }, { "value": "#18181b", "theme": { "Mode": "Dark" } }] },
  "--secondary":             { "type": "color", "value": [{ "value": "#f4f4f5" }, { "value": "#27272a", "theme": { "Mode": "Dark" } }] },
  "--secondary-foreground":  { "type": "color", "value": [{ "value": "#18181b" }, { "value": "#fafafa", "theme": { "Mode": "Dark" } }] },
  "--muted":                 { "type": "color", "value": [{ "value": "#f4f4f5" }, { "value": "#27272a", "theme": { "Mode": "Dark" } }] },
  "--muted-foreground":      { "type": "color", "value": [{ "value": "#71717a" }, { "value": "#a1a1aa", "theme": { "Mode": "Dark" } }] },
  "--accent":                { "type": "color", "value": [{ "value": "#f4f4f5" }, { "value": "#27272a", "theme": { "Mode": "Dark" } }] },
  "--accent-foreground":     { "type": "color", "value": [{ "value": "#18181b" }, { "value": "#fafafa", "theme": { "Mode": "Dark" } }] },
  "--destructive":           { "type": "color", "value": [{ "value": "#ef4444" }, { "value": "#7f1d1d", "theme": { "Mode": "Dark" } }] },
  "--border":                { "type": "color", "value": [{ "value": "#e4e4e7" }, { "value": "#27272a", "theme": { "Mode": "Dark" } }] },
  "--input":                 { "type": "color", "value": [{ "value": "#e4e4e7" }, { "value": "#27272a", "theme": { "Mode": "Dark" } }] },
  "--ring":                  { "type": "color", "value": [{ "value": "#18181b" }, { "value": "#d4d4d8", "theme": { "Mode": "Dark" } }] },
  "--white":                 { "type": "color", "value": "#ffffff" },
  "--black":                 { "type": "color", "value": "#000000" }
}
```

## Common Component Patterns

### Button

```json
{
  "type": "frame",
  "id": "btn01",
  "name": "Button/Default",
  "reusable": true,
  "fill": "$--primary",
  "cornerRadius": 6,
  "gap": 6,
  "padding": [10, 16],
  "justifyContent": "center",
  "alignItems": "center",
  "children": [
    {
      "type": "text",
      "id": "btxt1",
      "name": "Button Label",
      "fill": "$--primary-foreground",
      "content": "Button",
      "lineHeight": 1.43,
      "textAlign": "center",
      "textAlignVertical": "middle",
      "fontFamily": "Inter",
      "fontSize": 14,
      "fontWeight": "500"
    }
  ]
}
```

Button variants by fill:
- **Default/Primary**: `fill: "$--primary"`, text: `"$--primary-foreground"`
- **Secondary**: `fill: "$--secondary"`, text: `"$--secondary-foreground"`
- **Destructive**: `fill: "$--destructive"`, text: `"$--white"`
- **Outline**: `fill: "$--background"`, `stroke.fill: "$--border"`, text: `"$--foreground"`
- **Ghost**: `fill` disabled/empty, text: `"$--foreground"`

Button sizes:
- **Default**: `padding: [10, 16]`, fontSize 14
- **Large**: `padding: [8, 24]`, fontSize 14
- **Small**: `padding: [6, 12]`, fontSize 13

### Input Group (Label + Input)

```json
{
  "type": "frame",
  "id": "ig001",
  "name": "Input Group",
  "width": "fill_container",
  "layout": "vertical",
  "gap": 6,
  "children": [
    {
      "type": "text",
      "id": "lbl01",
      "name": "Label",
      "fill": "$--foreground",
      "textGrowth": "fixed-width",
      "width": "fill_container",
      "content": "Email",
      "lineHeight": 1.43,
      "fontFamily": "Inter",
      "fontSize": 14,
      "fontWeight": "500"
    },
    {
      "type": "frame",
      "id": "inp01",
      "name": "Input",
      "width": "fill_container",
      "height": 40,
      "fill": "$--background",
      "cornerRadius": 6,
      "stroke": { "align": "inside", "thickness": 1, "fill": "$--input" },
      "gap": 8,
      "padding": [10, 12],
      "alignItems": "center",
      "children": [
        {
          "type": "text",
          "id": "ph001",
          "name": "Placeholder",
          "fill": "$--muted-foreground",
          "content": "Enter your email...",
          "lineHeight": 1.43,
          "fontFamily": "Inter",
          "fontSize": 14,
          "fontWeight": "normal"
        }
      ]
    }
  ]
}
```

### Card

```json
{
  "type": "frame",
  "id": "crd01",
  "name": "Card",
  "width": 360,
  "fill": "$--card",
  "cornerRadius": 8,
  "stroke": { "align": "inside", "thickness": 1, "fill": "$--border" },
  "layout": "vertical",
  "padding": 24,
  "gap": 16,
  "children": [ ... ]
}
```

### Divider (OR separator)

```json
{
  "type": "frame",
  "id": "div01",
  "name": "Divider",
  "width": "fill_container",
  "gap": 16,
  "alignItems": "center",
  "children": [
    { "type": "frame", "id": "dl001", "width": "fill_container", "height": 1, "fill": "$--border" },
    { "type": "text", "id": "dt001", "fill": "$--muted-foreground", "content": "OR", "fontSize": 12, "fontWeight": "500", "fontFamily": "Inter", "lineHeight": 1.4 },
    { "type": "frame", "id": "dr001", "width": "fill_container", "height": 1, "fill": "$--border" }
  ]
}
```

## Complete Minimal .pen File Template

```json
{
  "version": "2.8",
  "children": [
    {
      "type": "frame",
      "id": "scrn1",
      "name": "Screen Name",
      "theme": { "Mode": "Dark" },
      "clip": true,
      "width": 1440,
      "height": 900,
      "fill": "$--background",
      "layout": "vertical",
      "children": [ ... ]
    }
  ],
  "themes": {
    "Mode": ["Light", "Dark"]
  },
  "variables": {
    ...shadcn dark zinc variables from above...
  }
}
```

Common screen sizes:
- Desktop: `1440×900`, `1920×1080`
- Tablet: `768×1024`
- Mobile: `375×812`, `393×852`
