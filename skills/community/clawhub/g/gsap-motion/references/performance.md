# Performance

Motion performance depends on what changes, how often it changes, and how much work the browser must do per frame.

## Preferred Properties

Prefer animating:

- `transform`
- `opacity`

Use caution with:

- `filter`
- `box-shadow`
- large blurred backdrops
- clip paths
- SVG path morphs

Avoid high-frequency animation of:

- `top`, `left`, `right`, `bottom`
- `width`, `height`
- margins and padding
- layout-dependent grid values

## Layout Thrash

Do not repeatedly read layout and write layout in the same frame loop.

If measurement is required:

- Read all needed measurements first.
- Then write transforms.
- Use Flip when the main problem is transitioning between layouts.

## Compositing

Use `will-change` sparingly and temporarily. Permanent `will-change` on many elements can waste memory.

Good use:

```css
.card[data-animating="true"] {
  will-change: transform, opacity;
}
```

Remove it after animation if many elements are involved.

## Lists And Staggers

Large lists can become expensive. For many items:

- Animate only visible items.
- Use small staggers.
- Batch reveals.
- Avoid animating nested children for every row.
- Consider virtualization for very large lists.

## Scroll

Scroll-linked motion needs extra care:

- Avoid too many active triggers.
- Prefer one section-level trigger over dozens of small triggers.
- Disable complex pinned scenes on low-width or touch-heavy contexts when appropriate.
- Refresh after layout-affecting assets load.

## Testing

Check:

- Low-end mobile or throttled CPU behavior.
- Repeated route changes or remounts.
- Resizing.
- Long content.
- Reduced motion.
- Browser console warnings.

The best animation is still a regression if it drops frames, duplicates after remount, or causes layout shifts.
