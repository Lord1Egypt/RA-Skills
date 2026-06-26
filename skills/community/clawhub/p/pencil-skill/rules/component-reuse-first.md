---
title: Search Before Create
impact: HIGH
impactDescription: Ignoring existing components and creating new ones every time will fragment your design system.
tags: component,reuse,search-nodes,anti-duplication
---

## Search Before Create

Before creating a new component or element, you must search for existing reusables with `search-nodes --reusable`. If you already have `btn-primary` and create a new button, the styles of the two buttons will evolve differently and become inconsistent. If there are search results, create an instance with `ref`.

**Incorrect (why it's bad):**

Create new button directly without search-nodes

```json
{
  "type": "frame",
  "id": "new-submit-btn",
  "fill": "#2563EB",
  "cornerRadius": 6,
  "padding": [
    10,
    20,
    10,
    20
  ],
  "children": [
    {
      "type": "text",
      "id": "new-btn-label",
      "content": "submit",
      "fill": "#FFFFFF",
      "fontSize": 15
    }
  ]
}
```

**Correct (Why it’s good):**

Step 1: First, search for existing reusables (run CLI search-nodes)

```bash
node scripts/search-nodes.mjs design.pen --name "button" --reusable
```

Step 2: Search result: `btn-primary` → Create instance with `ref`

```json
[
  {
    "type": "ref",
    "ref": "btn-primary",
    "id": "submit-btn",
    "descendants": {
      "label": {
        "content": "submit"
      }
    }
  }
]
```