# Typography Reference

## Table of Contents
1. Font Selection
2. Type Scale
3. Font Pairing
4. Line Height and Spacing
5. OpenType Features
6. Pixel and Display Fonts
7. Web Font Loading
8. Curated Font Pairings
9. Variable Fonts
10. Dark Mode Font Weight
11. Metric-Matched Font Fallbacks
12. Common Mistakes

---

## 1. Font Selection

### Banned Defaults
Never use these as primary typefaces: Inter, Roboto, Arial, Helvetica, system-ui, sans-serif (as the only declaration), Space Grotesk (overused in AI contexts), or any font that ships as a browser default.

### Where to Find Good Fonts
- Google Fonts: vast but requires curation. Sort by trending, not popular.
- Bunny Fonts: privacy-friendly Google Fonts mirror.
- Fontshare: free, high-quality fonts from Indian Type Foundry.
- Atipo Foundry: distinctive display and text faces.
- CDN: `https://fonts.cdnfonts.com` for broader selection.

### Selection Criteria
A good typeface for a project should:
- Match the emotional register of the content (a legal dashboard should not use a playful rounded sans)
- Have sufficient weight range (at minimum: regular, medium, bold)
- Include tabular figures if displaying data
- Support the required character sets
- Feel distinct from the last 5 things you built

### The Geist System
Vercel's Geist family offers three complementary typefaces:
- **Geist Sans**: clean, geometric sans for UI text
- **Geist Mono**: monospaced for code and data
- **Geist Pixel**: bitmap-inspired display font with 5 variants (Square, Grid, Circle, Triangle, Line), useful for banners, experimental layouts, and product moments where typography becomes part of the interface language

Install via `npm i geist`. Each variant has its own CSS variable (e.g., `--font-geist-pixel-square`).

---

## 2. Type Scale

Use a modular scale. Pick a ratio and apply it consistently.

| Ratio | Name | Use Case |
|---|---|---|
| 1.125 | Major Second | Dense data UIs, admin panels |
| 1.200 | Minor Third | General purpose, balanced |
| 1.250 | Major Third | Most common, works broadly |
| 1.333 | Perfect Fourth | Editorial, generous spacing |
| 1.500 | Perfect Fifth | Display-heavy, marketing |
| 1.618 | Golden Ratio | High-impact landing pages |

### Calculating Sizes
Base size: 16px (1rem). Multiply up for headings, divide down for captions.

```
Caption:  0.75rem (12px)
Small:    0.875rem (14px)
Body:     1rem (16px)
Large:    1.125rem (18px)
H4:       1.25rem (20px)
H3:       1.563rem (25px)
H2:       1.953rem (31px)
H1:       2.441rem (39px)
Display:  3.052rem (49px)
```

For fluid type, use `clamp()`:
```css
h1 { font-size: clamp(2rem, 5vw + 1rem, 3.5rem); }
```

---

## 3. Font Pairing

### Principles
- Pair fonts with contrasting structures: a serif display with a sans body, or a geometric sans heading with a humanist sans body.
- Never pair fonts that are too similar (two geometric sans faces will fight).
- One display font is enough. Two is almost always too many.
- The body font does the heavy lifting. It must be supremely readable at 16px.

### Proven Pairs
- **Display serif + sans body**: Playfair Display / Source Sans 3
- **Geometric sans + humanist sans**: Outfit / Nunito Sans
- **Slab + grotesque**: Zilla Slab / Work Sans
- **Monospace accent + sans body**: JetBrains Mono / DM Sans
- **Variable display + clean body**: Instrument Serif / Instrument Sans

---

## 4. Line Height and Spacing

| Context | Line Height | Letter Spacing |
|---|---|---|
| Body text | 1.5 to 1.6 | 0 to 0.01em |
| Headings (large) | 1.1 to 1.2 | -0.02 to -0.01em |
| Headings (small) | 1.2 to 1.3 | 0 |
| Captions | 1.4 | 0.02 to 0.05em |
| All caps text | 1.2 | 0.08 to 0.15em |
| Monospace/code | 1.5 to 1.7 | 0 |

### Paragraph Spacing
Use margin-bottom on paragraphs, not margin-top. Space between paragraphs should equal roughly the line-height value (1.5em works well). Never use `<br>` for spacing.

---

## 5. OpenType Features

When the font supports them, enable:
```css
.body-text {
  font-feature-settings: "liga" 1, "kern" 1;
  font-variant-ligatures: common-ligatures;
}
.data-table {
  font-variant-numeric: tabular-nums;
}
.legal-text {
  font-variant-numeric: oldstyle-nums;
}
.heading {
  font-feature-settings: "ss01" 1; /* Stylistic set */
}
```

---

## 6. Pixel and Display Fonts

Pixel fonts are useful for specific moments: retro interfaces, game UIs, terminal aesthetics, or when the digital nature of the medium should be emphasized. They are not novelty fonts when used with system thinking.

Key principles for pixel fonts:
- Only use at sizes that align with the pixel grid (multiples of the font's design size)
- Disable anti-aliasing for crisp rendering: `font-smooth: never; -webkit-font-smoothing: none;`
- Pair with a clean sans for body text
- Use for headings, labels, badges, or UI accents, not paragraphs

---

## 7. Web Font Loading

Use `font-display: swap` to prevent invisible text during load. Preload critical fonts:

```html
<link rel="preload" href="/fonts/display.woff2" as="font" type="font/woff2" crossorigin>
```

Subset fonts to the characters actually used. For Google Fonts, append `&text=` with the specific characters or use `&subset=latin`.

Self-host when possible. CDN fonts introduce a third-party dependency and a DNS lookup.

---

## 8. Curated Font Pairings

Twelve tested pairings using 2025-2026 trending typefaces. Each listing includes the source, ideal use case, and the CSS declaration with proper fallbacks.

### 8.1 Clash Display + Satoshi
- **Source**: Fontshare (free)
- **Use case**: SaaS landing pages, startup marketing sites
- **CSS**:
```css
--font-display: 'Clash Display', 'Arial Black', sans-serif;
--font-body: 'Satoshi', 'Helvetica Neue', Helvetica, sans-serif;
```

### 8.2 Cabinet Grotesk + General Sans
- **Source**: Fontshare (free)
- **Use case**: Creative agencies, portfolio sites, design tools
- **CSS**:
```css
--font-display: 'Cabinet Grotesk', 'Trebuchet MS', sans-serif;
--font-body: 'General Sans', 'Helvetica Neue', Helvetica, sans-serif;
```

### 8.3 Cal Sans + Geist Sans
- **Source**: Cal Sans from cal.com (free, OFL). Geist via `npm i geist`.
- **Use case**: Developer tools, open-source project sites, technical SaaS
- **CSS**:
```css
--font-display: 'Cal Sans', 'Arial Black', sans-serif;
--font-body: 'Geist', system-ui, -apple-system, sans-serif;
```

### 8.4 Instrument Serif + Instrument Sans
- **Source**: Google Fonts (free)
- **Use case**: Editorial, content platforms, long-form reading, magazines
- **CSS**:
```css
--font-display: 'Instrument Serif', Georgia, 'Times New Roman', serif;
--font-body: 'Instrument Sans', 'Helvetica Neue', Helvetica, sans-serif;
```

### 8.5 Clash Display + DM Sans
- **Source**: Clash Display from Fontshare. DM Sans from Google Fonts.
- **Use case**: Fintech dashboards, professional SaaS, enterprise tools
- **CSS**:
```css
--font-display: 'Clash Display', 'Arial Black', sans-serif;
--font-body: 'DM Sans', 'Helvetica Neue', Helvetica, sans-serif;
```

### 8.6 Plus Jakarta Sans + Plus Jakarta Sans
- **Source**: Google Fonts (free)
- **Use case**: Clean SaaS apps, admin panels, health and wellness platforms. Use weight contrast (700+ for headings, 400-500 for body) instead of two families.
- **CSS**:
```css
--font-display: 'Plus Jakarta Sans', 'Helvetica Neue', Helvetica, sans-serif;
--font-body: 'Plus Jakarta Sans', 'Helvetica Neue', Helvetica, sans-serif;
```

### 8.7 Satoshi + Outfit
- **Source**: Satoshi from Fontshare. Outfit from Google Fonts.
- **Use case**: Consumer apps, onboarding flows, friendly dashboards
- **CSS**:
```css
--font-display: 'Satoshi', 'Helvetica Neue', Helvetica, sans-serif;
--font-body: 'Outfit', 'Segoe UI', sans-serif;
```

### 8.8 Cabinet Grotesk + DM Sans
- **Source**: Cabinet Grotesk from Fontshare. DM Sans from Google Fonts.
- **Use case**: E-commerce, product marketing, brand-heavy pages
- **CSS**:
```css
--font-display: 'Cabinet Grotesk', 'Trebuchet MS', sans-serif;
--font-body: 'DM Sans', 'Helvetica Neue', Helvetica, sans-serif;
```

### 8.9 Instrument Serif + General Sans
- **Source**: Instrument Serif from Google Fonts. General Sans from Fontshare.
- **Use case**: Luxury, editorial commerce, lifestyle brands
- **CSS**:
```css
--font-display: 'Instrument Serif', Georgia, 'Times New Roman', serif;
--font-body: 'General Sans', 'Helvetica Neue', Helvetica, sans-serif;
```

### 8.10 Geist Sans + Geist Mono
- **Source**: `npm i geist` (free, Vercel)
- **Use case**: Developer platforms, CLI tools, documentation sites, code-heavy interfaces
- **CSS**:
```css
--font-body: 'Geist', system-ui, -apple-system, sans-serif;
--font-mono: 'Geist Mono', 'Cascadia Code', 'Fira Code', monospace;
```

### 8.11 Clash Display + JetBrains Mono (accent)
- **Source**: Clash Display from Fontshare. JetBrains Mono from Google Fonts or jetbrains.com.
- **Use case**: Technical marketing, API product pages, developer-facing landing pages
- **CSS**:
```css
--font-display: 'Clash Display', 'Arial Black', sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
--font-body: 'Satoshi', 'Helvetica Neue', Helvetica, sans-serif;
```

### 8.12 General Sans + Commit Mono
- **Source**: General Sans from Fontshare. Commit Mono from commitmono.com (free).
- **Use case**: Data-heavy dashboards, analytics platforms, dev tools with mixed prose and code
- **CSS**:
```css
--font-body: 'General Sans', 'Helvetica Neue', Helvetica, sans-serif;
--font-mono: 'Commit Mono', 'Berkeley Mono', 'SF Mono', monospace;
```

### Monospace Quick Reference
| Font | Source | Ligatures | Notes |
|---|---|---|---|
| Geist Mono | npm i geist | No | Clean, pairs with Geist Sans |
| JetBrains Mono | Google Fonts / jetbrains.com | Yes | Best ligature set, great for code blocks |
| Berkeley Mono | berkeleygraphics.com (paid) | No | Premium feel, excellent for terminals and data |
| Commit Mono | commitmono.com | No | Neutral, smart kerning, variable font |

---

## 9. Variable Fonts

### What They Are
Variable fonts pack an entire family (all weights, widths, italics, optical sizes) into a single file. Instead of loading separate files for Regular, Medium, Bold, and Black, you load one `.woff2` that contains a continuous range of values along design axes.

### Core Axes
| Axis | Tag | Range (typical) | Description |
|---|---|---|---|
| Weight | wght | 100-900 | Thin to Black |
| Width | wdth | 75-125 | Condensed to Expanded |
| Italic | ital | 0-1 | Upright to Italic |
| Slant | slnt | -12 to 0 | Oblique angle |
| Optical Size | opsz | 8-144 | Adjust for text size |

### Basic Usage
```css
@font-face {
  font-family: 'Satoshi';
  src: url('/fonts/Satoshi-Variable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-display: swap;
}

h1 { font-weight: 750; }       /* fractional weights */
body { font-weight: 420; }     /* precise control */
caption { font-weight: 350; }  /* lighter than regular */
```

### Weight Animation on Hover
```css
.nav-link {
  font-weight: 400;
  font-variation-settings: 'wght' 400;
  transition: font-variation-settings 0.2s ease;
}
.nav-link:hover {
  font-variation-settings: 'wght' 650;
}
```

Use `font-variation-settings` for animation because `font-weight` transitions are not smooth in all browsers. The `font-variation-settings` property animates along the continuous axis.

### Width Animation
```css
.expandable-label {
  font-variation-settings: 'wdth' 90;
  transition: font-variation-settings 0.3s ease;
}
.expandable-label:hover {
  font-variation-settings: 'wdth' 110;
}
```

### Custom Axes
Some variable fonts include custom axes (always uppercase tags). Example with Recursive:
```css
.code-block {
  font-family: 'Recursive', monospace;
  font-variation-settings: 'MONO' 1, 'CASL' 0, 'wght' 400;
}
.code-comment {
  font-variation-settings: 'MONO' 1, 'CASL' 1, 'wght' 300, 'slnt' -12;
}
```

### Recommended Variable Fonts
| Font | Axes | Source | Notes |
|---|---|---|---|
| Satoshi Variable | wght (300-900) | Fontshare | Best all-around variable sans for UI |
| General Sans Variable | wght (200-700) | Fontshare | Wide weight range, clean geometry |
| Plus Jakarta Sans | wght (200-800) | Google Fonts | Full variable support, friendly geometry |
| Instrument Sans | wght (400-700) | Google Fonts | Pairs with Instrument Serif variable |
| Commit Mono | wght (400-700) | commitmono.com | Monospace with smart kerning axis |

### Performance Benefit
A single variable font file (typically 50-120KB for Latin subset) replaces 4-8 static files (each 15-40KB). This reduces HTTP requests and total download size, especially when using more than 3 weights.

---

## 10. Dark Mode Font Weight

Light text on a dark background appears optically heavier than the same weight on white. Compensate by reducing body font weight in dark mode:

```css
:root[data-theme="dark"] {
  --body-weight: 350;
}
.body {
  font-weight: var(--body-weight, 400);
}
```

Also increase line-height by 0.05-0.1 for light-on-dark text to improve readability. This is a subtle refinement that separates polished dark themes from rushed ones.

---

## 11. Metric-Matched Font Fallbacks (Eliminate CLS)

Custom fonts cause Cumulative Layout Shift when the fallback and custom font have different metrics. Fix this with `@font-face` override descriptors that match the fallback to the custom font:

```css
@font-face {
  font-family: 'CustomFont-Fallback';
  src: local('Arial');
  size-adjust: 105%;
  ascent-override: 90%;
  descent-override: 20%;
  line-gap-override: 10%;
}

/* Use in the font stack */
--font-body: 'Satoshi', 'CustomFont-Fallback', sans-serif;
```

Measure your custom font's metrics against the fallback (tools like `fontpie` or the Chrome DevTools font panel help) and tune these four values. The result: zero layout shift on font load, even with `font-display: swap`.

---

## 12. Common Mistakes

- Using more than 3 font families on a page
- Setting body text below 16px on desktop or 14px on mobile
- Applying letter-spacing to body text (it reduces readability)
- Using light (300) font weight for body text on low-contrast backgrounds
- Centering long paragraphs (center alignment works for 1-2 lines maximum)
- Forgetting to set `max-width` on text blocks (ideal: 60-75 characters per line, roughly 600-750px)
- Using all caps for more than a few words without increasing letter-spacing
- Not adjusting font weight for dark mode (light-on-dark text appears heavier)
- Missing metric-matched fallbacks (causes CLS on font load)
