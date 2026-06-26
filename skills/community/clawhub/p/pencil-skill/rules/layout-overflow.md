---
title: Prevent Text Overflow
impact: CRITICAL
impactDescription: If textGrowth is missing, the text will exceed the container and the UI will break.
tags: layout,overflow,text,textGrowth
---

## Prevent Text Overflow

Text nodes must have the `textGrowth` property specified. If you only have a fixed `width` and no `textGrowth`, long text will either spill out of the container or be truncated. Set the width to `fill_container` and `textGrowth` to `"fixed-width"` to get word wrapping to work.

**Incorrect (why it's bad):**

```json
{
  "type": "frame",
  "id": "description-block",
  "layout": "vertical",
  "width": 480,
  "children": [
    {
      "type": "text",
      "id": "desc",
      "fontWeight": "$font.weight.regular",
      "width": 480,
      "height": 20,
      "fontSize": "$font.size.base",
      "content": "This text is very long and may not fit on one line."
    }
  ]
}
```

**Correct (Why it’s good):**

```json
{
  "type": "frame",
  "id": "description-block",
  "layout": "vertical",
  "gap": "$space.sm",
  "width": "fill_container",
  "children": [
    {
      "type": "text",
      "id": "desc",
      "fontWeight": "$font.weight.regular",
      "width": "fill_container",
      "height": "fit_content",
      "textGrowth": "fixed-width",
      "fontSize": "$font.size.base",
      "lineHeight": 1.6,
      "fill": "$color.foreground",
      "content": "This text is very long and may not fit on one line.",
      "fontFamily": "$font.family.body"
    }
  ]
}
```
