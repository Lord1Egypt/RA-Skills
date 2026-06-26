---
title: Token Naming Convention
impact: CRITICAL
impactDescription: Without token naming conventions, reuse and maintenance quickly become difficult.
tags: tokens,naming,variables
---

## Token Naming Convention

All design tokens should use dot-separated naming in the `$category.purpose.variant` format. Raw names like `$blue` or meaningless names like `$padding1` are forbidden. Proper naming should clearly expose hierarchy, e.g., `$color.primary`, `$font.size.lg`, `$space.md`.

**Incorrect (Why it's bad):**

```json
{
  "variables": {
    "blue": {
      "type": "color",
      "value": "#3B82F6"
    },
    "big-text": {
      "type": "number",
      "value": 24
    },
    "padding1": {
      "type": "number",
      "value": 16
    },
    "red2": {
      "type": "color",
      "value": "#EF4444"
    },
    "graylight": {
      "type": "color",
      "value": "#F9FAFB"
    }
  }
}
```

**Correct (Why it's good):**

> The example below uses single values to focus on naming patterns. For the real light/dark theme structure of color tokens, see the `token-theme-required` rule.

```json
{
  "variables": {
    "color.primary": {
      "type": "color",
      "value": "#3B82F6"
    },
    "color.destructive": {
      "type": "color",
      "value": "#EF4444"
    },
    "color.surface": {
      "type": "color",
      "value": "#F9FAFB"
    },
    "font.size.lg": {
      "type": "number",
      "value": 24
    },
    "font.size.base": {
      "type": "number",
      "value": 16
    },
    "space.md": {
      "type": "number",
      "value": 16
    },
    "space.lg": {
      "type": "number",
      "value": 24
    }
  }
}
```
