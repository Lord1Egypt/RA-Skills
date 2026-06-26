---
title: Responsive via Separate Frames
impact: HIGH
impactDescription: Responsive simulates independent frames for each resolution rather than processing single frame conditions.
tags: layout,responsive,breakpoint,mobile,desktop
---

## Responsive via Separate Frames

Since .pen does not have a CSS media query, the responsive version creates and expresses an independent frame for each resolution: 375 (mobile), 768 (tablet), and 1440 (desktop). Share components as `ref` to minimize duplication. If you try to handle all resolutions in one frame, layout becomes impossible.

**Incorrect (why it's bad):**

- No idea how it will look on mobile

```json
{
  "type": "frame",
  "id": "page-all",
  "width": 1440,
  "layout": "vertical",
  "children": [
    {
      "type": "frame",
      "id": "nav",
      "width": "fill_container"
    }
  ]
}
```

**Correct (Why it’s good):**

```json
[
  {
    "type": "frame",
    "id": "page-mobile",
    "width": 375,
    "height": "fit_content",
    "layout": "vertical",
    "gap": 0,
    "children": [
      {
        "type": "ref",
        "ref": "nav-mobile-comp",
        "id": "nav-mobile"
      },
      {
        "type": "ref",
        "ref": "hero-mobile-comp",
        "id": "hero-mobile"
      }
    ]
  },
  {
    "type": "frame",
    "id": "page-tablet",
    "width": 768,
    "height": "fit_content",
    "layout": "vertical",
    "gap": 0,
    "children": [
      {
        "type": "ref",
        "ref": "nav-topbar",
        "id": "nav-tablet"
      },
      {
        "type": "ref",
        "ref": "hero-default",
        "id": "hero-tablet"
      }
    ]
  },
  {
    "type": "frame",
    "id": "page-desktop",
    "width": 1440,
    "height": "fit_content",
    "layout": "vertical",
    "gap": 0,
    "children": [
      {
        "type": "ref",
        "ref": "nav-topbar",
        "id": "nav-desktop"
      },
      {
        "type": "ref",
        "ref": "hero-wide",
        "id": "hero-desktop"
      }
    ]
  }
]
```
