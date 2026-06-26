---
title: Declare Content Slots
impact: MEDIUM
impactDescription: Components with hard-coded content cannot be reused and must be created anew each time.
tags: component,slot,reusable,children
---

## Declare Content Slots

Components whose content changes (cards, modals, list items, etc.) must declare their content area as `slot`. If you hard-code the title and description directly inside the card, it cannot be reused at all when you need a card with different content. Declare `slot: ["content"]` and inject it as children in the ref instance.

**Incorrect (why it's bad):**

```json
{
  "id": "card-default",
  "name": "Card/Default",
  "type": "frame",
  "layout": "vertical",
  "gap": "$space.md",
  "padding": [
    "$space.lg",
    "$space.lg",
    "$space.lg",
    "$space.lg"
  ],
  "children": [
    {
      "type": "text",
      "id": "title",
      "fontWeight": "$font.weight.bold",
      "content": "Card title hardcoding"
    },
    {
      "type": "text",
      "id": "body",
      "fontWeight": "$font.weight.regular",
      "content": "Card body hardcoding"
    },
    {
      "type": "frame",
      "id": "footer"
    }
  ]
}
```

**Correct (Why it’s good):**

- Inject content into slot from instance

```json
[
  {
    "id": "card-default",
    "name": "Card/Default",
    "type": "frame",
    "layout": "vertical",
    "gap": "$space.md",
    "padding": [
      "$space.lg",
      "$space.lg",
      "$space.lg",
      "$space.lg"
    ],
    "fill": "$color.surface",
    "cornerRadius": "$radius.lg",
    "stroke": {
      "align": "inside",
      "thickness": "$stroke.thickness.default",
      "fill": "$color.border"
    },
    "slot": [
      "header",
      "content",
      "footer"
    ],
    "children": [
      {
        "type": "frame",
        "id": "slot-header",
        "name": "header",
        "width": "fill_container"
      },
      {
        "type": "frame",
        "id": "slot-content",
        "name": "content",
        "width": "fill_container"
      },
      {
        "type": "frame",
        "id": "slot-footer",
        "name": "footer",
        "width": "fill_container"
      }
    ]
  },
  {
    "type": "ref",
    "ref": "card-default",
    "id": "feature-card-1",
    "children": [
      {
        "type": "text",
        "id": "header-title",
        "name": "header",
        "content": "Real-time collaboration",
        "fontFamily": "$font.family.display",
        "fontSize": "$font.size.xl",
        "fontWeight": "$font.weight.semibold",
        "textGrowth": "auto"
      },
      {
        "type": "text",
        "id": "content-desc",
        "fontWeight": "$font.weight.regular",
        "name": "content",
        "content": "Edit simultaneously with your teammates.",
        "fontFamily": "$font.family.body",
        "fill": "$color.muted",
        "textGrowth": "auto"
      },
      {
        "type": "ref",
        "ref": "btn-ghost",
        "id": "footer-learn-more",
        "name": "footer"
      }
    ]
  }
]
```
