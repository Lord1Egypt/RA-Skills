---
title: Dark Mode — No Pure Black/White
impact: MEDIUM
impactDescription: Pure black/white dark mode causes glare and flat layers.
tags: color,dark-mode,elevation,contrast
---

## Dark Mode — No Pure Black/White

In dark mode, it is prohibited to use `#000000` for background and `#FFFFFF` for text. Pure black and white combinations have too much contrast, which creates glare and leaves no room for elevation (surface layer) to be expressed as brightness. Set the background to a dark navy/slate color, the surface to be slightly lighter than the background, and the text to be off-white.

**Incorrect (why it's bad):**

```bash
# CLI command (run in terminal)
node scripts/set-variables.mjs design.pen --var '<name>=<type>:<value>'
```

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
          "value": "#000000"
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
          "value": "#000000"
        },
        {
          "theme": {
            "mode": "dark"
          },
          "value": "#FFFFFF"
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
          "value": "#F5F5F5"
        },
        {
          "theme": {
            "mode": "dark"
          },
          "value": "#000000"
        }
      ]
    }
  }
}
```

**Correct (Why it’s good):**

```bash
# CLI command (run in terminal)
node scripts/set-variables.mjs design.pen --var '<name>=<type>:<value>'
```

- light=warm white, dark=deep navy
- Expression of elevation brighter than the background in dark mode
- Floating elements such as cards — brighter than the surface
- dark=off-white, not pure white

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
          "value": "#FAFAF7"
        },
        {
          "theme": {
            "mode": "dark"
          },
          "value": "#0F172A"
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
          "value": "#F5F5F0"
        },
        {
          "theme": {
            "mode": "dark"
          },
          "value": "#1E293B"
        }
      ]
    },
    "color.surface-raised": {
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
          "value": "#293548"
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
          "value": "#1C1C18"
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
    }
  }
}
```
