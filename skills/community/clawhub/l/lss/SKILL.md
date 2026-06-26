---
name: learnsocialstudies-ui-kit-react
description: Applies the Learn Social Studies brand system to React interfaces using CSS variables, reusable component conventions, light theme by default, and dark theme as optional override. Use for apps, dashboards, admin panels, forms, landing pages, and reusable UI systems.
version: 1.0.0
license: Complete terms in LICENSE.txt
---

# Learn Social Studies UI Kit for React

## Purpose
This skill standardizes Learn Social Studies visual design across React interfaces.
It is intended for:

- dashboards
- SaaS apps
- admin panels
- forms
- landing pages
- internal tools
- educational product interfaces

Apply this skill when a React project needs consistent Learn Social Studies branding,
reusable styling primitives, theme support, and developer-friendly UI conventions.

## Brand Intent
The resulting interface must feel:

- clear
- modern academic
- trustworthy
- structured
- lightweight
- brand-consistent

## Theme Model
- Default theme: `light`
- Optional override: `dark`
- Theme is controlled with the `data-theme` attribute on `<html>`
- Do not use `localStorage`
- Theme state should stay in app memory unless the host project already has an approved persistence layer

## Typography
- Headings: `Poppins`
- Body/UI text: `Montserrat`
- Code, tokens, IDs: `JetBrains Mono` or `Fira Code`

## Brand Color Rules
- Primary blue is the main action color
- Deep blue is for hierarchy and high-contrast supporting elements
- Gold is for accent and CTA emphasis only
- Warning uses amber, not brand gold
- Do not use pure black `#000000`
- Do not use yellow `#F3B723` as a page, card, panel, or alert background surface
- Do not use gradients on buttons or cards

## Developer Rules
When applying this skill:

1. Keep business logic untouched.
2. Do not change routing, data flow, API calls, or component behavior unless required for theme toggling.
3. Move reusable visual values into CSS variables.
4. Normalize buttons, inputs, cards, badges, tables, and modals.
5. Use reusable variants instead of page-specific one-off styles.
6. Avoid hardcoded colors when a token exists.
7. Preserve markup structure where possible.
8. Keep the UI clean, readable, and scalable.

## Recommended File Layout
```text
src/
  styles/
    tokens.css
    base.css
    components.css
  theme/
    ThemeProvider.tsx
    useTheme.ts
  components/
    Button/
    Input/
    Card/
    Badge/
```

## Font Loading
Add to the root HTML document:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

## Implementation Instructions
Use the template files included with this skill as the source of truth:

- `templates/react/src/styles/tokens.css`
- `templates/react/src/styles/base.css`
- `templates/react/src/styles/components.css`
- `templates/react/src/theme/ThemeProvider.tsx`
- `templates/react/src/theme/useTheme.ts`
- `templates/react/src/components/*`

If the target project already has its own component library:

- map the project components to these same tokens and variant rules
- keep variant names consistent: `primary`, `secondary`, `accent`
- keep status names consistent: `success`, `warning`, `error`, `info`

## Output Expectation
After applying this skill, the project should have:

- light theme by default
- optional dark theme
- reusable design tokens
- consistent typography
- consistent button/input/card/badge patterns
- maintainable UI styling without changing product logic
