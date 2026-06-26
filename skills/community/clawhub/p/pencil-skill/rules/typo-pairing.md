---
title: Font Pairing — Display + Body
impact: MEDIUM
impactDescription: Using only a single font creates flat typography with weak hierarchy and little personality.
tags: typography,font-pairing,display,body
---

## Font Pairing — Display + Body

Combining a Display font (hero/headings) with a Body font (body/UI) creates visual hierarchy and brand character. Using Inter everywhere is a common AI-pattern default. Choose one of the recommended pairings below or define a custom pairing with the same principle.

### Recommended font pairings

| Display (for headings) | Body (for body/UI) | Style |
|-----------------|----------------|------|
| Playfair Display | Source Sans 3 | Classic · Editorial |
| Fraunces | DM Sans | Modern · Editorial |
| Cormorant Garamond | Inter | Luxury · Minimal |
| JetBrains Mono | Inter | Tech · Developer Tool |
| Syne | Figtree | Creative · Bold |

**Incorrect (Why it's bad):**

```json
{
  "type": "frame",
  "id": "landing",
  "children": [
    {
      "type": "text",
      "id": "h1",
      "fontFamily": "Inter",
      "fontSize": "$font.size.5xl"
    },
    {
      "type": "text",
      "id": "h2",
      "fontFamily": "Inter",
      "fontSize": "$font.size.2xl"
    },
    {
      "type": "text",
      "id": "body",
      "fontFamily": "Inter",
      "fontSize": "$font.size.base"
    },
    {
      "type": "text",
      "id": "label",
      "fontFamily": "Inter",
      "fontSize": "$font.size.sm"
    }
  ]
}
```

**Correct (Why it's good):**

- Display font — large headings
- Display font — subheadings
- Body font — body text
- Body font — UI labels

```json
{
  "type": "frame",
  "id": "landing",
  "children": [
    {
      "type": "text",
      "id": "h1",
      "fontFamily": "$font.family.display",
      "fontSize": "$font.size.5xl",
      "fontWeight": "$font.weight.bold",
      "lineHeight": "$font.lineHeight.display",
      "textGrowth": "auto"
    },
    {
      "type": "text",
      "id": "h2",
      "fontFamily": "$font.family.display",
      "fontSize": "$font.size.2xl",
      "fontWeight": "$font.weight.semibold",
      "lineHeight": "$font.lineHeight.heading",
      "textGrowth": "auto"
    },
    {
      "type": "text",
      "id": "body",
      "fontFamily": "$font.family.body",
      "fontSize": "$font.size.base",
      "fontWeight": "$font.weight.regular",
      "lineHeight": "$font.lineHeight.body",
      "textGrowth": "auto"
    },
    {
      "type": "text",
      "id": "label",
      "fontFamily": "$font.family.body",
      "fontSize": "$font.size.sm",
      "fontWeight": "$font.weight.medium",
      "textGrowth": "auto"
    }
  ]
}
```
