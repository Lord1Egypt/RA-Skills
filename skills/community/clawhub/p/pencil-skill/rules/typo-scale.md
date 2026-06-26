---
title: Minimum 6-Step Type Scale
impact: MEDIUM
impactDescription: Inconsistent font sizes collapse hierarchy and reduce consistency.
tags: typography,scale,font-size,hierarchy
---

## Minimum 6-Step Type Scale

Define type scale with at least 6 steps (xs, sm, base, lg, xl, 2xl, 3xl, 4xl, 5xl). Arbitrary values like `12, 15, 19, 23` lack proportional hierarchy and look visually awkward. Build scale on Major Third (×1.25) or Minor Third (×1.2), then register as tokens.

**Incorrect (Why it's bad):**

- Apply after running `node scripts/set-variables.mjs <file.pen> --var '<name>=<type>:<value>'`

```json
{
  "variables": {
    "font.size.title": {
      "type": "number",
      "value": 23
    },
    "font.size.subtitle": {
      "type": "number",
      "value": 19
    },
    "font.size.text": {
      "type": "number",
      "value": 15
    },
    "font.size.small": {
      "type": "number",
      "value": 12
    }
  }
}
```

**Correct (Why it's good):**

- 9-step scale based on Major Third ratio (×1.25) (apply after running `node scripts/set-variables.mjs <file.pen> --var '<name>=<type>:<value>'`)

```json
{
  "variables": {
    "font.size.xs": {
      "type": "number",
      "value": 12
    },
    "font.size.sm": {
      "type": "number",
      "value": 14
    },
    "font.size.base": {
      "type": "number",
      "value": 16
    },
    "font.size.lg": {
      "type": "number",
      "value": 18
    },
    "font.size.xl": {
      "type": "number",
      "value": 20
    },
    "font.size.2xl": {
      "type": "number",
      "value": 24
    },
    "font.size.3xl": {
      "type": "number",
      "value": 30
    },
    "font.size.4xl": {
      "type": "number",
      "value": 36
    },
    "font.size.5xl": {
      "type": "number",
      "value": 48
    }
  }
}
```
