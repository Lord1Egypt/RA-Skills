# Token Boundary Guard

## Purpose

This is the enforcement ruleset for `graft`'s hard constraint: **token-level changes only**. Before writing ANY file edit, every proposed change must pass this guard. Changes that fail are rejected (removed from the plan) or flagged for manual user review.

## Classification Rules

### ✅ ALLOWED — Token-level changes

These are pure value changes that modify the visual appearance without altering structure, behavior, or content.

| Category | What's allowed | Examples |
|----------|---------------|----------|
| **Color values** | Changing hex, rgb, hsl, oklch, CSS variable values | `--primary: #7c3aed` → `--primary: #4F46E5` |
| **Spacing values** | Changing margin, padding, gap **values** (not adding/removing the property) | `--spacing-4: 16px` → `--spacing-4: 12px` |
| **Border-radius values** | Changing radius values | `border-radius: 12px` → `border-radius: 2px` |
| **Box-shadow values** | Changing or removing shadow definitions | `box-shadow: 0 4px 6px rgba(0,0,0,0.1)` → `box-shadow: none` |
| **Border values** | Changing border width, style, color | `border: none` → `border: 1px solid rgba(0,0,0,0.08)` |
| **Font-family** | Changing font stack | `font-family: 'Poppins'` → `font-family: 'Inter'` |
| **Font-weight** | Changing weight values | `font-weight: 700` → `font-weight: 600` |
| **Font-size** | Changing size values | `font-size: 3.5rem` → `font-size: 3rem` |
| **Line-height** | Changing line-height values | `line-height: 1.5` → `line-height: 1.1` |
| **Letter-spacing** | Changing tracking values | `letter-spacing: 0` → `letter-spacing: -0.02em` |
| **Transition duration** | Changing timing values | `transition: all 300ms` → `transition: all 200ms` |
| **Transition easing** | Changing easing function | `ease-in-out` → `cubic-bezier(0.4, 0, 0.2, 1)` |
| **Opacity values** | Changing opacity | `opacity: 0.8` → `opacity: 0.9` |
| **CSS custom property declarations** | Adding/modifying `--*` variable **values** in `:root` or theme blocks | Adding `--color-accent: #4F46E5` to `:root` |
| **Tailwind theme config values** | Changing values in `theme.extend.*` | `borderRadius: { DEFAULT: '0.5rem' }` → `{ DEFAULT: '0.125rem' }` |

### ❌ FORBIDDEN — Structural / behavioral changes

These change the DOM, layout strategy, component composition, or business logic. `graft` must never touch these.

| Category | What's forbidden | Why |
|----------|-----------------|-----|
| **DOM structure** | Adding, removing, or reordering HTML/JSX elements | Changes content architecture, not visual tokens |
| **Component composition** | Wrapping elements in new components, extracting sub-components | Architectural change |
| **Layout properties** | Adding `display: flex/grid`, changing `flex-direction`, `grid-template-*`, `position` | Changes spatial relationships, not token values |
| **Content / copy** | Changing text content, labels, microcopy, alt text | Not a design token |
| **Responsive breakpoints** | Adding/changing `@media` queries, breakpoint values | Structural layout concern |
| **File creation** | Creating new component files, new pages, new routes | Architectural change |
| **File deletion** | Deleting any files (even unused CSS files) | Destructive, outside scope |
| **File renaming** | Renaming files or moving files between directories | Organizational, outside scope |
| **Import changes** | Adding new dependencies, changing import paths | Build/dependency concern |
| **Business logic** | Any JavaScript/TypeScript logic changes | Not a design token |
| **Data fetching** | API calls, state management, hooks | Not a design token |
| **Event handlers** | onClick, onChange, form submissions | Not a design token |
| **Routing** | Route definitions, navigation logic | Not a design token |

### ⚠️ EDGE CASES — Require manual classification

| Situation | Rule |
|-----------|------|
| **Inline styles in JSX** (`style={{ color: 'red' }}`) | PREFER extracting the value to a CSS variable and referencing it, rather than editing the inline style directly. If extraction isn't practical, the inline value change is allowed but must be flagged to the user. |
| **Tailwind utility classes** (`className="bg-purple-500 rounded-xl"`) | Changing `bg-purple-500` → `bg-indigo-600` is a token change (allowed). Changing `flex-col` → `flex-row` is structural (forbidden). |
| **Adding a new CSS variable** to `:root` that didn't exist before | Allowed IF it's a token value that components will reference. This is creating a centralized token, which is the preferred approach. |
| **Adding a font `@import` or `<link>`** to load a new font family | Allowed — this is a dependency of a font-family token change. But flag it to the user since it adds a network request. |
| **Adding a new Tailwind plugin** (e.g., `@tailwindcss/typography`) | Forbidden — this is a dependency/build change, not a token change. |
| **Modifying `package.json`** to add a font package | Forbidden — dependency management is outside scope. Note the required package in the report instead. |
| **Dark mode variant additions** | If the project already has dark mode and you're changing dark mode token values: allowed. If you're adding dark mode support that didn't exist: forbidden (structural). |

## Enforcement Process

For EVERY proposed edit in the change plan:

1. Read the line/block being changed
2. Classify the change using the tables above
3. If ✅: include in the plan
4. If ❌: remove from the plan, add to "Skipped" section with explanation
5. If ⚠️: include in the plan with a warning flag, let the user decide

## Example Classifications

```
CHANGE: globals.css line 5: `--primary: #7c3aed` → `--primary: #4F46E5`
CLASS: ✅ Color value change in CSS custom property
ACTION: Include in plan

CHANGE: page.tsx line 12: `<div className="grid grid-cols-3">` → `<div className="grid grid-cols-2">`
CLASS: ❌ Layout structure change (grid column count)
ACTION: Remove from plan, add to Skipped: "Grid column count is structural, not a token"

CHANGE: button.tsx line 8: `style={{ borderRadius: 12 }}`  → `style={{ borderRadius: 2 }}`
CLASS: ⚠️ Token value change but in inline style
ACTION: Include with warning: "Recommend extracting to CSS variable `--radius-btn` instead of editing inline"

CHANGE: header.tsx line 3: `import { Menu } from 'lucide-react'` → `import { Menu } from '@heroicons/react'`
CLASS: ❌ Import/dependency change
ACTION: Remove from plan, add to Skipped: "Icon library change is a dependency swap, not a token change"
```
