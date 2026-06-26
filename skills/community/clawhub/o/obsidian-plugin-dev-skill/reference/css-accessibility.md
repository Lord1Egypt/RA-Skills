# CSS Styling

> For accessibility requirements (keyboard navigation, ARIA labels, focus indicators, touch targets), see [[reference/accessibility.md]].

## CSS Variables

Always use Obsidian's built-in CSS variables. Never hardcode colors.

### Core Variables

```css
/* Text */
var(--text-normal)
var(--text-muted)
var(--text-faint)
var(--text-accent)
var(--text-on-accent)

/* Backgrounds */
var(--background-primary)
var(--background-secondary)
var(--background-modifier-border)
var(--background-modifier-hover)
var(--background-modifier-active-press)
var(--background-modifier-error)

/* Interactive */
var(--interactive-normal)
var(--interactive-hover)
var(--interactive-accent)
var(--interactive-accent-hover)
var(--interactive-success)

/* Spacing & Sizing */
var(--size-4-1)  /* 4px */
var(--size-4-2)  /* 8px */
var(--size-4-3)  /* 12px */
var(--size-4-4)  /* 16px */

/* Typography */
var(--font-text)
var(--font-interface)
var(--font-monospace)
var(--font-smallest)
var(--font-smaller)
var(--font-small)
var(--font-ui-medium)

/* Borders */
var(--radius-s)
var(--radius-m)
var(--radius-l)

/* Shadows */
var(--shadow-s)
var(--shadow-m)
var(--shadow-l)
```

### Discovering Variables

1. Open DevTools (Ctrl+Shift+I)
2. Go to Sources → search for `app.css`
3. Or inspect any element and check computed styles

## CSS Scoping

Always scope your CSS to avoid affecting other plugins or Obsidian's UI.

```css
/* Scope to your plugin's container */
.my-plugin-view {
  /* styles */
}

/* Scope to a specific class on body */
body.my-plugin-active .target-element {
  /* styles */
}

/* Wrong: Don't style global elements */
/* .workspace { ... }  NO */
/* .nav-header { ... }  NO */
```

## Plugin Styles

If your plugin has styles, put them in `styles.css` in the plugin root.

```css
/* styles.css */
.my-plugin-container {
  padding: var(--size-4-2);
  color: var(--text-normal);
  background: var(--background-primary);
}

.my-plugin-button {
  background: var(--interactive-accent);
  color: var(--text-on-accent);
  border: none;
  border-radius: var(--radius-s);
  padding: var(--size-4-1) var(--size-4-2);
  cursor: pointer;
}

.my-plugin-button:hover {
  background: var(--interactive-accent-hover);
}
```

**Do NOT:**
- Add `<style>` elements in TypeScript
- Add `<link>` elements in TypeScript
- Use `el.style.setProperty()` for non-dynamic values
- Hardcode colors like `#fff`, `rgb(0,0,0)`

## Theme-Aware Styles

**Always provide both `.theme-dark` and `.theme-light` variants** when your CSS uses `background-color`, `border`, `box-shadow`, or `opacity`. Obsidian CSS variables auto-adapt to themes, but explicit theme blocks handle transparency and subtle visual differences that variables alone can't express.

```css
/* Base styles — prefer Obsidian vars for core colors */
.my-plugin-element {
  background: var(--background-primary);
  color: var(--text-normal);
  border: 1px solid var(--background-modifier-border);
}

/* Dark mode refinements — adjust transparency and shadows */
.theme-dark .my-plugin-element {
  border-color: rgba(255, 255, 255, 0.08);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
}

/* Light mode refinements */
.theme-light .my-plugin-element {
  border-color: rgba(0, 0, 0, 0.08);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
}
```

**When CSS variables alone are enough:**
- Text color (`var(--text-normal)` auto-switches)
- Background fills (`var(--background-primary)` auto-switches)
- Interactive states (`var(--interactive-accent)` auto-switches)

**When you NEED explicit `.theme-dark` / `.theme-light`:**
- Semi-transparent colors (`rgba(..., 0.1)` — alpha doesn't auto-adapt)
- Borders with subtle opacity
- Box shadows (depth looks different in dark vs light)
- Custom highlight/background colors not covered by Obsidian vars

## Mobile Styles

```css
/* Mobile specific */
.is-mobile .my-plugin-view {
  padding: var(--size-4-1);
  font-size: var(--font-ui-medium);
}

/* Desktop specific */
body:not(.is-mobile) .my-plugin-view {
  padding: var(--size-4-4);
}
```

## 4px Grid System

Obsidian uses a 4px-based spacing grid. Use multiples of 4 for padding/margin.

```css
.my-plugin-element {
  padding: var(--size-4-2);    /* 8px */
  margin: var(--size-4-3);     /* 12px */
  gap: var(--size-4-1);        /* 4px */
}
```

## CSS Best Practices

1. **Always use CSS variables** — never hardcode colors
2. **Scope styles** — prefix all classes with your plugin name
3. **4px grid** — use Obsidian's spacing variables
4. **No `<style>`/`<link>` in TS** — use `styles.css`
5. **Use `setHeading()`** — not `<h2>` in settings
6. **Sentence case** — all UI text
7. **No `!important`** — users can't override with snippets

> Accessibility requirements (keyboard nav, ARIA, focus indicators, touch targets) are in [[reference/accessibility.md]].
