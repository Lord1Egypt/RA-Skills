# Animation patterns (deck-spec path)

Use motion to signal craft — not decoration for its own sake. The canonical renderer ships scroll-triggered `.reveal` stagger on slide content; match this energy on the direct-HTML path.

## Baseline (automatic in rendered decks)

- Slides use scroll-snap + keyboard navigation
- Child elements (headings, cards, stats) fade up with staggered delay when the slide enters view
- `prefers-reduced-motion: reduce` disables motion

## When to add extra motion

| Feeling | Pattern | Notes |
|---------|---------|-------|
| Dramatic opener | Slow scale on hero title (0.95 → 1) | One beat only — don't loop |
| Tech / SaaS | Soft accent glow on h1 (`text-shadow` using `--accent`) | Already on `neon-glow` surface |
| Playful | Slight rotation on decorative shapes | ±6–12deg max |
| Editorial | Rule draw-in (width 0 → 100% on masthead bar) | CSS transition on `::before` |
| Retro / arcade | Scanline overlay + neon edge bar | Use `scanline-neon` surface theme |

## Direct-HTML path — copy this reveal pattern

```css
.reveal {
  opacity: 0;
  transform: translateY(22px);
  transition: opacity 0.65s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.65s cubic-bezier(0.16, 1, 0.3, 1);
  transition-delay: var(--reveal-delay, 0ms);
}
.slide.in-view .reveal { opacity: 1; transform: translateY(0); }
```

```javascript
// Mark h1, h2, cards, stats with class="reveal" and increment --reveal-delay
// Toggle .in-view on .slide via IntersectionObserver (threshold ~0.35)
```

## Do not

- Autoplay video backgrounds
- Infinite bounce on body text
- Parallax that causes nausea on scroll-snap decks
- Particles on every slide (one hero slide max)
