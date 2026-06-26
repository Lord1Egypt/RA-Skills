---
title: Aesthetic Typography — Display + Body Pairing
impact: HIGH
impactDescription: Same as using Inter alone Weight repetition creates a flat UI with no hierarchy.
tags: aesthetic,typography,font-pairing,weight
---

## Aesthetic Typography — Display + Body Pairing

It is a typical AI pattern to use Inter in all text and vary only the fontSize. Combine display fonts (Playfair Display, Fraunces, etc.) with body fonts (Source Sans 3, DM Sans, etc.), and use various weights of 400/500/600/700 to suit the role.

**Incorrect (why it's bad):**

```json
{
  "type": "frame",
  "id": "article",
  "layout": "vertical",
  "gap": "$space.md",
  "children": [
    {
      "type": "text",
      "id": "h1",
      "content": "title",
      "fontFamily": "Inter",
      "fontSize": "$font.size.4xl",
      "fontWeight": "700"
    },
    {
      "type": "text",
      "id": "h2",
      "content": "subtitle",
      "fontFamily": "Inter",
      "fontSize": "$font.size.2xl",
      "fontWeight": "700"
    },
    {
      "type": "text",
      "id": "body",
      "content": "body text",
      "fontFamily": "Inter",
      "fontSize": "$font.size.base",
      "fontWeight": "700"
    },
    {
      "type": "text",
      "id": "caption",
      "content": "caption",
      "fontFamily": "Inter",
      "fontSize": "$font.size.sm",
      "fontWeight": "700"
    }
  ]
}
```

**Correct (Why it’s good):**

```json
{
  "type": "frame",
  "id": "article",
  "layout": "vertical",
  "gap": "$space.md",
  "children": [
    {
      "type": "text",
      "id": "h1",
      "content": "title",
      "fontFamily": "$font.family.display",
      "fontSize": "$font.size.4xl",
      "fontWeight": "$font.weight.bold",
      "lineHeight": "$font.lineHeight.display",
      "fill": "$color.foreground",
      "textGrowth": "auto"
    },
    {
      "type": "text",
      "id": "h2",
      "content": "subtitle",
      "fontFamily": "$font.family.display",
      "fontSize": "$font.size.2xl",
      "fontWeight": "$font.weight.semibold",
      "lineHeight": "$font.lineHeight.heading",
      "fill": "$color.foreground",
      "textGrowth": "auto"
    },
    {
      "type": "text",
      "id": "body",
      "content": "body text",
      "fontFamily": "$font.family.body",
      "fontSize": "$font.size.base",
      "fontWeight": "$font.weight.regular",
      "lineHeight": "$font.lineHeight.body",
      "fill": "$color.foreground",
      "textGrowth": "auto"
    },
    {
      "type": "text",
      "id": "caption",
      "content": "caption",
      "fontFamily": "$font.family.body",
      "fontSize": "$font.size.sm",
      "fontWeight": "$font.weight.regular",
      "lineHeight": "$font.lineHeight.caption",
      "fill": "$color.muted",
      "textGrowth": "auto"
    }
  ]
}
```
