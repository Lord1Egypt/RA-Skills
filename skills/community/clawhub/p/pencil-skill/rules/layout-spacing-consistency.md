---
title: Gap/Padding Only — No Spacer Frames
impact: HIGH
impactDescription: Empty frame spacers are hard to maintain and pollute the layout hierarchy.
tags: layout,spacing,gap,padding,spacer
---

## Gap/Padding Only — No Spacer Frames

Never use empty frames (spacers) to create spacing. All spacing must be expressed using only the parent frame's `gap` or `padding` properties. Empty spacers increase child count, hurt readability, and force you to find and edit every spacer later when adjusting spacing.

**Incorrect (Why it's bad):**

- Empty frame for spacing

```json
{
  "type": "frame",
  "id": "form",
  "layout": "vertical",
  "children": [
    {
      "type": "frame",
      "id": "field-email",
      "width": "fill_container",
      "height": 48
    },
    {
      "type": "frame",
      "id": "spacer-1",
      "width": "fill_container",
      "height": 24
    },
    {
      "type": "frame",
      "id": "field-password",
      "width": "fill_container",
      "height": 48
    },
    {
      "type": "frame",
      "id": "spacer-2",
      "width": "fill_container",
      "height": 24
    },
    {
      "type": "frame",
      "id": "btn-submit",
      "width": "fill_container",
      "height": 44
    }
  ]
}
```

**Correct (Why it's good):**

```json
{
  "type": "frame",
  "id": "form",
  "layout": "vertical",
  "gap": "$space.lg",
  "padding": [
    "$space.xl",
    "$space.xl",
    "$space.xl",
    "$space.xl"
  ],
  "width": "fill_container",
  "children": [
    {
      "type": "frame",
      "id": "field-email",
      "width": "fill_container",
      "height": 48
    },
    {
      "type": "frame",
      "id": "field-password",
      "width": "fill_container",
      "height": 48
    },
    {
      "type": "frame",
      "id": "btn-submit",
      "width": "fill_container",
      "height": 44
    }
  ]
}
```
