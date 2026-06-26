---
title: Forbidden Spacing Patterns
impact: HIGH
impactDescription: Empty frame spacers and inconsistent values make layouts hard to understand and maintain.
tags: spacing,forbidden,spacer,hardcode
---

## Forbidden Spacing Patterns

The three patterns below are strictly forbidden: (1) empty frames as spacers, (2) arbitrary values not multiples of 4 (13, 30, 7, etc.), and (3) placing children directly in containers without padding. These patterns hide layout intent and create a maintenance nightmare when you later have to find and fix every spacer.

**Incorrect (Why it's bad):**

- ❌ Empty frame spacer
- ❌ Not a multiple of 4
- ❌ Inconsistent gap

```json
{
  "type": "frame",
  "id": "marketing-section",
  "layout": "vertical",
  "gap": 0,
  "children": [
    {
      "type": "text",
      "id": "eyebrow",
      "fontWeight": "$font.weight.medium",
      "content": "Intro"
    },
    {
      "type": "frame",
      "id": "spacer1",
      "height": 7
    },
    {
      "type": "text",
      "id": "headline",
      "fontWeight": "$font.weight.bold",
      "content": "Product Title"
    },
    {
      "type": "frame",
      "id": "spacer2",
      "height": 30
    },
    {
      "type": "frame",
      "id": "card-row",
      "layout": "horizontal",
      "gap": 13,
      "children": [
        {
          "type": "frame",
          "id": "c1",
          "width": 300,
          "height": 200
        },
        {
          "type": "frame",
          "id": "c2",
          "width": 300,
          "height": 200
        }
      ]
    }
  ]
}
```

**Correct (Why it's good):**

- Handle all spacing with gap, no spacers
- Consistent token-based gap

```json
{
  "type": "frame",
  "id": "marketing-section",
  "layout": "vertical",
  "gap": "$space.xl",
  "padding": [
    "$space.section",
    "$space.page",
    "$space.section",
    "$space.page"
  ],
  "children": [
    {
      "type": "text",
      "id": "eyebrow",
      "fontWeight": "$font.weight.medium",
      "content": "Intro",
      "textGrowth": "auto",
      "fontFamily": "$font.family.display"
    },
    {
      "type": "text",
      "id": "headline",
      "fontWeight": "$font.weight.bold",
      "content": "Product Title",
      "textGrowth": "auto",
      "fontFamily": "$font.family.display"
    },
    {
      "type": "frame",
      "id": "card-row",
      "layout": "horizontal",
      "gap": "$space.xl",
      "children": [
        {
          "type": "frame",
          "id": "c1",
          "width": "fill_container",
          "height": 200
        },
        {
          "type": "frame",
          "id": "c2",
          "width": "fill_container",
          "height": 200
        }
      ]
    }
  ]
}
```
