---
title: Variants as Separate Reusables
impact: HIGH
impactDescription: Putting conditional branches on a single component complicates reuse and increases maintenance costs.
tags: component,variant,reusable
---

## Variants as Separate Reusables

Variants with different styles, such as Primary/Secondary/Ghost variants of buttons, are implemented separately as reusable. It is prohibited to include conditional branches such as `if variant === 'primary'` in one component. Making each variant independently reusable simplifies instance creation and clarifies the intent.

**Incorrect (why it's bad):**

- Branching to variant props — increased complexity

```json
{
  "id": "button",
  "type": "frame",
  "reusable": true,
  "props": {
    "variant": "primary"
  },
  "children": [
    {
      "type": "text",
      "id": "label",
      "content": "button",
      "fill": {
        "if_prop_variant_primary": "$color.on-primary",
        "else": "$color.primary"
      }
    }
  ]
}
```

**Correct (Why it’s good):**

```json
[
  {
    "id": "btn-primary",
    "name": "Button/Primary",
    "type": "frame",
    "reusable": true,
    "layout": "horizontal",
    "fill": "$color.primary",
    "cornerRadius": "$radius.md",
    "padding": [
      "$space.sm",
      "$space.lg",
      "$space.sm",
      "$space.lg"
    ],
    "children": [
      {
        "type": "text",
        "id": "label",
        "content": "button",
        "fill": "$color.on-primary",
        "fontSize": "$font.size.base",
        "fontWeight": "$font.weight.medium",
        "fontFamily": "$font.family.body",
        "textGrowth": "auto"
      }
    ]
  },
  {
    "id": "btn-secondary",
    "name": "Button/Secondary",
    "type": "frame",
    "reusable": true,
    "layout": "horizontal",
    "fill": "transparent",
    "stroke": {
      "thickness": "$stroke.thickness.default",
      "fill": "$color.primary",
      "align": "inside"
    },
    "cornerRadius": "$radius.md",
    "padding": [
      "$space.sm",
      "$space.lg",
      "$space.sm",
      "$space.lg"
    ],
    "children": [
      {
        "type": "text",
        "id": "label",
        "content": "button",
        "fill": "$color.primary",
        "fontSize": "$font.size.base",
        "fontWeight": "$font.weight.medium",
        "fontFamily": "$font.family.body",
        "textGrowth": "auto"
      }
    ]
  },
  {
    "id": "btn-ghost",
    "name": "Button/Ghost",
    "type": "frame",
    "reusable": true,
    "layout": "horizontal",
    "fill": "transparent",
    "cornerRadius": "$radius.md",
    "padding": [
      "$space.sm",
      "$space.lg",
      "$space.sm",
      "$space.lg"
    ],
    "children": [
      {
        "type": "text",
        "id": "label",
        "content": "button",
        "fill": "$color.foreground",
        "fontSize": "$font.size.base",
        "fontWeight": "$font.weight.medium",
        "fontFamily": "$font.family.body",
        "textGrowth": "auto"
      }
    ]
  }
]
```
