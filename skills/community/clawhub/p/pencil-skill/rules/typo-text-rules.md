---
title: Text Column Width & Alignment Rules
impact: MEDIUM
impactDescription: Overly wide text columns cause reading fatigue, and centered body text reduces readability.
tags: typography,line-length,alignment,letter-spacing
---

## Text Column Width & Alignment Rules

Optimal readability for body text is about 65–75 characters per line. If `widthMode: "fill_container"` text stretches across full 1440px width, lines become too long to read comfortably. Constrain max width for body containers, default to left alignment (except right-to-left languages), and add `letterSpacing` for uppercase text.

**Incorrect (Why it's bad):**

```json
{
  "type": "frame",
  "id": "article-section",
  "width": "fill_container",
  "layout": "vertical",
  "padding": [
    "$space.section",
    "$space.page",
    "$space.section",
    "$space.page"
  ],
  "children": [
    {
      "type": "text",
      "id": "article-body",
      "fontWeight": "$font.weight.regular",
      "width": "fill_container",
      "textGrowth": "fixed-width",
      "textAlign": "center",
      "content": "Centered body copy across the full 1440px width. Lines are too long to read comfortably, and centered paragraphs make line starts harder to track."
    }
  ]
}
```

**Correct (Why it's good):**

- Max width 672px ≈ about 70 characters
- Add letterSpacing to uppercase

```json
{
  "type": "frame",
  "id": "article-section",
  "width": "fill_container",
  "layout": "vertical",
  "padding": [
    "$space.section",
    "$space.page",
    "$space.section",
    "$space.page"
  ],
  "children": [
    {
      "type": "frame",
      "id": "text-column",
      "width": 672,
      "layout": "vertical",
      "gap": "$space.lg",
      "children": [
        {
          "type": "text",
          "id": "eyebrow",
          "content": "CATEGORY",
          "textAlign": "left",
          "letterSpacing": 2,
          "fontSize": "$font.size.sm",
          "fontWeight": "$font.weight.medium",
          "fill": "$color.primary",
          "textGrowth": "auto",
          "fontFamily": "$font.family.display"
        },
        {
          "type": "text",
          "id": "article-body",
          "fontWeight": "$font.weight.regular",
          "width": "fill_container",
          "textGrowth": "fixed-width",
          "textAlign": "left",
          "lineHeight": "$font.lineHeight.body",
          "content": "Constrained width and left alignment ensure optimal readability.",
          "fontFamily": "$font.family.body"
        }
      ]
    }
  ],
  "alignItems": "center"
}
```
