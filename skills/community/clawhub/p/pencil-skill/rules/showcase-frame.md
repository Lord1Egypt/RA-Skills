---
title: Create Showcase Frame First
impact: MEDIUM
impactDescription: If there is no design system, build the showcase frame first to systematize tokens and components.
tags: showcase,frame,design-system,setup
---

## Create Showcase Frame First

For a new project without an existing design system, create the showcase frame before building real pages. The showcase frame gathers the color palette, type scale, and component inventory in one place and acts as your design system. If you build pages first without it, token/component reuse becomes difficult.

**Example showcase Frame structure:**

```json
{
  "type": "frame",
  "id": "showcase",
  "name": "_Design System Showcase",
  "layout": "vertical",
  "gap": "$space.section",
  "padding": [
    "$space.section",
    "$space.page",
    "$space.section",
    "$space.page"
  ],
  "fill": "$color.background",
  "children": [
    {
      "type": "frame",
      "id": "section-colors",
      "name": "🎨 Colors",
      "layout": "vertical",
      "gap": "$space.lg",
      "children": [
        {
          "type": "text",
          "id": "colors-title",
          "content": "Color System",
          "fontFamily": "$font.family.display",
          "fontSize": "$font.size.2xl",
          "fontWeight": "$font.weight.bold",
          "textGrowth": "auto"
        },
        {
          "type": "frame",
          "id": "color-swatches",
          "layout": "horizontal",
          "gap": "$space.md",
          "children": [
            {
              "type": "frame",
              "id": "swatch-primary",
              "fill": "$color.primary",
              "width": 80,
              "height": 80,
              "cornerRadius": "$radius.md"
            },
            {
              "type": "frame",
              "id": "swatch-surface",
              "fill": "$color.surface",
              "width": 80,
              "height": 80,
              "cornerRadius": "$radius.md",
              "stroke": {
                "align": "inside",
                "thickness": "$stroke.thickness.default",
                "fill": "$color.border"
              }
            },
            {
              "type": "frame",
              "id": "swatch-foreground",
              "fill": "$color.foreground",
              "width": 80,
              "height": 80,
              "cornerRadius": "$radius.md"
            },
            {
              "type": "frame",
              "id": "swatch-muted",
              "fill": "$color.muted",
              "width": 80,
              "height": 80,
              "cornerRadius": "$radius.md"
            },
            {
              "type": "frame",
              "id": "swatch-destructive",
              "fill": "$color.destructive",
              "width": 80,
              "height": 80,
              "cornerRadius": "$radius.md"
            }
          ]
        }
      ]
    },
    {
      "type": "frame",
      "id": "section-typography",
      "name": "✍️ Typography",
      "layout": "vertical",
      "gap": "$space.sm",
      "children": [
        {
          "type": "text",
          "id": "typo-5xl",
          "content": "Display 5xl — 48px Bold",
          "fontSize": "$font.size.5xl",
          "fontWeight": "$font.weight.bold",
          "fontFamily": "$font.family.display",
          "textGrowth": "auto"
        },
        {
          "type": "text",
          "id": "typo-3xl",
          "content": "Heading 3xl — 30px SemiBold",
          "fontSize": "$font.size.3xl",
          "fontWeight": "$font.weight.semibold",
          "fontFamily": "$font.family.display",
          "textGrowth": "auto"
        },
        {
          "type": "text",
          "id": "typo-base",
          "content": "Body base — 16px Regular. This is sample body text.",
          "fontSize": "$font.size.base",
          "fontWeight": "$font.weight.regular",
          "fontFamily": "$font.family.body",
          "textGrowth": "auto"
        },
        {
          "type": "text",
          "id": "typo-sm",
          "content": "Caption sm — 14px Medium",
          "fontSize": "$font.size.sm",
          "fontWeight": "$font.weight.medium",
          "fontFamily": "$font.family.body",
          "fill": "$color.muted",
          "textGrowth": "auto"
        }
      ]
    },
    {
      "type": "frame",
      "id": "section-components",
      "name": "🧩 Components",
      "layout": "horizontal",
      "gap": "$space.lg",
      "children": [
        {
          "type": "ref",
          "ref": "btn-primary",
          "id": "demo-btn-primary"
        },
        {
          "type": "ref",
          "ref": "btn-secondary",
          "id": "demo-btn-secondary"
        },
        {
          "type": "ref",
          "ref": "btn-ghost",
          "id": "demo-btn-ghost"
        },
        {
          "type": "ref",
          "ref": "badge-default",
          "id": "demo-badge"
        }
      ]
    }
  ]
}
```
