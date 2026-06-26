---
title: Proximity — Varied Gap by Relationship
impact: MEDIUM
impactDescription: If all spacing is identical, relationships between elements (within-group vs between-groups) are not visually clear.
tags: spacing,proximity,gap,grouping,gestalt
---

## Proximity — Varied Gap by Relationship

Set small gaps between related elements, medium gaps between groups, and large gaps between sections. If you use `gap: 16` everywhere, icon-label spacing looks the same as card-to-card spacing, so relationships disappear. Implement Gestalt Proximity through spacing.

**Incorrect (Why it's bad):**

```json
{
  "type": "frame",
  "id": "feature-card",
  "layout": "vertical",
  "gap": 16,
  "children": [
    {
      "type": "frame",
      "id": "icon-row",
      "layout": "horizontal",
      "gap": 16,
      "children": [
        {
          "type": "frame",
          "id": "icon",
          "width": 24,
          "height": 24,
          "fill": {
            "type": "image",
            "url": "icon.svg",
            "mode": "fill"
          }
        },
        {
          "type": "text",
          "id": "icon-label",
          "fontWeight": "$font.weight.medium",
          "content": "Fast deployment"
        }
      ]
    },
    {
      "type": "text",
      "id": "card-title",
      "fontWeight": "$font.weight.bold",
      "content": "One-click deployment"
    },
    {
      "type": "text",
      "id": "card-desc",
      "fontWeight": "$font.weight.regular",
      "content": "This is descriptive text."
    }
  ]
}
```

**Correct (Why it's good):**

- Between sections inside card: 16px
- Between icon and label: 4px (tightly grouped)
- Between title and description: 8px (same content block)

```json
{
  "type": "frame",
  "id": "feature-card",
  "layout": "vertical",
  "gap": "$space.lg",
  "padding": [
    "$space.xl",
    "$space.xl",
    "$space.xl",
    "$space.xl"
  ],
  "children": [
    {
      "type": "frame",
      "id": "icon-row",
      "layout": "horizontal",
      "gap": "$space.xs",
      "children": [
        {
          "type": "frame",
          "id": "icon",
          "width": 20,
          "height": 20,
          "fill": {
            "type": "image",
            "url": "icon.svg",
            "mode": "fill"
          }
        },
        {
          "type": "text",
          "id": "icon-label",
          "fontWeight": "$font.weight.medium",
          "content": "Fast deployment",
          "fontSize": "$font.size.sm",
          "fill": "$color.primary",
          "textGrowth": "auto",
          "fontFamily": "$font.family.body"
        }
      ]
    },
    {
      "type": "frame",
      "id": "card-text",
      "layout": "vertical",
      "gap": "$space.sm",
      "children": [
        {
          "type": "text",
          "id": "card-title",
          "content": "One-click deployment",
          "fontSize": "$font.size.xl",
          "fontWeight": "$font.weight.semibold",
          "textGrowth": "auto",
          "fontFamily": "$font.family.display"
        },
        {
          "type": "text",
          "id": "card-desc",
          "fontWeight": "$font.weight.regular",
          "content": "This is descriptive text.",
          "fontSize": "$font.size.base",
          "fill": "$color.muted",
          "textGrowth": "auto",
          "fontFamily": "$font.family.body"
        }
      ]
    }
  ]
}
```
