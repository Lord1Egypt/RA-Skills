# UI Component Patterns

These are commonly used component structure patterns in `.pen` files.

## Button

```json
{
  "type": "frame",
  "id": "btn-primary",
  "name": "Button/Primary",
  "reusable": true,
  "layout": "horizontal",
  "gap": "$space.sm",
  "padding": [
    "$space.sm",
    "$space.lg",
    "$space.sm",
    "$space.lg"
  ],
  "alignItems": "center",
  "justifyContent": "center",
  "cornerRadius": "$radius.md",
  "fill": "$color.primary",
  "children": [
    {
      "type": "text",
      "id": "btn-primary-label",
      "content": "Button",
      "textGrowth": "auto",
      "fontSize": "$font.size.sm",
      "fontWeight": "$font.weight.medium",
      "fontFamily": "$font.family.body",
      "fill": "$color.on-primary"
    }
  ]
}
```

## Card

```json
{
  "type": "frame",
  "id": "card-default",
  "name": "Card/Default",
  "reusable": true,
  "layout": "vertical",
  "gap": "$space.lg",
  "padding": "$space.xl",
  "cornerRadius": "$radius.xl",
  "fill": "$color.surface",
  "effect": {
    "type": "shadow",
    "shadowType": "outer",
    "offset": {
      "x": "$effect.shadow.offset.x",
      "y": "$effect.shadow.offset.y"
    },
    "blur": "$effect.shadow.blur",
    "spread": "$effect.shadow.spread",
    "color": "$color.shadow"
  },
  "slot": [
    "content"
  ],
  "children": [
    {
      "type": "text",
      "id": "card-title",
      "content": "Card Title",
      "textGrowth": "auto",
      "fontSize": "$font.size.lg",
      "fontWeight": "$font.weight.semibold",
      "fontFamily": "$font.family.body",
      "fill": "$color.foreground"
    },
    {
      "type": "frame",
      "id": "card-content",
      "name": "content",
      "layout": "vertical",
      "width": "fill_container",
      "height": "fit_content"
    }
  ]
}
```

## Input Field

```json
{
  "type": "frame",
  "id": "input-field",
  "name": "Form/InputField",
  "reusable": true,
  "layout": "vertical",
  "gap": "$space.sm",
  "children": [
    {
      "type": "text",
      "id": "input-label",
      "content": "Label",
      "textGrowth": "auto",
      "fontSize": "$font.size.sm",
      "fontWeight": "$font.weight.medium",
      "fontFamily": "$font.family.body",
      "fill": "$color.foreground"
    },
    {
      "type": "frame",
      "id": "input-box",
      "layout": "horizontal",
      "padding": [
        "$space.sm",
        "$space.md",
        "$space.sm",
        "$space.md"
      ],
      "cornerRadius": "$radius.sm",
      "stroke": {
        "align": "inside",
        "thickness": "$stroke.thickness.default",
        "fill": "$color.border"
      },
      "fill": "$color.surface",
      "children": [
        {
          "type": "text",
          "id": "input-placeholder",
          "fontWeight": "$font.weight.regular",
          "content": "Placeholder",
          "textGrowth": "auto",
          "fontSize": "$font.size.sm",
          "fontFamily": "$font.family.body",
          "fill": "$color.muted"
        }
      ]
    }
  ]
}
```

## Navigation Bar

```json
{
  "type": "frame",
  "id": "nav-topbar",
  "name": "Nav/TopBar",
  "reusable": true,
  "layout": "horizontal",
  "padding": [
    "$space.md",
    "$space.xl",
    "$space.md",
    "$space.xl"
  ],
  "alignItems": "center",
  "justifyContent": "space_between",
  "width": "fill_container",
  "fill": "$color.surface",
  "stroke": {
    "align": "inside",
    "thickness": "$stroke.thickness.default",
    "fill": "$color.border"
  },
  "children": [
    {
      "type": "text",
      "id": "navbar-logo",
      "content": "Logo",
      "textGrowth": "auto",
      "fontSize": "$font.size.xl",
      "fontWeight": "$font.weight.bold",
      "fontFamily": "$font.family.body",
      "fill": "$color.foreground"
    },
    {
      "type": "frame",
      "id": "navbar-links",
      "layout": "horizontal",
      "gap": "$space.xl",
      "children": [
        {
          "type": "text",
          "id": "nav-1",
          "content": "Home",
          "textGrowth": "auto",
          "fontSize": "$font.size.sm",
          "fontFamily": "$font.family.body",
          "fill": "$color.foreground",
          "fontWeight": "$font.weight.medium"
        },
        {
          "type": "text",
          "id": "nav-2",
          "content": "About",
          "textGrowth": "auto",
          "fontSize": "$font.size.sm",
          "fontFamily": "$font.family.body",
          "fill": "$color.muted",
          "fontWeight": "$font.weight.medium"
        },
        {
          "type": "text",
          "id": "nav-3",
          "content": "Contact",
          "textGrowth": "auto",
          "fontSize": "$font.size.sm",
          "fontFamily": "$font.family.body",
          "fill": "$color.muted",
          "fontWeight": "$font.weight.medium"
        }
      ]
    }
  ]
}
```

## Hero Section

```json
{
  "type": "frame",
  "id": "hero",
  "layout": "vertical",
  "gap": "$space.xl",
  "padding": [
    "$space.section",
    "$space.2xl",
    "$space.section",
    "$space.2xl"
  ],
  "width": "fill_container",
  "fill": "$color.background",
  "children": [
    {
      "type": "text",
      "id": "hero-kicker",
      "content": "B2B Analytics Platform",
      "textGrowth": "auto",
      "fontSize": "$font.size.sm",
      "fontFamily": "$font.family.body",
      "fill": "$color.muted",
      "fontWeight": "$font.weight.semibold"
    },
    {
      "type": "text",
      "id": "hero-title",
      "content": "213 teams onboarded in just 3 weeks after beta launch",
      "textGrowth": "auto",
      "fontSize": "$font.size.5xl",
      "fontWeight": "$font.weight.bold",
      "fontFamily": "$font.family.display",
      "fill": "$color.foreground"
    },
    {
      "type": "text",
      "id": "hero-sub",
      "content": "Dashboard setup time dropped by an average of 42%, and team reports are auto-published every day at 9 AM.",
      "textGrowth": "auto",
      "fontSize": "$font.size.lg",
      "fontFamily": "$font.family.body",
      "fill": "$color.muted",
      "fontWeight": "$font.weight.regular"
    },
    {
      "type": "frame",
      "id": "hero-cta",
      "layout": "horizontal",
      "gap": "$space.md",
      "children": [
        {
          "type": "ref",
          "id": "hero-btn-primary",
          "ref": "btn-primary"
        },
        {
          "type": "ref",
          "id": "hero-btn-secondary",
          "ref": "btn-secondary"
        }
      ]
    }
  ]
}
```