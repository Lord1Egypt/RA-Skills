# Design Tokens

This file defines the CSS custom property system. Select a brand preset and copy the corresponding `:root` block into the presentation.

---

## Brand Presets

### Preset: Shopee / Sea (DEFAULT)

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&family=Open+Sans:wght@300;400;500;600;700&family=Roboto+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

```css
:root {
    /* Colors — Shopee Corporate */
    --accent-primary: #ee4d2d;
    --accent-secondary: #05007E;
    --color-heading: #05007E;
    --accent: #ee4d2d;
    --accent-glow: rgba(238, 77, 45, 0.3);
    --bg-primary: #ffffff;
    --bg-secondary: #f7f8fa;
    --bg-card: #f7f8fa;
    --bg-card-hover: #f0f1f5;
    --text-primary: #1a1a1a;
    --text-secondary: #5a5f6b;
    --text-muted: #999999;
    --text-on-accent: #ffffff;
    --border-subtle: rgba(0,0,0,0.06);
    --border-card: #eee;

    /* Typography */
    --font-display: 'Lato', sans-serif;
    --font-body: 'Open Sans', sans-serif;
    --font-mono: 'Roboto Mono', monospace;

    /* Brand Config */
    --brand-has-logo: 1; /* 1 = show logo elements, 0 = hide */
    --section-bg: #05007E; /* section divider background */
}
```

**Logos (MANDATORY — both Shopee AND SeaMoney):** Embed via CSS `content: url(data:image/png;base64,...)` targeting `img.brand-logo.shopee` and `img.brand-logo.seamoney`. Both logos MUST appear on cover slides, section dividers, content headers, and closing slides. Copy the actual base64 data from the most recent presentation file.

```css
img.brand-logo.shopee { content: url(data:image/png;base64,...SHOPEE_LOGO_DATA...); }
img.brand-logo.seamoney { content: url(data:image/png;base64,...SEAMONEY_LOGO_DATA...); }
```

HTML pattern: `<img src="data:," class="brand-logo shopee" alt="Shopee">` and `<img src="data:," class="brand-logo seamoney" alt="SeaMoney">`.

---

### Preset: Neutral / Minimal

```html
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

```css
:root {
    /* Colors — Neutral Corporate */
    --accent-primary: #2563eb;
    --accent-secondary: #1e293b;
    --color-heading: #1e293b;
    --accent: #2563eb;
    --accent-glow: rgba(37, 99, 235, 0.2);
    --bg-primary: #ffffff;
    --bg-secondary: #f8fafc;
    --bg-card: #f8fafc;
    --bg-card-hover: #f1f5f9;
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --text-muted: #94a3b8;
    --text-on-accent: #ffffff;
    --border-subtle: rgba(0,0,0,0.06);
    --border-card: #e2e8f0;

    /* Typography */
    --font-display: 'DM Sans', sans-serif;
    --font-body: 'Inter', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;

    /* Brand Config */
    --brand-has-logo: 0;
    --section-bg: #1e293b;
}
```

**Logos:** None. Hide all `.brand-logo` containers or replace with text-only headers.

---

### Preset: Custom

Start from the Shopee/Sea preset and swap these values:

```css
:root {
    --accent-primary: <USER_PRIMARY_COLOR>;
    --accent-secondary: <USER_SECONDARY_COLOR>;
    --color-heading: <USER_SECONDARY_COLOR>;
    --accent: <USER_PRIMARY_COLOR>;
    --accent-glow: <USER_PRIMARY_COLOR with 0.2 alpha>;
    --section-bg: <USER_SECONDARY_COLOR>;

    /* Typography — swap if user provides font preferences */
    --font-display: <USER_DISPLAY_FONT>;
    --font-body: <USER_BODY_FONT>;
    --font-mono: <USER_MONO_FONT>;

    --brand-has-logo: <1 if user provides logo, else 0>;
}
```

---

## Shared Token Scale (ALL presets use these)

These structural tokens do NOT change between presets:

```css
:root {
    /* Typography — sizes */
    --title-size: clamp(1.5rem, 5vw, 4rem);
    --h2-size: clamp(1.25rem, 3.5vw, 2.5rem);
    --h3-size: clamp(1rem, 2.5vw, 1.75rem);
    --h4-size: clamp(0.85rem, 1.6vw, 1.3rem);
    --body-size: clamp(0.75rem, 1.5vw, 1.125rem);
    --small-size: clamp(0.65rem, 1vw, 0.875rem);
    --eyebrow-size: clamp(0.6rem, 0.95vw, 0.85rem);
    --card-num-size: clamp(0.55rem, 0.8vw, 0.75rem);
    --cta-size: clamp(1.2rem, 2.8vw, 2.2rem);

    /* Spacing */
    --slide-padding: clamp(1rem, 4vw, 4rem);
    --content-gap: clamp(0.5rem, 2vw, 2rem);
    --element-gap: clamp(0.25rem, 1vw, 1rem);

    /* Sidebar */
    --sidebar-width: clamp(180px, 16vw, 240px);

    /* Comment Panel */
    --comment-panel-width: clamp(220px, 20vw, 320px);
    --panel-transition: 0.35s cubic-bezier(0.16, 1, 0.3, 1);

    /* Edit mode */
    --edit-extra: 0px;

    /* Zoom */
    --zoom-level: 1;

    /* Animation */
    --ease: cubic-bezier(0.16, 1, 0.3, 1);
    --duration: 0.7s;
}
```

---

## Base Typography Rules

```css
.slide-content h1 { font-size: var(--title-size); font-weight: 900; line-height: 1.1; font-family: var(--font-display); }
.slide-content h2 { font-size: var(--h2-size); font-weight: 700; line-height: 1.2; font-family: var(--font-display); color: var(--color-heading); }
.slide-content h3 { font-size: var(--h3-size); font-weight: 700; font-family: var(--font-display); color: var(--color-heading); }
.slide-content h4 { font-size: var(--h4-size); font-weight: 700; font-family: var(--font-display); color: var(--color-heading); }
.slide-content p  { font-size: var(--body-size); line-height: 1.6; font-family: var(--font-body); color: var(--text-secondary); }
```

## Status Colors (shared across all presets)

| Color | CSS | Usage |
|-------|-----|-------|
| Green (positive) | `#16803c` | Positive metrics, on-track |
| Red (negative) | `#dc2626` | Negative metrics, at-risk |
| Green bg | `#dcfce7` | On-track badge background |
| Red bg | `#fef2f2` | At-risk badge background |
| Green dots | `#86efac` | Mitigation list markers |
| Red dots | `#fca5a5` | Risk list markers |

## Reveal Animations

```css
.reveal {
    opacity: 0; transform: translateY(25px);
    transition: opacity var(--duration) var(--ease), transform var(--duration) var(--ease);
}
.reveal-left {
    opacity: 0; transform: translateX(-30px);
    transition: opacity var(--duration) var(--ease), transform var(--duration) var(--ease);
}
.reveal-scale {
    opacity: 0; transform: scale(0.92);
    transition: opacity var(--duration) var(--ease), transform var(--duration) var(--ease);
}
.slide.visible .reveal,
.slide.visible .reveal-left,
.slide.visible .reveal-scale {
    opacity: 1; transform: translateY(0) translateX(0) scale(1);
}
.slide.visible .reveal:nth-child(1) { transition-delay: 0.1s; }
.slide.visible .reveal:nth-child(2) { transition-delay: 0.2s; }
.slide.visible .reveal:nth-child(3) { transition-delay: 0.3s; }
.slide.visible .reveal:nth-child(4) { transition-delay: 0.4s; }
.slide.visible .reveal:nth-child(5) { transition-delay: 0.5s; }
.slide.visible .reveal:nth-child(6) { transition-delay: 0.6s; }
```
