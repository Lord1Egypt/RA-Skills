# Browser Integration

## Baseline Pattern

Use this when the caller wants paragraph height without repeated DOM measurement:

```ts
import { prepare, layout } from '@chenglou/pretext';

await document.fonts.ready;

const font = getComputedStyle(node).font;
const lineHeight = Number.parseFloat(getComputedStyle(node).lineHeight);
const prepared = prepare(text, font);
const { height, lineCount } = layout(prepared, width, lineHeight);
```

## Browser Checklist

1. Wait for `document.fonts.ready` if fonts are web-loaded.
2. Use the actual UI `font` value, not a guessed family name.
3. Use the actual UI `line-height` value, not a CSS default assumption.
4. Prepare once and reuse on resize.
5. Re-prepare when text, font, locale, or white-space mode changes.

## Textarea-Like Content

Use `pre-wrap` when ordinary spaces, tabs, and hard breaks must stay visible:

```ts
const prepared = prepare(text, font, { whiteSpace: 'pre-wrap' });
const metrics = layout(prepared, width, lineHeight);
```

## Practical Verification Loop

- Render one real DOM paragraph and one Pretext-driven measurement side by side.
- Compare representative samples:
  - plain Latin
  - mixed CJK or Arabic
  - emoji
  - narrow widths
- Accept tiny pixel deltas only when they are explainable and non-user-visible.
