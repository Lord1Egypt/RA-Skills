---
title: Prevent overlap between elements
impact: CRITICAL
impactDescription: Without width calculation and placement rules between sibling elements, feeds/sidebars overlap in 3-column layouts.
tags: layout,no-overlap,three-column,auto-layout,overflow
---

## Prevent overlap between elements

The most common causes of sibling elements overlapping in a three-column layout are overuse of `fit_content`, omission of `gap`, unverified width summation, and absolute coordinate placement. Be sure to place sibling frames using Auto Layout, and specify the `width` of each column as a fixed value or `fill_container`. Only overlays/modals allow the `layout: "none"` + z-order exception.

Essential rules:
1. In a three-column layout, each column must specify `width` as a fixed value or `fill_container` (parallel placement of `fit_content` is prohibited)
2. Parent frame requires `layout: "horizontal"` + `gap`
3. Calculate column width sum + gap so that it does not exceed the parent width
4. Do not use `x`, `y` absolute coordinates for sibling placement (Auto Layout required)
5. Overlay/modal only exception (see z-order rules)

**Incorrect (why it's bad):**

```json
{
  "type": "frame",
  "id": "layout-shell",
  "width": "$layout.page.width",
  "height": "fit_content",
  "layout": "none",
  "children": [
    {
      "type": "frame",
      "id": "left-sidebar",
      "x": 0,
      "y": 0,
      "width": "fit_content",
      "height": "fit_content",
      "layout": "vertical",
      "children": [
        {
          "type": "text",
          "id": "left-title",
          "content": "my community",
          "fontFamily": "$font.family.body",
          "fontWeight": "$font.weight.semibold",
          "textGrowth": "auto",
          "fill": "$color.foreground"
        }
      ]
    },
    {
      "type": "frame",
      "id": "feed-column",
      "x": 220,
      "y": 0,
      "width": "fit_content",
      "height": "fit_content",
      "layout": "vertical",
      "children": [
        {
          "type": "text",
          "id": "feed-title",
          "content": "feed",
          "fontFamily": "$font.family.display",
          "fontWeight": "$font.weight.semibold",
          "textGrowth": "auto",
          "fill": "$color.foreground"
        }
      ]
    },
    {
      "type": "frame",
      "id": "right-sidebar",
      "x": 980,
      "y": 0,
      "width": "fit_content",
      "height": "fit_content",
      "layout": "vertical",
      "children": [
        {
          "type": "text",
          "id": "right-title",
          "content": "Trending",
          "fontFamily": "$font.family.body",
          "fontWeight": "$font.weight.semibold",
          "textGrowth": "auto",
          "fill": "$color.foreground"
        }
      ]
    }
  ]
}
```

**Correct (Why it’s good):**

```json
{
  "type": "frame",
  "id": "layout-shell",
  "width": "$layout.page.width",
  "height": "fit_content",
  "layout": "horizontal",
  "gap": "$space.section",
  "padding": [
    "$space.section",
    "$space.section",
    "$space.section",
    "$space.section"
  ],
  "alignItems": "start",
  "children": [
    {
      "type": "frame",
      "id": "left-sidebar",
      "width": "$layout.sidebar.left",
      "height": "fit_content",
      "layout": "vertical",
      "gap": "$space.md",
      "children": [
        {
          "type": "text",
          "id": "left-title",
          "content": "my community",
          "fontFamily": "$font.family.body",
          "fontWeight": "$font.weight.semibold",
          "textGrowth": "auto",
          "fill": "$color.foreground"
        }
      ]
    },
    {
      "type": "frame",
      "id": "feed-column",
      "width": "fill_container",
      "height": "fit_content",
      "layout": "vertical",
      "gap": "$space.lg",
      "children": [
        {
          "type": "text",
          "id": "feed-title",
          "content": "feed",
          "fontFamily": "$font.family.display",
          "fontWeight": "$font.weight.semibold",
          "textGrowth": "auto",
          "fill": "$color.foreground"
        }
      ]
    },
    {
      "type": "frame",
      "id": "right-sidebar",
      "width": "$layout.sidebar.right",
      "height": "fit_content",
      "layout": "vertical",
      "gap": "$space.md",
      "children": [
        {
          "type": "text",
          "id": "right-title",
          "content": "Trending",
          "fontFamily": "$font.family.body",
          "fontWeight": "$font.weight.semibold",
          "textGrowth": "auto",
          "fill": "$color.foreground"
        }
      ]
    }
  ]
}
```

Width verification example:
- `left(200) + center(fill) + right(280) + gap(32 * 2) + padding(32 * 2) <= parent(1440)`
- The fixed width sum and spacing must be confirmed first so the central `fill_container` can safely occupy the remaining space.
