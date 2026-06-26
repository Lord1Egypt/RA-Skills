---
title: 4pt/8pt Grid System
impact: HIGH
impactDescription: Inconsistent spacing values break visual consistency and make design-dev handoff difficult.
tags: spacing,grid,8pt,consistency
---

## 4pt/8pt Grid System

All gap, padding, and margin values must be multiples of 4. Allowed values: `4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96`. Arbitrary odd values like `gap: 13` or `padding: 17` are forbidden. Following this rule keeps designs aligned to the grid and easier to implement in CSS.

**Incorrect (Why it's bad):**

```json
{
  "type": "frame",
  "id": "form-card",
  "layout": "vertical",
  "gap": 13,
  "padding": [
    15,
    17,
    15,
    17
  ],
  "children": [
    {
      "type": "frame",
      "id": "input-group",
      "layout": "vertical",
      "gap": 7
    },
    {
      "type": "frame",
      "id": "btn-row",
      "layout": "horizontal",
      "gap": 11
    }
  ]
}
```

**Correct (Why it's good):**

```bash
# CLI command (run in terminal)
node scripts/set-variables.mjs design.pen --var '<name>=<type>:<value>'
```

```json
[
  {
    "variables": {
      "space.xs": {
        "type": "number",
        "value": 4
      },
      "space.sm": {
        "type": "number",
        "value": 8
      },
      "space.md": {
        "type": "number",
        "value": 12
      },
      "space.lg": {
        "type": "number",
        "value": 16
      },
      "space.xl": {
        "type": "number",
        "value": 24
      },
      "space.2xl": {
        "type": "number",
        "value": 32
      },
      "space.3xl": {
        "type": "number",
        "value": 48
      },
      "space.section": {
        "type": "number",
        "value": 96
      },
      "space.page": {
        "type": "number",
        "value": 120
      }
    }
  },
  {
    "type": "frame",
    "id": "form-card",
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
        "id": "input-group",
        "layout": "vertical",
        "gap": "$space.md"
      },
      {
        "type": "frame",
        "id": "btn-row",
        "layout": "horizontal",
        "gap": "$space.sm"
      }
    ]
  }
]
```
