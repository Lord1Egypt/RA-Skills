---
title: Break AI Layout Patterns
impact: HIGH
impactDescription: Avoid the typical AI layout of hero → 3 cards → CTA → footer and maintain visual interest.
tags: aesthetic,layout,anti-ai,visual-hierarchy
---

## Break AI Layout Patterns

The pattern of centering all elements and repeating three rows of cards with equal padding is typical of AI-generated design. Add variation to the visual flow by using asymmetrical two-column layouts, varying section heights, full-bleed images, and offset grids.

**Incorrect (why it's bad):**

- Center aligned hero
- Center aligned CTA

```json
{
  "type": "frame",
  "id": "page",
  "layout": "vertical",
  "align": "center",
  "children": [
    {
      "type": "frame",
      "id": "hero",
      "width": "fill_container",
      "height": 600
    },
    {
      "type": "frame",
      "id": "features",
      "layout": "horizontal",
      "children": [
        {
          "type": "frame",
          "id": "card1",
          "width": 400,
          "height": 300
        },
        {
          "type": "frame",
          "id": "card2",
          "width": 400,
          "height": 300
        },
        {
          "type": "frame",
          "id": "card3",
          "width": 400,
          "height": 300
        }
      ]
    },
    {
      "type": "frame",
      "id": "cta",
      "width": "fill_container",
      "height": 300
    }
  ]
}
```

**Correct (Why it’s good):**

```json
{
  "type": "frame",
  "id": "page",
  "layout": "vertical",
  "gap": 0,
  "children": [
    {
      "type": "frame",
      "id": "hero-asymmetric",
      "layout": "horizontal",
      "width": "fill_container",
      "height": 700,
      "children": [
        {
          "type": "frame",
          "id": "hero-text",
          "width": 560,
          "layout": "vertical",
          "gap": "$space.xl",
          "padding": [
            "$space.section",
            "$space.page",
            "$space.section",
            "$space.page"
          ]
        },
        {
          "type": "frame",
          "id": "hero-img",
          "width": "fill_container",
          "height": "fill_container",
          "fill": {
            "type": "image",
            "url": "hero.jpg",
            "mode": "fill"
          }
        }
      ]
    },
    {
      "type": "frame",
      "id": "feature-offset",
      "layout": "horizontal",
      "width": "fill_container",
      "height": "fit_content",
      "padding": [
        "$space.section",
        "$space.page",
        "$space.section",
        "$space.page"
      ],
      "gap": "$space.xl",
      "children": [
        {
          "type": "frame",
          "id": "feature-large",
          "width": 640,
          "height": 480
        },
        {
          "type": "frame",
          "id": "feature-stack",
          "layout": "vertical",
          "gap": "$space.lg",
          "width": "fill_container",
          "children": [
            {
              "type": "frame",
              "id": "feature-sm-1",
              "width": "fill_container",
              "height": 220
            },
            {
              "type": "frame",
              "id": "feature-sm-2",
              "width": "fill_container",
              "height": 220
            }
          ]
        }
      ]
    }
  ]
}
```
