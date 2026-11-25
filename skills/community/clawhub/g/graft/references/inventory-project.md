# Inventory Project — Detecting Local Design Tokens

## Purpose

Before grafting, the skill must understand what design tokens the local project currently uses and where they live. This reference documents how to detect and scan token sources across common web stacks.

## Detection Strategy

Scan in this order (most common to least common). Stop at the first match within each category, but check all categories since projects often mix approaches.

### 1. Plain CSS Custom Properties

**Files to check:**
- `src/index.css`, `src/globals.css`, `src/global.css`, `src/app.css`
- `app/globals.css`, `app/global.css`
- `styles/globals.css`, `styles/variables.css`, `styles/theme.css`
- Any `.css` file containing `:root {` with `--` custom properties

**What to extract:**
- All `--*` custom property declarations inside `:root` or `html` or `body`
- Group by prefix convention if present (e.g., `--color-*`, `--spacing-*`, `--font-*`)
- Note which files reference these variables (to understand usage scope)

**Detection signal:** `grep -rn "^\s*--" --include="*.css"` in `src/` and `app/`

### 2. Tailwind CSS

**Files to check:**
- `tailwind.config.js`, `tailwind.config.ts`, `tailwind.config.mjs`, `tailwind.config.cjs`
- `postcss.config.js` (confirms Tailwind is in use)

**What to extract:**
- `theme.colors` — all color definitions
- `theme.fontFamily` — font stack
- `theme.fontSize` — size scale
- `theme.spacing` — spacing scale (if customized beyond defaults)
- `theme.borderRadius` — radius scale
- `theme.boxShadow` — shadow definitions
- `theme.extend.*` — any extensions to defaults
- `theme.transitionDuration`, `theme.transitionTimingFunction` — motion tokens

**Detection signal:** File `tailwind.config.*` exists in project root or `src/`

### 3. shadcn/ui

**Files to check:**
- `components.json` (shadcn config)
- `src/globals.css` or `app/globals.css` with HSL variable pattern

**What to extract:**
- HSL color variables: `--background`, `--foreground`, `--primary`, `--secondary`, `--muted`, `--accent`, `--destructive`, `--card`, `--popover`, `--border`, `--input`, `--ring`
- Dark mode variants (`.dark` class or `@media (prefers-color-scheme: dark)`)
- `--radius` variable

**Detection signal:** File `components.json` with `"style"` field, OR CSS file with `--background:` HSL values

### 4. CSS-in-JS (styled-components / emotion)

**Files to check:**
- `src/theme.ts`, `src/theme.js`, `src/styles/theme.ts`
- `src/theme/index.ts`, `src/design-tokens.ts`
- Look for files containing `ThemeProvider` or `import { ThemeProvider }`

**What to extract:**
- Theme object properties: `colors`, `fonts`, `fontSizes`, `space`, `radii`, `shadows`
- Nested variant definitions

**Detection signal:** `grep -rn "ThemeProvider\|createTheme\|styled\." --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx"`

### 5. Design Token Files (JSON/YAML)

**Files to check:**
- `tokens.json`, `design-tokens.json`, `theme.json`
- `tokens/`, `design-tokens/` directories
- Style Dictionary config (`config.json` with `"source"` pointing to token files)

**What to extract:**
- All token categories defined in the file
- Note the format (W3C Design Tokens, Style Dictionary, custom)

**Detection signal:** JSON files with nested `"color"`, `"spacing"`, `"typography"` keys

### 6. Framework-specific

**Next.js App Router:**
- `app/layout.tsx` — may import fonts and apply them globally
- `next.config.js` — may have image config relevant to aspect ratios

**Vite / vanilla:**
- `index.html` — may have inline `<style>` or font imports
- `src/style.css`, `src/main.css`

**Vue:**
- `src/assets/main.css`, `src/assets/base.css`
- `<style>` blocks in `.vue` files with `:root` variables

**Svelte:**
- `src/app.css`, `src/app.postcss`
- `<style>` blocks in `+layout.svelte`

## Output Format

After scanning, produce a summary:

```
Stack detected: [Tailwind + shadcn/ui | Plain CSS | CSS-in-JS | etc.]

Token sources found:
  - globals.css (23 CSS custom properties)
  - tailwind.config.ts (custom colors, fonts, radii)
  - components.json (shadcn config, style: "new-york")

Current tokens (by category):
  Colors:
    --background: 0 0% 100% (white)
    --foreground: 222.2 84% 4.9% (near-black)
    --primary: 262.1 83.3% 57.8% (purple)
    ...
  Typography:
    --font-sans: Inter, system-ui, sans-serif
    Base size: 16px (1rem)
    ...
  Radii:
    --radius: 0.5rem (8px)
    ...
  Shadows:
    [none defined / shadow-sm: 0 1px 2px rgba(0,0,0,0.05)]
    ...
  Motion:
    [none defined / transition-duration: 150ms]
    ...
```

If the detected stack is ambiguous (e.g., both Tailwind config and raw CSS variables exist), ask the user which is the primary token source before proceeding to the diff phase.
