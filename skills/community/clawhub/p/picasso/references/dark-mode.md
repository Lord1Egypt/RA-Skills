# Dark Mode Reference

## Table of Contents
1. Preference Hierarchy
2. CSS Custom Properties Approach
3. Mode Transition
4. Surface Elevation in Dark Mode
5. Color Adjustments
6. Image and Media Handling
7. Testing Dark Mode
8. Forced Colors and High Contrast
9. Common Mistakes

---

## 1. Preference Hierarchy

System preference is the default. User override persists via localStorage. Never force dark mode without a toggle.

```js
// Check system preference, then user override
const stored = localStorage.getItem('theme');
const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
const isDark = stored ? stored === 'dark' : systemDark;
document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
```

```css
/* System preference as base */
:root { color-scheme: light dark; }

/* Light (default) */
:root, [data-theme="light"] {
  --surface-0: oklch(0.99 0.005 var(--hue));
  --text-primary: oklch(0.15 0.02 var(--hue));
}

/* Dark */
[data-theme="dark"] {
  --surface-0: oklch(0.11 0.02 var(--hue));
  --text-primary: oklch(0.93 0.01 var(--hue));
}
```

---

## 2. CSS Custom Properties Approach

Define all colors as CSS variables. Never hardcode hex in components. Dark mode is a variable swap, not a rewrite.

```css
[data-theme="dark"] {
  --surface-0: oklch(0.11 0.02 230);   /* page bg */
  --surface-1: oklch(0.14 0.02 230);   /* card bg */
  --surface-2: oklch(0.17 0.022 230);  /* elevated bg */
  --surface-3: oklch(0.20 0.024 230);  /* hover bg */
  --border: oklch(0.22 0.015 230);
  --text-primary: oklch(0.93 0.01 230);
  --text-secondary: oklch(0.62 0.02 230);
  --text-muted: oklch(0.42 0.015 230);
}
```

---

## 3. Mode Transition

Never instant-swap. Use a 200ms opacity transition on the body. Disable transitions during the swap to prevent every element animating individually.

```css
/* Add this class during theme switch, remove after 200ms */
.theme-transitioning * {
  transition: none !important;
}

body {
  transition: background-color 0.2s ease-out, color 0.2s ease-out;
}
```

```js
function toggleTheme() {
  document.body.classList.add('theme-transitioning');
  const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = next;
  localStorage.setItem('theme', next);
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      document.body.classList.remove('theme-transitioning');
    });
  });
}
```

---

## 4. Surface Elevation in Dark Mode

In dark mode, elevated surfaces get LIGHTER, not darker. This is the opposite of light mode where shadows darken surfaces. Without this, dark mode looks flat.

```
Light mode elevation:  surface-0 (lightest) → surface-3 (slightly darker)
Dark mode elevation:   surface-0 (darkest)  → surface-3 (slightly lighter)
```

Shadows are nearly invisible in dark mode. Replace with surface lightness differentiation and subtle border glow:

```css
[data-theme="dark"] .card {
  background: var(--surface-1);
  border: 1px solid oklch(1 0 0 / 0.06);
  /* Shadow optional — use border + surface tint instead */
  box-shadow: 0 0 0 1px oklch(1 0 0 / 0.03);
}
```

---

## 5. Color Adjustments

Accent colors need lower chroma in dark mode. Full-saturation accents on dark backgrounds are harsh.

```css
:root { --accent: oklch(0.55 0.25 250); }         /* light: saturated */
[data-theme="dark"] { --accent: oklch(0.65 0.18 250); } /* dark: lighter, less chroma */
```

Semantic colors also need adjustment:
- Success green: lighter, less saturated
- Error red: lighter to maintain contrast
- Warning amber: reduce chroma to avoid glowing

Text colors: minimum lightness 0.60 in OKLCH for body text on dark backgrounds. Below 0.55 looks washed out on cheap screens even if it passes WCAG.

---

## 6. Image and Media Handling

Dim images slightly in dark mode to reduce glare. SVGs should use currentColor or CSS variables.

```css
[data-theme="dark"] img:not([data-no-dim]) {
  filter: brightness(0.9) contrast(1.05);
}

[data-theme="dark"] svg { color: var(--text-primary); }
```

For decorative images, consider `mix-blend-mode: luminosity` to desaturate:
```css
[data-theme="dark"] .hero-image {
  mix-blend-mode: luminosity;
  opacity: 0.8;
}
```

---

## 7. Testing Dark Mode

Dark mode is not "invert the colors." Test these specifically:

1. **Contrast ratios** — recheck all text/background pairs. WCAG ratios change.
2. **Shadows** — are they visible? If not, use border or surface tint instead.
3. **Form inputs** — autofill styling overrides your dark background. Fix with `-webkit-box-shadow: 0 0 0 1000px var(--surface-1) inset`.
4. **Selection color** — `::selection` background needs to contrast with dark text highlight.
5. **Scrollbar** — custom scrollbar thumb must be visible on dark track.
6. **Third-party embeds** — iframes, maps, payment forms may not respect your dark mode.
7. **Screenshots** — take a screenshot and look at it on a non-retina screen. Subtle contrast often vanishes.

---

## 8. Forced Colors and High Contrast

Windows High Contrast mode (`@media (forced-colors: active)`) overrides ALL custom colors. Your tinted neutrals, subtle borders, and custom focus rings will disappear.

```css
@media (forced-colors: active) {
  .card { border: 1px solid CanvasText; }
  :focus-visible { outline: 2px solid Highlight; }
  .btn-primary { border: 2px solid ButtonText; }
}
```

Never use `forced-color-adjust: none` globally. Only on specific elements where you've provided a system-color fallback.

---

## 9. Common Mistakes

- **Instant theme swap without transition.** Jarring. Always fade (200ms).
- **Shadows that work in light but vanish in dark.** Replace with borders + surface tint.
- **Same accent chroma in both modes.** Reduce chroma for dark mode.
- **Checking contrast only in light mode.** Dark mode ratios are different — recheck.
- **`background: black` for dark mode.** Never pure black. Tint toward your hue.
- **Not testing autofill.** Browsers apply white backgrounds to autofilled inputs.
- **Not testing scrollbar.** Custom scrollbar may be invisible on dark backgrounds.
- **Storing theme in state instead of localStorage.** Causes flash of wrong theme on reload.
- **No `color-scheme: dark` declaration.** Browser UI elements (scrollbars, form controls) won't adapt without it.
