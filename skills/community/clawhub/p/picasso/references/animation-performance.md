# Animation Performance Reference

## Table of Contents
1. Compositor-Only Properties
2. Will-Change Best Practices
3. Layout Thrashing
4. IntersectionObserver vs Scroll Events
5. Web Animations API
6. Performance Measurement
7. Testing on Low-End Devices
8. Contain Property
9. Common Mistakes

---

## 1. Compositor-Only Properties

Only two CSS properties can be animated without triggering layout or paint: **transform** and **opacity**. Everything else causes reflow.

| Property | Layout | Paint | Composite | Animate? |
|---|---|---|---|---|
| `transform` | No | No | Yes | **Yes** |
| `opacity` | No | No | Yes | **Yes** |
| `filter` | No | Yes | Yes | Carefully |
| `background-color` | No | Yes | No | Avoid |
| `width`, `height` | Yes | Yes | No | **Never** |
| `top`, `left` | Yes | Yes | No | **Never** |
| `margin`, `padding` | Yes | Yes | No | **Never** |
| `border-radius` | No | Yes | No | Avoid |

```css
/* Good: compositor-only */
.slide-in {
  transform: translateX(-100%);
  opacity: 0;
  transition: transform 300ms var(--ease-out), opacity 300ms var(--ease-out);
}
.slide-in.active {
  transform: translateX(0);
  opacity: 1;
}

/* Bad: triggers layout on every frame */
.slide-in-bad {
  left: -100%;
  transition: left 300ms ease;
}
```

---

## 2. Will-Change Best Practices

`will-change` promotes an element to its own compositor layer. This speeds up animation but consumes GPU memory.

Rules:
- Add `will-change` BEFORE the animation starts (e.g., on hover, not in the animation itself).
- Remove it AFTER the animation completes.
- Never use `will-change: all` — it promotes everything.
- Never apply it to more than 10 elements simultaneously.
- Don't put it in your stylesheet permanently.

```js
// Good: apply before, remove after
element.addEventListener('mouseenter', () => {
  element.style.willChange = 'transform';
});
element.addEventListener('transitionend', () => {
  element.style.willChange = 'auto';
});
```

```css
/* Acceptable: for elements that are ALWAYS animated (e.g., loading spinners) */
.spinner { will-change: transform; }

/* Bad: permanent will-change on static elements */
.card { will-change: transform, opacity; } /* don't do this */
```

---

## 3. Layout Thrashing

Reading layout properties then writing them in a loop forces the browser to recalculate layout on every iteration.

```js
// BAD: layout thrashing (read-write-read-write)
elements.forEach(el => {
  const height = el.offsetHeight;    // READ — forces layout
  el.style.height = height + 10 + 'px'; // WRITE — invalidates layout
});

// GOOD: batch reads, then batch writes
const heights = elements.map(el => el.offsetHeight); // all reads first
elements.forEach((el, i) => {
  el.style.height = heights[i] + 10 + 'px'; // all writes after
});
```

Properties that trigger forced layout when read: `offsetHeight`, `offsetWidth`, `getBoundingClientRect()`, `scrollTop`, `clientHeight`, `getComputedStyle()`.

---

## 4. IntersectionObserver vs Scroll Events

| | `scroll` event | IntersectionObserver |
|---|---|---|
| Performance | Fires every pixel, blocks main thread | Async, fires on threshold crossing |
| Throttling | Manual (requestAnimationFrame) | Built-in |
| Use case | Scroll-linked animation (position) | Visibility detection (enter/exit) |
| Recommendation | Almost never | Almost always |

```js
// Good: IntersectionObserver for reveal animations
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      entry.target.classList.toggle('visible', entry.isIntersecting);
    });
  },
  { threshold: 0.1 }
);
```

For scroll-linked animations where you need exact scroll position, use the Scroll-Driven Animations API:

```css
@keyframes fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.scroll-reveal {
  animation: fade-in linear;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}
```

---

## 5. Web Animations API

For complex JS-driven animations, use WAAPI instead of manual `requestAnimationFrame`:

```js
element.animate(
  [
    { transform: 'translateY(20px)', opacity: 0 },
    { transform: 'translateY(0)', opacity: 1 }
  ],
  {
    duration: 300,
    easing: 'cubic-bezier(0.16, 1, 0.3, 1)',
    fill: 'forwards'
  }
);
```

Benefits over CSS: programmable, cancellable, can read progress, can reverse.

---

## 6. Performance Measurement

```js
// Measure animation frame rate
let frames = 0;
let lastTime = performance.now();

function countFrames() {
  frames++;
  const now = performance.now();
  if (now - lastTime >= 1000) {
    console.log(`FPS: ${frames}`);
    frames = 0;
    lastTime = now;
  }
  requestAnimationFrame(countFrames);
}
requestAnimationFrame(countFrames);
```

Chrome DevTools:
1. Performance tab → Record → interact with animations → Stop
2. Look for long frames (> 16ms) in the flame chart
3. Rendering tab → Paint flashing (green = repaint, should be minimal)
4. Rendering tab → Layer borders (orange = composited layers)

Target: 60fps = 16.67ms per frame. If ANY frame takes > 33ms, users perceive jank.

---

## 7. Testing on Low-End Devices

Your M-series Mac is not representative. Test with:
- **Chrome DevTools CPU throttling:** Performance tab → CPU → 6x slowdown
- **Network throttling:** Slow 3G preset to test loading animations
- **Real device:** Test on a 3-year-old Android phone if possible

If an animation stutters at 6x CPU throttle, reduce:
1. Number of concurrent animations
2. Element count being animated
3. Complexity of each animation

---

## 8. Contain Property

`contain` tells the browser what NOT to recalculate when an element changes.

```css
/* Isolate layout/paint to this element */
.card {
  contain: layout paint;
}

/* Full isolation — best for off-screen or independent components */
.widget {
  contain: strict; /* = size + layout + paint + style */
}

/* Content containment — layout + paint + style (most common) */
.list-item {
  contain: content;
}
```

Use `contain: content` on repeated elements (list items, cards) to prevent layout changes from propagating to siblings.

---

## 9. Common Mistakes

- **Animating `width`/`height`/`top`/`left`.** Use `transform: translate/scale` instead.
- **`will-change` on everything.** Max 10 elements. Remove after animation completes.
- **`addEventListener('scroll')` for visibility.** Use IntersectionObserver.
- **Reading layout properties in animation loops.** Batch reads before writes.
- **Testing only on fast hardware.** Use Chrome CPU throttling at 6x.
- **No frame budget awareness.** 16ms per frame. If your JS takes 20ms, you drop frames.
- **CSS `transition: all`.** Transitions every property including layout triggers.
- **Forgetting `contain` on repeated elements.** One card's layout change recalculates the entire list.
- **`requestAnimationFrame` without cancellation.** Always store the ID and `cancelAnimationFrame` on cleanup.
