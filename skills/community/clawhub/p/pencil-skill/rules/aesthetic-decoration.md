---
title: No Gratuitous Decoration
impact: MEDIUM
impactDescription: Gradient blobs and excessive shadows reduce content focus and make the design look AI-generated.
tags: aesthetic,decoration,shadow,blob,gradient
---

## No Gratuitous Decoration

Blurred gradient blobs in the background, `lg shadow` on every card, and meaningless pattern overlays are stereotypical decorations of AI-generated designs. Create visual distinction with spacing and typography hierarchy, and use shadows minimally only when representing real elevation (cards floating above the background).

**Incorrect (Why it's bad):**

- Meaningless decorative blob

```json
{
  "type": "frame",
  "id": "page-bg",
  "fill": "$color.background",
  "children": [
    {
      "type": "frame",
      "id": "blob-decoration",
      "x": -100,
      "y": -80,
      "width": 600,
      "height": 600,
      "fill": "radial-gradient(circle, #8B5CF640 0%, transparent 70%)"
    },
    {
      "type": "frame",
      "id": "card",
      "fill": "$color.surface",
      "effect": {
        "type": "shadow",
        "shadowType": "outer",
        "offset": {
          "x": 0,
          "y": 20
        },
        "blur": 40,
        "spread": 0,
        "color": "#00000040"
      },
      "cornerRadius": 20
    }
  ]
}
```

**Correct (Why it's good):**

- Minimal shadow used only to express elevation

```json
{
  "type": "frame",
  "id": "page-bg",
  "fill": "$color.background",
  "layout": "vertical",
  "gap": "$space.section",
  "padding": [
    "$space.section",
    "$space.page",
    "$space.section",
    "$space.page"
  ],
  "children": [
    {
      "type": "frame",
      "id": "card",
      "fill": "$color.surface",
      "stroke": {
        "thickness": "$stroke.thickness.default",
        "fill": "$color.border",
        "align": "inside"
      },
      "effect": {
        "type": "shadow",
        "shadowType": "outer",
        "offset": {
          "x": "$effect.shadow.offset.x",
          "y": "$effect.shadow.offset.y"
        },
        "blur": "$effect.shadow.blur",
        "spread": "$effect.shadow.spread",
        "color": "$color.shadow"
      },
      "cornerRadius": "$radius.lg"
    }
  ]
}
```
