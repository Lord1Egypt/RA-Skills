# Color and Contrast Reference

## Table of Contents
1. Color Space and Manipulation
2. Palette Construction
3. Tinted Neutrals
4. Dark Mode
5. Accessibility
6. CSS Variables Pattern
7. Curated Color Palettes
8. Wide Gamut Colors (P3)
9. `light-dark()` CSS Function
10. `color-mix()` for Runtime Blending
11. Common Mistakes

---

## 1. Color Space and Manipulation

Use OKLCH for perceptually uniform color. Unlike HSL, OKLCH ensures that colors at the same lightness value actually appear equally bright to the human eye.

```css
/* OKLCH: lightness (0-1), chroma (0-0.4), hue (0-360) */
--accent: oklch(0.65 0.25 25);        /* vibrant red-orange */
--accent-hover: oklch(0.60 0.28 25);  /* darker, more saturated */
--accent-muted: oklch(0.75 0.08 25);  /* same hue, much less chroma */
```

For programmatic palette generation, adjust lightness for tints/shades, chroma for saturation, and hue for variation. OKLCH makes this predictable.

---

## 2. Palette Construction

### The 60-30-10 Rule
- 60% dominant (surface/background)
- 30% secondary (cards, sections, supporting elements)
- 10% accent (CTAs, active states, highlights)

### Building a Palette
1. Start with the accent color (the brand or action color)
2. Derive a surface color: very low chroma version of the accent hue
3. Build neutral scale: tinted toward the accent hue (never pure gray)
4. Add a semantic layer: success (green family), warning (amber), error (red), info (blue)
5. Generate dark mode variants by inverting the lightness scale, not the colors

### Token Structure
```css
:root {
  /* Surfaces */
  --surface-0: oklch(0.99 0.005 80);    /* page background */
  --surface-1: oklch(0.97 0.008 80);    /* card background */
  --surface-2: oklch(0.94 0.01 80);     /* elevated/hover surface */
  --surface-3: oklch(0.90 0.012 80);    /* active/selected surface */

  /* Text */
  --text-primary: oklch(0.15 0.02 80);
  --text-secondary: oklch(0.40 0.02 80);
  --text-tertiary: oklch(0.55 0.015 80);

  /* Accent */
  --accent: oklch(0.55 0.25 30);
  --accent-hover: oklch(0.50 0.28 30);
  --accent-subtle: oklch(0.92 0.04 30);

  /* Borders */
  --border: oklch(0.88 0.01 80);
  --border-strong: oklch(0.78 0.015 80);

  /* Semantic */
  --success: oklch(0.55 0.18 145);
  --warning: oklch(0.65 0.18 70);
  --error: oklch(0.55 0.22 25);
}
```

---

## 3. Tinted Neutrals

Never use pure gray (#808080, rgb(128,128,128), etc.). Always tint neutrals toward the dominant hue of the palette. This creates warmth and cohesion.

**Warm neutrals** (tinted toward amber/brown): suited for editorial, luxury, organic brands
**Cool neutrals** (tinted toward blue/slate): suited for tech, data, professional tools
**Neutral neutrals** (tinted toward the accent hue at very low chroma): the most versatile approach

```css
/* Instead of #333333 */
--text-primary: oklch(0.25 0.015 260);  /* cool-tinted dark */

/* Instead of #f5f5f5 */
--surface-bg: oklch(0.97 0.005 260);    /* cool-tinted light */
```

---

## 4. Dark Mode

Dark mode is not "invert everything." Follow these rules:

1. Surface colors get darker but retain their hue tint
2. Text colors flip but never become pure white (use oklch lightness 0.93-0.97)
3. Accent colors often need a lightness bump (+0.05 to +0.10) to maintain contrast
4. Shadows become less visible on dark surfaces; use subtle inner glows or border effects instead
5. Elevation in dark mode goes lighter (higher surfaces are lighter), opposite of light mode
6. Images and illustrations may need reduced brightness/contrast (`filter: brightness(0.9)`)

```css
[data-theme="dark"] {
  --surface-0: oklch(0.13 0.01 260);
  --surface-1: oklch(0.17 0.012 260);
  --surface-2: oklch(0.21 0.015 260);
  --text-primary: oklch(0.93 0.01 260);
  --text-secondary: oklch(0.70 0.01 260);
  --border: oklch(0.25 0.01 260);
}
```

---

## 5. Accessibility

### Contrast Requirements (WCAG 2.2)
- Normal text (<24px or <18.66px bold): 4.5:1 minimum
- Large text (>=24px or >=18.66px bold): 3:1 minimum
- UI components and graphical objects: 3:1 minimum
- Focus indicators: 3:1 against adjacent colors

### Testing
Use OKLCH lightness difference as a quick heuristic: a difference of 0.40+ between text and background lightness values usually passes AA. For precise checking, use the APCA (Advanced Perceptual Contrast Algorithm) when possible, as it better represents human perception than WCAG 2.x contrast ratios.

### Color Blindness
Never use color as the only way to convey information. Pair color with icons, patterns, or text labels. Test palettes with a deuteranopia/protanopia simulator.

---

## 6. CSS Variables Pattern

Define all colors as CSS custom properties. Group by function, not by color name.

```css
/* Good: semantic naming */
--color-surface: ...;
--color-text: ...;
--color-accent: ...;
--color-border: ...;

/* Bad: literal naming */
--blue: ...;
--dark-gray: ...;
--light-blue: ...;
```

For component-level overrides:
```css
.card {
  --card-bg: var(--surface-1);
  --card-border: var(--border);
  background: var(--card-bg);
  border: 1px solid var(--card-border);
}
.card.highlighted {
  --card-bg: var(--accent-subtle);
  --card-border: var(--accent);
}
```

---

## 7. Curated Color Palettes

Ten tested OKLCH palettes ready to drop into any project. Each includes a complete token set. Copy the one that fits your domain, then adjust chroma and hue to taste.

### 7.1 Warm Terracotta
**Vibe**: Earthy, grounded, artisanal. Good for lifestyle brands, wellness, real estate, organic products.
```css
:root {
  --surface-0: oklch(0.98 0.008 55);
  --surface-1: oklch(0.95 0.012 55);
  --text-primary: oklch(0.18 0.025 55);
  --text-secondary: oklch(0.42 0.02 55);
  --accent: oklch(0.58 0.16 45);
  --accent-hover: oklch(0.52 0.18 45);
  --accent-subtle: oklch(0.93 0.04 45);
  --border: oklch(0.87 0.015 55);
  --success: oklch(0.55 0.16 155);
  --warning: oklch(0.68 0.16 75);
  --error: oklch(0.55 0.20 25);
}
```

### 7.2 Forest Green
**Vibe**: Natural, sustainable, trustworthy. Good for fintech, health, environmental, agriculture.
```css
:root {
  --surface-0: oklch(0.98 0.006 145);
  --surface-1: oklch(0.96 0.01 145);
  --text-primary: oklch(0.17 0.03 150);
  --text-secondary: oklch(0.40 0.02 150);
  --accent: oklch(0.52 0.14 155);
  --accent-hover: oklch(0.46 0.16 155);
  --accent-subtle: oklch(0.93 0.04 155);
  --border: oklch(0.88 0.012 145);
  --success: oklch(0.55 0.16 145);
  --warning: oklch(0.66 0.16 80);
  --error: oklch(0.55 0.20 25);
}
```

### 7.3 Amber Gold
**Vibe**: Premium, confident, optimistic. Good for finance, luxury SaaS, productivity tools.
```css
:root {
  --surface-0: oklch(0.99 0.005 85);
  --surface-1: oklch(0.96 0.01 85);
  --text-primary: oklch(0.16 0.02 85);
  --text-secondary: oklch(0.40 0.018 85);
  --accent: oklch(0.68 0.18 75);
  --accent-hover: oklch(0.62 0.20 75);
  --accent-subtle: oklch(0.94 0.04 75);
  --border: oklch(0.88 0.012 85);
  --success: oklch(0.55 0.16 150);
  --warning: oklch(0.68 0.18 75);
  --error: oklch(0.55 0.20 28);
}
```

### 7.4 Coral Salmon
**Vibe**: Warm, energetic, approachable. Good for social apps, creative tools, food and hospitality.
```css
:root {
  --surface-0: oklch(0.98 0.006 30);
  --surface-1: oklch(0.96 0.01 30);
  --text-primary: oklch(0.18 0.02 30);
  --text-secondary: oklch(0.42 0.018 30);
  --accent: oklch(0.65 0.20 25);
  --accent-hover: oklch(0.58 0.22 25);
  --accent-subtle: oklch(0.94 0.04 25);
  --border: oklch(0.88 0.012 30);
  --success: oklch(0.55 0.16 150);
  --warning: oklch(0.66 0.16 75);
  --error: oklch(0.52 0.22 20);
}
```

### 7.5 Deep Teal
**Vibe**: Calm, medical, authoritative. Good for health tech, enterprise SaaS, data platforms, legal.
```css
:root {
  --surface-0: oklch(0.98 0.005 195);
  --surface-1: oklch(0.96 0.008 195);
  --text-primary: oklch(0.16 0.025 200);
  --text-secondary: oklch(0.40 0.02 200);
  --accent: oklch(0.52 0.12 195);
  --accent-hover: oklch(0.46 0.14 195);
  --accent-subtle: oklch(0.93 0.03 195);
  --border: oklch(0.88 0.01 195);
  --success: oklch(0.55 0.14 155);
  --warning: oklch(0.66 0.16 75);
  --error: oklch(0.55 0.20 25);
}
```

### 7.6 Slate Blue
**Vibe**: Professional, systematic, dependable. Good for project management, B2B SaaS, documentation.
```css
:root {
  --surface-0: oklch(0.98 0.005 250);
  --surface-1: oklch(0.96 0.008 250);
  --text-primary: oklch(0.17 0.02 250);
  --text-secondary: oklch(0.42 0.018 250);
  --accent: oklch(0.55 0.14 250);
  --accent-hover: oklch(0.49 0.16 250);
  --accent-subtle: oklch(0.93 0.03 250);
  --border: oklch(0.88 0.01 250);
  --success: oklch(0.55 0.16 150);
  --warning: oklch(0.66 0.16 75);
  --error: oklch(0.55 0.20 25);
}
```

### 7.7 Burgundy
**Vibe**: Sophisticated, editorial, rich. Good for wine/food, publishing, luxury, fashion.
```css
:root {
  --surface-0: oklch(0.98 0.006 10);
  --surface-1: oklch(0.96 0.01 10);
  --text-primary: oklch(0.16 0.025 10);
  --text-secondary: oklch(0.40 0.02 10);
  --accent: oklch(0.42 0.16 15);
  --accent-hover: oklch(0.36 0.18 15);
  --accent-subtle: oklch(0.93 0.04 15);
  --border: oklch(0.87 0.012 10);
  --success: oklch(0.55 0.16 150);
  --warning: oklch(0.66 0.16 75);
  --error: oklch(0.50 0.20 25);
}
```

### 7.8 Sage
**Vibe**: Soft, organic, restorative. Good for wellness, meditation, journaling, therapy platforms.
```css
:root {
  --surface-0: oklch(0.98 0.006 130);
  --surface-1: oklch(0.95 0.012 130);
  --text-primary: oklch(0.20 0.02 130);
  --text-secondary: oklch(0.42 0.018 130);
  --accent: oklch(0.58 0.10 130);
  --accent-hover: oklch(0.52 0.12 130);
  --accent-subtle: oklch(0.93 0.03 130);
  --border: oklch(0.88 0.01 130);
  --success: oklch(0.55 0.14 150);
  --warning: oklch(0.66 0.15 75);
  --error: oklch(0.55 0.18 25);
}
```

### 7.9 Charcoal with Orange Accent
**Vibe**: Bold, industrial, high-contrast. Good for dev tools, gaming, analytics, creative coding.
```css
:root {
  --surface-0: oklch(0.97 0.003 60);
  --surface-1: oklch(0.94 0.005 60);
  --text-primary: oklch(0.15 0.01 60);
  --text-secondary: oklch(0.40 0.01 60);
  --accent: oklch(0.65 0.22 55);
  --accent-hover: oklch(0.58 0.24 55);
  --accent-subtle: oklch(0.94 0.04 55);
  --border: oklch(0.86 0.008 60);
  --success: oklch(0.55 0.16 150);
  --warning: oklch(0.66 0.18 70);
  --error: oklch(0.55 0.22 25);
}
```

### 7.10 Monochrome Black and White
**Vibe**: Stark, typographic, gallery-like. Good for portfolios, photography, editorial, minimal SaaS.
```css
:root {
  --surface-0: oklch(0.99 0.000 0);
  --surface-1: oklch(0.96 0.000 0);
  --text-primary: oklch(0.13 0.000 0);
  --text-secondary: oklch(0.45 0.000 0);
  --accent: oklch(0.15 0.000 0);
  --accent-hover: oklch(0.25 0.000 0);
  --accent-subtle: oklch(0.93 0.000 0);
  --border: oklch(0.85 0.000 0);
  --success: oklch(0.50 0.14 150);
  --warning: oklch(0.62 0.14 75);
  --error: oklch(0.50 0.18 25);
}
```

For the monochrome palette, the accent is near-black. CTAs rely on fill weight (solid black buttons with white text) rather than color. Semantic colors (success, warning, error) break the monochrome intentionally so they remain functional.

---

## 8. Wide Gamut Colors (P3)

### What is Display P3?
Display P3 is a color space that covers roughly 25% more visible colors than sRGB. Modern Apple devices, most OLED screens, and recent monitors support it. Colors outside the sRGB gamut appear more vivid without being oversaturated.

### CSS Syntax
```css
/* Display P3 via color() function */
--accent: color(display-p3 0.92 0.34 0.15);       /* vivid orange impossible in sRGB */
--success: color(display-p3 0.18 0.75 0.35);       /* richer green */
--highlight: color(display-p3 1 0.85 0);            /* pure P3 yellow */
```

### Feature Detection
```css
@media (color-gamut: p3) {
  :root {
    --accent: color(display-p3 0.92 0.34 0.15);
    --success: color(display-p3 0.18 0.75 0.35);
  }
}
```

### Progressive Enhancement Pattern
Always define an sRGB fallback first, then override for wide gamut displays. This ensures every screen gets a reasonable color.

```css
:root {
  /* sRGB fallback (works everywhere) */
  --accent: oklch(0.65 0.22 35);
  --success: oklch(0.55 0.18 150);
  --highlight: oklch(0.82 0.18 90);
}

@media (color-gamut: p3) {
  :root {
    /* P3 override (wider gamut screens) */
    --accent: oklch(0.65 0.27 35);          /* push chroma beyond sRGB limit */
    --success: oklch(0.55 0.22 150);
    --highlight: oklch(0.82 0.22 90);
  }
}
```

Note: OKLCH values automatically map to the widest gamut the browser and display support. Increasing chroma beyond ~0.15-0.20 (depending on hue) often pushes into P3 territory. This makes OKLCH the ideal space for progressive enhancement because you write one value and the browser resolves it to the best available gamut.

### When to Use P3
- Hero gradients and accent splashes where vibrancy matters
- Success/error states that need to "pop" on capable screens
- Brand colors that were designed in P3 (increasingly common)
- Image overlays and tinted surfaces that blend with wide-gamut photography

### When NOT to Use P3
- Body text colors (perceptual difference is negligible)
- Border and surface tokens (subtle differences, not worth the complexity)
- Any context where the sRGB version already looks correct

---

## 9. `light-dark()` CSS Function

The `light-dark()` function returns one of two values depending on the current `color-scheme`. This eliminates the need for duplicate variable declarations in many cases:

```css
:root {
  color-scheme: light dark;
}

.surface {
  background: light-dark(oklch(0.97 0.005 260), oklch(0.17 0.012 260));
}
.text {
  color: light-dark(oklch(0.20 0.015 260), oklch(0.93 0.01 260));
}
.border {
  border-color: light-dark(oklch(0.88 0.01 260), oklch(0.25 0.01 260));
}
```

Use `light-dark()` for simple color flips (surfaces, text, borders). For complex theme differences (shadow systems, accent adjustments, chroma changes), continue using `[data-theme="dark"]` selectors or CSS custom properties for full control.

Browser support: baseline since March 2024 (Chrome 123, Firefox 120, Safari 17.5).

---

## 10. `color-mix()` for Runtime Blending

`color-mix()` blends two colors at runtime without defining intermediate tokens. Useful for hover states, tinted surfaces, and dynamic theming:

```css
/* Hover: darken accent by mixing with black */
.btn:hover {
  background: color-mix(in oklch, var(--accent), black 15%);
}

/* Subtle tint: mix accent into white */
.surface-tinted {
  background: color-mix(in oklch, var(--accent), white 92%);
}

/* Disabled: reduce opacity feel by mixing with the surface */
.btn:disabled {
  background: color-mix(in oklch, var(--accent), var(--surface-0) 60%);
}
```

Always specify `in oklch` for perceptually uniform blending. Mixing `in srgb` produces muddier results, especially across hues.

---

## 11. Common Mistakes

- Using pure black (#000) for text (use tinted near-black instead)
- Using gray text on colored backgrounds (low contrast, hard to read)
- Applying opacity to achieve lighter colors (makes elements look washed out; use chroma reduction instead)
- Using too many accent colors (one primary accent, one secondary maximum)
- Forgetting to test dark mode after building light mode
- Using brand colors at full saturation for large surfaces (they vibrate and cause eye strain; reserve full chroma for small accents)
- Not providing hover/focus states with visible color change
- Using `color-mix(in srgb, ...)` instead of `color-mix(in oklch, ...)` (sRGB blending produces muddier, less predictable results)
