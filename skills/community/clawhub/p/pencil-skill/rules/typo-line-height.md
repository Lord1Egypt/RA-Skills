---
title: Line Height by Text Size
impact: MEDIUM
impactDescription: Using the same line-height for all text makes large headings too loose and body text too tight.
tags: typography,line-height,readability
---

## Line Height by Text Size

Line height should vary by text size. As a rule: large display text tight (1.1), body text loose (1.6), captions medium (1.4). If all text uses `lineHeight: 1.5`, display headings feel cramped and body readability suffers.

**Incorrect (Why it's bad):**

```json
{
  "type": "frame",
  "id": "content",
  "layout": "vertical",
  "children": [
    {
      "type": "text",
      "id": "display",
      "fontWeight": "$font.weight.bold",
      "fontSize": "$font.size.5xl",
      "lineHeight": 1.5,
      "content": "Large Hero Title",
      "textGrowth": "auto"
    },
    {
      "type": "text",
      "id": "heading",
      "fontWeight": "$font.weight.semibold",
      "fontSize": "$font.size.3xl",
      "lineHeight": 1.5,
      "content": "Section Title",
      "textGrowth": "auto"
    },
    {
      "type": "text",
      "id": "body",
      "fontWeight": "$font.weight.regular",
      "fontSize": "$font.size.base",
      "lineHeight": 1.5,
      "content": "Body text appears across multiple lines",
      "textGrowth": "auto"
    },
    {
      "type": "text",
      "id": "caption",
      "fontWeight": "$font.weight.regular",
      "fontSize": "$font.size.xs",
      "lineHeight": 1.5,
      "content": "Caption",
      "textGrowth": "auto"
    }
  ]
}
```

**Correct (Why it's good):**

```bash
# CLI command (run in terminal)
node scripts/set-variables.mjs design.pen --var '<name>=<type>:<value>'
```

- display — 48px+ large headings
- heading — 24~36px subheadings
- subheading — 18~20px
- body — 14~16px body text
- caption — 12px captions

```json
[
  {
    "variables": {
      "font.lineHeight.display": {
        "type": "number",
        "value": 1.1
      },
      "font.lineHeight.heading": {
        "type": "number",
        "value": 1.2
      },
      "font.lineHeight.subheading": {
        "type": "number",
        "value": 1.35
      },
      "font.lineHeight.body": {
        "type": "number",
        "value": 1.6
      },
      "font.lineHeight.caption": {
        "type": "number",
        "value": 1.4
      }
    }
  },
  {
    "type": "frame",
    "id": "content",
    "layout": "vertical",
    "children": [
      {
        "type": "text",
        "id": "display",
        "fontWeight": "$font.weight.bold",
        "fontFamily": "$font.family.display",
        "fontSize": "$font.size.5xl",
        "lineHeight": "$font.lineHeight.display",
        "content": "Large Hero Title",
        "textGrowth": "auto"
      },
      {
        "type": "text",
        "id": "heading",
        "fontWeight": "$font.weight.semibold",
        "fontFamily": "$font.family.display",
        "fontSize": "$font.size.3xl",
        "lineHeight": "$font.lineHeight.heading",
        "content": "Section Title",
        "textGrowth": "auto"
      },
      {
        "type": "text",
        "id": "body",
        "fontWeight": "$font.weight.regular",
        "fontFamily": "$font.family.body",
        "fontSize": "$font.size.base",
        "lineHeight": "$font.lineHeight.body",
        "content": "Body text appears across multiple lines",
        "textGrowth": "auto"
      },
      {
        "type": "text",
        "id": "caption",
        "fontWeight": "$font.weight.regular",
        "fontFamily": "$font.family.body",
        "fontSize": "$font.size.xs",
        "lineHeight": "$font.lineHeight.caption",
        "content": "Caption",
        "textGrowth": "auto"
      }
    ]
  }
]
```
