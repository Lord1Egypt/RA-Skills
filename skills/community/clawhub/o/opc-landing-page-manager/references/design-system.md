# Design System

> Reference for visual design decisions: color, typography, spacing, and layout.
> Load with `read_file("references/design-system.md")` during the Design and Build phases.

---

## Color Palette Selection

### Pre-Built Palettes by Product Type

#### SaaS / Tech Product
```css
--primary: #2563eb;       /* Blue — trust, reliability */
--primary-dark: #1d4ed8;
--accent: #f59e0b;        /* Amber — CTA, attention */
--bg: #ffffff;
--bg-alt: #f8fafc;        /* Slate-50 — alternate sections */
--text: #1e293b;          /* Slate-800 */
--text-muted: #64748b;    /* Slate-500 */
--border: #e2e8f0;        /* Slate-200 */
--success: #10b981;
--error: #ef4444;
```

#### Creative / Design Product
```css
--primary: #8b5cf6;       /* Purple — creativity, premium */
--primary-dark: #7c3aed;
--accent: #f43f5e;        /* Rose — CTA, energy */
--bg: #ffffff;
--bg-alt: #faf5ff;        /* Purple-50 */
--text: #1e1b4b;          /* Indigo-950 */
--text-muted: #6b7280;
--border: #e5e7eb;
--success: #10b981;
--error: #ef4444;
```

#### Business / Finance Product
```css
--primary: #0f766e;       /* Teal — stability, growth */
--primary-dark: #115e59;
--accent: #ea580c;        /* Orange — CTA, warmth */
--bg: #ffffff;
--bg-alt: #f0fdfa;        /* Teal-50 */
--text: #134e4a;          /* Teal-900 */
--text-muted: #6b7280;
--border: #e5e7eb;
--success: #10b981;
--error: #ef4444;
```

#### Bold / Startup
```css
--primary: #dc2626;       /* Red — energy, urgency */
--primary-dark: #b91c1c;
--accent: #facc15;        /* Yellow — CTA, attention */
--bg: #ffffff;
--bg-alt: #fef2f2;        /* Red-50 */
--text: #1c1917;          /* Stone-900 */
--text-muted: #78716c;
--border: #e7e5e4;
--success: #10b981;
--error: #ef4444;
```

#### Minimal / Clean
```css
--primary: #18181b;       /* Near-black — elegance */
--primary-dark: #09090b;
--accent: #2563eb;        /* Blue — subtle CTA */
--bg: #ffffff;
--bg-alt: #fafafa;        /* Zinc-50 */
--text: #18181b;          /* Zinc-900 */
--text-muted: #71717a;    /* Zinc-500 */
--border: #e4e4e7;        /* Zinc-200 */
--success: #10b981;
--error: #ef4444;
```

#### Dark Mode
```css
--primary: #3b82f6;       /* Blue — stands out on dark */
--primary-dark: #2563eb;
--accent: #f59e0b;        /* Amber — high contrast CTA */
--bg: #0f172a;            /* Slate-900 */
--bg-alt: #1e293b;        /* Slate-800 */
--text: #f1f5f9;          /* Slate-100 */
--text-muted: #94a3b8;    /* Slate-400 */
--border: #334155;        /* Slate-700 */
--success: #34d399;
--error: #f87171;
```

### Color Rules

1. **CTA button** uses `--accent` color — must be the highest-contrast interactive element
2. **Primary** is the brand color — used for headings, links, key elements
3. **Background alternates** between `--bg` and `--bg-alt` for visual section separation
4. **Text** uses `--text` for headings and body, `--text-muted` for secondary text
5. **Never use more than 3 colors** (primary + accent + neutral) — simplicity converts

---

## Typography

### Font Stacks (System Fonts — No External Dependencies)

```css
/* Primary — headings */
--font-heading: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;

/* Body — readable text */
--font-body: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;

/* Monospace — code, technical */
--font-mono: 'SF Mono', 'Cascadia Code', 'Fira Code', Consolas, monospace;
```

### Google Fonts Pairings (Optional — User Can Request)

| Heading Font | Body Font | Vibe |
|-------------|-----------|------|
| Inter | Inter | Clean, modern, professional |
| Plus Jakarta Sans | Inter | Friendly, startup |
| DM Sans | DM Sans | Geometric, minimal |
| Outfit | Source Sans 3 | Bold, contemporary |
| Fraunces | Inter | Premium, editorial |
| Space Grotesk | DM Sans | Tech, futuristic |

**Default**: System fonts. Google Fonts only when user requests specific typography or brand requirements.

### Type Scale

```css
--text-xs: 0.75rem;    /* 12px — labels, fine print */
--text-sm: 0.875rem;   /* 14px — captions, meta */
--text-base: 1rem;     /* 16px — body text */
--text-lg: 1.125rem;   /* 18px — lead paragraphs */
--text-xl: 1.25rem;    /* 20px — section intros */
--text-2xl: 1.5rem;    /* 24px — sub-section headings */
--text-3xl: 1.875rem;  /* 30px — section headings */
--text-4xl: 2.25rem;   /* 36px — hero subheadline */
--text-5xl: 3rem;      /* 48px — hero headline (desktop) */
--text-6xl: 3.75rem;   /* 60px — hero headline (large) */
```

### Typography Rules

1. **Max 2 font families** — one for headings, one for body (or the same for both)
2. **Body text ≥ 16px** — never smaller on any device
3. **Line height**: 1.5 for body, 1.2 for headings
4. **Max line length**: 65-75 characters per line (~600px container for body text)
5. **Font weight contrast**: Headings 600-800, body 400
6. **Letter spacing**: Slight increase (0.01-0.02em) for uppercase labels

---

## Spacing System

```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
--space-24: 6rem;     /* 96px */
--space-32: 8rem;     /* 128px */
```

### Section Spacing

| Element | Desktop | Mobile |
|---------|---------|--------|
| Between sections | `--space-20` to `--space-24` (80-96px) | `--space-12` to `--space-16` (48-64px) |
| Section padding (horizontal) | `--space-8` (32px) | `--space-4` to `--space-6` (16-24px) |
| Between heading and content | `--space-6` to `--space-8` (24-32px) | `--space-4` (16px) |
| Between content blocks | `--space-4` to `--space-6` (16-24px) | `--space-4` (16px) |
| Between paragraphs | `--space-4` (16px) | `--space-4` (16px) |

---

## Layout Patterns

### Max Widths

```css
--max-w-content: 1200px;  /* Content container */
--max-w-text: 680px;       /* Text-heavy sections */
--max-w-wide: 1400px;      /* Full-width sections with padding */
```

### Grid Patterns

```css
/* 2-column split (hero, text + image) */
.split { display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; }

/* 3-column grid (features, benefits) */
.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; }

/* 4-column grid (logos, small items) */
.grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; }

/* Mobile: all stack to single column */
@media (max-width: 768px) {
  .split, .grid-3, .grid-4 {
    grid-template-columns: 1fr;
  }
}
```

### Responsive Breakpoints

```css
/* Mobile first */
/* Default: mobile (< 640px) */
@media (min-width: 640px)  { /* sm — large phones, small tablets */ }
@media (min-width: 768px)  { /* md — tablets */ }
@media (min-width: 1024px) { /* lg — desktops */ }
@media (min-width: 1280px) { /* xl — large desktops */ }
```

---

## Component Styles

### Buttons

```css
/* Primary CTA */
.btn-primary {
  background: var(--accent);
  color: white;
  padding: 0.875rem 2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 1.125rem;
  border: none;
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s;
}
.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* Secondary/Ghost */
.btn-secondary {
  background: transparent;
  color: var(--primary);
  padding: 0.875rem 2rem;
  border: 2px solid var(--primary);
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
}
```

### Cards

```css
.card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  padding: 2rem;
  transition: box-shadow 0.2s;
}
.card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
```

### Section Alternation

```css
.section { padding: 5rem 2rem; }
.section-alt { background: var(--bg-alt); }
```

---

## Visual Hierarchy Rules

1. **Size**: Larger = more important. Hero headline > section heading > body text.
2. **Weight**: Bolder = more important. 700+ for key messages, 400 for body.
3. **Color**: High contrast for primary content, muted for secondary.
4. **Space**: More whitespace around important elements isolates and emphasizes them.
5. **Position**: Top-left (in LTR) gets read first. CTA should be in the natural scan path.

### Emphasis Order (For Any Section)

1. Heading — largest, boldest
2. Key statistic or value proposition — second largest or highlighted color
3. Supporting text — normal body size
4. CTA or link — accent color, clear interactive affordance
5. Fine print — smallest, most muted

---

## Image Placeholders

Since the skill generates HTML without real images, use these placeholder strategies:

### CSS Gradient Placeholders
```css
.hero-visual {
  background: linear-gradient(135deg, var(--primary-dark), var(--primary));
  border-radius: 1rem;
  aspect-ratio: 16/9;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.25rem;
}
```

### SVG Icon Placeholders
Use inline SVG for feature icons — no external dependencies.

### Image Source Comments
```html
<!-- Replace with: product screenshot, 1200x800px, PNG or WebP -->
<div class="hero-visual">
  <span>📸 Product Screenshot</span>
</div>
```

---

## Accessibility Basics

1. **Color contrast**: Text must have 4.5:1 ratio against background (WCAG AA)
2. **Alt text**: All informational images need alt attributes
3. **Semantic HTML**: Use `<header>`, `<main>`, `<section>`, `<footer>`, `<nav>`
4. **Keyboard navigation**: CTA buttons must be focusable and have focus styles
5. **Skip navigation**: Include a skip-to-content link for screen readers
6. **Form labels**: All input fields have associated labels
7. **Heading hierarchy**: h1 → h2 → h3, never skip levels

---

*Reference for opc-landing-page-manager.*
