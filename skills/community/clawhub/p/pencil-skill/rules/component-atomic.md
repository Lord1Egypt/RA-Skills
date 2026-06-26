---
title: Atomic Design Hierarchy
impact: HIGH
impactDescription: Flat structured pages are not reusable and cannot maintain consistency.
tags: component,atomic-design,atom,molecule,organism
---

## Atomic Design Hierarchy

Components must be combined in the following hierarchy: Atom → Molecule → Organism → Template. Make Atoms (buttons, icons, badges) reusable first, combine them with refs in Molecules (cards, form fields), and combine Molecules in Organisms (navigation, feature sections). It is prohibited to flatly list all elements directly in the page frame.

**Incorrect (why it's bad):**

```json
{
  "type": "frame",
  "id": "home-page",
  "layout": "vertical",
  "children": [
    {
      "type": "frame",
      "id": "logo",
      "width": 120,
      "height": 32
    },
    {
      "type": "text",
      "id": "nav-item-1",
      "content": "product"
    },
    {
      "type": "text",
      "id": "nav-item-2",
      "content": "price"
    },
    {
      "type": "frame",
      "id": "hero-bg",
      "width": "fill_container",
      "height": 600
    },
    {
      "type": "text",
      "id": "hero-title",
      "content": "title"
    },
    {
      "type": "frame",
      "id": "card-1",
      "width": 360,
      "height": 240
    },
    {
      "type": "frame",
      "id": "card-2",
      "width": 360,
      "height": 240
    },
    {
      "type": "frame",
      "id": "card-3",
      "width": 360,
      "height": 240
    }
  ]
}
```

**Correct (Why it’s good):**

- Step 1: Register Atom — Specify reusable=true on individual nodes
- Step 2: Molecule — Card combines Button Atom with ref
- Step 3: Organism — Nav combines atoms
- Step 4: Page — Combine with Organism ref

```json
[
  {
    "type": "frame",
    "id": "btn-primary",
    "name": "Button/Primary",
    "reusable": true,
    "layout": "horizontal"
  },
  {
    "type": "frame",
    "id": "badge-default",
    "name": "Badge/Default",
    "reusable": true,
    "layout": "horizontal"
  },
  {
    "id": "card-feature",
    "name": "Card/Feature",
    "type": "frame",
    "reusable": true,
    "layout": "vertical",
    "children": [
      {
        "type": "frame",
        "id": "card-icon"
      },
      {
        "type": "text",
        "id": "card-title",
        "fontWeight": "$font.weight.bold",
        "fontFamily": "$font.family.display",
        "textGrowth": "auto"
      },
      {
        "type": "text",
        "id": "card-body",
        "fontWeight": "$font.weight.regular",
        "fontFamily": "$font.family.body",
        "textGrowth": "auto"
      },
      {
        "type": "ref",
        "ref": "btn-primary",
        "id": "card-cta"
      }
    ]
  },
  {
    "id": "nav-topbar",
    "name": "Nav/TopBar",
    "type": "frame",
    "reusable": true,
    "layout": "horizontal",
    "children": [
      {
        "type": "frame",
        "id": "logo"
      },
      {
        "type": "frame",
        "id": "nav-links",
        "layout": "horizontal"
      },
      {
        "type": "ref",
        "ref": "btn-primary",
        "id": "cta-nav"
      }
    ]
  },
  {
    "type": "frame",
    "id": "home-page",
    "layout": "vertical",
    "children": [
      {
        "type": "ref",
        "ref": "nav-topbar",
        "id": "nav"
      },
      {
        "type": "ref",
        "ref": "hero-default",
        "id": "hero"
      },
      {
        "type": "ref",
        "ref": "section-features",
        "id": "features"
      }
    ]
  }
]
```
