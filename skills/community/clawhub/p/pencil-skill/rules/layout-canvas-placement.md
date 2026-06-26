---
title: Top-level canvas placement — no layer overlap
impact: CRITICAL
impactDescription: Missing top-level coordinates places nodes at (0,0) by default and causes component libraries and showcases to overlap.
tags: layout,canvas,top-level,placement,overlap,bounding-box
---

## Top-level canvas placement — no layer overlap

All top-level nodes in root `children` (reusables, showcase frames, and utility canvases) must define explicit `x` and `y` coordinates and must not overlap each other. In `.pen`, missing top-level coordinates commonly collapse nodes to `(0,0)`, creating invisible stacking and broken handoff.

> **Note:** Top-level canvas coordinates (`x`, `y`) are inherently absolute and are exempt from the "no hardcoded values" token rule. Only colors, spacing, typography, and radii require token references.

Essential rules:
1. Every top-level child node must include `x` and `y`
2. Place reusable components in a dedicated **Component Library** zone (for example, `x = 40` with sufficient vertical spacing)
3. Place showcase frames in a separate zone to the right of the library (for example, `x >= 800`)
4. Keep minimum vertical spacing between sibling nodes: previous node estimated height + at least `80px`
5. After placement, verify absolute bounding boxes do not intersect

Recommended canvas layout pattern:

```text
Canvas Layout:
┌─────────────────────────────────────────────────┐
│  Component Library (x=40)   │  Showcases (x=800+)  │
│  ┌──────────────┐          │  ┌────────────────┐  │
│  │ VoteButton   │ y=40     │  │ Light Showcase │ y=40  │
│  └──────────────┘          │  │ (1440 wide)    │  │
│  ┌──────────────┐          │  └────────────────┘  │
│  │ SidebarItem  │ y=200    │                      │
│  └──────────────┘          │  ┌────────────────┐  │
│  ┌──────────────┐          │  │ Dark Showcase  │ y=1200  │
│  │ NavBar       │ y=320    │  │ (1440 wide)    │  │
│  └──────────────┘          │  └────────────────┘  │
│  ┌──────────────┐          │                      │
│  │ PostCard     │ y=500    │                      │
│  └──────────────┘          │                      │
└─────────────────────────────────────────────────┘
```

**Incorrect (Why it's bad):**

- Top-level nodes are missing `x`, `y`
- All three nodes collapse to `(0,0)` and overlap

```json
{
  "version": "2.8",
  "children": [
    {
      "type": "frame",
      "id": "vote-button",
      "name": "Button/Vote",
      "reusable": true,
      "width": "$component.button.width",
      "height": "$component.button.height",
      "layout": "horizontal",
      "fill": "$color.primary",
      "children": [
        {
          "type": "text",
          "id": "vote-button-label",
          "content": "Vote",
          "fontFamily": "$font.family.body",
          "fontWeight": "$font.weight.semibold",
          "textGrowth": "auto",
          "fill": "$color.on-primary"
        }
      ]
    },
    {
      "type": "frame",
      "id": "sidebar-item",
      "name": "Sidebar/Item",
      "reusable": true,
      "width": "$component.sidebar.item.width",
      "height": "$component.sidebar.item.height",
      "layout": "horizontal",
      "fill": "$color.surface"
    },
    {
      "type": "frame",
      "id": "showcase-light",
      "name": "Showcase/Light",
      "width": "$layout.showcase.width",
      "height": "$layout.showcase.height",
      "layout": "vertical",
      "fill": "$color.background",
      "children": [
        {
          "type": "text",
          "id": "showcase-light-title",
          "content": "Light Theme Showcase",
          "fontFamily": "$font.family.display",
          "fontWeight": "$font.weight.bold",
          "textGrowth": "auto",
          "fill": "$color.foreground"
        }
      ]
    }
  ]
}
```

**Correct (Why it's good):**

- Every top-level node has explicit `x`, `y`
- Component library and showcase zones are separated on canvas
- Vertical spacing is preserved, preventing collisions

```json
{
  "version": "2.8",
  "children": [
    {
      "type": "frame",
      "id": "vote-button",
      "name": "Button/Vote",
      "reusable": true,
      "x": 40,
      "y": 40,
      "width": "$component.button.width",
      "height": "$component.button.height",
      "layout": "horizontal",
      "fill": "$color.primary",
      "children": [
        {
          "type": "text",
          "id": "vote-button-label",
          "content": "Vote",
          "fontFamily": "$font.family.body",
          "fontWeight": "$font.weight.semibold",
          "textGrowth": "auto",
          "fill": "$color.on-primary"
        }
      ]
    },
    {
      "type": "frame",
      "id": "sidebar-item",
      "name": "Sidebar/Item",
      "reusable": true,
      "x": 40,
      "y": 200,
      "width": "$component.sidebar.item.width",
      "height": "$component.sidebar.item.height",
      "layout": "horizontal",
      "fill": "$color.surface"
    },
    {
      "type": "frame",
      "id": "showcase-light",
      "name": "Showcase/Light",
      "x": 800,
      "y": 40,
      "width": "$layout.showcase.width",
      "height": "$layout.showcase.height",
      "layout": "vertical",
      "fill": "$color.background",
      "children": [
        {
          "type": "text",
          "id": "showcase-light-title",
          "content": "Light Theme Showcase",
          "fontFamily": "$font.family.display",
          "fontWeight": "$font.weight.bold",
          "textGrowth": "auto",
          "fill": "$color.foreground"
        }
      ]
    },
    {
      "type": "frame",
      "id": "showcase-dark",
      "name": "Showcase/Dark",
      "x": 800,
      "y": 1200,
      "width": "$layout.showcase.width",
      "height": "$layout.showcase.height",
      "layout": "vertical",
      "fill": "$color.background-inverse",
      "children": [
        {
          "type": "text",
          "id": "showcase-dark-title",
          "content": "Dark Theme Showcase",
          "fontFamily": "$font.family.display",
          "fontWeight": "$font.weight.bold",
          "textGrowth": "auto",
          "fill": "$color.foreground-inverse"
        }
      ]
    }
  ]
}
```