---
title: Sizing Mode by Context
impact: CRITICAL
impactDescription: Overuse of fixed px makes responsive layouts impossible.
tags: layout,sizing,responsive,width,height
---

## Sizing Mode by Context

Depending on the role of the element, different size modes must be applied. The principle is that the screen frame is fixed px, section/row is `fill_container`, text block is `fit_content`, and button label is `auto`. If you use fixed px everywhere, it will get cut off or have spaces as the content expands.

**Incorrect (why it's bad):**

```json
{
  "type": "frame",
  "id": "page",
  "width": 1440,
  "height": 900,
  "children": [
    {
      "type": "frame",
      "id": "section-hero",
      "width": 1440,
      "height": 600,
      "children": [
        {
          "type": "text",
          "id": "headline",
          "fontWeight": "$font.weight.bold",
          "width": 600,
          "height": 48,
          "content": "Headline"
        },
        {
          "type": "text",
          "id": "sub",
          "fontWeight": "$font.weight.regular",
          "width": 600,
          "height": 24,
          "content": "Subtitle text"
        }
      ]
    }
  ]
}
```

**Correct (Why it’s good):**

```json
{
  "type": "frame",
  "id": "page",
  "width": 1440,
  "height": 900,
  "children": [
    {
      "type": "frame",
      "id": "section-hero",
      "width": "fill_container",
      "height": "fit_content",
      "layout": "vertical",
      "gap": "$space.lg",
      "padding": [
        "$space.section",
        "$space.page",
        "$space.section",
        "$space.page"
      ],
      "children": [
        {
          "type": "text",
          "id": "headline",
          "fontWeight": "$font.weight.bold",
          "width": "fill_container",
          "height": "fit_content",
          "textGrowth": "auto",
          "content": "Headline",
          "fontFamily": "$font.family.display"
        },
        {
          "type": "text",
          "id": "sub",
          "fontWeight": "$font.weight.regular",
          "width": "fill_container",
          "height": "fit_content",
          "textGrowth": "auto",
          "content": "Subtitle text",
          "fontFamily": "$font.family.display"
        }
      ]
    }
  ]
}
```
