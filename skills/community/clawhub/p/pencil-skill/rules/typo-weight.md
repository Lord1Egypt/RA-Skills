---
title: Font Weight by Role
impact: MEDIUM
impactDescription: Using the same weight for all text removes hierarchy.
tags: typography,font-weight,hierarchy
---

## Font Weight by Role

Font weights should be differentiated by role. Basic rule: body → 400, UI label/caption → 500, subheading/card title → 600, large heading/hero → 700. If everything is 700, nothing stands out; if everything is 400, hierarchy disappears.

**Incorrect (Why it's bad):**

```json
{
  "type": "frame",
  "id": "blog-post",
  "layout": "vertical",
  "children": [
    {
      "type": "text",
      "id": "post-title",
      "content": "Blog Title",
      "fontSize": "$font.size.4xl",
      "fontWeight": "$font.weight.bold"
    },
    {
      "type": "text",
      "id": "post-sub",
      "content": "Subtitle",
      "fontSize": "$font.size.xl",
      "fontWeight": "$font.weight.bold"
    },
    {
      "type": "text",
      "id": "post-date",
      "content": "Jan 12, 2024",
      "fontSize": "$font.size.sm",
      "fontWeight": "$font.weight.bold"
    },
    {
      "type": "text",
      "id": "post-body",
      "content": "Body content goes here",
      "fontSize": "$font.size.base",
      "fontWeight": "$font.weight.bold"
    }
  ]
}
```

**Correct (Why it's good):**

- Large heading — Bold
- Subheading — SemiBold
- UI label — Medium
- Body — Regular

```json
{
  "type": "frame",
  "id": "blog-post",
  "layout": "vertical",
  "gap": "$space.md",
  "children": [
    {
      "type": "text",
      "id": "post-title",
      "content": "Blog Title",
      "fontSize": "$font.size.4xl",
      "fontWeight": "$font.weight.bold",
      "fontFamily": "$font.family.body",
      "textGrowth": "auto"
    },
    {
      "type": "text",
      "id": "post-sub",
      "content": "Subtitle",
      "fontSize": "$font.size.xl",
      "fontWeight": "$font.weight.semibold",
      "fontFamily": "$font.family.body",
      "textGrowth": "auto"
    },
    {
      "type": "text",
      "id": "post-date",
      "content": "Jan 12, 2024",
      "fontSize": "$font.size.sm",
      "fontWeight": "$font.weight.medium",
      "fontFamily": "$font.family.body",
      "textGrowth": "auto",
      "fill": "$color.muted"
    },
    {
      "type": "text",
      "id": "post-body",
      "content": "Body content goes here",
      "fontSize": "$font.size.base",
      "fontWeight": "$font.weight.regular",
      "fontFamily": "$font.family.body",
      "textGrowth": "auto",
      "lineHeight": "$font.lineHeight.body"
    }
  ]
}
```
