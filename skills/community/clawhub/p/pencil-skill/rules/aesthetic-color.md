---
title: Avoid AI-looking Color Choices
impact: HIGH
impactDescription: Tailwind blue-500 and purple→blue gradients are the strongest signals of AI-generated design.
tags: aesthetic,color,palette,anti-ai,gradient
---

## Avoid AI-looking Color Choices

`primary: #3B82F6` (Tailwind blue-500) and purple→blue linear gradients are already saturated defaults from AI design tools. Define brand-specific colors, use warm gray neutrals, and apply them with a 60-30-10 ratio.

**Incorrect (Why it's bad):**

```bash
# CLI command (run in terminal)
node scripts/set-variables.mjs design.pen --var '<name>=<type>:<value>'
```

```json
{
  "variables": {
    "color.primary": {
      "type": "color",
      "value": "#3B82F6"
    },
    "color.secondary": {
      "type": "color",
      "value": "#8B5CF6"
    },
    "color.background": {
      "type": "color",
      "value": "#FFFFFF"
    },
    "gradient.hero": {
      "type": "string",
      "value": "linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%)"
    }
  }
}
```

**Correct (Why it's good):**

```bash
# CLI command (run in terminal)
node scripts/set-variables.mjs design.pen --var '<name>=<type>:<value>'
```

- Brand-specific teal tones — not Tailwind defaults
- Warm amber accent
- 60% — warm white, not pure #FFF
- 30% — warm gray

```json
{
  "themes": {
    "mode": [
      "light",
      "dark"
    ]
  },
  "variables": {
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
    "color.secondary": {
      "type": "color",
      "value": [
        {
          "theme": {
            "mode": "light"
          },
          "value": "#D97706"
        },
        {
          "theme": {
            "mode": "dark"
          },
          "value": "#FCD34D"
        }
      ]
    },
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
          "value": "#141410"
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
          "value": "#1C1C18"
        }
      ]
    }
  }
}
```