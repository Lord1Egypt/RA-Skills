---
title: Component Slash Naming
impact: HIGH
impactDescription: Non-standard naming hinders component discovery and team collaboration.
tags: component,naming,convention,slash
---

## Component Slash Naming

Every reusable component is named **two fields**:
- `id`: slug without slash (`btn-primary`, `card-default`, `nav-topbar`)
- `name`: Figma standard slash naming (`"Button/Primary"`, `"Card/Default"`, `"Nav/TopBar"`)

Schema validation will fail if `id` contains a slash (`/`). Camel case, underscores, and abbreviations are also prohibited. Slash separation in `name` is consistent with the Figma standard and allows grouping by category when searching with `search-nodes --reusable`.

**Incorrect (why it's bad):**

- Camel cases are prohibited.
- No underscores
- No abbreviations
- Single name without categories
- Single name without variations

```json
[
  {
    "id": "primaryBtn",
    "reusable": true
  },
  {
    "id": "card_large",
    "reusable": true
  },
  {
    "id": "navBar",
    "reusable": true
  },
  {
    "id": "FormInputText",
    "reusable": true
  },
  {
    "id": "modal",
    "reusable": true
  }
]
```

**Correct (Why it’s good):**

- id: slug, name: Figma slash naming

```json
[
  {
    "id": "btn-primary",
    "name": "Button/Primary",
    "reusable": true
  },
  {
    "id": "btn-secondary",
    "name": "Button/Secondary",
    "reusable": true
  },
  {
    "id": "btn-ghost",
    "name": "Button/Ghost",
    "reusable": true
  },
  {
    "id": "card-default",
    "name": "Card/Default",
    "reusable": true
  },
  {
    "id": "card-featured",
    "name": "Card/Featured",
    "reusable": true
  },
  {
    "id": "nav-topbar",
    "name": "Nav/TopBar",
    "reusable": true
  },
  {
    "id": "nav-mobile",
    "name": "Nav/Mobile",
    "reusable": true
  },
  {
    "id": "form-input-text",
    "name": "Form/InputText",
    "reusable": true
  },
  {
    "id": "form-input-password",
    "name": "Form/InputPassword",
    "reusable": true
  },
  {
    "id": "modal-default",
    "name": "Modal/Default",
    "reusable": true
  },
  {
    "id": "modal-confirm",
    "name": "Modal/Confirm",
    "reusable": true
  }
]
```
