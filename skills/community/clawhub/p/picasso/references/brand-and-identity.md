# Brand and Identity Reference

## Table of Contents
1. Logo Sizing Rules
2. Logo Placement
3. Logo Lockup Variants
4. Brand Color Usage
5. Brand Typography
6. Consistency Across Pages
7. When to Bend Brand Rules
8. Common Mistakes

---

## 1. Logo Sizing Rules

- **Minimum size:** 24px height for icon-only, 32px height for full logo. Below this it's illegible.
- **Clear space:** Minimum clear space around logo = the height of the logo's icon element. No text or elements may intrude.
- **Typical sizes by context:**

| Context | Height |
|---|---|
| Favicon | 32px |
| Mobile header | 28-32px |
| Desktop header | 32-40px |
| Footer | 24-28px |
| Hero/marketing | 48-64px |
| App splash | 80-120px |

```css
.logo { height: 32px; width: auto; } /* maintain aspect ratio */
.logo-icon { height: 28px; width: 28px; }
```

---

## 2. Logo Placement

- **Header:** top-left for LTR, top-right for RTL. Always links to homepage.
- **Footer:** bottom-left or bottom-center. Smaller than header.
- **Marketing pages:** centered for hero sections, left-aligned for navigation.
- **Loading/splash:** centered vertically and horizontally.

The header logo is the most important. It should be the first visual element the user sees, but not dominate the page. Keep it slim.

---

## 3. Logo Lockup Variants

Every brand needs at least 3 logo variants:

1. **Full lockup:** icon + wordmark (for headers, marketing)
2. **Icon only:** for favicons, app icons, small spaces, mobile headers
3. **Wordmark only:** for editorial/text-heavy contexts

```jsx
// Responsive logo: icon on mobile, full on desktop
<Link href="/" className="flex items-center gap-2">
  <img src="/logo-icon.svg" alt="" className="h-7 w-7" />
  <span className="hidden sm:inline text-sm font-bold tracking-tight">Brand Name</span>
</Link>
```

---

## 4. Brand Color Usage

Follow the 60-30-10 rule with brand colors:
- **60%** — neutral surfaces (backgrounds, cards). Brand color should NOT be the 60%.
- **30%** — supporting colors (borders, secondary text, section backgrounds).
- **10%** — brand/accent color (CTAs, active states, highlights). This is where brand color goes.

```css
:root {
  --brand: oklch(0.55 0.25 250);       /* Primary brand color — use at 10% */
  --brand-subtle: oklch(0.95 0.03 250); /* Tinted background — use sparingly */
  --brand-on-dark: oklch(0.70 0.18 250); /* Lighter variant for dark backgrounds */
}
```

Never use brand color as background for large areas (hero sections, full-width bars) unless the brand is specifically known for it (like Spotify's green). Large saturated surfaces are fatiguing.

---

## 5. Brand Typography

If the brand has a custom/licensed font, use it for headings only. Body text should be a readable, web-optimized font.

```css
/* Brand font for headings */
h1, h2, h3 { font-family: 'Brand Display', var(--font-body); }

/* Readable font for body */
body { font-family: 'DM Sans', system-ui, sans-serif; }
```

If the brand font isn't available for web, find the closest web-safe alternative:
- Futura → use Outfit or Jost
- Helvetica Neue → use Inter (only acceptable here) or Geist
- Garamond → use EB Garamond or Cormorant

---

## 6. Consistency Across Pages

Every page should share:
- Same header and footer (identical, not "similar")
- Same color palette (no page-specific colors)
- Same typography scale
- Same border-radius philosophy
- Same spacing scale

Variation should come from layout and content, not from inconsistent styling. A dashboard page and a marketing page can look different through layout while sharing the same design tokens.

---

## 7. When to Bend Brand Rules

Strict brand adherence isn't always right:
- **Data-dense dashboards:** Brand color as accent only. Don't fight with data colors.
- **Error states:** Use standard red for errors, not brand color. Users need instant recognition.
- **Third-party embeds:** Payment forms, maps, chat widgets have their own styling. Don't fight it.
- **Dark mode:** Brand color may need lightness/chroma adjustment to maintain contrast.
- **Accessibility:** If brand colors don't meet WCAG contrast, accessibility wins.

---

## 8. Common Mistakes

- **Logo too small in the header.** Minimum 28px height. Users need to identify the brand instantly.
- **Brand color as full-width background.** Fatiguing. Use at 10% ratio maximum.
- **Different fonts on every page.** Pick 2 fonts and use them everywhere.
- **Logo without clear space.** Crowded logos look unprofessional. Enforce minimum padding.
- **No icon-only variant.** Mobile needs a compact logo. Don't just shrink the full lockup.
- **Brand color unchanged in dark mode.** Adjust lightness and chroma for dark backgrounds.
- **Inconsistent border radius between pages.** One sharp page and one rounded page = two brands.
