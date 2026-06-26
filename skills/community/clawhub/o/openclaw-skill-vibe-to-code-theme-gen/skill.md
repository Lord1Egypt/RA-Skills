---
name: VibeTheme
description: Generates a color palette and CSS variables based on a descriptive atmosphere
version: 1.0.0-openclaw-skill-vibe-to-code-theme-gen
commands:
  - name: generate_theme
    description: Generates a color palette and CSS variables based on a descriptive atmosphere
    parameters:
      - name: vibe
        type: string
        required: true
        description: A descriptive atmosphere to base the color palette on (e.g. "cozy autumn evening", "neon cyberpunk city")
      - name: format
        type: string
        required: false
        description: "Output format: css (default), tailwind, or vscode"
---

# VibeTheme

VibeTheme generates a color palette and CSS variables based on a descriptive atmosphere.

## Usage

```
/vibe_theme generate_theme --vibe "<atmosphere>" [--format css|tailwind|vscode]
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `vibe`    | Yes      | A descriptive atmosphere to base the color palette on (e.g. "cozy autumn evening", "neon cyberpunk city") |
| `format`  | No       | Output format: `css` (default), `tailwind`, or `vscode` |

## What It Does

1. Takes a descriptive vibe string as input.
2. Generates a harmonious color palette inspired by the atmosphere.
3. Outputs in the chosen format:
   - **css** — A `:root { ... }` block of CSS custom properties.
   - **tailwind** — A `colors: { ... }` object for `tailwind.config.js`.
   - **vscode** — A `.json` structure for VS Code's `workbench.colorCustomizations`.
