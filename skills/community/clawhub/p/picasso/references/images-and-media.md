# Images and Media Reference

## Table of Contents
1. Format Selection
2. Responsive Images
3. Preventing Layout Shift
4. Image as Design Element
5. Avatar Systems
6. Favicon and App Icons
7. Open Graph Images
8. Video Backgrounds
9. Common Mistakes

---

## 1. Format Selection

| Format | Use Case | Browser Support |
|---|---|---|
| AVIF | Best compression for photos, modern browsers | Chrome, Firefox, Safari 16.4+ |
| WebP | General purpose, wide support | All modern browsers |
| JPEG | Photos, fallback for older browsers | Universal |
| PNG | Transparency, screenshots, UI elements | Universal |
| SVG | Icons, illustrations, logos — scales infinitely | Universal |

Decision tree:
- Is it an icon or illustration? → **SVG**
- Does it need transparency? → **PNG** (or WebP with alpha)
- Is it a photo? → **AVIF** with WebP fallback, JPEG last resort

```html
<picture>
  <source srcset="hero.avif" type="image/avif" />
  <source srcset="hero.webp" type="image/webp" />
  <img src="hero.jpg" alt="Hero description" width="1200" height="630" loading="lazy" />
</picture>
```

---

## 2. Responsive Images

Always provide multiple sizes. The browser picks the best one.

```html
<img
  src="product-800.webp"
  srcset="product-400.webp 400w, product-800.webp 800w, product-1200.webp 1200w"
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 600px"
  alt="Product shot"
  width="800"
  height="600"
  loading="lazy"
  decoding="async"
/>
```

Rules:
- `sizes` must match your CSS layout. If the image is 50% of viewport on desktop, say `50vw`.
- Generate 3-4 variants: 400w, 800w, 1200w, 2400w (for retina).
- Use `loading="lazy"` on everything EXCEPT the LCP image (above the fold).
- Use `decoding="async"` on all images.

---

## 3. Preventing Layout Shift

Every `<img>` without dimensions causes CLS. Always set width and height OR use aspect-ratio.

```html
<!-- Option 1: Explicit dimensions -->
<img src="photo.webp" width="800" height="600" alt="..." />

<!-- Option 2: CSS aspect-ratio -->
<img src="photo.webp" class="w-full aspect-[4/3] object-cover" alt="..." />
```

For Next.js Image component, width/height are required. Use `fill` prop with a sized container for responsive images.

---

## 4. Image as Design Element

```css
/* Cover: fill container, crop to fit */
.hero-img { object-fit: cover; object-position: center 30%; }

/* Contain: show full image, letterbox if needed */
.product-img { object-fit: contain; }

/* Gradient overlay on image */
.card-img-overlay {
  position: relative;
}
.card-img-overlay::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, oklch(0 0 0 / 0.7), transparent 60%);
}
```

---

## 5. Avatar Systems

Consistent sizing scale for avatars:

```css
.avatar-xs { width: 24px; height: 24px; } /* inline mentions */
.avatar-sm { width: 32px; height: 32px; } /* list items */
.avatar-md { width: 40px; height: 40px; } /* cards, comments */
.avatar-lg { width: 56px; height: 56px; } /* profiles */
.avatar-xl { width: 80px; height: 80px; } /* hero profiles */
```

Fallback for missing avatars: use initials on a deterministic background color.

```jsx
function Avatar({ name, src, size = 'md' }) {
  const initials = name.split(' ').map(n => n[0]).join('').slice(0, 2);
  const hue = name.split('').reduce((acc, c) => acc + c.charCodeAt(0), 0) % 360;

  if (src) return <img src={src} alt={name} className={`avatar-${size} rounded-full`} />;
  return (
    <div className={`avatar-${size} rounded-full flex items-center justify-center font-bold text-white`}
      style={{ background: `oklch(0.55 0.15 ${hue})` }}>
      {initials}
    </div>
  );
}
```

---

## 6. Favicon and App Icons

Generate all required formats:

| File | Size | Use |
|---|---|---|
| `favicon.ico` | 32x32 | Legacy browsers |
| `favicon.svg` | Scalable | Modern browsers (supports dark mode via CSS) |
| `apple-touch-icon.png` | 180x180 | iOS home screen |
| `icon-192.png` | 192x192 | Android/PWA |
| `icon-512.png` | 512x512 | PWA splash screen |

```html
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
<link rel="icon" href="/favicon.ico" sizes="32x32" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
```

SVG favicon supports dark mode:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <style>
    circle { fill: #1a1a2e; }
    @media (prefers-color-scheme: dark) { circle { fill: #e0e0ff; } }
  </style>
  <circle cx="16" cy="16" r="14" />
</svg>
```

---

## 7. Open Graph Images

OG images control how your site appears in social shares. Size: **1200x630px**.

Rules:
- Text must be legible at thumbnail size (~300px wide)
- Use 48-72px font size minimum for titles
- High contrast text on background
- Include brand logo (small, corner)
- Don't rely on small text — it's unreadable in feeds

```html
<meta property="og:image" content="https://example.com/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="Product name — tagline" />
```

---

## 8. Video Backgrounds

Use sparingly. Auto-playing background video must be:
- Muted (`muted` attribute required for autoplay)
- Short (5-15 seconds, looped)
- Compressed aggressively (< 2MB)
- Has a poster image fallback
- Respects `prefers-reduced-motion` (show poster only)

```html
<video autoplay muted loop playsinline poster="fallback.webp"
  class="absolute inset-0 w-full h-full object-cover">
  <source src="bg.mp4" type="video/mp4" />
</video>
```

```css
@media (prefers-reduced-motion: reduce) {
  video[autoplay] { display: none; }
  /* Poster image shows via the parent's background */
}
```

---

## 9. Common Mistakes

- **No `width`/`height` on images.** Causes layout shift. Always set dimensions.
- **`loading="lazy"` on the hero image.** The LCP image must load eagerly.
- **JPEG for everything.** Use AVIF/WebP for 50-80% size reduction.
- **Images without `alt` text.** Decorative images use `alt=""`, meaningful images describe the content.
- **Retina images at 1x.** Serve 2x resolution for high-DPI screens via srcset.
- **No `decoding="async"`.** Blocks main thread without it.
- **Favicon only as .ico.** Modern browsers prefer SVG (scales, supports dark mode).
- **OG images with small text.** Unreadable in social feeds. Minimum 48px font.
- **Background video without `prefers-reduced-motion` check.** Accessibility violation.
