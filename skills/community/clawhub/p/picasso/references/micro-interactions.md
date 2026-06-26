# Micro-Interactions Reference

## Table of Contents
1. Scroll-Triggered Animations
2. Page Transitions
3. Button and Press Feedback
4. Toggle and Switch Animations
5. Number and Text Morphing
6. Magnetic and Cursor Effects
7. Gesture-Based Interactions
8. Animation Performance Budget
9. Common Mistakes

---

## 1. Scroll-Triggered Animations

Use IntersectionObserver. Never `addEventListener('scroll')` — it fires on every pixel and destroys performance.

```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('revealed');
      observer.unobserve(entry.target); // animate once
    }
  });
}, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.reveal-on-scroll').forEach(el => observer.observe(el));
```

```css
.reveal-on-scroll {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.5s var(--ease-out), transform 0.5s var(--ease-out);
}
.reveal-on-scroll.revealed {
  opacity: 1;
  transform: translateY(0);
}
```

Parallax: max 10% speed difference. More than that causes motion sickness.

```css
.parallax-slow { transform: translateY(calc(var(--scroll-y) * -0.05)); }
```

---

## 2. Page Transitions

View Transitions API for smooth page-to-page navigation:

```css
::view-transition-old(root) {
  animation: fade-out 200ms ease-in forwards;
}
::view-transition-new(root) {
  animation: fade-in 300ms ease-out forwards;
}

@keyframes fade-out { to { opacity: 0; } }
@keyframes fade-in { from { opacity: 0; } }
```

```js
// In Next.js App Router or SPA
if (document.startViewTransition) {
  document.startViewTransition(() => {
    // Update DOM here
  });
}
```

Shared element transitions for items that persist between pages:

```css
.product-image { view-transition-name: product-hero; }

::view-transition-old(product-hero),
::view-transition-new(product-hero) {
  animation-duration: 300ms;
}
```

---

## 3. Button and Press Feedback

Combine scale + shadow reduction for a physical "press" feel:

```css
.btn {
  transition: transform 80ms ease-out, box-shadow 80ms ease-out;
}
.btn:active {
  transform: scale(0.97);
  box-shadow: 0 1px 2px oklch(0 0 0 / 0.1); /* shadow shrinks on press */
}
```

For icon buttons, use a radial ripple:

```css
.icon-btn {
  position: relative;
  overflow: hidden;
}
.icon-btn::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at var(--x, 50%) var(--y, 50%), oklch(1 0 0 / 0.1) 0%, transparent 60%);
  opacity: 0;
  transition: opacity 150ms;
}
.icon-btn:active::after { opacity: 1; }
```

---

## 4. Toggle and Switch Animations

```css
.toggle-track {
  width: 44px;
  height: 24px;
  border-radius: 12px;
  background: var(--surface-3);
  transition: background-color 200ms ease-out;
  position: relative;
}
.toggle-track[aria-checked="true"] {
  background: var(--accent);
}
.toggle-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: white;
  position: absolute;
  top: 2px;
  left: 2px;
  transition: transform 200ms var(--ease-out);
  box-shadow: 0 1px 3px oklch(0 0 0 / 0.15);
}
.toggle-track[aria-checked="true"] .toggle-thumb {
  transform: translateX(20px);
}
```

Checkbox checkmark: draw with SVG stroke-dasharray animation (150ms).

---

## 5. Number and Text Morphing

For counters and changing text, use `torph` or CSS counter animation:

```css
@property --num {
  syntax: '<integer>';
  initial-value: 0;
  inherits: false;
}
.counter {
  transition: --num 1s ease-out;
  counter-reset: num var(--num);
}
.counter::after {
  content: counter(num);
}
```

For text morphing between labels (e.g., tab switching):

```jsx
import { TextMorph } from 'torph/react';

<TextMorph>{activeTab === 'overview' ? 'Overview' : 'Details'}</TextMorph>
```

---

## 6. Magnetic and Cursor Effects

Subtle magnetic pull toward buttons/links. Max displacement: 8px. Only on desktop (no hover on mobile).

```js
// Apply to elements with data-magnetic
document.querySelectorAll('[data-magnetic]').forEach(el => {
  el.addEventListener('mousemove', (e) => {
    const rect = el.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;
    el.style.transform = `translate(${x * 0.15}px, ${y * 0.15}px)`;
  });
  el.addEventListener('mouseleave', () => {
    el.style.transform = '';
    el.style.transition = 'transform 0.3s var(--ease-out)';
  });
});
```

Custom cursor (use sparingly — only for creative/portfolio sites):

```css
.custom-cursor {
  cursor: none;
}
.cursor-dot {
  width: 8px; height: 8px;
  background: var(--accent);
  border-radius: 50%;
  position: fixed;
  pointer-events: none;
  z-index: 9999;
  transition: transform 0.1s;
  mix-blend-mode: difference;
}
```

---

## 7. Gesture-Based Interactions

Mobile gestures require `touch-action` CSS to prevent browser defaults:

```css
/* Horizontal swipe area — disable horizontal scroll */
.swipe-container { touch-action: pan-y; }

/* Pinch-to-zoom area */
.zoomable { touch-action: manipulation; }
```

Swipe detection (vanilla, no library):

```js
let startX = 0;
el.addEventListener('touchstart', e => { startX = e.touches[0].clientX; });
el.addEventListener('touchend', e => {
  const diff = e.changedTouches[0].clientX - startX;
  if (Math.abs(diff) > 50) { // 50px threshold
    diff > 0 ? onSwipeRight() : onSwipeLeft();
  }
});
```

Gesture discoverability: NEVER rely on hidden gestures. Always provide a visible button alternative. Swipe should be a shortcut, not the only way.

---

## 8. Animation Performance Budget

- **Max 3 concurrent animations** on screen at once. More causes frame drops on mid-range devices.
- **Only animate `transform` and `opacity`** — these are compositor-only and skip layout/paint.
- **Use `will-change` sparingly** — add before animation starts, remove after. Never `will-change: all`.
- **16ms frame budget** — if your animation JS takes more than 16ms per frame, it drops below 60fps.
- **Test with CPU throttling** — Chrome DevTools → Performance → CPU 6x slowdown. If it stutters there, it stutters on real phones.

```css
/* Good: compositor-only */
.animate-enter {
  will-change: transform, opacity;
  animation: slide-in 300ms var(--ease-out) forwards;
}
.animate-enter.done { will-change: auto; } /* remove after animation */

@keyframes slide-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
```

---

## 9. Common Mistakes

- **`addEventListener('scroll')` for animations.** Use IntersectionObserver.
- **Animating `width`, `height`, `top`, `left`.** Triggers layout. Use `transform` only.
- **More than 3 concurrent animations.** Causes jank on real devices.
- **`will-change` on everything.** Creates a compositing layer per element. Memory hog.
- **Parallax with large speed differences.** Max 10% or users get motion sick.
- **Hidden gestures with no visible alternative.** Users won't discover them.
- **No `prefers-reduced-motion` check.** Wrap all non-essential motion in the media query.
- **Magnetic effects on mobile.** No hover on touch devices. Gate with `@media (hover: hover)`.
- **Page transitions without fallback.** View Transitions API isn't universal. Always provide a no-transition fallback.
