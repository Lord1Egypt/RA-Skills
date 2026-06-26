# Theming (SVG)

Use this file when you need theme concepts for SVG output or want to match beautiful-mermaid's theming pipeline.

## Core Concepts

- Two-color foundation: `bg` and `fg` derive the rest via `color-mix()`.
- Enriched mode: optional `line`, `accent`, `muted`, `surface`, `border`.
- CSS custom properties are applied on `<svg>` for live theme switching.

## APIs

```typescript
import { renderMermaid, THEMES, DEFAULTS, fromShikiTheme } from 'beautiful-mermaid'

const svg = await renderMermaid(diagram, THEMES['tokyo-night'])
const themed = fromShikiTheme(shikiThemeObject)
```

## Live Theme Switch

```javascript
const svgElement = document.querySelector('svg')
svgElement.style.setProperty('--bg', '#282a36')
svgElement.style.setProperty('--fg', '#f8f8f2')
```
