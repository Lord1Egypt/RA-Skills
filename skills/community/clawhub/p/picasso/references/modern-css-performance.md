# Modern CSS & Web Performance Reference

## 1. Modern CSS Features (2024-2025)

### CSS Nesting (Baseline 2024)
Native nesting eliminates preprocessor dependency.

```css
.card {
  padding: 1rem;
  > h2:first-child { margin-block-start: 0; }
  &:hover { box-shadow: 0 4px 12px rgb(0 0 0 / 0.1); }
  @media (width >= 768px) { padding: 2rem; }
}
```

### Cascade Layers (@layer)
Control specificity ordering without selector wars.

```css
@layer reset, base, components, utilities;
@layer reset { *, *::before, *::after { box-sizing: border-box; margin: 0; } }
@layer base { body { font-family: system-ui; line-height: 1.6; } }
@layer components { .btn { padding: 0.5rem 1rem; border-radius: 0.375rem; } }
```

### :has() Selector
Style parents based on children.

```css
form:has(:invalid) { border-color: red; }
.card:has(img) { grid-template-rows: auto 1fr; }
body:has(dialog[open]) { overflow: hidden; }
```

### CSS Anchor Positioning
Position elements relative to other elements without JS.

```css
.trigger { anchor-name: --tooltip-anchor; }
.tooltip {
  position: absolute;
  position-anchor: --tooltip-anchor;
  top: anchor(bottom);
  left: anchor(center);
  translate: -50% 0.5rem;
}
```

### @scope
Restrict styles to a DOM subtree with optional lower boundary.

```css
@scope (.card) to (.card-content) {
  h2 { font-size: 1.25rem; font-weight: 600; }
  p { color: var(--muted); }
}
```

### @property (Typed Custom Properties)
Register custom properties with type, initial value, and inheritance. Enables animating custom properties.

```css
@property --gradient-angle {
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}
.gradient-border {
  --gradient-angle: 0deg;
  border-image: conic-gradient(from var(--gradient-angle), #f06, #9f6, #06f) 1;
  animation: spin 3s linear infinite;
}
@keyframes spin { to { --gradient-angle: 360deg; } }
```

### color-mix()
Blend colors in any color space at runtime.

```css
.button {
  --brand: oklch(0.65 0.25 260);
  background: var(--brand);
  &:hover { background: color-mix(in oklch, var(--brand) 85%, white); }
  &:active { background: color-mix(in oklch, var(--brand) 80%, black); }
}
```

### Logical Properties
Write direction-agnostic layouts (LTR/RTL safe).

Key mappings: `margin-left` -> `margin-inline-start`, `padding-top` -> `padding-block-start`, `width` -> `inline-size`, `height` -> `block-size`.

```css
.sidebar { margin-inline-end: 2rem; padding-block: 1rem; border-inline-start: 3px solid var(--accent); }
```

### Subgrid
Child grids align to parent grid tracks.

```css
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.grid > .card {
  display: grid;
  grid-row: span 3;
  grid-template-rows: subgrid;
}
```

### Popover API
Native popovers with light-dismiss, no JS required.

```html
<button popovertarget="info">Info</button>
<div popover id="info">Content here. Click outside to dismiss.</div>
```

```css
[popover] {
  &::backdrop { background: rgb(0 0 0 / 0.25); }
  opacity: 0; transition: opacity 0.2s, display 0.2s allow-discrete;
  &:popover-open { opacity: 1; }
}
```

---

## 2. Core Web Vitals Optimization

**Thresholds:** LCP < 2.5s | CLS < 0.1 | INP < 200ms

### LCP (Largest Contentful Paint)
- Preload hero images: `<link rel="preload" as="image" href="hero.webp" fetchpriority="high">`
- Use `fetchpriority="high"` on the LCP `<img>` element.
- Eliminate render-blocking CSS/JS; inline critical CSS.
- Use CDN, compress with Brotli.

### CLS (Cumulative Layout Shift)
- Always set `width`/`height` or `aspect-ratio` on images and video.
- Reserve space for ads/embeds with `min-height`.
- Use `font-display: optional` (best CLS) or `swap` (best UX).
- Avoid inserting content above the fold after load.

### INP (Interaction to Next Paint)
Replaced FID in March 2024. Measures all interactions across the page lifecycle.

```js
button.addEventListener('click', () => {
  button.classList.add('pressed');       // instant visual feedback
  requestAnimationFrame(() => {
    setTimeout(() => doHeavyWork(), 0);  // yield to browser
  });
});
```

- Break long tasks with `scheduler.yield()` (or `setTimeout(0)` fallback).
- Use `content-visibility: auto` for off-screen DOM.
- Avoid layout thrashing: batch reads, then batch writes.

---

## 3. Image Optimization

| Format | Best For | vs JPEG |
|--------|----------|---------|
| **AVIF** | Photos, complex images | ~50% smaller |
| **WebP** | Photos, transparency | ~30% smaller |
| **SVG** | Icons, logos, illustrations | Infinitely scalable |
| **PNG** | Screenshots, pixel-precise | Lossless only |

### Responsive Images Pattern

```html
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg"
    srcset="hero-400.jpg 400w, hero-800.jpg 800w, hero-1200.jpg 1200w"
    sizes="(max-width: 600px) 100vw, (max-width: 1200px) 50vw, 33vw"
    alt="Hero" width="1200" height="675"
    loading="lazy" decoding="async">
</picture>
```

**Rules:** Never lazy-load above-the-fold images (hurts LCP). Use `fetchpriority="high"` on LCP image. Always include `width`/`height` for CLS prevention.

### Blur-Up Placeholder

```css
.img-placeholder {
  background: url('data:image/webp;base64,...') center/cover;
  aspect-ratio: 16/9;
}
.img-placeholder img {
  opacity: 0; transition: opacity 0.3s;
  &.loaded { opacity: 1; }
}
```

---

## 4. Font Performance

### Optimal Loading Strategy

```html
<link rel="preload" href="/fonts/display.woff2" as="font" type="font/woff2" crossorigin>
```

```css
@font-face {
  font-family: 'Display';
  src: url('/fonts/display.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;
  unicode-range: U+0000-00FF;
}
```

### font-display Decision Guide
- **`swap`**: shows fallback immediately, swaps when loaded. Best for body text. Causes FOUT.
- **`optional`**: uses web font only if cached/instant. Best CLS score.
- **`fallback`**: 100ms blank, then fallback, short swap window. Good compromise.
- **`block`**: up to 3s invisible text (FOIT). Avoid for body text.

### Variable Fonts
One file replaces multiple weight/style files. Use when you need 3+ weights. A single variable font (~90KB) replaces 6 static files (360KB+).

### Subsetting
Strip unused glyphs with `pyftsubset` or `glyphhanger`. Can reduce 200KB+ files to 15-30KB.

---

## 5. Critical CSS & Resource Hints

### Critical CSS Pattern

```html
<head>
  <style>/* inlined above-the-fold styles, ~14KB max */</style>
  <link rel="preload" href="/styles.css" as="style" onload="this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="/styles.css"></noscript>
</head>
```

### Resource Hints

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="dns-prefetch" href="https://analytics.example.com">
<link rel="preload" href="/critical.woff2" as="font" crossorigin>
<link rel="prefetch" href="/next-page.js">
<link rel="modulepreload" href="/app.js">
```

**Build tools:** Use `critical` (npm) or `critters` (webpack/vite plugin) to auto-extract above-fold CSS at build time.

---

## 6. Tailwind CSS v4

Released January 2025. Core rewritten in Rust (Oxide engine). Full builds 3.8x faster, incremental rebuilds up to 182x faster.

### CSS-First Configuration

```css
@import "tailwindcss";

@theme {
  --color-brand: oklch(0.65 0.25 260);
  --font-display: "Satoshi", sans-serif;
  --breakpoint-3xl: 1920px;
  --ease-fluid: cubic-bezier(0.3, 0, 0, 1);
}
```

No `tailwind.config.js` needed. All customization lives in CSS via `@theme`.

### Key Changes
- **Automatic content detection** -- scans files, respects `.gitignore`.
- **Built on `@layer`, `@property`, `color-mix()`**.
- **Container queries** built in: `@sm:`, `@md:` variants.
- **3D transforms**: `rotate-x-45 transform-3d perspective-distant`.
- **`@starting-style`** support for enter/exit transitions with `transition-discrete`.
- **`not-*` variant**: `not-hover:opacity-75`, `not-last:border-b`.

---

## 7. Advanced Animation APIs

### View Transitions API

```css
@view-transition { navigation: auto; }
.hero-image { view-transition-name: hero; }
::view-transition-old(hero) { animation: fade-out 0.3s ease-out; }
::view-transition-new(hero) { animation: fade-in 0.3s ease-in; }
```

```js
document.startViewTransition(() => updateDOM());
```

### Scroll-Driven Animations (No JS, Off Main Thread)

```css
.progress-bar {
  animation: grow-width linear;
  animation-timeline: scroll();
}
@keyframes grow-width { from { width: 0; } to { width: 100%; } }

.reveal {
  animation: fade-slide-up linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}
@keyframes fade-slide-up {
  from { opacity: 0; translate: 0 2rem; }
  to { opacity: 1; translate: 0; }
}
```

### Web Animations API (WAAPI)

```js
element.animate(
  [{ transform: 'translateY(0)', opacity: 1 },
   { transform: 'translateY(-20px)', opacity: 0 }],
  { duration: 300, easing: 'ease-out', fill: 'forwards' }
);
```

### GSAP ScrollTrigger

```js
gsap.to('.hero-title', {
  scrollTrigger: {
    trigger: '.hero', start: 'top top', end: 'bottom top',
    scrub: true, pin: true
  },
  y: -100, opacity: 0, scale: 0.9
});
```

---

## Browser Support (Baseline 2025)

| Feature | Chrome | Firefox | Safari |
|---------|--------|---------|--------|
| CSS Nesting | 120+ | 117+ | 17.2+ |
| :has() | 105+ | 121+ | 15.4+ |
| @layer | 99+ | 97+ | 15.4+ |
| Subgrid | 117+ | 71+ | 16+ |
| Anchor Positioning | 125+ | Nightly | No |
| View Transitions (SPA) | 111+ | 144+ | 18+ |
| Scroll-driven Animations | 115+ | Nightly | No |
| Popover API | 114+ | 125+ | 17+ |
| @property | 85+ | 128+ | 15.4+ |
| color-mix() | 111+ | 113+ | 16.2+ |
