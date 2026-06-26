---
title: Z-Order via Children Order
impact: HIGH
impactDescription: Because the `children` array order determines z-order, overlays/badges must be placed last.
tags: layout,z-order,overlay,badge,children
---

## Z-Order via Children Order

In `.pen`, z-order is determined by the order of the `children` array. Children that come later render on top. Overlays, badges, modal backdrops, and similar layers must be placed at the end of `children`, and the container should use `layout: "none"` (absolute positioning).

**Incorrect (Why it's bad):**

- Badge comes first — hidden under the image

```json
{
  "type": "frame",
  "id": "product-card",
  "layout": "vertical",
  "children": [
    {
      "type": "frame",
      "id": "badge-new",
      "fill": "$color.primary",
      "width": 48,
      "height": 24
    },
    {
      "type": "frame",
      "id": "product-img",
      "width": "fill_container",
      "height": 200,
      "fill": {
        "type": "image",
        "url": "product.jpg",
        "mode": "fill"
      }
    },
    {
      "type": "text",
      "id": "product-name",
      "fontWeight": "$font.weight.semibold",
      "content": "Product Name",
      "textGrowth": "auto"
    }
  ]
}
```

**Correct (Why it's good):**

- Badge comes last — renders above the image

```json
{
  "type": "frame",
  "id": "product-card",
  "layout": "none",
  "width": 320,
  "height": 280,
  "children": [
    {
      "type": "frame",
      "id": "card-content",
      "layout": "vertical",
      "x": 0,
      "y": 0,
      "width": 320,
      "height": 280,
      "children": [
        {
          "type": "frame",
          "id": "product-img",
          "width": "fill_container",
          "height": 200,
          "fill": {
            "type": "image",
            "url": "product.jpg",
            "mode": "fill"
          }
        },
        {
          "type": "text",
          "id": "product-name",
          "fontWeight": "$font.weight.semibold",
          "content": "Product Name",
          "fill": "$color.foreground",
          "textGrowth": "auto",
          "fontFamily": "$font.family.body"
        }
      ]
    },
    {
      "type": "frame",
      "id": "badge-new",
      "x": 12,
      "y": 12,
      "width": 48,
      "height": 24,
      "fill": "$color.primary",
      "cornerRadius": "$radius.xs",
      "children": [
        {
          "type": "text",
          "id": "badge-label",
          "fontWeight": "$font.weight.bold",
          "content": "NEW",
          "fill": "$color.on-primary",
          "fontSize": "$font.size.xs",
          "textGrowth": "auto",
          "fontFamily": "$font.family.body"
        }
      ]
    }
  ]
}
```
