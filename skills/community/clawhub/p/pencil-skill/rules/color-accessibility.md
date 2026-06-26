---
title: WCAG 2.1 AA Contrast Ratio
impact: CRITICAL
impactDescription: Low-contrast text is unreadable to the visually impaired and violates legal accessibility standards.
tags: color,accessibility,WCAG,contrast,a11y
---

## WCAG 2.1 AA Contrast Ratio

Plain text requires a contrast ratio of **4.5:1 or higher** compared to the background, and large text (18px bold or higher) requires a contrast ratio of **3:1 or higher**. Writing light gray text on a white background or purple text on a blue background is an inadequate contrast ratio. When defining tokens, verify the contrast ratio for both light and dark.

**Incorrect (why it's bad):**

- #C0C0C0 on #FFFFFF = Contrast 1.5:1 — FAIL
- #9CA3AF on #FFFFFF = Contrast 2.5:1 — FAIL

```json
{
  "type": "frame",
  "id": "card",
  "fill": "#FFFFFF",
  "children": [
    {
      "type": "text",
      "id": "label",
      "fontWeight": "$font.weight.medium",
      "content": "Product Category",
      "fill": "#C0C0C0",
      "fontSize": "$font.size.sm"
    },
    {
      "type": "text",
      "id": "price",
      "fontWeight": "$font.weight.bold",
      "content": "$29.00",
      "fill": "#9CA3AF",
      "fontSize": "$font.size.lg"
    }
  ]
}
```

**Correct (Why it’s good):**

- $color.muted = #6B7280 on #FFFFFF = Contrast 4.6:1 — AA PASS
- $color.foreground = #111827 on #FFFFFF = Contrast 16:1 — AAA PASS

```json
{
  "type": "frame",
  "id": "card",
  "fill": "$color.background",
  "children": [
    {
      "type": "text",
      "id": "label",
      "fontWeight": "$font.weight.medium",
      "content": "Product Category",
      "fill": "$color.muted",
      "fontSize": "$font.size.sm",
      "textGrowth": "auto",
      "fontFamily": "$font.family.body"
    },
    {
      "type": "text",
      "id": "price",
      "fontWeight": "$font.weight.bold",
      "content": "$29.00",
      "fill": "$color.foreground",
      "fontSize": "$font.size.lg",
      "textGrowth": "auto",
      "fontFamily": "$font.family.body"
    }
  ]
}
```
