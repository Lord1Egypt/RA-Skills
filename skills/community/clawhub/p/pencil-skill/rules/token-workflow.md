---
title: Token Registration Workflow
impact: HIGH
impactDescription: Starting design before tokens are registered often requires full refactoring later.
tags: tokens,workflow,set-variables,get-variables
---

## Token Registration Workflow

You must register tokens before getting started with design. Workflow: ① Register tokens with `set-variables` → ② Confirm registration with `get-variables` → ③ Reference `$token.name` in design. If you start by entering raw values directly, replacing them with tokens later requires editing every node.

**Incorrect (Why it's bad):**

- Start designing immediately without token registration

```json
{
  "type": "frame",
  "id": "landing-page",
  "fill": "#FFFFFF",
  "layout": "vertical",
  "children": [
    {
      "type": "text",
      "content": "Welcome",
      "fontSize": 48,
      "fill": "#111827"
    },
    {
      "type": "frame",
      "id": "cta",
      "fill": "#3B82F6",
      "children": [
        {
          "type": "text",
          "content": "Get Started",
          "fill": "#FFFFFF",
          "fontSize": 16
        }
      ]
    }
  ]
}
```

**Correct (Why it's good):**

```bash
# CLI command (run in terminal)
node scripts/set-variables.mjs design.pen --var '<name>=<type>:<value>'
node scripts/get-variables.mjs design.pen
```

- Step 1: Token registration
- Step 2: Confirm registration (optional) - run get-variables and verify the result
- Step 3: Design using token references

```json
[
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
      "font.size.5xl": {
        "type": "number",
        "value": 48
      },
      "font.size.base": {
        "type": "number",
        "value": 16
      }
    }
  },
  {},
  {
    "type": "frame",
    "id": "landing-page",
    "fill": "$color.background",
    "layout": "vertical",
    "children": [
      {
        "type": "text",
        "id": "welcome",
        "fontWeight": "$font.weight.bold",
        "content": "Welcome",
        "fontFamily": "$font.family.display",
        "fontSize": "$font.size.5xl",
        "fill": "$color.foreground",
        "textGrowth": "auto"
      },
      {
        "type": "frame",
        "fill": "$color.primary",
        "children": [
          {
            "type": "text",
            "id": "cta-label",
            "fontWeight": "$font.weight.semibold",
            "content": "Get Started",
            "fontFamily": "$font.family.body",
            "fill": "$color.on-primary",
            "fontSize": "$font.size.base",
            "textGrowth": "auto"
          }
        ]
      }
    ]
  }
]
```
