---
title: Padding by Element Type
impact: MEDIUM
impactDescription: Using the same padding on every element erases hierarchy—buttons feel like cards, and cards feel like pages.
tags: spacing,padding,button,card,section
---

## Padding by Element Type

Padding should vary by element type. Small elements (buttons) need small padding, containers (cards) medium, sections large, and page-level containers largest. If everything uses `padding: 16`, elements of different scale look visually identical.

**Incorrect (Why it's bad):**

```json
{
  "type": "frame",
  "id": "page",
  "padding": [
    16,
    16,
    16,
    16
  ],
  "children": [
    {
      "type": "frame",
      "id": "section",
      "padding": [
        16,
        16,
        16,
        16
      ],
      "children": [
        {
          "type": "frame",
          "id": "card",
          "padding": [
            16,
            16,
            16,
            16
          ],
          "children": [
            {
              "type": "frame",
              "id": "btn",
              "padding": [
                16,
                16,
                16,
                16
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

**Correct (Why it's good):**

- Page horizontal: 120px
- Section vertical: 96px
- Card: 24px on all sides
- Button: 8px vertical, 16px horizontal
- Badge: 4px vertical, 8px horizontal

```json
{
  "type": "frame",
  "id": "page",
  "padding": [
    0,
    "$space.page",
    0,
    "$space.page"
  ],
  "children": [
    {
      "type": "frame",
      "id": "section",
      "padding": [
        "$space.section",
        0,
        "$space.section",
        0
      ],
      "children": [
        {
          "type": "frame",
          "id": "card",
          "padding": [
            "$space.xl",
            "$space.xl",
            "$space.xl",
            "$space.xl"
          ],
          "children": [
            {
              "type": "frame",
              "id": "btn-primary",
              "padding": [
                "$space.sm",
                "$space.lg",
                "$space.sm",
                "$space.lg"
              ]
            },
            {
              "type": "frame",
              "id": "badge",
              "padding": [
                "$space.xs",
                "$space.sm",
                "$space.xs",
                "$space.sm"
              ]
            }
          ]
        }
      ]
    }
  ]
}
```
