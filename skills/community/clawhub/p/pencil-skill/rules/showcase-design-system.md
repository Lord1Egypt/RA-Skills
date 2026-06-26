---
title: Leverage Existing Design System
impact: HIGH
impactDescription: Ignoring the design system and rebuilding from scratch breaks consistency and doubles effort.
tags: showcase,design-system,reusable,search-nodes
---

## Leverage Existing Design System

Before starting design work, always search existing components with `search-nodes --reusable` and reuse them. If Button, Card, Nav, and others already exist, recreating them causes style mismatches. Instantiate existing components via `ref`.

**Incorrect (Why it's bad):**

Creating a new card immediately without search-nodes

```json
{
  "type": "frame",
  "id": "new-product-card",
  "fill": "#F9FAFB",
  "cornerRadius": 12,
  "padding": [
    20,
    20,
    20,
    20
  ],
  "layout": "vertical",
  "gap": 12,
  "children": [
    {
      "type": "text",
      "id": "card-title",
      "content": "Product Name",
      "fontSize": 18,
      "fontWeight": "600"
    },
    {
      "type": "text",
      "id": "card-price",
      "content": "$29.00",
      "fontSize": 16
    },
    {
      "type": "frame",
      "id": "new-btn",
      "fill": "#3B82F6",
      "children": [
        {
          "type": "text",
          "id": "btn-label",
          "content": "Buy Now",
          "fill": "#FFFFFF"
        }
      ]
    }
  ]
}
```

**Correct (Why it's good):**

Step 1: Search existing reusable items (run CLI search-nodes)

```bash
node scripts/search-nodes.mjs design.pen --name "card" --reusable
node scripts/search-nodes.mjs design.pen --name "button" --reusable
```

Step 2: Found `card-product` in search results → create instance via `ref`

```json
[
  {
    "type": "ref",
    "ref": "card-product",
    "id": "product-card-1",
    "descendants": {
      "card-title": {
        "content": "Product Name"
      },
      "card-price": {
        "content": "$29.00"
      },
      "cta-btn": {
        "type": "ref",
        "ref": "btn-primary",
        "id": "cta-btn",
        "descendants": {
          "label": {
            "content": "Buy Now"
          }
        }
      }
    }
  }
]
```