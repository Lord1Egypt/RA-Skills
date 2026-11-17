# Accessibility

Motion should improve comprehension without making the interface harder to use.

## Reduced Motion

Respect `prefers-reduced-motion`.

Reduced motion does not always mean no feedback. Replace large movement with:

- Opacity changes.
- Instant state changes.
- Short fades.
- Color, outline, or elevation changes.
- Progress updates without scroll-scrubbed movement.

Example:

```ts
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
```

Use this only in client-side code.

## Vestibular Safety

Avoid or reduce:

- Large parallax movement.
- Zooming through space.
- Long diagonal motion.
- Spinning or rotating UI.
- Scroll-jacked scenes.
- Motion that continues while the user is trying to read.

## Focus And Input

Animation must not break keyboard flow:

- Keep focus visible.
- Do not animate focused controls away unexpectedly.
- Do not trap focus unless using a real modal/dialog pattern.
- Do not delay availability of primary controls.
- Preserve logical DOM order even if visual order animates.

## Screen Readers

Screen readers consume DOM semantics, not the animation. Keep semantic structure intact:

- Use real headings, buttons, links, lists, and regions.
- Do not split meaningful text in a way that destroys accessible names.
- Keep live updates concise and intentional.

## SplitText

Text-splitting effects need extra care:

- Keep the original readable text available to assistive technology.
- Avoid letter-by-letter animation for long or important reading.
- Provide a reduced-motion path.
- Confirm copied text, selection, and responsive wrapping still behave acceptably.

## Timing

Interface feedback should be quick. Avoid sequences that force users to wait before they can act.

For content entrances, keep the first meaningful content visible early and avoid stagger chains that delay the last items excessively.
