---
title: Use Semantic Color Tokens
impact: CRITICAL
impactDescription: Using raw palette color names makes theme switching and rebranding impractical.
tags: tokens,color,semantic,palette
---

## Use Semantic Color Tokens

Color tokens must use semantic names like `$color.primary`, `$color.surface`, `$color.foreground`, not raw palette names like `$color.blue500`. Required semantic colors: `background`, `surface`, `foreground`, `muted`, `primary`, `on-primary`, `border`, `destructive`. With semantic naming, dark mode only requires swapping values.

**Incorrect (Why it's bad):**

```json
{
  "type": "frame",
  "id": "card",
  "fill": "#F9FAFB",
  "stroke": {
    "align": "inside",
    "thickness": 1,
    "fill": "#E5E7EB"
  },
  "children": [
    {
      "type": "text",
      "id": "title",
      "fontWeight": "$font.weight.bold",
      "fill": "#111827",
      "content": "Card Title"
    },
    {
      "type": "text",
      "id": "sub",
      "fontWeight": "$font.weight.regular",
      "fill": "#9CA3AF",
      "content": "Subtitle"
    },
    {
      "type": "frame",
      "id": "btn",
      "fill": "#3B82F6",
      "children": [
        {
          "type": "text",
          "id": "btn-label",
          "fontWeight": "$font.weight.semibold",
          "fill": "#FFFFFF",
          "content": "Confirm"
        }
      ]
    }
  ]
}
```

**Correct (Why it's good):**

```json
{
  "type": "frame",
  "id": "card",
  "fill": "$color.surface",
  "stroke": {
    "thickness": "$stroke.thickness.default",
    "fill": "$color.border",
    "align": "inside"
  },
  "children": [
    {
      "type": "text",
      "id": "title",
      "fontWeight": "$font.weight.bold",
      "fill": "$color.foreground",
      "content": "Card Title",
      "textGrowth": "auto",
      "fontFamily": "$font.family.display"
    },
    {
      "type": "text",
      "id": "sub",
      "fontWeight": "$font.weight.regular",
      "fill": "$color.muted",
      "content": "Subtitle",
      "textGrowth": "auto",
      "fontFamily": "$font.family.body"
    },
    {
      "type": "frame",
      "id": "btn",
      "fill": "$color.primary",
      "children": [
        {
          "type": "text",
          "id": "btn-label",
          "fontWeight": "$font.weight.semibold",
          "fill": "$color.on-primary",
          "content": "Confirm",
          "textGrowth": "auto",
          "fontFamily": "$font.family.body"
        }
      ]
    }
  ]
}
```
