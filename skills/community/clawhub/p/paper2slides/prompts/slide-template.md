# Slide HTML Template

Every presentation follows this architecture. Single self-contained HTML file with all CSS and JS inline.

## HTML Structure

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentation Title</title>

    <!-- Fonts from Google Fonts or Fontshare — never system fonts -->
    <link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">

    <style>
        /* === THEME VARIABLES === */
        :root {
            /* Colors — from chosen style preset */
            --bg-primary: ...;
            --text-primary: ...;
            --accent: ...;

            /* Typography — MUST use clamp() */
            --title-size: clamp(2rem, 5.5vw, 4.5rem);
            --h2-size: clamp(1.4rem, 3.5vw, 2.4rem);
            --h3-size: clamp(1rem, 2.2vw, 1.5rem);
            --body-size: clamp(0.78rem, 1.4vw, 1.05rem);
            --small-size: clamp(0.65rem, 1vw, 0.85rem);

            /* Spacing — MUST use clamp() */
            --slide-padding: clamp(1.5rem, 5vw, 5rem);
            --content-gap: clamp(0.75rem, 2vw, 2rem);

            /* Animation */
            --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
            --duration-normal: 0.6s;
        }

        /* === MANDATORY VIEWPORT-BASE CSS === */
        /* Paste the full viewport-base.css contents below */
    </style>
</head>
<body>
    <div class="progress-bar" id="progressBar"></div>
    <nav class="nav-dots" id="navDots"></nav>

    <!-- Slides -->
    <section class="slide title-slide">...</section>
    <section class="slide">...</section>

    <script>/* Presentation controller + optional editor */</script>
</body>
</html>
```

## Mandatory Viewport CSS

Include this ENTIRE block in every presentation:

```css
html, body { height: 100%; overflow-x: hidden; }
html { scroll-snap-type: y mandatory; scroll-behavior: smooth; }

.slide {
    width: 100vw;
    height: 100vh;
    height: 100dvh;
    overflow: hidden;        /* CRITICAL */
    scroll-snap-align: start;
    display: flex;
    flex-direction: column;
    position: relative;
}
.slide-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    max-height: 100%;
    overflow: hidden;
    padding: var(--slide-padding);
}

/* Responsive breakpoints */
@media (max-height: 700px) {
    :root {
        --slide-padding: clamp(0.75rem, 3vw, 2rem);
        --title-size: clamp(1.25rem, 4.5vw, 2.5rem);
    }
}
@media (max-height: 600px) {
    :root {
        --slide-padding: clamp(0.5rem, 2.5vw, 1.5rem);
        --body-size: clamp(0.7rem, 1.2vw, 0.95rem);
    }
    .nav-dots, .decorative { display: none; }
}
@media (max-height: 500px) {
    :root {
        --title-size: clamp(1rem, 3.5vw, 1.5rem);
        --body-size: clamp(0.65rem, 1vw, 0.85rem);
    }
}
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.2s !important;
    }
}
```

## Content Density Limits (per slide)

| Slide Type | Maximum Content |
|------------|-----------------|
| Title | 1 heading + 1 subtitle + tagline |
| Content | 1 heading + 4-6 bullets OR 1 heading + 2 paragraphs |
| Feature grid | 1 heading + 6 cards max (2x3 or 3x2) |
| Code/formula | 1 heading + 8-10 lines |
| Quote | 1 quote (max 3 lines) + attribution |

**Overflow → split into multiple slides. Never cram, never scroll.**

## Animations

```css
.reveal {
    opacity: 0;
    transform: translateY(24px);
    transition: opacity 0.6s var(--ease-out-expo),
                transform 0.6s var(--ease-out-expo);
}
.slide.visible .reveal { opacity: 1; transform: translateY(0); }

/* Stagger children */
.reveal:nth-child(1) { transition-delay: 0.05s; }
.reveal:nth-child(2) { transition-delay: 0.12s; }
.reveal:nth-child(3) { transition-delay: 0.19s; }
.reveal:nth-child(4) { transition-delay: 0.26s; }
```

## Required JavaScript

### SlidePresentation Controller

Must include:
- **IntersectionObserver**: Add `.visible` when slide enters viewport (threshold: 0.5)
- **Keyboard nav**: Arrow keys, Space, PageUp/Down, Home/End
- **Touch nav**: Swipe detection (threshold 50px)
- **Wheel nav**: Debounced (800ms) mouse wheel
- **Progress bar**: Fixed top bar, width = percentage
- **Nav dots**: Fixed right side, generated per slide, click to jump

### Inline Editor (opt-in only)

Only include if user requested editing. Three access methods:

1. **Hotzone hover** — 80×80px fixed top-left, shows ✏️ button with 400ms hide delay
2. **Button click** — Toggle contentEditable on all text elements
3. **E key** — Keyboard shortcut (skip when contenteditable is active)

```javascript
// CRITICAL: Use JS hover with timeout, NOT CSS ~ sibling selector
// CSS-only approach breaks because pointer-events:none on hidden button
// interrupts hover chain when moving from hotzone to button

hotzone.addEventListener('mouseleave', () => {
    hideTimeout = setTimeout(() => {
        if (!editor.isActive) toggle.classList.remove('show');
    }, 400);  // Grace period for mouse movement
});
editToggle.addEventListener('mouseenter', () => {
    clearTimeout(hideTimeout);
});
```

**Save/restore**: Serialize all editable elements' innerHTML to `localStorage` on exit/Ctrl+S. Load on page init.

## CSS Gotcha

Never negate CSS functions directly:
```css
/* WRONG — silently ignored */
right: -clamp(28px, 3.5vw, 44px);

/* CORRECT */
right: calc(-1 * clamp(28px, 3.5vw, 44px));
```
