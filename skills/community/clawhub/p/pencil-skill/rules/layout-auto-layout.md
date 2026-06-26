---
title: Auto Layout Required
impact: CRITICAL
impactDescription: If all containers do not have Auto Layout, overflow and alignment collapse will occur.
tags: layout,auto-layout,overflow
---

## Auto Layout Required

All container frames must specify the `layout` attribute. If `layout: "none"`, children overlap with absolute coordinates, and the layout will be broken when content is changed. Enable automatic alignment with `layout: "vertical"` or `"horizontal"` + `gap`.

**Incorrect (why it's bad):**

```json
{
  "type": "frame",
  "id": "card-container",
  "layout": "none",
  "width": 360,
  "height": 200,
  "children": [
    {
      "type": "text",
      "id": "title",
      "fontWeight": "$font.weight.bold",
      "x": 16,
      "y": 16,
      "content": "title"
    },
    {
      "type": "text",
      "id": "body",
      "fontWeight": "$font.weight.regular",
      "x": 16,
      "y": 48,
      "content": "text"
    },
    {
      "type": "frame",
      "id": "btn",
      "x": 16,
      "y": 160,
      "width": 120,
      "height": 36
    }
  ]
}
```

**Correct (Why it’s good):**

```json
{
  "type": "frame",
  "id": "card-container",
  "layout": "vertical",
  "gap": "$space.md",
  "padding": [
    "$space.lg",
    "$space.lg",
    "$space.lg",
    "$space.lg"
  ],
  "width": 360,
  "height": "fit_content",
  "children": [
    {
      "type": "text",
      "id": "title",
      "fontWeight": "$font.weight.bold",
      "content": "title",
      "fill": "$color.foreground",
      "textGrowth": "auto",
      "fontFamily": "$font.family.display"
    },
    {
      "type": "text",
      "id": "body",
      "fontWeight": "$font.weight.regular",
      "content": "text",
      "fill": "$color.muted",
      "textGrowth": "auto",
      "fontFamily": "$font.family.body"
    },
    {
      "type": "frame",
      "id": "btn",
      "width": "fill_container",
      "height": 36
    }
  ]
}
```
