---
title: No Hardcoded Values — Use Tokens
impact: CRITICAL
impactDescription: Using direct values in fill, fontSize, and padding breaks overall consistency and makes maintenance unmanageable.
tags: tokens,hardcode,fill,fontSize,spacing
---

## No Hardcoded Values — Use Tokens

Use token references (`$`) for all design properties, including `fill`, `fontSize`, `padding`, `gap`, and `cornerRadius`. If you write literal values like `"#3B82F6"`, `16`, or `"bold"` directly, changing brand color or scale later requires hunting through the entire file.

**Incorrect (Why it's bad):**

```json
{
  "type": "frame",
  "id": "hero-section",
  "fill": "#EFF6FF",
  "padding": [
    64,
    120,
    64,
    120
  ],
  "layout": "vertical",
  "gap": 32,
  "children": [
    {
      "type": "text",
      "id": "hero-title",
      "content": "Product Name",
      "fontSize": 48,
      "fontWeight": "700",
      "fill": "#111827",
      "lineHeight": 1.1
    },
    {
      "type": "frame",
      "id": "cta-btn",
      "fill": "#3B82F6",
      "cornerRadius": 8,
      "padding": [
        12,
        24,
        12,
        24
      ]
    }
  ]
}
```

**Correct (Why it's good):**

```json
{
  "type": "frame",
  "id": "hero-section",
  "fill": "$color.background",
  "padding": [
    "$space.section",
    "$space.page",
    "$space.section",
    "$space.page"
  ],
  "layout": "vertical",
  "gap": "$space.xl",
  "children": [
    {
      "type": "text",
      "id": "hero-title",
      "content": "Product Name",
      "fontSize": "$font.size.5xl",
      "fontWeight": "$font.weight.bold",
      "fill": "$color.foreground",
      "lineHeight": "$font.lineHeight.display",
      "textGrowth": "auto",
      "fontFamily": "$font.family.display"
    },
    {
      "type": "frame",
      "id": "cta-btn",
      "fill": "$color.primary",
      "cornerRadius": "$radius.md",
      "padding": [
        "$space.sm",
        "$space.lg",
        "$space.sm",
        "$space.lg"
      ]
    }
  ]
}
```
