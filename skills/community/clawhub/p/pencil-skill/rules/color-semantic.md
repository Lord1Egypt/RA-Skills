---
title: 3-Layer Color System
impact: HIGH
impactDescription: Layerless color tokens make theme switching and rebranding impossible.
tags: color,semantic,tokens,palette,system
---

## 3-Layer Color System

The color system is designed in three layers. ① Primitive (primary color palette: `$palette.teal.500`) → ② Semantic (role-based: `$color.primary`) → ③ Component (Component only: `$btn.bg`). In design files, only Semantic layers are used, and direct references to Primitives are prohibited.

**Incorrect (why it's bad):**

```json
{
  "type": "frame",
  "id": "alert-error",
  "fill": "$palette.red.50",
  "stroke": {
    "align": "inside",
    "thickness": 1,
    "fill": "$palette.red.200"
  },
  "children": [
    {
      "type": "text",
      "id": "error-msg",
      "fontWeight": "$font.weight.medium",
      "fill": "$palette.red.700",
      "content": "error message"
    }
  ]
}
```

**Correct (Why it’s good):**

- Semantic layer definition (applied after executing CLI (set-variables))
- Error status background

```json
[
  {
    "variables": {
      "color.destructive": {
        "type": "color",
        "value": [
          {
            "theme": {
              "mode": "light"
            },
            "value": "#FEF2F2"
          },
          {
            "theme": {
              "mode": "dark"
            },
            "value": "#450A0A"
          }
        ]
      },
      "color.destructive-border": {
        "type": "color",
        "value": [
          {
            "theme": {
              "mode": "light"
            },
            "value": "#FECACA"
          },
          {
            "theme": {
              "mode": "dark"
            },
            "value": "#7F1D1D"
          }
        ]
      },
      "color.destructive-foreground": {
        "type": "color",
        "value": [
          {
            "theme": {
              "mode": "light"
            },
            "value": "#B91C1C"
          },
          {
            "theme": {
              "mode": "dark"
            },
            "value": "#FCA5A5"
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
            "value": "#0D9488"
          },
          {
            "theme": {
              "mode": "dark"
            },
            "value": "#2DD4BF"
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
      "color.muted": {
        "type": "color",
        "value": [
          {
            "theme": {
              "mode": "light"
            },
            "value": "#6B7280"
          },
          {
            "theme": {
              "mode": "dark"
            },
            "value": "#94A3B8"
          }
        ]
      },
      "color.border": {
        "type": "color",
        "value": [
          {
            "theme": {
              "mode": "light"
            },
            "value": "#E5E7EB"
          },
          {
            "theme": {
              "mode": "dark"
            },
            "value": "#334155"
          }
        ]
      }
    }
  },
  {
    "type": "frame",
    "id": "alert-error",
    "fill": "$color.destructive",
    "stroke": {
      "align": "inside",
      "thickness": "$stroke.thickness.default",
      "fill": "$color.destructive-border"
    },
    "children": [
      {
        "type": "text",
        "id": "error-msg",
        "fontWeight": "$font.weight.medium",
        "fontFamily": "$font.family.body",
        "textGrowth": "auto",
        "fill": "$color.destructive-foreground",
        "content": "error message"
      }
    ]
  }
]
```
