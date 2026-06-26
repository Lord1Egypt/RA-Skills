---
title: 60-30-10 Color Ratio
impact: MEDIUM
impactDescription: An even distribution of colors creates a visually distracting and distracting design.
tags: color,ratio,palette,balance
---

## 60-30-10 Color Ratio

Color distribution follows the 60-30-10 ratio. 60% neutral (background, surface), 30% secondary (section background, secondary UI), 10% primary accent (CTA button, link, emphasis). If the five colors are evenly distributed, it results in a distracting design where you don't know where to focus your attention.

**Incorrect (why it's bad):**

- blue
- purple
- pink
- yellow
- Green

```json
{
  "type": "frame",
  "id": "home",
  "layout": "vertical",
  "children": [
    {
      "type": "frame",
      "id": "nav",
      "fill": "#3B82F6",
      "height": "fit_content"
    },
    {
      "type": "frame",
      "id": "hero",
      "fill": "#8B5CF6",
      "height": 500
    },
    {
      "type": "frame",
      "id": "features",
      "fill": "#EC4899",
      "height": 400
    },
    {
      "type": "frame",
      "id": "testimonial",
      "fill": "#F59E0B",
      "height": 300
    },
    {
      "type": "frame",
      "id": "cta",
      "fill": "#10B981",
      "height": 300
    }
  ]
}
```

**Correct (Why it’s good):**

- 60% — Neutral background
- 60% neutral
- 30% surface — differentiated but neutral series
- 30% surface
- 10% primary accent — Emphasize only the CTA

```json
{
  "type": "frame",
  "id": "home",
  "layout": "vertical",
  "fill": "$color.background",
  "children": [
    {
      "type": "frame",
      "id": "nav",
      "fill": "$color.background"
    },
    {
      "type": "frame",
      "id": "hero",
      "fill": "$color.background"
    },
    {
      "type": "frame",
      "id": "features",
      "fill": "$color.surface"
    },
    {
      "type": "frame",
      "id": "cta-section",
      "fill": "$color.surface",
      "children": [
        {
          "type": "frame",
          "id": "cta-btn",
          "fill": "$color.primary"
        }
      ]
    }
  ]
}
```
