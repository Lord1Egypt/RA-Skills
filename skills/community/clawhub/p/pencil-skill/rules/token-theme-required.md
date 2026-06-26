---
title: Theme Axes Required (light/dark)
impact: CRITICAL
impactDescription: Designs created without theme axes cannot properly support dark mode.
tags: tokens,theme,dark-mode,light-mode,variables
---

## Theme Axes Required (light/dark)

When declaring variables, you must define a `themes` axis and support at least `light` and `dark` modes. If only single values exist without `themes`, dark-mode migration becomes a manual refactoring nightmare. Register variables with theme structure via `set-variables`.

**Incorrect (Why it's bad):**

```json
{
  "variables": {
    "color.background": {
      "type": "color",
      "value": "#FFFFFF"
    },
    "color.foreground": {
      "type": "color",
      "value": "#111827"
    },
    "color.primary": {
      "type": "color",
      "value": "#3B82F6"
    },
    "color.surface": {
      "type": "color",
      "value": "#F9FAFB"
    }
  }
}
```

**Correct (Why it's good):**

```json
{
  "themes": {
    "mode": [
      "light",
      "dark"
    ]
  },
  "variables": {
    "color.background": {
      "type": "color",
      "value": [
        {
          "theme": {
            "mode": "light"
          },
          "value": "#FFFFFF"
        },
        {
          "theme": {
            "mode": "dark"
          },
          "value": "#0F172A"
        }
      ]
    },
    "color.foreground": {
      "type": "color",
      "value": [
        {
          "theme": {
            "mode": "light"
          },
          "value": "#111827"
        },
        {
          "theme": {
            "mode": "dark"
          },
          "value": "#F1F5F9"
        }
      ]
    },
    "color.primary": {
      "type": "color",
      "value": [
        {
          "theme": {
            "mode": "light"
          },
          "value": "#3B82F6"
        },
        {
          "theme": {
            "mode": "dark"
          },
          "value": "#60A5FA"
        }
      ]
    },
    "color.surface": {
      "type": "color",
      "value": [
        {
          "theme": {
            "mode": "light"
          },
          "value": "#F9FAFB"
        },
        {
          "theme": {
            "mode": "dark"
          },
          "value": "#1E293B"
        }
      ]
    }
  }
}
```
